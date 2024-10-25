from sentry.conf.server import *
import os

# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "sentry.db.postgres",
        "NAME": os.getenv('POSTGRES_DB', "postgres"),
        "USER": os.getenv('POSTGRES_USER', "postgres"),
        "PASSWORD": os.getenv('POSTGRES_PASSWORD', ""),
        "HOST": "postgres",
        "PORT": "",
    }
}

# You should not change this setting after your database has been created
SENTRY_USE_BIG_INTS = True

# Instruct Sentry that this install intends to be run by a single organization
SENTRY_SINGLE_ORGANIZATION = True

SENTRY_OPTIONS["system.event-retention-days"] = int(
    os.getenv("SENTRY_EVENT_RETENTION_DAYS", "90")
)

# Redis configuration
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = os.getenv('REDIS_PORT', '6379')
redis_password = os.getenv('REDIS_PASSWORD', '')

SENTRY_OPTIONS.update({
    'redis.clusters': {
        'default': {
            'hosts': {
                0: {
                    'host': redis_host,
                    'port': redis_port,
                    'password': redis_password,
                    'db': '0',
                }
            }
        }
    },
    'redis.options': {
        'hosts': {
            0: {
                'host': redis_host,
                'port': redis_port,
                'password': redis_password,
            }
        }
    }
})

# TSDB Configuration (Time-series database)
SENTRY_TSDB = "sentry.tsdb.redis.RedisTSDB"
SENTRY_OPTIONS.update({
    'tsdb.backend': 'sentry.tsdb.redis.RedisTSDB',
})

# Queue (Celery) configuration
BROKER_URL = "redis://{}:{}/{}".format(redis_host, redis_port, 0)

# Cache configuration
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": ["memcached:11211"],
        "TIMEOUT": 3600,
        "OPTIONS": {"ignore_exc": True},
    }
}

# A primary cache is required for things such as processing events
SENTRY_CACHE = "sentry.cache.redis.RedisCache"

# Kafka configuration
DEFAULT_KAFKA_OPTIONS = {
    "bootstrap.servers": "kafka:9092",
    "message.max.bytes": 50000000,
    "socket.timeout.ms": 1000,
}

SENTRY_EVENTSTREAM = "sentry.eventstream.kafka.KafkaEventStream"
SENTRY_EVENTSTREAM_OPTIONS = {"producer_configuration": DEFAULT_KAFKA_OPTIONS}

KAFKA_CLUSTERS["default"] = DEFAULT_KAFKA_OPTIONS

# Rate limits
SENTRY_RATELIMITER = "sentry.ratelimits.redis.RedisRateLimiter"

# Update Buffers
SENTRY_BUFFER = "sentry.buffer.redis.RedisBuffer"

# Quotas
SENTRY_QUOTAS = "sentry.quotas.redis.RedisQuota"

# Search and Snuba
SENTRY_SEARCH = "sentry.search.snuba.EventsDatasetSnubaSearchBackend"
SENTRY_SEARCH_OPTIONS = {}
SENTRY_TAGSTORE_OPTIONS = {}

# Digests
SENTRY_DIGESTS = "sentry.digests.backends.redis.RedisBackend"

# Metrics Backend
SENTRY_METRICS_BACKEND = "sentry.metrics.redis.RedisMetricsBackend"
SENTRY_METRICS_OPTIONS = {
    "host": redis_host,
    "port": redis_port,
    "password": redis_password,
    "db": "1",
}

SENTRY_RELEASE_HEALTH = "sentry.release_health.metrics.MetricsReleaseHealthBackend"
SENTRY_RELEASE_MONITOR = "sentry.release_health.release_monitor.metrics.MetricReleaseMonitorBackend"

# Web Server
SENTRY_WEB_HOST = "0.0.0.0"
SENTRY_WEB_PORT = 9000
SENTRY_WEB_OPTIONS = {
    "http": "%s:%s" % (SENTRY_WEB_HOST, SENTRY_WEB_PORT),
    "protocol": "uwsgi",
    "uwsgi-socket": None,
    "so-keepalive": True,
    "http-keepalive": 15,
    "http-chunked-input": True,
    "workers": 3,
    "threads": 4,
    "memory-report": False,
    "max-requests": 100000,
    "max-requests-delta": 500,
    "max-worker-lifetime": 86400,
    "thunder-lock": True,
    "log-x-forwarded-for": False,
    "buffer-size": 32768,
    "limit-post": 209715200,
    "disable-logging": True,
    "reload-on-rss": 600,
    "ignore-sigpipe": True,
    "ignore-write-errors": True,
    "disable-write-exception": True,
}

# Mail
SENTRY_OPTIONS["mail.list-namespace"] = os.getenv("SENTRY_MAIL_HOST", "localhost")
SENTRY_OPTIONS["mail.from"] = f"sentry@{SENTRY_OPTIONS['mail.list-namespace']}"

# Features
SENTRY_FEATURES["projects:sample-events"] = False
SENTRY_FEATURES.update(
    {
        feature: True
        for feature in (
            "organizations:discover",
            "organizations:events",
            "organizations:global-views",
            "organizations:incidents",
            "organizations:integrations-issue-basic",
            "organizations:integrations-issue-sync",
            "organizations:invite-members",
            "organizations:metric-alert-builder-aggregate",
            "organizations:sso-basic",
            "organizations:sso-rippling",
            "organizations:sso-saml2",
            "organizations:performance-view",
            "organizations:advanced-search",
            "organizations:session-replay",
            "organizations:profiling",
            "organizations:dashboards-mep",
            "projects:custom-inbound-filters",
            "projects:data-forwarding",
            "projects:discard-groups",
            "projects:plugins",
            "projects:rate-limits",
            "projects:servicehooks",
        )
        + (
            # Additional features
            "organizations:profiling",
            "organizations:performance-view",
            "organizations:dashboards-edit",
            "organizations:discover-basic",
            "organizations:discover-query",
            "organizations:alert-filters",
            "organizations:custom-symbol-sources",
            "organizations:event-attachments",
        )
    }
)

# CSP
CSP_REPORT_ONLY = True

# Optional OpenAI Integration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SENTRY_FEATURES["organizations:open-ai-suggestion"] = bool(OPENAI_API_KEY)

# File storage
SENTRY_OPTIONS.update({
    "filestore.backend": "filesystem",
    "filestore.options": {
        "location": "/data/files"
    }
})

# Symbol storage
SENTRY_OPTIONS.update({
    "symbolserver.enabled": True,
    "dsym.cache-path": "/data/dsym-cache",
    "releasefile.cache-path": "/data/releasefile-cache",
})

# Self-hosted settings
SENTRY_SELF_HOSTED_ERRORS_ONLY = os.getenv("COMPOSE_PROFILES") != "feature-complete"
