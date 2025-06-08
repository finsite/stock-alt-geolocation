"""Entry point for the stock-alt-geolocation processor service."""

import sys
import time
import signal
import types

from app.config import get_environment, get_poller_name
from app.utils.setup_logger import setup_logger
from app.queue_handler import consume_messages
from app.processor import enrich_with_geolocation
from app.output_handler import send_to_output

logger = setup_logger("stock_alt_geolocation")
shutdown = False


def _graceful_shutdown(signum: int, frame: types.FrameType | None) -> None:
    """Signal handler to gracefully shut down the service."""
    global shutdown
    logger.info("🛑 Shutdown signal received, stopping listener...")
    shutdown = True


def process_batch(batch: list[dict]) -> None:
    """Process a batch of raw messages, enrich them, and send output."""
    if not batch:
        logger.warning("⚠️ Received empty batch, skipping.")
        return

    logger.info("📦 Processing batch of %d messages", len(batch))
    enriched = []
    for msg in batch:
        try:
            enriched_msg = enrich_with_geolocation(msg.copy())  # Defensive copy
            enriched.append(enriched_msg)
        except Exception as e:
            logger.exception("❌ Failed to enrich message: %s", e)

    if enriched:
        try:
            send_to_output(enriched)
            logger.info("✅ Successfully handled %d enriched messages", len(enriched))
        except Exception as e:
            logger.exception("❌ Failed to send enriched data to output: %s", e)


def main() -> None:
    """Bootstraps the service and enters the consume loop."""
    logger.info("🚀 Starting stock-alt-geolocation service")
    logger.info(f"🌍 Environment: {get_environment()}")
    logger.info(f"📛 Service Name: {get_poller_name()}")

    signal.signal(signal.SIGINT, _graceful_shutdown)
    signal.signal(signal.SIGTERM, _graceful_shutdown)

    try:
        consume_messages(callback=process_batch)
    except Exception as e:
        logger.exception("❌ Unhandled exception in consume_messages: %s", e)
        raise


if __name__ == "__main__":
    restart_attempts = 0
    while not shutdown:
        try:
            main()
            logger.warning("⚠️ main() exited unexpectedly, restarting...")
        except Exception as e:
            restart_attempts += 1
            logger.error("🔁 Restart #%d due to: %s", restart_attempts, e)
            if restart_attempts >= 5:
                logger.critical("🚨 Too many consecutive failures, exiting.")
                sys.exit(1)
            time.sleep(5)

    logger.info("🛑 Service shutdown complete.")
    sys.exit(0)
