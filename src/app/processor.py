"""Processor module for enriching data with geolocation information."""

from typing import Any

import requests

from app import config
from app.utils.setup_logger import setup_logger
from app.utils.types import validate_dict

logger = setup_logger(__name__)


def enrich_with_geolocation(record: dict[str, Any]) -> dict[str, Any]:
    """Adds geolocation fields based on IP address using the configured provider.

    Args:
        record (dict): The input message dictionary.

    Returns:
        dict: The enriched message with a `geolocation` field added.

    """
    validate_dict(record, required_keys=["ip_address"])
    ip = record.get("ip_address")

    geo = {"status": "unknown"}

    provider = config.get_geolocation_provider().lower()
    api_key = config.get_geolocation_api_key()

    try:
        if provider == "ipstack":
            url = f"http://api.ipstack.com/{ip}?access_key={api_key}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            geo = {
                "ip": ip,
                "country": data.get("country_code"),
                "region": data.get("region_code"),
                "city": data.get("city"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "status": "ok",
                "provider": provider,
            }

        else:
            logger.warning("⚠️ Unsupported geolocation provider: %s", provider)
            geo = {"status": "unsupported_provider", "provider": provider}

        logger.debug("✅ Enriched geolocation for IP %s: %s", ip, geo)

    except Exception as e:
        logger.exception("❌ Geolocation enrichment error for IP %s: %s", ip, e)
        geo = {"status": "error", "error": str(e), "provider": provider}

    record["geolocation"] = geo
    return record
