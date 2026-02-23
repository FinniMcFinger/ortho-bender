import dotenv

dotenv.load_dotenv()

import constants as const
import cal
import posts

import aiocron
import discord
import logging

from discord.ext import commands


class CronJobs:
    def __init__(self, bot: commands.Bot) -> None:
        log = logging.getLogger('CronJobs')

        @aiocron.crontab(const.CRON_TIME)
        async def post_readings():
            log.debug('sending messages')
            old_cal_channel = await bot.fetch_channel(const.OLD_CAL_CHANNEL)
            log.debug(f'Got old cal channel: {old_cal_channel}')
            new_cal_channel = await bot.fetch_channel(const.NEW_CAL_CHANNEL)
            log.debug(f'Got new cal channel: {new_cal_channel}')
            old_cal_data = cal.get_today_data(use_new_cal=False)
            old_cal_content = cal.get_post_contents(old_cal_data)
            old_cal_messages = posts.create_messages(old_cal_content)
            new_cal_data = cal.get_today_data()
            new_cal_content = cal.get_post_contents(new_cal_data)
            new_cal_messages = posts.create_messages(new_cal_content)

            for message in old_cal_messages:
                await old_cal_channel.send(message)

            for message in new_cal_messages:
                await new_cal_channel.send(message)


class Bender(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', help_command=None, intents=discord.Intents.default())
        self.log = logging.getLogger('Bender')

    async def setup_hook(self) -> None:
        cron = CronJobs(self)

    async def close(self):
        await super().close()

    async def on_ready(self) -> None:
        config = (
            f'token set?: {const.TOKEN is not None}; guild: {const.GUILD}; old cal channel: {const.OLD_CAL_CHANNEL}, '
            f'new cal channel: {const.NEW_CAL_CHANNEL}')
        self.log.info(config)


bender = Bender()
bender.run(const.TOKEN)
