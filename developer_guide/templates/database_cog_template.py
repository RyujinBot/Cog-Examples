"""
Database Cog Template for Ryujin Bot
Use this template for creating cogs that need database integration.
"""

import nextcord
from nextcord.ext import commands
from cogs.utils.db import add_warning, get_warning_count, get_user_warnings

class DatabaseCogTemplate(commands.Cog):
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

    # EXAMPLE: Command that adds data to database
    @nextcord.slash_command(
        name="add_data",
        description="An example command that adds data to the database."
    )
    async def add_data(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(
            name="user",
            description="The user to add data for",
            required=True
        ),
        data: str = nextcord.SlashOption(
            name="data",
            description="Data to store",
            required=True
        )
    ):
        # 1. Blacklist check
        user_id = interaction.user.id
        is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
        
        if is_blacklisted:
            embed = self.create_blacklist_embed(blacklist_reason)
            await interaction.send(embed=embed, ephemeral=True)
            return

        # 2. Permission check
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.send(
                "❌ You don't have permission to use this command.",
                ephemeral=True
            )
            return

        try:
            # 3. Database operation
            # Replace this with your actual database function
            # Example using warning system:
            warning_id = await add_warning(
                self.bot.connection,
                interaction.guild.id,
                user.id,
                interaction.user.id,
                data
            )

            if warning_id is None:
                await interaction.send(
                    "❌ Failed to add data to database.",
                    ephemeral=True
                )
                return

            # 4. Get updated data
            total_count = await get_warning_count(
                self.bot.connection,
                interaction.guild.id,
                user.id
            )

            # 5. Create success embed
            embed = nextcord.Embed(
                title="✅ Data Added",
                description=f"Data has been added for **{user.mention}**.",
                color=nextcord.Color.green()
            )
            embed.add_field(name="User", value=f"{user.mention} ({user.name})", inline=True)
            embed.add_field(name="Added by", value=f"{interaction.user.mention} ({interaction.user.name})", inline=True)
            embed.add_field(name="Data", value=data, inline=False)
            embed.add_field(name="ID", value=f"#{warning_id}", inline=True)
            embed.add_field(name="Total Count", value=f"{total_count}", inline=True)
            
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Database System",
                icon_url=self.RYUJIN_LOGO
            )
            embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)

            await self.bot.maybe_send_ad(interaction)
            await interaction.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.send(
                f"❌ An error occurred: `{e}`",
                ephemeral=True
            )

    # EXAMPLE: Command that retrieves data from database
    @nextcord.slash_command(
        name="get_data",
        description="An example command that retrieves data from the database."
    )
    async def get_data(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(
            name="user",
            description="The user to get data for",
            required=True
        )
    ):
        # 1. Blacklist check
        user_id = interaction.user.id
        is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
        
        if is_blacklisted:
            embed = self.create_blacklist_embed(blacklist_reason)
            await interaction.send(embed=embed, ephemeral=True)
            return

        # 2. Permission check
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.send(
                "❌ You don't have permission to use this command.",
                ephemeral=True
            )
            return

        try:
            # 3. Database retrieval
            # Replace with your actual database function
            data_list = await get_user_warnings(
                self.bot.connection,
                interaction.guild.id,
                user.id
            )

            total_count = await get_warning_count(
                self.bot.connection,
                interaction.guild.id,
                user.id
            )

            if not data_list:
                # No data found
                embed = nextcord.Embed(
                    title="📋 Data History",
                    description=f"**{user.mention}** has no data in this server.",
                    color=nextcord.Color.green()
                )
                embed.add_field(name="User", value=f"{user.mention} ({user.name})", inline=True)
                embed.add_field(name="Total Count", value="0", inline=True)
                embed.add_field(name="Status", value="✅ Clean record", inline=True)
                
                embed.set_footer(
                    text="© Ryujin Bot (2023-2025) | Database System",
                    icon_url=self.RYUJIN_LOGO
                )
                embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)

                await self.bot.maybe_send_ad(interaction)
                await interaction.send(embed=embed, ephemeral=True)
                return

            # 4. Format data for display
            data_text = ""
            for i, data_item in enumerate(data_list[:10], 1):  # Limit to 10 items
                data_id, moderator_id, reason, date = data_item
                
                # Try to get moderator name
                try:
                    moderator = await self.bot.fetch_user(moderator_id)
                    moderator_name = moderator.name
                except:
                    moderator_name = f"Unknown User ({moderator_id})"
                
                data_text += f"**#{data_id}** | {moderator_name} | {date}\n└ {reason}\n\n"

            if len(data_list) > 10:
                data_text += f"*... and {len(data_list) - 10} more items*"

            # 5. Create embed
            embed = nextcord.Embed(
                title="📋 Data History",
                description=f"**{user.mention}** has **{total_count}** data entries in this server.",
                color=nextcord.Color.blue()
            )
            embed.add_field(name="User", value=f"{user.mention} ({user.name})", inline=True)
            embed.add_field(name="Total Count", value=f"{total_count}", inline=True)
            embed.add_field(name="Recent Data", value=data_text, inline=False)
            
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Database System",
                icon_url=self.RYUJIN_LOGO
            )
            embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)

            await self.bot.maybe_send_ad(interaction)
            await interaction.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.send(
                f"❌ An error occurred: `{e}`",
                ephemeral=True
            )

def setup(bot):
    bot.add_cog(DatabaseCogTemplate(bot)) 