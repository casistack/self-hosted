from sentry.conf.server import *
import os

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

SENTRY_SINGLE_ORGANIZATION = True
SENTRY_USE_BIG_INTS = True

# Redis configuration
SENTRY_OPTIONS["redis.clusters"] = {
    "default": {
        "hosts": {0: {"host": "redis", "password": "", "port": "6379", "db": "0"}}
    }
}

# Queue configuration
BROKER_URL = "redis://redis:6379/0"

# Cache configuration
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": ["memcached:11211"],
        "TIMEOUT": 3600,
    }
}

SENTRY_CACHE = "sentry.cache.redis.RedisCache"

# Kafka configuration
DEFAULT_KAFKA_OPTIONS = {
    "bootstrap.servers": "kafka:9092",
    "message.max.bytes": 50000000,
}

SENTRY_EVENTSTREAM = "sentry.eventstream.kafka.KafkaEventStream"
SENTRY_EVENTSTREAM_OPTIONS = {"producer_configuration": DEFAULT_KAFKA_OPTIONS}

KAFKA_CLUSTERS["default"] = DEFAULT_KAFKA_OPTIONS

# Core services
SENTRY_TSDB = "sentry.tsdb.redissnuba.RedisSnubaTSDB"
SENTRY_BUFFER = "sentry.buffer.redis.RedisBuffer"
SENTRY_QUOTAS = "sentry.quotas.redis.RedisQuota"
SENTRY_DIGESTS = "sentry.digests.backends.redis.RedisBackend"

# Web Server
SENTRY_WEB_HOST = "0.0.0.0"
SENTRY_WEB_PORT = 9000
SENTRY_WEB_OPTIONS = {
    "http": "%s:%s" % (SENTRY_WEB_HOST, SENTRY_WEB_PORT),
    "protocol": "uwsgi",
    "workers": 3,
    "threads": 4,
    "max-requests": 100000,
}

# Features
SENTRY_FEATURES.update(
    {
        feature: True
        for feature in (
            "organizations:metrics",
            "organizations:performance-view",
            "organizations:session-replay",
            "organizations:incidents",
            "organizations:discover",
            "organizations:events",
            "organizations:global-views",
            "organizations:integrations-issue-basic",
            "organizations:integrations-issue-sync",
            "projects:servicehooks",
        )
    }
)
