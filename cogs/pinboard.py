import discord

from discord.ext.commands import Cog, command, Context

from utils.impersonate_webhook import ImpersonateWebhook
from db import db


class Pinboard(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_add(self, payload : discord.RawReactionActionEvent):
        if  payload.emoji.name != "📌":
            return

        guild_id = payload.guild_id
        channel_id = payload.channel_id
        message_id = payload.message_id
        user_id = payload.user_id


        if db.fetchone("SELECT 1 FROM pin_log WHERE message_id = ?",message_id):
            return

        db.execute(
            "INSERT INTO pin_log(guild_id, channel_id, message_id, user_id) VALUES (?, ?, ?, ?)",
            guild_id, channel_id, message_id, user_id
        )

        # check if there is a pinboard configured for the current guild
        pinboard_channel_id = self._get_pinboard_channel(guild_id)
        if not pinboard_channel_id:
            return
        
        current_channel = self.bot.get_channel(channel_id) or await self.bot.fetch_channel(channel_id)
        message = await current_channel.fetch_message(message_id)
        webhook = ImpersonateWebhook(
            self.bot, channel_id=pinboard_channel_id, name="pinboard-hook"
        )

        await webhook.impersonate_message(message)

    @command()
    async def pinboard(self, ctx: Context, channel: discord.TextChannel):
        """'!pinboard [channel]' sets the channel where the pins will be posted"""
        self._set_pinboard_channel(ctx.guild.id, channel.id)
        await ctx.send(f"Pinboard channel set to {channel.mention}.")

    @staticmethod
    def _set_pinboard_channel(guild_id: int, channel_id: int):
        db.execute(
            "REPLACE INTO config(guild_id, config_key, config_value) VALUES (?, ?, ?)",
            guild_id,
            "pinboard_channel",
            channel_id,
        )

    @staticmethod
    def _get_pinboard_channel(guild_id: int):
        result = db.fetchone(
            "SELECT config_value FROM config WHERE guild_id = ? AND config_key = ?",
            guild_id,
            "pinboard_channel",
        )
        
        return int(result[0]) if result else None



async def setup(bot):
    await bot.add_cog(Pinboard(bot))
