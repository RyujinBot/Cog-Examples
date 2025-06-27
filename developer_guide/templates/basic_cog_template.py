"""
Basic Cog Template for Ryujin Bot
Use this template as a starting point for creating new cogs.
"""

import nextcord
from nextcord.ext import commands

class BasicCogTemplate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.RYUJIN_LOGO = "https://cdn.discordapp.com/avatars/1059400568805785620/63a77f852ea29f37961f458c53fb5a97.png"

    # REQUIRED: Blacklist check methods
    def check_blacklist(self, user_id):
        if hasattr(self.bot, 'blacklist') and user_id in self.bot.blacklist:
            return True, self.bot.blacklist[user_id]
        return False, None

    def create_blacklist_embed(self, reason):
        embed = nextcord.Embed(
            title="You are blacklisted!",
            description=f"**You can't use Ryujin's commands anymore because you have been blacklisted for `{reason}`.**",
            color=nextcord.Color.red()
        )
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Blacklist System",
            icon_url=self.RYUJIN_LOGO
        )
        
        embed.set_author(
            name="Ryujin",
            icon_url=self.RYUJIN_LOGO
        )
        return embed

    # EXAMPLE: Simple command with no parameters
    @nextcord.slash_command(
        name="example",
        description="An example command that demonstrates the basic structure."
    )
    async def example(self, interaction: nextcord.Interaction):
        # 1. ALWAYS check blacklist first
        user_id = interaction.user.id
        is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
        
        if is_blacklisted:
            embed = self.create_blacklist_embed(blacklist_reason)
            await interaction.send(embed=embed, ephemeral=True)
            return

        # 2. Your command logic here
        try:
            # Replace this with your actual command logic
            result = "This is an example response!"
            
            # 3. Create response embed
            embed = nextcord.Embed(
                title="✅ Example Command",
                description=f"**Result:** {result}",
                color=nextcord.Color.green()
            )
            
            # 4. Set footer and author (REQUIRED)
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Information System",  # Change category as needed
                icon_url=self.RYUJIN_LOGO
            )
            
            embed.set_author(
                name="Ryujin",
                icon_url=self.RYUJIN_LOGO
            )

            # 5. Send response (ORDER MATTERS!)
            await self.bot.maybe_send_ad(interaction)
            await interaction.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.send(f"❌ An error occurred: `{e}`", ephemeral=True)

    # EXAMPLE: Command with parameters
    @nextcord.slash_command(
        name="example_with_params",
        description="An example command with parameters."
    )
    async def example_with_params(
        self,
        interaction: nextcord.Interaction,
        text: str = nextcord.SlashOption(
            name="text",
            description="Some text input",
            required=True
        ),
        number: int = nextcord.SlashOption(
            name="number",
            description="A number input",
            required=False
        )
    ):
        # 1. Blacklist check
        user_id = interaction.user.id
        is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
        
        if is_blacklisted:
            embed = self.create_blacklist_embed(blacklist_reason)
            await interaction.send(embed=embed, ephemeral=True)
            return

        # 2. Parameter validation
        if number and number <= 0:
            await interaction.send("❌ Number must be positive.", ephemeral=True)
            return

        # 3. Your command logic
        try:
            result = f"Text: {text}"
            if number:
                result += f"\nNumber: {number}"
            
            embed = nextcord.Embed(
                title="✅ Parameters Example",
                description=f"**Result:**\n{result}",
                color=nextcord.Color.green()
            )
            
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Information System",
                icon_url=self.RYUJIN_LOGO
            )
            embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)

            await self.bot.maybe_send_ad(interaction)
            await interaction.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.send(f"❌ An error occurred: `{e}`", ephemeral=True)

def setup(bot):
    bot.add_cog(BasicCogTemplate(bot)) 