import os

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
OLD_CAL_CHANNEL = os.getenv('OLD_CAL_CHANNEL')
NEW_CAL_CHANNEL = os.getenv('NEW_CAL_CHANNEL')
CRON_TIME = os.getenv('CRON_TIME')
TIMEZONE = os.getenv('TIMEZONE', 'America/Chicago')
