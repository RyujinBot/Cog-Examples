# 📚 Real-World Examples

## 🎯 Information Commands

### Simple Info Command
```python
@nextcord.slash_command(
    name="ping",
    description="Check bot latency."
)
async def ping(self, interaction: nextcord.Interaction):
    user_id = interaction.user.id
    is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
    
    if is_blacklisted:
        embed = self.create_blacklist_embed(blacklist_reason)
        await interaction.send(embed=embed, ephemeral=True)
        return

    latency = round(self.bot.latency * 1000)
    
    embed = nextcord.Embed(
        title="🏓 Pong!",
        description=f"**Bot Latency:** {latency}ms",
        color=nextcord.Color.green()
    )
    embed.set_footer(
        text="© Ryujin Bot (2023-2025) | Information System",
        icon_url=self.RYUJIN_LOGO
    )
    embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)

    await self.bot.maybe_send_ad(interaction)
    await interaction.send(embed=embed, ephemeral=True)
```

### User Info Command
```python
@nextcord.slash_command(
    name="userinfo",
    description="Get information about a user."
)
async def userinfo(
    self,
    interaction: nextcord.Interaction,
    user: nextcord.Member = nextcord.SlashOption(
        name="user",
        description="The user to get info about",
        required=False
    )
):
    user_id = interaction.user.id
    is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
    
    if is_blacklisted:
        embed = self.create_blacklist_embed(blacklist_reason)
        await interaction.send(embed=embed, ephemeral=True)
        return

    target_user = user or interaction.user
    
    embed = nextcord.Embed(
        title="👤 User Information",
        description=f"Information about **{target_user.mention}**",
        color=nextcord.Color.blue()
    )
    embed.add_field(name="Username", value=f"{target_user.name}", inline=True)
    embed.add_field(name="Display Name", value=f"{target_user.display_name}", inline=True)
    embed.add_field(name="ID", value=f"{target_user.id}", inline=True)
    embed.add_field(name="Joined Server", value=f"<t:{int(target_user.joined_at.timestamp())}:R>", inline=True)
    embed.add_field(name="Account Created", value=f"<t:{int(target_user.created_at.timestamp())}:R>", inline=True)
    embed.add_field(name="Top Role", value=f"{target_user.top_role.mention}", inline=True)
    
    embed.set_thumbnail(url=target_user.display_avatar.url)
    embed.set_footer(
        text="© Ryujin Bot (2023-2025) | Information System",
        icon_url=self.RYUJIN_LOGO
    )
    embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)

    await self.bot.maybe_send_ad(interaction)
    await interaction.send(embed=embed, ephemeral=True)
```

## 🛡️ Moderation Commands

### Kick Command
```python
@nextcord.slash_command(
    name="kick",
    description="Kick a member from the server.",
    default_member_permissions=nextcord.Permissions(kick_members=True)
)
async def kick(
    self,
    interaction: nextcord.Interaction,
    user: nextcord.Member = nextcord.SlashOption(
        name="user",
        description="The user to kick",
        required=True
    ),
    reason: str = nextcord.SlashOption(
        name="reason",
        description="Reason for the kick",
        required=False
    )
):
    user_id = interaction.user.id
    is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
    
    if is_blacklisted:
        embed = self.create_blacklist_embed(blacklist_reason)
        await interaction.send(embed=embed, ephemeral=True)
        return

    if not interaction.user.guild_permissions.kick_members:
        await interaction.send("❌ You don't have permission to kick members.", ephemeral=True)
        return

    if user.top_role >= interaction.user.top_role:
        await interaction.send("❌ You can't kick this user due to role hierarchy.", ephemeral=True)
        return

    if user.id == interaction.user.id:
        await interaction.send("❌ You can't kick yourself.", ephemeral=True)
        return

    try:
        kick_reason = reason or "No reason provided"
        await user.kick(reason=f"{interaction.user.name}: {kick_reason}")
        
        embed = nextcord.Embed(
            title="👢 User Kicked",
            description=f"**{user.mention}** has been kicked from the server.",
            color=nextcord.Color.red()
        )
        embed.add_field(name="User", value=f"{user.mention} ({user.name})", inline=True)
        embed.add_field(name="Kicked by", value=f"{interaction.user.mention} ({interaction.user.name})", inline=True)
        embed.add_field(name="Reason", value=kick_reason, inline=False)
        
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Moderation System",
            icon_url=self.RYUJIN_LOGO
        )
        embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)

        await self.bot.maybe_send_ad(interaction)
        await interaction.send(embed=embed, ephemeral=True)

    except Exception as e:
        await interaction.send(f"❌ An error occurred: `{e}`", ephemeral=True)
```

### Timeout Command with Duration
```python
@nextcord.slash_command(
    name="timeout",
    description="Timeout a member.",
    default_member_permissions=nextcord.Permissions(moderate_members=True)
)
async def timeout(
    self,
    interaction: nextcord.Interaction,
    user: nextcord.Member = nextcord.SlashOption(
        name="user",
        description="The user to timeout",
        required=True
    ),
    duration: str = nextcord.SlashOption(
        name="duration",
        description="Timeout duration (e.g., 1d, 2h, 30m)",
        required=True
    ),
    reason: str = nextcord.SlashOption(
        name="reason",
        description="Reason for the timeout",
        required=False
    )
):
    user_id = interaction.user.id
    is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
    
    if is_blacklisted:
        embed = self.create_blacklist_embed(blacklist_reason)
        await interaction.send(embed=embed, ephemeral=True)
        return

    if not interaction.user.guild_permissions.moderate_members:
        await interaction.send("❌ You don't have permission to timeout members.", ephemeral=True)
        return

    if user.top_role >= interaction.user.top_role:
        await interaction.send("❌ You can't timeout this user due to role hierarchy.", ephemeral=True)
        return

    # Parse duration
    from datetime import datetime, timedelta
    
    def parse_duration(duration_str):
        duration_str = duration_str.lower()
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
            else:
                minutes = int(duration_str)
                return timedelta(minutes=minutes)
        except ValueError:
            return None

    duration_delta = parse_duration(duration)
    if not duration_delta:
        await interaction.send("❌ Invalid duration format. Use: 1d, 2h, 30m, etc.", ephemeral=True)
        return

    if duration_delta > timedelta(days=28):
        await interaction.send("❌ Timeout cannot exceed 28 days.", ephemeral=True)
        return

    try:
        timeout_reason = reason or "No reason provided"
        await user.timeout(duration_delta, reason=f"{interaction.user.name}: {timeout_reason}")
        
        embed = nextcord.Embed(
            title="⏰ User Timed Out",
            description=f"**{user.mention}** has been timed out.",
            color=nextcord.Color.yellow()
        )
        embed.add_field(name="User", value=f"{user.mention} ({user.name})", inline=True)
        embed.add_field(name="Timed out by", value=f"{interaction.user.mention} ({interaction.user.name})", inline=True)
        embed.add_field(name="Duration", value=duration, inline=True)
        embed.add_field(name="Expires", value=f"<t:{int((datetime.now() + duration_delta).timestamp())}:R>", inline=True)
        embed.add_field(name="Reason", value=timeout_reason, inline=False)
        
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Moderation System",
            icon_url=self.RYUJIN_LOGO
        )
        embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)

        await self.bot.maybe_send_ad(interaction)
        await interaction.send(embed=embed, ephemeral=True)

    except Exception as e:
        await interaction.send(f"❌ An error occurred: `{e}`", ephemeral=True)
```

## 🎵 Media Commands

### Audio Processing Command
```python
@nextcord.slash_command(
    name="nightcore",
    description="Convert audio to nightcore style."
)
async def nightcore(
    self,
    interaction: nextcord.Interaction,
    speed: float = nextcord.SlashOption(
        name="speed",
        description="Speed multiplier (1.0-3.0)",
        required=False,
        min_value=1.0,
        max_value=3.0
    ),
    pitch: float = nextcord.SlashOption(
        name="pitch",
        description="Pitch multiplier (1.0-3.0)",
        required=False,
        min_value=1.0,
        max_value=3.0
    )
):
    user_id = interaction.user.id
    is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
    
    if is_blacklisted:
        embed = self.create_blacklist_embed(blacklist_reason)
        await interaction.send(embed=embed, ephemeral=True)
        return

    # Check if user is in a voice channel
    if not interaction.user.voice:
        await interaction.send("❌ You must be in a voice channel to use this command.", ephemeral=True)
        return

    try:
        speed = speed or 1.25
        pitch = pitch or 1.25
        
        embed = nextcord.Embed(
            title="🎵 Nightcore Processing",
            description=f"Processing audio with nightcore settings...",
            color=nextcord.Color.blue()
        )
        embed.add_field(name="Speed", value=f"{speed}x", inline=True)
        embed.add_field(name="Pitch", value=f"{pitch}x", inline=True)
        embed.add_field(name="Channel", value=f"{interaction.user.voice.channel.name}", inline=True)
        
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Media Processing System",
            icon_url=self.RYUJIN_LOGO
        )
        embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)

        await self.bot.maybe_send_ad(interaction)
        await interaction.send(embed=embed, ephemeral=True)

        # Your audio processing logic here
        # ...

    except Exception as e:
        await interaction.send(f"❌ An error occurred: `{e}`", ephemeral=True)
```

## 🎮 Community Commands

### AFK Command
```python
@nextcord.slash_command(
    name="afk",
    description="Set your AFK status."
)
async def afk(
    self,
    interaction: nextcord.Interaction,
    reason: str = nextcord.SlashOption(
        name="reason",
        description="Reason for being AFK",
        required=False
    )
):
    user_id = interaction.user.id
    is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
    
    if is_blacklisted:
        embed = self.create_blacklist_embed(blacklist_reason)
        await interaction.send(embed=embed, ephemeral=True)
        return

    try:
        afk_reason = reason or "No reason provided"
        
        # Store AFK data (you'd implement this with your database)
        # await store_afk_data(self.bot.connection, interaction.user.id, afk_reason)
        
        embed = nextcord.Embed(
            title="😴 AFK Status Set",
            description=f"**{interaction.user.mention}** is now AFK.",
            color=nextcord.Color.blue()
        )
        embed.add_field(name="User", value=f"{interaction.user.mention} ({interaction.user.name})", inline=True)
        embed.add_field(name="Reason", value=afk_reason, inline=True)
        embed.add_field(name="Status", value="😴 AFK", inline=True)
        
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Social & Community System",
            icon_url=self.RYUJIN_LOGO
        )
        embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)

        await self.bot.maybe_send_ad(interaction)
        await interaction.send(embed=embed, ephemeral=True)

    except Exception as e:
        await interaction.send(f"❌ An error occurred: `{e}`", ephemeral=True)
```

## 🔧 Development Commands

### Bot Stats Command
```python
@nextcord.slash_command(
    name="botstats",
    description="Show bot statistics."
)
async def botstats(self, interaction: nextcord.Interaction):
    user_id = interaction.user.id
    is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
    
    if is_blacklisted:
        embed = self.create_blacklist_embed(blacklist_reason)
        await interaction.send(embed=embed, ephemeral=True)
        return

    if not interaction.user.guild_permissions.administrator:
        await interaction.send("❌ You need administrator permissions to view bot stats.", ephemeral=True)
        return

    try:
        embed = nextcord.Embed(
            title="📊 Bot Statistics",
            description="Current bot performance and usage statistics.",
            color=nextcord.Color.green()
        )
        embed.add_field(name="Servers", value=f"{len(self.bot.guilds)}", inline=True)
        embed.add_field(name="Users", value=f"{len(self.bot.users)}", inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Uptime", value=f"<t:{int(self.bot.start_time.timestamp())}:R>", inline=True)
        embed.add_field(name="Commands", value=f"{len(self.bot.commands)}", inline=True)
        embed.add_field(name="Cogs", value=f"{len(self.bot.cogs)}", inline=True)
        
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Development System",
            icon_url=self.RYUJIN_LOGO
        )
        embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)

        await self.bot.maybe_send_ad(interaction)
        await interaction.send(embed=embed, ephemeral=True)

    except Exception as e:
        await interaction.send(f"❌ An error occurred: `{e}`", ephemeral=True)
```

## 💡 Tips and Best Practices

### 1. Error Handling
Always wrap your main logic in try-catch blocks and provide specific error messages.

### 2. Permission Checks
Check both user and bot permissions before executing commands.

### 3. Role Hierarchy
For moderation commands, always check role hierarchy to prevent abuse.

### 4. User Experience
Provide clear feedback and use appropriate colors for different types of actions.

### 5. Database Operations
Handle database errors gracefully and provide fallback responses.

### 6. Performance
Keep database queries efficient and avoid blocking operations.

### 7. Security
Validate all inputs and prevent common security issues.

### 8. Consistency
Follow the established patterns and use consistent formatting throughout your code.

## 🎯 Common Patterns

### Duration Parsing
```python
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
```

### DM Sending with Error Handling
```python
try:
    dm_embed = nextcord.Embed(
        title="Notification Title",
        description="Your notification message here",
        color=nextcord.Color.blue()
    )
    dm_embed.set_footer(
        text="© Ryujin Bot (2023-2025) | System Name",
        icon_url=self.RYUJIN_LOGO
    )
    
    await user.send(embed=dm_embed)
    dm_sent = True
except:
    dm_sent = False
```

### Parameter Validation
```python
# Check if user is in voice channel
if not interaction.user.voice:
    await interaction.send("❌ You must be in a voice channel to use this command.", ephemeral=True)
    return

# Check if user is not the bot
if user.id == self.bot.user.id:
    await interaction.send("❌ You can't target the bot.", ephemeral=True)
    return

# Check if user is not self
if user.id == interaction.user.id:
    await interaction.send("❌ You can't target yourself.", ephemeral=True)
    return
```

Use these examples as reference when creating your own cogs! 🚀 