import discord

from discord.ext.commands import Cog, command, Context

from utils.impersonate_webhook import ImpersonateWebhook
from db import db


class Pinboard(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji != "📌" or user.bot:
            return

        # check if there is a pinboard configured for the current guild
        pinboard_channel_id = self._get_pinboard_channel(reaction.message.guild.id)
        if not pinboard_channel_id:
            return

        message = reaction.message
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
