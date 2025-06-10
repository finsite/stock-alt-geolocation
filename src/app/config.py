"""Repo-specific configuration for stock-alt-geolocation."""

from app.config_shared import *


def get_poller_name() -> str:
    """Return the name of the poller for this service."""
    return get_config_value("POLLER_NAME", "stock_alt_geolocation")


def get_rabbitmq_queue() -> str:
    """Return the RabbitMQ queue name for this poller."""
    return get_config_value("RABBITMQ_QUEUE", "stock_alt_geolocation_queue")


def get_dlq_name() -> str:
    """Return the Dead Letter Queue (DLQ) name for this poller."""
    return get_config_value("DLQ_NAME", "stock_alt_geolocation_dlq")


def get_geolocation_provider() -> str:
    """Return the name of the geolocation provider (e.g., 'ipstack')."""
    return get_config_value("GEOLOCATION_PROVIDER", "ipstack")


def get_geolocation_api_key() -> str:
    """Return the API key used to access the geolocation provider."""
    return get_config_value("GEOLOCATION_API_KEY", "")
