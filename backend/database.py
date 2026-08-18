from neo4j import GraphDatabase
from config import get_settings
import logging

logger = logging.getLogger(__name__)

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        settings = get_settings()
        try:
            _driver = GraphDatabase.driver(
                settings.cognodb_uri,
                auth=(settings.cognodb_user, settings.cognodb_password),
                connection_timeout=10,
                max_connection_lifetime=3600,
            )
            _driver.verify_connectivity()
            logger.info("Connected to CognoDB successfully")
        except Exception as e:
            logger.error(f"Failed to connect to CognoDB: {e}")
            raise
    return _driver


def close_driver():
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


def run_query(query: str, parameters: dict = None):
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, parameters or {})
        return [record.data() for record in result]


def run_write_query(query: str, parameters: dict = None):
    driver = get_driver()
    with driver.session() as session:
        result = session.execute_write(
            lambda tx: tx.run(query, parameters or {}).data()
        )
        return result
