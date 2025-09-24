# Der BergdoktorBot – A Multi-Doctor Doctolib Appointment Telegram Notifier

[![Docker Build](https://github.com/MarcelWMeyer/der-bergdoktorbot-a-doctolib-doctors-appointment-telegram-notifier/actions/workflows/ci.yml/badge.svg)](https://github.com/MarcelWMeyer/der-bergdoktorbot-a-doctolib-doctors-appointment-telegram-notifier/actions/workflows/ci.yml)
[![Docker Hub](https://img.shields.io/docker/v/MarcelWMeyer/bergdoktorbot?label=Docker%20Hub&logo=docker)](https://hub.docker.com/r/MarcelWMeyer/bergdoktorbot)
[![License](https://img.shields.io/github/license/MarcelWMeyer/der-bergdoktorbot-a-doctolib-doctors-appointment-telegram-notifier)](LICENSE.md)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

![Der BergdoktorBot banner](images/Der_Bergdoktor_banner_with_working_title_and_project_description.jpg)

Get Telegram notifications about doctor's appointments from **multiple doctors simultaneously** on [doctolib.de](https://www.doctolib.de/). This Docker-based bot monitors multiple doctors and sends **combined notifications** when appointments become available.

## ✨ Features

- 🏥 **Multi-Doctor Monitoring**: Monitor unlimited doctors simultaneously
- 🐳 **Docker Ready**: Easy deployment with Docker Compose
- 📱 **Smart Notifications**: Combined Telegram messages for all available appointments
- ⚙️ **Flexible Configuration**: Environment variables for easy setup
- 🔄 **Reliable Scheduling**: Loop-based execution (no cron issues)
- 🔒 **Privacy Focused**: No login required, works with public availability data

ℹ️ 🔒 🔧 Remember that this script does not know anything about your doctolib details behind your login so you have to **monitor** and **adjust** it on the go to reduce unwanted notifications.

## Setup

### Telegram Bot Setup

The setup follows these [instructions](https://sarafian.github.io/low-code/2020/03/24/create-private-telegram-chatbot.html). For simplicity I tried to compress it even more in the following step by step list:

1. **Create** a Telegram bot using [@botfather](https://web.telegram.org/k/#@BotFather) ([FAQ](https://core.telegram.org/bots/faq)).
   - Username: `@<NAME>Bot`
   - Disable `Allow Groups?`
   - Turn on `Group Privacy`
   
   The bot `Token` will be available once the bot is created.
   <br>Write it down, you'll need it in a later step.

2. **Create** a **private** group. Everyone in the group will see the messages from your bot.
   - Group name: `MyPrivateGroup`
   - Group Type: `private`
   
   Warning: **Do not** edit special permissions for users as this will [convert the group into a supergroup](https://stackoverflow.com/a/62291433) which **does not work** with this code.

3. Temporarily **enable** `Allow Groups?` on the bot.
4. **Add** the bot to the group.
5. Immediately **deactivate** `Allow Groups?` on the bot after adding it to the group.
6. **Post** a test message into the group via the app or the browser (required to get the next step running).
   Start message with `/` in order for the bot to be able to read it (`Group Privacy` is turned on by default).
7. **Retrieve** group `chat_id` by visiting `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates` in the browser.
   <br>Write it down, you'll need it in a later step.
8. Let the bot **send** a test message via visiting `https://api.telegram.org/bot<BOT_TOKEN>/sendMessage?chat_id=<GROUP_CHAT_ID>&text=Test` in the browser.
   <br>The message should appear in the group chat.

### Quick Start with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/MarcelWMeyer/der-bergdoktorbot-a-doctolib-doctors-appointment-telegram-notifier.git
   cd der-bergdoktorbot-a-doctolib-doctors-appointment-telegram-notifier
   ```

2. **Copy the environment template**
   ```bash
   cp .env.example .env
   ```

3. **Configure your settings** (see Configuration section below)
   ```bash
   nano .env  # or use your preferred editor
   ```

4. **Start the bot**
   ```bash
   docker-compose up -d
   ```

5. **Check the logs**
   ```bash
   docker-compose logs -f bergdoktorbot
   ```

### Configuration

#### For Each Doctor You Want to Monitor:

You do **not** have to be signed in to doctolib.de to get the required URLs.

1. **Navigate to [doctolib.de](https://www.doctolib.de/)**
2. **Search for your doctor** and go to their profile page
3. **Open browser dev tools** (`F12`), go to `Network` tab
4. **Click `TERMIN BUCHEN`** and complete the appointment wizard
5. **Copy the browser URL** for the booking page
6. **Filter for `Fetch/XHR`** in the Network tab
7. **Find the `availabilities.json` request** and copy its full URL
8. **Add to `.env` file** using the pattern below:

```bash
# Doctor 1
DOCTOR_1_NAME=Your Doctor Name
DOCTOR_1_AVAILABILITIES_URL=https://www.doctolib.de/availabilities.json?...
DOCTOR_1_BOOKING_URL=https://www.doctolib.de/your-doctor/booking/...
DOCTOR_1_MOVE_BOOKING_URL=  # Optional

# Doctor 2 (add as many as needed)
DOCTOR_2_NAME=Another Doctor
DOCTOR_2_AVAILABILITIES_URL=https://www.doctolib.de/availabilities.json?...
DOCTOR_2_BOOKING_URL=https://www.doctolib.de/another-doctor/booking/...
```

### Alternative: Manual Installation

If you prefer to run without Docker:

1. **Install Python 3.7+**
2. **Configure environment variables** in your system or create a `.env` file
3. **Run manually:**
   ```bash
   python notifyDoctolibDoctorsAppointment.py
   ```
4. **Or schedule with cron:**
   ```bash
   # Run every 5 minutes from 7 AM to 11 PM
   */5 7-23 * * * cd /path/to/bot && python notifyDoctolibDoctorsAppointment.py
   ```

## Environment Variables

Configure these in your `.env` file:

### Required Settings

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from @BotFather | `123456789:ABC-DEF...` |
| `TELEGRAM_CHAT_ID` | Your Telegram group chat ID | `-123456789` |

### Doctor Configuration (Multi-Doctor Support)

For each doctor, use the pattern `DOCTOR_X_*` where X is a number (1, 2, 3, etc.):

| Variable Pattern | Description | Required |
|------------------|-------------|----------|
| `DOCTOR_X_NAME` | Display name for the doctor | ✅ |
| `DOCTOR_X_AVAILABILITIES_URL` | Full availabilities.json URL from Network tab | ✅ |
| `DOCTOR_X_BOOKING_URL` | Booking page URL | ✅ |
| `DOCTOR_X_MOVE_BOOKING_URL` | Optional: Move existing appointment URL | ❌ |

**Example:**
```bash
DOCTOR_1_NAME=Dr. Smith - Cardiology
DOCTOR_1_AVAILABILITIES_URL=https://www.doctolib.de/availabilities.json?visit_motive_ids=123...
DOCTOR_1_BOOKING_URL=https://www.doctolib.de/dr-smith/booking/...

DOCTOR_2_NAME=Dr. Johnson - Dermatology  
DOCTOR_2_AVAILABILITIES_URL=https://www.doctolib.de/availabilities.json?visit_motive_ids=456...
DOCTOR_2_BOOKING_URL=https://www.doctolib.de/dr-johnson/booking/...
```

### Optional Settings

| Variable | Description | Default | Type |
|----------|-------------|---------|------|
| `UPCOMING_DAYS` | Days to monitor for appointments (max 15) | `15` | `int` |
| `NOTIFY_HOURLY` | Send hourly notifications for later appointments | `false` | `bool` |
| `INTERVAL_MINUTES` | Minutes between checks | `5` | `int` |
| `RUN_MODE` | `cron` for scheduled, `manual` for one-time | `cron` | `str` |

### Legacy Support (Deprecated)

The old single-doctor variables are still supported for backward compatibility:
- `AVAILABILITIES_URL`, `BOOKING_URL`, `APPOINTMENT_NAME`, `MOVE_BOOKING_URL`

## Example Notification

When appointments are found, you'll receive a combined notification like this:

```
🏥 Arzttermin-Update

🔥 Verfügbare Termine:
👨‍⚕️ Dr. Smith - Cardiology
   🔥 3 Termine in 5 Tagen!
   📞 Jetzt buchen

👨‍⚕️ Dr. Johnson - Dermatology  
   🔥 2 Termine in 5 Tagen!
   📞 Jetzt buchen

💊 Der BergdoktorBot
```

## Docker Commands

| Command | Description |
|---------|-------------|
| `docker-compose up -d` | Start bot in background |
| `docker-compose logs -f bergdoktorbot` | View live logs |
| `docker-compose down` | Stop the bot |
| `docker-compose restart` | Restart the bot |
| `docker-compose run --rm -e RUN_MODE=manual bergdoktorbot` | Test run |

## Troubleshooting

- **No doctors configured**: Check your `DOCTOR_X_*` variables in `.env`
- **API errors**: Verify your `availabilities.json` URLs are current
- **No notifications**: Check Telegram token and chat ID
- **Container issues**: Run `docker-compose logs bergdoktorbot` for details

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## Disclaimer

This tool is for educational purposes and personal use only. Please respect Doctolib's terms of service and don't overload their servers. The authors are not responsible for any misuse of this tool.

---

**Repository Topics**: `doctolib`, `telegram-bot`, `appointment-notifier`, `docker`, `python`, `healthcare`, `automation`, `multi-doctor`, `germany`