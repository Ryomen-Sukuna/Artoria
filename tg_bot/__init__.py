import logging
import os
import sys
import time
import spamwatch
from redis import StrictRedis
from pyrogram import Client, errors

import telegram.ext as tg
from telethon import TelegramClient

since_time_start = time.time()

# enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler()],
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get('TOKEN', None)

    try:
        OWNER_ID = int(os.environ.get('OWNER_ID', None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")
    
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        SUDO_USERS = {int(x) for x in os.environ.get("SUDO_USERS", "").split()}
        DEV_USERS = {int(x) for x in os.environ.get("DEV_USERS", "").split()}
    except ValueError:
        raise Exception(
            "Your sudo or dev users list does not contain valid integers.")

    try:
        SUPPORT_USERS = {int(x) for x in os.environ.get("SUPPORT_USERS", "").split()}
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = {int(x) for x in os.environ.get("WHITELIST_USERS", "").split()}
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")
    
    START_IMG = os.environ.get('START_IMG', "")
    EVENT_LOGS = os.environ.get('EVENT_LOGS', None)
    MESSAGE_DUMP = os.environ.get('MESSAGE_DUMP', None) 
    ERROR_DUMP = os.environ.get('ERROR_DUMP', None)
    JOIN_LOGGER = os.environ.get('JOIN_LOGGER', None)

    WEBHOOK = bool(os.environ.get('WEBHOOK', False))
    URL = os.environ.get('URL', "")  # Does not contain token
    PORT = int(os.environ.get('PORT', 5000))
    CERT_PATH = os.environ.get("CERT_PATH")

    API_ID = os.environ.get('API_ID', None)
    API_HASH = os.environ.get('API_HASH', None)
    DB_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    DONATION_LINK = os.environ.get('DONATION_LINK')
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "").split()
    DEL_CMDS = bool(os.environ.get('DEL_CMDS', False))
    STRICT_GMUTE = bool(os.environ.get('STRICT_GMUTE', False))
    STRICT_GBAN = bool(os.environ.get('STRICT_GBAN', False))
    WORKERS = int(os.environ.get('WORKERS', 8)) 

    CASH_API_KEY = os.environ.get('CASH_API_KEY', None)
    TIME_API_KEY = os.environ.get('TIME_API_KEY', None)
    AI_API_KEY = os.environ.get('AI_API_KEY', None)
    WALL_API = os.environ.get('WALL_API', None)
    API_WEATHER = os.environ.get('API_WEATHER', None)

    SUPPORT_CHAT = os.environ.get('SUPPORT_CHAT', None)
    SPAMWATCH_SUPPORT_CHAT = os.environ.get('SPAMWATCH_SUPPORT_CHAT', None)
    SPAMWATCH = os.environ.get('SPAMWATCH_API', None)
    REDIS_URL = os.environ.get('REDIS_URL', None)
    CUSTOM_CMD = os.environ.get('CUSTOM_CMD', ('/', '!'))
    REPOSITORY = os.environ.get('REPOSITORY', "")
    IBM_WATSON_CRED_URL = os.environ.get("IBM_WATSON_CRED_URL", None)
    IBM_WATSON_CRED_PASSWORD = os.environ.get("IBM_WATSON_CRED_PASSWORD", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")


    try:
        WHITELIST_CHATS = {int(x) for x in os.environ.get('WHITELIST_CHATS', "").split()}
    except ValueError:
        raise Exception(
            "Your blacklisted chats list does not contain valid integers.")

    try:
        BLACKLIST_CHATS = {int(x) for x in os.environ.get('BLACKLIST_CHATS', "").split()}
    except ValueError:
        raise Exception(
            "Your blacklisted chats list does not contain valid integers.")


else:
     LOGGER.warning("Unknown Crash!")
    
    

SUDO_USERS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)

if SPAMWATCH == None:
    spamwtc = None
    LOGGER.warning("Invalid spamwatch api")
else:
    spamwtc = spamwatch.Client(SPAMWATCH)


REDIS = StrictRedis.from_url(REDIS_URL,decode_responses=True)
try:
    REDIS.ping()
    LOGGER.info("Your redis server is now alive!")
except BaseException:
    raise Exception("Your redis server is not alive, please check again.")


api_id = API_ID
api_hash = API_HASH

updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
client = TelegramClient("saber", API_ID, API_HASH)
pbot = Client("saberPyro", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

dispatcher = updater.dispatcher

SUDO_USERS = list(SUDO_USERS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)

# Load at end to ensure all prev variables have been set
from tg_bot.modules.helper_funcs.handlers import CustomCommandHandler

if CUSTOM_CMD and len(CUSTOM_CMD) >= 1:
    tg.CommandHandler = CustomCommandHandler
