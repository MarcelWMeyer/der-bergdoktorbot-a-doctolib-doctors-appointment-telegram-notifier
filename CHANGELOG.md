# Changelog

All notable changes to Der BergdoktorBot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-09-24

### 🎉 Major Release: Multi-Doctor Support

### Added
- **Multi-Doctor Monitoring**: Monitor unlimited doctors simultaneously using `DOCTOR_X_*` environment variables
- **Docker Containerization**: Full Docker and Docker Compose support for easy deployment
- **Combined Notifications**: Single Telegram message showing all available appointments
- **Loop-based Scheduling**: Reliable execution system replacing cron complexity
- **Smart Message Formatting**: Rich HTML formatting with individual booking links per doctor
- **Environment Configuration**: Complete `.env` file support for all settings
- **Manual vs Scheduled Modes**: `RUN_MODE` setting for testing and production
- **Flexible Intervals**: Configurable check intervals via `INTERVAL_MINUTES`

### Changed
- **Architecture**: Completely rewritten for multi-doctor support
- **Configuration**: Moved from hardcoded constants to environment variables
- **Scheduling**: Replaced cron with simple loop-based execution
- **Notifications**: Enhanced message format with doctor-specific information
- **Error Handling**: Improved error handling and logging for Docker environments

### Deprecated
- **Legacy Variables**: Single-doctor variables (`AVAILABILITIES_URL`, `BOOKING_URL`, etc.) still supported but deprecated

### Technical Details
- **Language**: Python 3.11+ with standard library only
- **Container**: Based on `python:3.11-slim` for minimal footprint  
- **Dependencies**: No external Python packages required
- **Compatibility**: Backward compatible with v1.x configurations

### Migration Guide
To upgrade from v1.x:
1. Copy your existing variables to the new `DOCTOR_1_*` format in `.env`
2. Use Docker Compose for deployment: `docker-compose up -d`
3. Old hardcoded variables in the Python file are no longer needed

## [1.0.0] - 2023-XX-XX

### Added
- Initial release with single doctor monitoring
- Telegram notifications for appointment availability
- Cron-based scheduling
- Basic Doctolib API integration