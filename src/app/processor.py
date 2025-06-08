# src/app/processor.py

"""Processor module for enriching data with geolocation information."""

from typing import Any
from app.utils.setup_logger import setup_logger
from app.utils.types import validate_dict

logger = setup_logger(__name__)


def enrich_with_geolocation(record: dict[str, Any]) -> dict[str, Any]:
    """Adds geolocation fields based on IP address or other location hints.

    Args:
        record (dict): The input message dictionary.

    Returns:
        dict: The enriched message with a `geolocation` field added.
    """
    # Validate input schema (e.g. ensure 'ip_address' key exists)
    validate_dict(record, required_keys=["ip_address"])

    ip = record.get("ip_address")
    geo = {"status": "unknown"}

    try:
        # **Production note**: Replace this mock with a real lookup, e.g.:
        # from geoip import GeoIP; geo_data = GeoIP().city(ip)
        # geo = {"ip": ip, **geo_data}
        geo = {
            "ip": ip,
            "country": "US",
            "region": "CA",
            "city": "San Francisco",
            "status": "mocked",
        }
        logger.debug("✅ Enriched geolocation for IP %s: %s", ip, geo)
    except Exception as e:
        logger.exception("❌ Geolocation enrichment error for IP %s: %s", ip, e)
        geo = {"status": "error", "error": str(e)}

    record["geolocation"] = geo
    return record
