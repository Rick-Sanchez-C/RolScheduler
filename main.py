import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import functions
from VoteView import VoteView

load_dotenv()  # take environment variables from .env.
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
BOT_TOKEN = os.getenv('BOT_TOKEN')
game_info = {}


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}. Synced commands globally.')


# Slash command to create a game
@bot.tree.command(name="crear_evento", description="Crea una partida de rol")
@app_commands.describe(
    days="Días de la semana (e.g., l,m,x)",
    organizer="Organizador de la partida",
    role="Rol que puede participar",
    force_next_week="Forzar la próxima semana",
    hours="Horas a ofrecer (e.g., 15:00,20:00,20:30)"
)
async def create_game(
        interaction: discord.Interaction,
        days: str,
        organizer: discord.Member,
        role: discord.Role = None,
        force_next_week: bool = False,
        hours: str = None
):
    if not functions.check_days(days):
        await interaction.response.send_message("Días no válidos. Usa: l, m, x, j, v, s, d.", ephemeral=True)
        return
    if hours and not functions.check_hours(hours):
        await interaction.response.send_message("Horas no válidas. Usa el formato: 15:00,20:00,20:30", ephemeral=True)
        return

    hours_array = hours.split(",") if hours else None
    timestamps = functions.transform_strdays_to_timestamps(days, force_next_week, hours_array)
    mention = role.mention if role else "@everyone"
    message = await interaction.channel.send(f"Se anuncia partida de rol, elegid a que hora está disponible. {mention}")
    game_info[message.id] = {
        "organizer": organizer,
        "role": role,
        "timestamps": timestamps,
        "votes": {},
        "participants": []
    }
    await message.edit(content=message.content, view=VoteView(message.id,game_info[message.id]))





bot.run(BOT_TOKEN)
