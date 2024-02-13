import os
from collections import deque

import discord
from discord.ext import commands
from discord.ext.commands.context import Context

q = deque()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command(name="raise")
async def _raise(ctx: Context, *, arg=None):
    match arg:
        case "list":
            print("Listing queue")
            msg = "Here is the current queue:\n"

            for person in q:
                msg += f"- {person}"

            await ctx.send(msg)
        case "clear":
            current_roles = [r.name for r in ctx.author.roles]

            if "Admin" in current_roles or "Mod" in current_roles:
                print("Clearing queue")
                q.clear()
                await ctx.send(f"Queue cleared, {ctx.author.display_name}")
            else:
                await ctx.send(
                    f"Sorry {ctx.author.display_name}, only Mods or Admins can clear the queue."
                )
        case "next":
            if len(q) < 1:
                await ctx.send("Nobody else in the queue!")
                return
            print("popping next person from queue")
            got = q.popleft()
            await ctx.send(f"Next up: {got}")
        case None:
            if ctx.author.display_name in q:
                print(f"{ctx.author.display_name} already in the queue")
                await ctx.send(
                    f"{ctx.author.display_name}, you are already in the queue"
                )
                return

            print(f"Adding {ctx.author.display_name} to queue")
            q.append(ctx.author.display_name)
            await ctx.send(f"{ctx.author.display_name} added to queue")

    # await ctx.send(f"Adding you to the queue: {ctx.author}")


def main():
    token: str = os.getenv("DISCORD_TOKEN")
    bot.run(token)


if __name__ == "__main__":
    main()
