import dotenv

dotenv.load_dotenv()

import constants as const
import calendar as cal
import discord
import logging

from discord.ext import commands, tasks


log = logging.getLogger('discord')
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    config = (f'token set?: {const.TOKEN is not None}; guild: {const.GUILD}; old cal channel: {const.OLD_CAL_CHANNEL}, '
              f'new cal channel: {const.NEW_CAL_CHANNEL}')
    print(config)
    await post_readings.start()


@tasks.loop(seconds=1.0)
async def post_readings():
    print('sending messages')
    old_cal_channel = await bot.fetch_channel(const.OLD_CAL_CHANNEL)
    print(f'Got old cal channel: {old_cal_channel}')
    new_cal_channel = await bot.fetch_channel(const.NEW_CAL_CHANNEL)
    print(f'Got new cal channel: {new_cal_channel}')
    exit()


@post_readings.before_loop
async def before():
    await bot.wait_until_ready()
    print(f'{bot.user} is ready.')



bot.run(const.TOKEN)
