# Copilot Instructions for Der BergdoktorBot

## Project Overview
This is a **Multi-Doctor Telegram Bot** that monitors multiple Doctolib.de doctors simultaneously for appointment availability. The architecture is containerized with Docker and supports unlimited concurrent doctor monitoring through environment variable configuration.

## Core Architecture
- **Single executable**: `notifyDoctolibDoctorsAppointment.py` contains all logic
- **Multi-doctor support**: Dynamic doctor configuration via `DOCTOR_X_*` environment variables
- **Docker-first approach**: Designed for containerized deployment with Docker Compose
- **Loop-based scheduling**: Reliable execution without cron complexities
- **Combined notifications**: Single Telegram message for all available appointments
- **Stateless operation**: Each run is independent, no persistent state required

## Key Integration Points

### Doctolib API Integration
- Uses `AVAILABILITIES_URL` (extracted from browser network tab) to fetch appointment data
- Dynamically modifies URL parameters: `limit`, `start_date` based on configuration
- Requires specific User-Agent header to avoid blocking
- Parses JSON response structure: `availabilities.total`, `availabilities.availabilities[].slots[]`

### Telegram Bot Integration  
- Uses HTTP GET requests to Telegram Bot API (no SDK)
- Sends HTML-formatted messages with inline links
- Message format includes appointment count, booking links, and optional move-booking links
- Requires `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` (group chat, not individual)

## Critical Developer Workflows

### Testing Changes
```powershell
# Local testing (ensure constants are configured first)
python notifyDoctolibDoctorsAppointment.py

# Docker testing (preferred method)
docker-compose run --rm bergdoktorbot
```

### Deployment Options
1. **Docker (Recommended)**: 
   - Configure `.env` file with environment variables
   - `docker-compose up -d` (runs in cron mode by default)
2. **Traditional Cron**: 
   - Script must be executable: `chmod +x` on Unix systems  
   - Typical cron entry: `* 7-23 * * * python /path/to/notifyDoctolibDoctorsAppointment.py`

## Project-Specific Patterns

### Multi-Doctor Configuration Strategy
- **Environment variables**: All configuration via Docker `.env` file
- **Required variables**: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
- **Doctor pattern**: `DOCTOR_X_NAME`, `DOCTOR_X_AVAILABILITIES_URL`, `DOCTOR_X_BOOKING_URL` where X is 1,2,3...
- **Dynamic discovery**: Script automatically finds all `DOCTOR_X_*` patterns using regex
- **Script exits early** if no doctors configured or required Telegram variables missing
- **Legacy support**: Old single-doctor variables still work for backward compatibility
- Uses `os.getenv()` with comprehensive environment variable parsing

### URL Manipulation Pattern
```python
# Standard pattern for modifying Doctolib URLs
urlParts = urllib.parse.urlparse(AVAILABILITIES_URL)
query = dict(urllib.parse.parse_qsl(urlParts.query))
query.update({'limit': UPCOMING_DAYS, 'start_date': date.today()})
newUrl = urlParts._replace(query=urllib.parse.urlencode(query)).geturl()
```

### Datetime Handling Convention
- Uses `datetime.fromisoformat()` for parsing Doctolib's ISO8601 dates
- Removes timezone info with `.replace(tzinfo=None)` for comparisons
- `MAX_DATETIME_IN_FUTURE` controls "earlier appointment" detection logic

### Telegram Message Formatting
- Uses HTML parse mode with specific tags: `<a href="">`, `<i>`
- URL encoding via `urllib.parse.quote()` for message content
- Conditional message building based on notification type and configuration

## Dependencies & External Systems
- **Zero external dependencies**: Uses only Python standard library
- **Doctolib.de**: Relies on their availabilities.json API endpoint structure
- **Telegram Bot API**: Direct HTTP calls, no wrapper library
- **Cron**: Expected runtime environment for scheduling

## File Structure Context
- `images/`: Contains project branding and documentation assets
- `README.md`: Comprehensive setup instructions with step-by-step Telegram bot creation
- Single Python file contains all business logic - avoid splitting into modules