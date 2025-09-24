from datetime import date, datetime, timedelta
import json
import os
import urllib.parse
import urllib.request
import re

# Enable verbose logging
print(f"[{datetime.now()}] BergdoktorBot starting...")

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
UPCOMING_DAYS = int(os.getenv('UPCOMING_DAYS', '15'))
MAX_DATETIME_IN_FUTURE = datetime.today() + timedelta(days = UPCOMING_DAYS)
NOTIFY_HOURLY = os.getenv('NOTIFY_HOURLY', 'false').lower() == 'true'

# Legacy support for single doctor configuration
LEGACY_AVAILABILITIES_URL = os.getenv('AVAILABILITIES_URL', '')
LEGACY_BOOKING_URL = os.getenv('BOOKING_URL', 'https://www.doctolib.de/')
LEGACY_APPOINTMENT_NAME = os.getenv('APPOINTMENT_NAME') or None
LEGACY_MOVE_BOOKING_URL = os.getenv('MOVE_BOOKING_URL') or None

def get_doctor_configurations():
    """Extract all doctor configurations from environment variables"""
    doctors = []
    env_vars = dict(os.environ)
    
    # Find all DOCTOR_X_ prefixed variables
    doctor_numbers = set()
    for key in env_vars.keys():
        match = re.match(r'DOCTOR_(\d+)_', key)
        if match:
            doctor_numbers.add(int(match.group(1)))
    
    # Build configurations for each doctor
    for doctor_num in sorted(doctor_numbers):
        prefix = f'DOCTOR_{doctor_num}_'
        
        name = os.getenv(f'{prefix}NAME', f'Doctor {doctor_num}')
        availabilities_url = os.getenv(f'{prefix}AVAILABILITIES_URL', '')
        booking_url = os.getenv(f'{prefix}BOOKING_URL', 'https://www.doctolib.de/')
        move_booking_url = os.getenv(f'{prefix}MOVE_BOOKING_URL') or None
        
        if availabilities_url:  # Only add if URL is provided
            doctors.append({
                'name': name,
                'availabilities_url': availabilities_url,
                'booking_url': booking_url,
                'move_booking_url': move_booking_url
            })
    
    # Add legacy configuration if no new-style doctors are configured
    if not doctors and LEGACY_AVAILABILITIES_URL:
        doctors.append({
            'name': LEGACY_APPOINTMENT_NAME or 'Legacy Doctor',
            'availabilities_url': LEGACY_AVAILABILITIES_URL,
            'booking_url': LEGACY_BOOKING_URL,
            'move_booking_url': LEGACY_MOVE_BOOKING_URL
        })
    
    return doctors

# Get all doctor configurations
DOCTORS = get_doctor_configurations()

if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID) or UPCOMING_DAYS > 15 or not DOCTORS:
    print(f"[{datetime.now()}] Configuration error - missing required settings or no doctors configured")
    exit()

def check_doctor_availability(doctor):
    """Check availability for a single doctor"""
    try:
        urlParts = urllib.parse.urlparse(doctor['availabilities_url'])
        query = dict(urllib.parse.parse_qsl(urlParts.query))
        query.update({
            'limit': UPCOMING_DAYS,
            'start_date': date.today(),
        })
        newAvailabilitiesUrl = (urlParts
                                    ._replace(query = urllib.parse.urlencode(query))
                                    .geturl())
        request = (urllib
                        .request
                        .Request(newAvailabilitiesUrl))
        request.add_header(
            'User-Agent',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        )
        response = (urllib.request
                            .urlopen(request)
                            .read()
                            .decode('utf-8'))

        availabilities = json.loads(response)
        
        slotsInNearFuture = availabilities['total']
        slotInNearFutureExist = slotsInNearFuture > 0
        
        earlierSlotExists = False
        if slotInNearFutureExist:
            for day in availabilities['availabilities']:
                if len(day['slots']) == 0:
                    continue
                nextDatetimeIso8601 = day['date']
                nextDatetime = (datetime.fromisoformat(nextDatetimeIso8601)
                                        .replace(tzinfo = None))
                if nextDatetime < MAX_DATETIME_IN_FUTURE:
                    earlierSlotExists = True
                    break
        
        return {
            'doctor': doctor,
            'slots_total': slotsInNearFuture,
            'slots_exist': slotInNearFutureExist,
            'earlier_slots': earlierSlotExists,
            'availabilities': availabilities,
            'success': True
        }
    except Exception as e:
        print(f"[{datetime.now()}] Error checking {doctor['name']}: {e}")
        return {
            'doctor': doctor,
            'success': False,
            'error': str(e)
        }

def send_telegram_message(message):
    """Send a message via Telegram"""
    urlEncodedMessage = urllib.parse.quote(message)
    telegram_url = (f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
                    f'?chat_id={TELEGRAM_CHAT_ID}'
                    f'&text={urlEncodedMessage}'
                    f'&parse_mode=HTML'
                    f'&disable_web_page_preview=true')

    print(f"[{datetime.now()}] Sending Telegram message: {message[:100]}...")
    try:
        response = urllib.request.urlopen(telegram_url)
        print(f"[{datetime.now()}] Message sent successfully!")
        return True
    except Exception as e:
        print(f"[{datetime.now()}] Error sending message: {e}")
        return False

# Check all doctors
print(f"[{datetime.now()}] Checking {len(DOCTORS)} doctor(s)...")
results = []
for doctor in DOCTORS:
    print(f"[{datetime.now()}] Checking {doctor['name']}...")
    result = check_doctor_availability(doctor)
    results.append(result)
    if result['success']:
        print(f"[{datetime.now()}] {doctor['name']}: Found {result['slots_total']} slots")
    else:
        print(f"[{datetime.now()}] {doctor['name']}: Error - {result['error']}")

# Determine if notification is needed
available_doctors = [r for r in results if r['success'] and (r['earlier_slots'] or r['slots_exist'])]
isOnTheHour = datetime.now().minute == 0
isHourlyNotificationDue = isOnTheHour and NOTIFY_HOURLY

if not available_doctors and not isHourlyNotificationDue:
    total_slots = sum(r['slots_total'] for r in results if r['success'])
    total_earlier = sum(1 for r in results if r['success'] and r['earlier_slots'])
    print(f"[{datetime.now()}] No notification needed. Total slots: {total_slots}, Earlier slots: {total_earlier}, Hourly due: {isHourlyNotificationDue}")
    exit()

print(f"[{datetime.now()}] Preparing notification...")

# Build notification message
message = '🏥 <b>Arzttermin-Update</b>\n\n'

# Add available appointments
if available_doctors:
    message += '� <b>Verfügbare Termine:</b>\n'
    for result in available_doctors:
        doctor = result['doctor']
        slots = result['slots_total']
        pluralSuffix = 'e' if slots > 1 else ''
        
        message += f'�‍⚕️ <b>{doctor["name"]}</b>\n'
        if result['earlier_slots']:
            message += f'   🔥 {slots} Termin{pluralSuffix} in {UPCOMING_DAYS} Tagen!\n'
        else:
            message += f'   📅 {slots} Termin{pluralSuffix} verfügbar\n'
        
        message += f'   📞 <a href="{doctor["booking_url"]}">Jetzt buchen</a>\n'
        if doctor['move_booking_url']:
            message += f'   🚚 <a href="{doctor["move_booking_url"]}">Termin verschieben</a>\n'
        message += '\n'

# Add hourly notifications for doctors without immediate slots
if isHourlyNotificationDue:
    hourly_doctors = [r for r in results if r['success'] and not r['earlier_slots'] and r['slots_exist']]
    if hourly_doctors:
        message += '🐌 <b>Spätere Termine:</b>\n'
        for result in hourly_doctors:
            doctor = result['doctor']
            try:
                nextSlotDatetimeIso8601 = result['availabilities']['next_slot']
                nextSlotDate = (datetime.fromisoformat(nextSlotDatetimeIso8601)
                                            .strftime('%d %B %Y'))
                message += f'�‍⚕️ {doctor["name"]}: <i>{nextSlotDate}</i>\n'
            except:
                message += f'👨‍⚕️ {doctor["name"]}: Termine verfügbar\n'

message += '\n💊 Der BergdoktorBot'

# Send the notification
send_telegram_message(message)
