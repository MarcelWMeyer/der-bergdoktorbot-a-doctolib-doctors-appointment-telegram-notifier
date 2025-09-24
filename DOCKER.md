# Docker Setup for Der BergdoktorBot

This document explains how to run the Multi-Doctor BergdoktorBot using Docker and Docker Compose.

## ✨ Features

- 🏥 **Multi-Doctor Monitoring**: Monitor unlimited doctors simultaneously
- 🐳 **Docker Ready**: Simple deployment with Docker Compose
- 📱 **Smart Notifications**: Combined Telegram messages for all available appointments
- 🔄 **Reliable Scheduling**: Loop-based execution (no cron complexity)

## Quick Start

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your multi-doctor configuration:**
   - Add your Telegram bot token and chat ID
   - Configure multiple doctors using `DOCTOR_X_*` pattern
   - Adjust scheduling and notification settings

3. **Start the service:**

### Default: Automatic Scheduling
Run the bot continuously, checking every 5 minutes:
```bash
docker-compose up -d
```

### Manual Execution
To run the script once manually for testing:
```bash
docker-compose run --rm -e RUN_MODE=manual bergdoktorbot
```

## Multi-Doctor Configuration

Configure multiple doctors using the `DOCTOR_X_*` pattern in your `.env` file:

```bash
# Doctor 1
DOCTOR_1_NAME=Dr. Smith - Cardiology
DOCTOR_1_AVAILABILITIES_URL=https://www.doctolib.de/availabilities.json?...
DOCTOR_1_BOOKING_URL=https://www.doctolib.de/dr-smith/booking/...
DOCTOR_1_MOVE_BOOKING_URL=  # Optional

# Doctor 2
DOCTOR_2_NAME=Dr. Johnson - Dermatology
DOCTOR_2_AVAILABILITIES_URL=https://www.doctolib.de/availabilities.json?...
DOCTOR_2_BOOKING_URL=https://www.doctolib.de/dr-johnson/booking/...

# Add as many doctors as needed...
```

### Required Variables (Per Doctor)
- `DOCTOR_X_NAME`: Display name for the doctor
- `DOCTOR_X_AVAILABILITIES_URL`: Complete Doctolib availabilities.json URL
- `DOCTOR_X_BOOKING_URL`: Doctolib booking page URL

### Global Required Variables
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `TELEGRAM_CHAT_ID`: Your Telegram group chat ID

### Optional Variables
- `DOCTOR_X_MOVE_BOOKING_URL`: URL for moving existing appointments (per doctor)
- `UPCOMING_DAYS`: Days to monitor (1-15, default: 15)
- `NOTIFY_HOURLY`: Enable hourly notifications for distant appointments (true/false)
- `INTERVAL_MINUTES`: Minutes between checks (default: 5)
- `RUN_MODE`: Execution mode - 'cron' for scheduled, 'manual' for one-time (default: cron)

## Docker Commands

### Build the image:
```bash
docker-compose build
```

### Start the service (default: cron mode):
```bash
docker-compose up -d
```

### Run manually (one-time execution):
Set `RUN_MODE=manual` in `.env`, then:
```bash
docker-compose run --rm bergdoktorbot
```

### View logs:
```bash
docker-compose logs -f bergdoktorbot
```

### Stop the service:
```bash
docker-compose down
```

## Troubleshooting

### Check if container is running:
```bash
docker ps
```

### Execute commands inside the container:
```bash
docker-compose exec bergdoktorbot bash
```

### Test configuration:
```bash
# Set RUN_MODE=manual in .env first, then:
docker-compose run --rm bergdoktorbot
```

## Security Notes

- Never commit your `.env` file with real credentials
- The container runs as a non-root user for security
- Environment variables are isolated within the container