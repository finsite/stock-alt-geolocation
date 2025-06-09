"""Repo-specific configuration for stock-alt-geolocation."""

from app.config_shared import *


def get_poller_name() -> str:
    return get_config_value("POLLER_NAME", "stock_alt_geolocation")


def get_rabbitmq_queue() -> str:
    return get_config_value("RABBITMQ_QUEUE", "stock_alt_geolocation_queue")


def get_dlq_name() -> str:
    return get_config_value("DLQ_NAME", "stock_alt_geolocation_dlq")


def get_geolocation_provider() -> str:
    return get_config_value("GEOLOCATION_PROVIDER", "ipstack")


def get_geolocation_api_key() -> str:
    return get_config_value("GEOLOCATION_API_KEY", "")
