import dotenv

dotenv.load_dotenv()

import constants as const
import calendar as cal
import discord
import logging

from discord.ext import commands


GUILD = const.GUILD
log = logging.getLogger('discord')
intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents)
client.run(const.TOKEN)
