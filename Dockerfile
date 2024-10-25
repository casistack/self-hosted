ARG SENTRY_IMAGE=getsentry/sentry:latest
FROM ${SENTRY_IMAGE}

# Copy configuration files
COPY config.py /etc/sentry/
COPY config.yml /etc/sentry/

# Make sure permissions are correct
RUN chown -R sentry:sentry /etc/sentry/
