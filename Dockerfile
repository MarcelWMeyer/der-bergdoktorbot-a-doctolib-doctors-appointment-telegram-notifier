# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the Python script
COPY notifyDoctolibDoctorsAppointment.py .

# Create cron entry script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Make the script executable
RUN chmod +x notifyDoctolibDoctorsAppointment.py

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app

# Switch to root for cron setup
USER root

# Use custom entrypoint
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]