import discord
from discord.ext import commands

# Set up the bot with member intents enabled
intents = discord.Intents.default()
intents.members = True  # To handle member events
intents.message_content = True  # To access the content of messages

bot = commands.Bot(command_prefix='/', intents=intents)


# This event will run when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Event triggered when a new member joins the server
@bot.event
async def on_member_join(member):
    # Define the channel where you want to send the welcome message
    channel = discord.utils.get(member.guild.text_channels, name='🚀﹕welcome')  # Replace 'welcome' with your channel name
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}! We're glad to have you here!")
    else:
        print(f"Channel 'welcome' not found in {member.guild.name}")

# Command to create a ticket panel
@bot.command()
async def ticketpanel(ctx):
    button = discord.ui.Button(label="Create Ticket", style=discord.ButtonStyle.green)

    async def button_callback(interaction):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True),
            ctx.guild.me: discord.PermissionOverwrite(view_channel=True)
        }
        ticket_channel = await ctx.guild.create_text_channel(f'ticket-{interaction.user.name}', overwrites=overwrites)
        await ticket_channel.send(f'{interaction.user.mention}, your ticket has been created!')

    button.callback = button_callback
    view = discord.ui.View()
    view.add_item(button)

    await ctx.send("Click the button below to create a ticket:", view=view)

# Vouch command - to vouch for another member
@bot.command()
async def vouch(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    # Define the vouch channel where you want to log vouches
    vouch_channel = discord.utils.get(ctx.guild.text_channels, name="⭐﹕vouches")  # Replace 'vouches' with your channel name
    if vouch_channel:
        await vouch_channel.send(f"{ctx.author.mention} vouched for {member.mention}. Reason: {reason}")
        await ctx.send(f"You vouched for {member.mention} successfully!")
    else:
        await ctx.send("Vouch channel not found. Please create a channel named 'vouches'.")

# Run the bot with your token
bot.run(' ')
