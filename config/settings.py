# Standard Python
import logging
import os


def get_credential_from_env_var(env_var_name):
    if env_var_name in os.environ:
        credential = os.environ[env_var_name]
    else:
        raise ValueError(f"""
        Could not retrieve credential.
        No environment variable named '{env_var_name}' found.
        """)

    return credential

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
logging.basicConfig(format='%(levelname)s: %(message)s')

ACCOUNT_ID = get_credential_from_env_var(env_var_name="OANDA_ACCOUNT_ID")
API_TOKEN = get_credential_from_env_var(env_var_name="OANDA_API_TOKEN")

# Build absolute path to spxusd_years directory
# This file is in config/settings.py, so go up one level to oanda_price_collector
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CONFIG_DIR)
SPXUSD_DATA_DIR = os.path.join(PROJECT_ROOT, "spxusd_years")
