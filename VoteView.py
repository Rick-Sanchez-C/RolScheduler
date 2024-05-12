import discord
from discord.ext import commands

class VoteView(discord.ui.View):
    def __init__(self, message_id, game_info):
        super().__init__(timeout=180)
        self.message_id = message_id
        self.game_info = game_info
        self.voted_users = set()  # Track users who have voted

        # Obtener los timestamps del mensaje correspondiente
        timestamps = self.game_info["timestamps"]

        # Crear un menú de selección múltiple
        options = [
            discord.SelectOption(label=label, value=timestamp)
            for timestamp, label in timestamps.items()
        ]

        self.select_menu = discord.ui.Select(
            placeholder="Selecciona las horas que prefieras",
            min_values=1,
            max_values=len(options),
            options=options,
            custom_id="select_menu"
        )

        self.select_menu.callback = self.select_callback
        self.add_item(self.select_menu)

        # Añadir botones para el organizador
        reset_button = discord.ui.Button(label="Resetear", style=discord.ButtonStyle.danger, custom_id="reset_button")
        complete_button = discord.ui.Button(label="Completar", style=discord.ButtonStyle.success, custom_id="complete_button")

        reset_button.callback = self.reset_button_callback
        complete_button.callback = self.complete_button_callback

        self.add_item(reset_button)
        self.add_item(complete_button)

    async def select_callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if self.game_info["role"] is not None and self.game_info["role"] not in interaction.user.roles:
            await interaction.response.send_message("No tienes permiso para votar.", ephemeral=True)
            return

        if user_id in self.voted_users:
            await interaction.response.send_message("Ya has votado.", ephemeral=True)
            return
        selected_options = self.select_menu.values
        self.game_info["votes"][user_id] = selected_options
        self.voted_users.add(user_id)
        if interaction.user.id == self.game_info["organizer"].id:
            timestamps = self.game_info["timestamps"]
            self.select_menu.options = [
                discord.SelectOption(label=label, value=timestamp)
                for timestamp, label in timestamps.items()
                if timestamp in selected_options
            ]
            self.select_menu.max_values = len(self.select_menu.options)
            self.select_menu.min_values = 1
            await interaction.message.edit(view=self)

        # Mostrar estadísticas
        await self.show_statistics(interaction)

        await interaction.response.send_message(f"Has seleccionado: {', '.join(selected_options)}", ephemeral=True)

    async def show_statistics(self, interaction):
        vote_counts = {timestamp: 0 for timestamp in self.game_info["timestamps"]}
        for votes in self.game_info["votes"].values():
            for vote in votes:
                if vote in vote_counts:
                    vote_counts[vote] += 1

        stats_message = "Estadísticas de votación:\n"
        for timestamp, count in vote_counts.items():
            stats_message += f"{self.game_info['timestamps'][timestamp]}: {count} votos\n"

        original_message = await interaction.channel.fetch_message(self.message_id)
        content_parts = original_message.content.split("\n\n")
        new_content = content_parts[0]  # Keep the initial part of the message
        new_content += f"\n\n{stats_message}"
        await original_message.edit(content=new_content)

    async def reset_button_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.game_info["organizer"].id:
            await interaction.response.send_message("Solo el organizador puede resetear la votación.", ephemeral=True)
            return

        # Resetear votos y habilitar el menú de selección
        self.game_info["votes"].clear()
        self.voted_users.clear()
        self.select_menu.disabled = False

        original_message = await interaction.channel.fetch_message(self.message_id)
        content_parts = original_message.content.split("\n\n")
        new_content = content_parts[0]  # Keep only the initial part of the message
        await original_message.edit(content=new_content)

        await interaction.message.edit(view=self)
        await interaction.response.send_message("La votación ha sido reseteada.", ephemeral=True)

    async def complete_button_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.game_info["organizer"].id:
            await interaction.response.send_message("Solo el organizador puede completar la votación.", ephemeral=True)
            return

        # Anunciar el evento completado
        await interaction.channel.send("La votación ha sido completada. El evento ha sido anunciado.")

        # Deshabilitar todos los elementos
        self.select_menu.disabled = True
        for item in self.children:
            item.disabled = True
        role = self.game_info["role"]
        mention = role.mention if role else "@everyone"
        most_voted = self.get_most_voted()
        await interaction.channel.send(f"La hora seleccionada es: {self.game_info['timestamps'][most_voted]}. {mention}")
        await interaction.message.edit(view=self)

    def get_most_voted(self):
        vote_counts = {timestamp: 0 for timestamp in self.game_info["timestamps"]}
        for votes in self.game_info["votes"].values():
            for vote in votes:
                if vote in vote_counts:
                    vote_counts[vote] += 1

        most_voted = max(vote_counts, key=vote_counts.get)
        return most_voted
