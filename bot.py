import os
from collections import deque

import discord
from discord.ext import commands

q = deque()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command(name="raise")
async def _raise(
    ctx: commands.context.Context,
    *,
    arg=None,
):
    match arg:
        case "help":
            msg = "Here are some commands you can run\n"
            msg += "- `!raise` - add yourself to the queue\n"
            msg += "- `!raise list` - list the current queue\n"
            msg += "- `!raise next` - get the next person up from the queue - _Admin/Mods only_\n"
            msg += "- `!raise clear` - clear the queue -  _Admin/Mods only_\n"
            await ctx.send(msg)
        case "list":
            print("Listing queue")
            if len(q) < 1:
                await ctx.send("The queue is empty!")
            else:
                msg = "Here is the current queue:\n"

                for person in q:
                    msg += f"- {person}\n"

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
            current_roles = [r.name for r in ctx.author.roles]
            if "Admin" in current_roles or "Mod" in current_roles:
                if len(q) < 1:
                    await ctx.send("Nobody else in the queue!")
                    return
                print("popping next person from queue")
                got = q.popleft()
                await ctx.send(f"Next up: {got}")
            else:
                await ctx.send(
                    f"Sorry {ctx.author.display_name}, only Mods or Admins can get the next up person"
                )
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


def main():
    token: str = os.getenv("DISCORD_TOKEN")
    bot.run(token)


if __name__ == "__main__":
    main()
