import discord
from discord.ext import commands

from evilbot.gcpintegration.sheets import Ev1lSheetWrapper


def run_bot(token: str, sheet_wrapper: Ev1lSheetWrapper):
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(intents=intents)

    @bot.slash_command(name="ping", guild_ids=[714051795282034760])
    async def ping(ctx):
        await ctx.respond("pong")

    @bot.slash_command(name="wtb", guild_ids=[714051795282034760])
    async def wtb(ctx, commodity: discord.Option(str)):  # type: ignore
        commodity = str(commodity).upper()
        offers = list(sheet_wrapper.offerings(commodity))
        if not offers:
            await ctx.respond(f"Could not find offering for commodity '{commodity}'")
        else:
            resp = "\n".join(str(x) for x in offers)
            print(resp)
            await ctx.respond(resp)

    bot.run(token)
