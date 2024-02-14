import os
from collections import deque

import discord
from discord.ext import commands
from discord.types.member import Member

q = deque()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def is_mod_or_admin(m: discord.Member) -> bool:
    current_roles = [r.name for r in m.roles]

    if "Admin" in current_roles or "Mod" in current_roles:
        return True
    return False


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
            if len(q) < 1:
                await ctx.send("The queue is empty!")
            else:
                msg = "Here is the current queue:\n"

                for person in q:
                    msg += f"- {person.mention}\n"

                await ctx.send(msg)
        case "clear":
            if is_mod_or_admin(ctx.author):
                q.clear()
                await ctx.send(f"Queue cleared, {ctx.author.mention}")
            else:
                await ctx.send(
                    f"Sorry {ctx.author.mention}, only Mods or Admins can clear the queue."
                )
        case "next":
            if is_mod_or_admin(ctx.author):
                if len(q) < 1:
                    await ctx.send("Nobody else in the queue!")
                    return
                got: discord.Member = q.popleft()
                await ctx.send(f"Next up: {got.mention}")
            else:
                await ctx.send(
                    f"Sorry {ctx.author.mention}, only Mods or Admins can get the next up person"
                )
        case None:
            if ctx.author in q:
                await ctx.send(f"{ctx.author.mention}, you are already in the queue")
                return

            q.append(ctx.author)
            await ctx.send(f"{ctx.author.mention} added to queue")


def main():
    token: str = os.getenv("DISCORD_TOKEN")
    bot.run(token)


if __name__ == "__main__":
    main()
