# import discord
# from discord.ext import commands
# import logging
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()
# token = os.getenv('DISCORD_TOKEN')

# # Logging setup
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# intents = discord.Intents.default()
# intents.message_content = True
# intents.members = True

# bot = commands.Bot(command_prefix='^', intents=intents)

# # Secret role name
# secret_role = "Gamer"

# # Bad words list
# bad_words = ["shit", "fuck", "bastard", "bitch", "dick", "asshole", "slut", "whore"]

# @bot.event
# async def on_ready():
#     print(f"We are ready to go in, {bot.user.name}")

# @bot.event
# async def on_member_join(member):
#     await member.send(f"Welcome to the server {member.name}!")

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     # Check for bad words
#     msg_content = message.content.lower()
#     if any(bad_word in msg_content for bad_word in bad_words):
#         try:
#             await message.delete()
#             await message.channel.send(f"{message.author.mention}, please don't use bad words!")
#         except discord.Forbidden:
#             print("Bot doesn't have permission to delete messages.")
#         return  # stop further command processing if message was deleted

#     await bot.process_commands(message)

# @bot.command()
# async def hello(ctx):
#     await ctx.send(f"Hello {ctx.author.mention}!")

# @bot.command()
# async def assign(ctx):
#     role = discord.utils.get(ctx.guild.roles, name=secret_role)
#     if role:
#         await ctx.author.add_roles(role)
#         await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
#     else:
#         await ctx.send("Role doesn't exist.")

# @bot.command()
# async def remove(ctx):
#     role = discord.utils.get(ctx.guild.roles, name=secret_role)
#     if role:
#         await ctx.author.remove_roles(role)
#         await ctx.send(f"{ctx.author.mention} has had the {secret_role} role removed.")
#     else:
#         await ctx.send("Role doesn't exist.")

# @bot.command()
# async def dm(ctx, *, msg):
#     await ctx.author.send(f"You said: {msg}")

# @bot.command()
# async def reply(ctx):
#     await ctx.reply("This is a reply to your message!")

# @bot.command()
# async def poll(ctx, *, question):
#     embed = discord.Embed(title="New Poll", description=question, color=0x00ff00)
#     poll_message = await ctx.send(embed=embed)
#     await poll_message.add_reaction("👍")
#     await poll_message.add_reaction("👎")

# @bot.command()
# @commands.has_role(secret_role)
# async def secret(ctx):
#     await ctx.send("Welcome to the club!")

# @secret.error
# async def secret_error(ctx, error):
#     if isinstance(error, commands.MissingRole):
#         await ctx.send("You do not have permission to do that!")

# bot.run(token, log_handler=handler, log_level=logging.DEBUG)




import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Logging setup
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='^', intents=intents)
secret_role = "Gamer"

# List of bad words
bad_words = [
    "shit", "fuck", "bastard", "bitch", "dick", "asshole", "slut", "whore",
    "madarchod", "behenchod", "bsdk", "mc", "bc", "chod", "chutiya", "chut", "lund",
    "gaand", "randi", "harami", "suar", "kamina", "kutte", "kutti", "bhosdike",
    "lavde", "lavda", "maadarchod", "teri maa", "teri behen", "gaand mara"
]

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} commands.")
    except Exception as e:
        print(f"⚠️ Error syncing commands: {e}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg_content = message.content.lower()
    if any(bad in msg_content for bad in bad_words):
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, please don't use bad words!")
        except discord.Forbidden:
            print("⚠️ Bot doesn't have permission to delete messages.")
        return

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    else:
        await ctx.send("Role doesn't exist.")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} role removed.")
    else:
        await ctx.send("Role doesn't exist.")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said: {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")

@bot.command()
async def poll(ctx, *, question: str = None):
    if question is None:
        await ctx.send("❗ Please provide a question for the poll.\nExample: `^poll Should we host a tournament?`")
        return

    embed = discord.Embed(
        title="🗳️ New Poll",
        description=question,
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Poll created by {ctx.author.display_name}")
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the club!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to do that!")

# ✅ Slash command (for Active Developer Badge)
@bot.tree.command(name="ping", description="Replies with Pong! (Needed for Active Developer badge)")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! 🏓, {interaction.user.mention}")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
