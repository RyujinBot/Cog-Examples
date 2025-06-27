"""
Moderation Cog Template for Ryujin Bot
Use this template for creating moderation commands.
"""

import nextcord
from nextcord.ext import commands

class ModerationCogTemplate(commands.Cog):
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

    # EXAMPLE: Moderation command with user parameter
    @nextcord.slash_command(
        name="moderate_user",
        description="An example moderation command.",
        default_member_permissions=nextcord.Permissions(manage_messages=True)
    )
    async def moderate_user(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(
            name="user",
            description="The user to moderate",
            required=True
        ),
        reason: str = nextcord.SlashOption(
            name="reason",
            description="Reason for the action",
            required=False
        )
    ):
        # 1. ALWAYS check blacklist first
        user_id = interaction.user.id
        is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
        
        if is_blacklisted:
            embed = self.create_blacklist_embed(blacklist_reason)
            await interaction.send(embed=embed, ephemeral=True)
            return

        # 2. Check permissions
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.send(
                "❌ You don't have permission to use this command.",
                ephemeral=True
            )
            return

        if not interaction.guild.me.guild_permissions.manage_messages:
            await interaction.send(
                "❌ I don't have permission to use this command.",
                ephemeral=True
            )
            return

        # 3. Check role hierarchy
        if user.top_role >= interaction.user.top_role:
            await interaction.send(
                "❌ You can't moderate this user due to role hierarchy.",
                ephemeral=True
            )
            return

        if user.top_role >= interaction.guild.me.top_role:
            await interaction.send(
                "❌ I can't moderate this user due to role hierarchy.",
                ephemeral=True
            )
            return

        # 4. Additional checks
        if user.id == interaction.user.id:
            await interaction.send(
                "❌ You can't moderate yourself.",
                ephemeral=True
            )
            return

        if user.id == self.bot.user.id:
            await interaction.send(
                "❌ You can't moderate the bot.",
                ephemeral=True
            )
            return

        # 5. Your moderation logic here
        try:
            # Replace this with your actual moderation logic
            action_reason = reason or "No reason provided"
            
            # Example: Send DM to user (if possible)
            try:
                dm_embed = nextcord.Embed(
                    title="⚠️ You have been moderated",
                    description=f"You have been moderated in **{interaction.guild.name}**",
                    color=nextcord.Color.yellow()
                )
                dm_embed.add_field(name="Reason", value=action_reason, inline=False)
                dm_embed.add_field(name="Moderated by", value=f"{interaction.user.mention} ({interaction.user.name})", inline=False)
                
                dm_embed.set_footer(
                    text="© Ryujin Bot (2023-2025) | Moderation System",
                    icon_url=self.RYUJIN_LOGO
                )
                
                await user.send(embed=dm_embed)
                dm_sent = True
            except:
                dm_sent = False

            # 6. Create success embed
            embed = nextcord.Embed(
                title="✅ User Moderated",
                description=f"**{user.mention}** has been moderated successfully.",
                color=nextcord.Color.green()
            )
            embed.add_field(name="User", value=f"{user.mention} ({user.name})", inline=True)
            embed.add_field(name="Moderated by", value=f"{interaction.user.mention} ({interaction.user.name})", inline=True)
            embed.add_field(name="Reason", value=action_reason, inline=False)
            
            if dm_sent:
                embed.add_field(name="DM Status", value="✅ DM sent to user", inline=True)
            else:
                embed.add_field(name="DM Status", value="❌ Could not send DM (DMs closed)", inline=True)
            
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Moderation System",
                icon_url=self.RYUJIN_LOGO
            )
            
            embed.set_author(
                name="Ryujin",
                icon_url=self.RYUJIN_LOGO
            )

            # 7. Send response (ORDER MATTERS!)
            await self.bot.maybe_send_ad(interaction)
            await interaction.send(embed=embed, ephemeral=True)

        except nextcord.Forbidden:
            await interaction.send(
                "❌ I don't have permission to moderate this user.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.send(
                f"❌ An error occurred while moderating the user: `{e}`",
                ephemeral=True
            )

    # EXAMPLE: Command with duration parsing
    @nextcord.slash_command(
        name="temporary_action",
        description="An example command with duration parsing.",
        default_member_permissions=nextcord.Permissions(manage_messages=True)
    )
    async def temporary_action(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(
            name="user",
            description="The user to act upon",
            required=True
        ),
        duration: str = nextcord.SlashOption(
            name="duration",
            description="Duration (e.g., 1d, 2h, 30m, permanent)",
            required=False
        ),
        reason: str = nextcord.SlashOption(
            name="reason",
            description="Reason for the action",
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

        # 2. Permission checks (same as above)
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.send("❌ You don't have permission to use this command.", ephemeral=True)
            return

        if user.top_role >= interaction.user.top_role:
            await interaction.send("❌ You can't moderate this user due to role hierarchy.", ephemeral=True)
            return

        # 3. Duration parsing
        from datetime import datetime, timedelta
        
        def parse_duration(duration_str):
            if not duration_str:
                return None
            
            duration_str = duration_str.lower()
            if duration_str == "permanent" or duration_str == "perm":
                return None
            
            try:
                if duration_str.endswith('d'):
                    days = int(duration_str[:-1])
                    return timedelta(days=days)
                elif duration_str.endswith('h'):
                    hours = int(duration_str[:-1])
                    return timedelta(hours=hours)
                elif duration_str.endswith('m'):
                    minutes = int(duration_str[:-1])
                    return timedelta(minutes=minutes)
                elif duration_str.endswith('s'):
                    seconds = int(duration_str[:-1])
                    return timedelta(seconds=seconds)
                else:
                    hours = int(duration_str)
                    return timedelta(hours=hours)
            except ValueError:
                return None

        duration_delta = parse_duration(duration) if duration else None
        is_permanent = duration_delta is None
        
        # 4. Your logic here
        try:
            action_reason = reason or "No reason provided"
            if duration and not is_permanent:
                action_reason += f" (Duration: {duration})"

            # Create embed with duration info
            embed = nextcord.Embed(
                title="⏰ Temporary Action",
                description=f"**{user.mention}** has been acted upon.",
                color=nextcord.Color.blue()
            )
            embed.add_field(name="User", value=f"{user.mention} ({user.name})", inline=True)
            embed.add_field(name="Action by", value=f"{interaction.user.mention} ({interaction.user.name})", inline=True)
            embed.add_field(name="Reason", value=action_reason, inline=False)
            
            if not is_permanent and duration_delta:
                embed.add_field(name="Duration", value=duration, inline=True)
                embed.add_field(name="Expires", value=f"<t:{int((datetime.now() + duration_delta).timestamp())}:R>", inline=True)
            else:
                embed.add_field(name="Duration", value="Permanent", inline=True)
            
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Moderation System",
                icon_url=self.RYUJIN_LOGO
            )
            embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)

            await self.bot.maybe_send_ad(interaction)
            await interaction.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.send(f"❌ An error occurred: `{e}`", ephemeral=True)

def setup(bot):
    bot.add_cog(ModerationCogTemplate(bot)) 