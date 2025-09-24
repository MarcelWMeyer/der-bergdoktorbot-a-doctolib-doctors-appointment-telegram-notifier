# Contributing to Der BergdoktorBot

Thank you for your interest in contributing to Der BergdoktorBot! This document provides guidelines for contributing to the project.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/der-bergdoktorbot-a-doctolib-doctors-appointment-telegram-notifier.git
   ```
3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Set up development environment**
   ```bash
   cp .env.example .env
   # Edit .env with your test configuration
   ```

## 🐳 Development with Docker

### Testing Changes
```bash
# Build and test locally
docker-compose build
docker-compose run --rm -e RUN_MODE=manual bergdoktorbot

# Run in background for testing
docker-compose up -d
docker-compose logs -f bergdoktorbot
```

### Code Structure
- **Single File Architecture**: All logic in `notifyDoctolibDoctorsAppointment.py`
- **No External Dependencies**: Uses only Python standard library
- **Environment Driven**: All configuration via environment variables
- **Docker First**: Designed for containerized deployment

## 📝 Coding Standards

### Python Style
- **PEP 8 compliant** where reasonable
- **Standard library only** - no external dependencies
- **Clear variable names** that explain purpose
- **Comprehensive error handling** with logging
- **Environment variable pattern**: `DOCTOR_X_*` for multi-doctor support

### Key Patterns
```python
# Environment variable parsing
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# Multi-doctor discovery
doctor_numbers = set()
for key in env_vars.keys():
    match = re.match(r'DOCTOR_(\d+)_', key)
    if match:
        doctor_numbers.add(int(match.group(1)))

# Logging format
print(f"[{datetime.now()}] Message here...")
```

## 🧪 Testing

### Manual Testing
```bash
# Test configuration parsing
docker-compose run --rm -e RUN_MODE=manual bergdoktorbot

# Test with minimal config
docker-compose run --rm -e RUN_MODE=manual -e DOCTOR_1_NAME="Test" bergdoktorbot
```

### Integration Testing
- Test with real Doctolib URLs (use your own)
- Verify Telegram notifications work
- Test error handling with invalid URLs
- Confirm multi-doctor scenarios

## 📋 Pull Request Process

1. **Update documentation** if needed
2. **Test your changes** thoroughly with Docker
3. **Update CHANGELOG.md** with your changes
4. **Create clear commit messages**
5. **Submit pull request** with description of changes

### Commit Message Format
```
type(scope): description

feat(multi-doctor): add support for unlimited doctors
fix(docker): resolve environment variable loading
docs(readme): update installation instructions
```

## 🐛 Bug Reports

When reporting bugs, please include:
- **Environment**: Docker version, OS, etc.
- **Configuration**: Anonymized `.env` settings
- **Logs**: Output from `docker-compose logs bergdoktorbot`
- **Steps to reproduce**
- **Expected vs actual behavior**

## 💡 Feature Requests

For feature requests:
- **Describe the use case** clearly
- **Explain the benefit** to users
- **Consider Docker compatibility**
- **Think about multi-doctor scenarios**

## 🔒 Security

- **Never commit** real tokens, URLs, or personal data
- **Use `.env` files** for sensitive configuration
- **Report security issues** privately via GitHub

## 📄 Documentation

When updating docs:
- **README.md**: User-facing instructions
- **DOCKER.md**: Docker-specific setup
- **CHANGELOG.md**: Version history
- **Comments**: Code should be self-documenting

## 🏗️ Architecture Decisions

### Why Single File?
- **Simplicity**: Easy to understand and deploy
- **No Dependencies**: Works everywhere Python runs
- **Docker Friendly**: Single file to copy into container

### Why Environment Variables?
- **Docker Standard**: Natural for containerized apps
- **Multi-Environment**: Easy dev/test/prod configurations
- **Security**: Keeps secrets out of code

### Why Loop Instead of Cron?
- **Docker Compatibility**: Cron in containers is complex
- **Logging**: Direct stdout/stderr for Docker logs
- **Reliability**: Easier to debug and monitor

## 🤝 Code of Conduct

- **Be respectful** and inclusive
- **Help others** learn and contribute
- **Focus on the code**, not the person
- **Assume good intentions**

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and help
- **README.md**: For setup and usage instructions

Thank you for contributing to Der BergdoktorBot! 🏥🤖