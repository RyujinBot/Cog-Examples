# 📋 Coding Standards & Conventions

## 🎯 General Principles

### Code Quality
- **Readability over cleverness** - Write code that's easy to understand
- **Consistency is key** - Follow established patterns
- **Documentation matters** - Comment complex logic
- **Error handling is mandatory** - Always handle potential errors
- **Security first** - Validate all inputs and check permissions

### Performance
- **Efficient database queries** - Optimize database operations
- **Minimize API calls** - Cache data when possible
- **Avoid blocking operations** - Use async/await properly
- **Memory management** - Clean up resources properly

## 📝 Naming Conventions

### Files and Classes
```python
# File names: lowercase with underscores
user_info.py
moderation_commands.py
audio_processor.py

# Class names: PascalCase with "Cog" suffix
class UserInfoCog(commands.Cog):
class ModerationCommandsCog(commands.Cog):
class AudioProcessorCog(commands.Cog):
```

### Variables and Functions
```python
# Variables: snake_case
user_id = interaction.user.id
is_blacklisted = True
blacklist_reason = "Spam"

# Functions: snake_case
def check_blacklist(self, user_id):
def create_blacklist_embed(self, reason):
def parse_duration(self, duration_str):

# Constants: UPPER_SNAKE_CASE
RYUJIN_LOGO = "https://..."
MAX_DURATION = 28
DEFAULT_TIMEOUT = 300
```

### Command Names
```python
# Command names: descriptive and lowercase
@nextcord.slash_command(name="userinfo")
@nextcord.slash_command(name="kick_user")
@nextcord.slash_command(name="audio_nightcore")
```

## 🔧 Code Structure

### Required Imports Order
```python
# 1. Standard library imports
import os
import json
from datetime import datetime, timedelta

# 2. Third-party imports
import nextcord
from nextcord.ext import commands

# 3. Local imports
from cogs.utils.db import add_warning, get_warning_count
from cogs.utils.embeds import create_success_embed
```

### Class Structure
```python
class YourCogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.RYUJIN_LOGO = "https://cdn.discordapp.com/avatars/1059400568805785620/63a77f852ea29f37961f458c53fb5a97.png"

    # 1. Utility methods first
    def check_blacklist(self, user_id):
        # Implementation

    def create_blacklist_embed(self, reason):
        # Implementation

    # 2. Helper methods
    def parse_duration(self, duration_str):
        # Implementation

    # 3. Command methods
    @nextcord.slash_command(name="command_name")
    async def command_name(self, interaction: nextcord.Interaction):
        # Implementation

def setup(bot):
    bot.add_cog(YourCogCog(bot))
```

## 🎨 Embed Standards

### Color Guidelines
```python
# Success actions
color=nextcord.Color.green()

# Errors, bans, blacklist
color=nextcord.Color.red()

# Warnings
color=nextcord.Color.yellow()

# Special actions (softbans, etc.)
color=nextcord.Color.orange()

# Information
color=nextcord.Color.blue()

# Neutral actions
color=nextcord.Color.dark_grey()
```

### Embed Structure
```python
embed = nextcord.Embed(
    title="✅ Success Title",  # Use appropriate emoji
    description="Clear description of what happened",
    color=nextcord.Color.green()
)

# Add fields for structured information
embed.add_field(name="User", value=f"{user.mention} ({user.name})", inline=True)
embed.add_field(name="Action by", value=f"{interaction.user.mention} ({interaction.user.name})", inline=True)
embed.add_field(name="Reason", value=reason, inline=False)  # Longer content = inline=False

# Always set footer and author
embed.set_footer(
    text="© Ryujin Bot (2023-2025) | System Name",
    icon_url=self.RYUJIN_LOGO
)
embed.set_author(
    name="Ryujin",
    icon_url=self.RYUJIN_LOGO
)
```

### Footer Text Standards
```
"© Ryujin Bot (2023-2025) | [Category] System"
```

Categories:
- `Moderation System`
- `Information System`
- `Media Tools System`
- `Media Processing System`
- `After Effects System`
- `Development System`
- `Social & Community System`
- `Blacklist System`

## 🔒 Security Standards

### Permission Checks
```python
# Always check user permissions first
if not interaction.user.guild_permissions.manage_messages:
    await interaction.send("❌ You don't have permission to use this command.", ephemeral=True)
    return

# Check bot permissions
if not interaction.guild.me.guild_permissions.manage_messages:
    await interaction.send("❌ I don't have permission to use this command.", ephemeral=True)
    return

# Check role hierarchy for moderation commands
if user.top_role >= interaction.user.top_role:
    await interaction.send("❌ You can't moderate this user due to role hierarchy.", ephemeral=True)
    return
```

### Input Validation
```python
# Validate numeric inputs
if number <= 0:
    await interaction.send("❌ Number must be positive.", ephemeral=True)
    return

# Validate string inputs
if len(text) > 1000:
    await interaction.send("❌ Text is too long (max 1000 characters).", ephemeral=True)
    return

# Validate duration
if duration_delta > timedelta(days=28):
    await interaction.send("❌ Duration cannot exceed 28 days.", ephemeral=True)
    return
```

### Blacklist Check (Required)
```python
# ALWAYS check blacklist first in every command
user_id = interaction.user.id
is_blacklisted, blacklist_reason = self.check_blacklist(user_id)

if is_blacklisted:
    embed = self.create_blacklist_embed(blacklist_reason)
    await interaction.send(embed=embed, ephemeral=True)
    return
```

## 📊 Database Standards

### Connection Usage
```python
# Always use self.bot.connection
warning_id = await add_warning(
    self.bot.connection,
    interaction.guild.id,
    user.id,
    interaction.user.id,
    reason
)
```

### Error Handling
```python
try:
    result = await database_operation(self.bot.connection, ...)
    if result is None:
        await interaction.send("❌ Database operation failed.", ephemeral=True)
        return
except Exception as e:
    await interaction.send(f"❌ Database error: `{e}`", ephemeral=True)
    return
```

### Data Validation
```python
# Validate data before database operations
if not reason or len(reason.strip()) == 0:
    await interaction.send("❌ Reason cannot be empty.", ephemeral=True)
    return

# Sanitize inputs
reason = reason.strip()[:500]  # Limit length
```

## 🚀 Command Standards

### Command Structure
```python
@nextcord.slash_command(
    name="command_name",
    description="Clear description of what the command does.",
    default_member_permissions=nextcord.Permissions(permission_name=True)  # If needed
)
async def command_name(
    self,
    interaction: nextcord.Interaction,
    param1: str = nextcord.SlashOption(
        name="param1",
        description="Description of parameter",
        required=True
    ),
    param2: int = nextcord.SlashOption(
        name="param2",
        description="Description of parameter",
        required=False,
        min_value=1,
        max_value=100
    )
):
    # 1. Blacklist check
    user_id = interaction.user.id
    is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
    
    if is_blacklisted:
        embed = self.create_blacklist_embed(blacklist_reason)
        await interaction.send(embed=embed, ephemeral=True)
        return

    # 2. Permission checks
    if not interaction.user.guild_permissions.required_permission:
        await interaction.send("❌ You don't have permission to use this command.", ephemeral=True)
        return

    # 3. Parameter validation
    if param2 and param2 <= 0:
        await interaction.send("❌ Parameter must be positive.", ephemeral=True)
        return

    # 4. Main logic
    try:
        # Your command logic here
        
        # 5. Create response
        embed = nextcord.Embed(
            title="✅ Success",
            description="Success message",
            color=nextcord.Color.green()
        )
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | System Name",
            icon_url=self.RYUJIN_LOGO
        )
        embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)

        # 6. Send response (order matters!)
        await self.bot.maybe_send_ad(interaction)
        await interaction.send(embed=embed, ephemeral=True)

    except Exception as e:
        await interaction.send(f"❌ An error occurred: `{e}`", ephemeral=True)
```

### Response Order (Critical)
```python
# CORRECT ORDER:
await self.bot.maybe_send_ad(interaction)
await interaction.send(embed=embed, ephemeral=True)

# WRONG ORDER:
await interaction.send(embed=embed, ephemeral=True)
await self.bot.maybe_send_ad(interaction)
```

## 📝 Documentation Standards

### Comments
```python
# Use comments to explain complex logic
def parse_duration(self, duration_str):
    """Parse duration string (e.g., '1d', '2h', '30m') and return timedelta"""
    if not duration_str:
        return None
    
    # Handle permanent duration
    if duration_str.lower() in ["permanent", "perm"]:
        return None
    
    # Parse numeric duration with units
    try:
        if duration_str.endswith('d'):
            days = int(duration_str[:-1])
            return timedelta(days=days)
        # ... more parsing logic
    except ValueError:
        return None
```

### Docstrings
```python
def complex_function(self, param1, param2):
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
    
    Returns:
        Description of what is returned
    
    Raises:
        ExceptionType: When and why this exception is raised
    """
    # Implementation
```

## 🧪 Testing Standards

### Test Cases to Consider
- [ ] Valid inputs work correctly
- [ ] Invalid inputs are handled gracefully
- [ ] Permission checks work
- [ ] Blacklist system works
- [ ] Error scenarios are handled
- [ ] Database operations succeed/fail appropriately
- [ ] Edge cases are covered

### Testing Checklist
```python
# Test these scenarios:
# 1. Normal usage
# 2. Missing permissions
# 3. Invalid parameters
# 4. Blacklisted user
# 5. Role hierarchy issues
# 6. Database errors
# 7. Network errors
# 8. Self-targeting
# 9. Bot-targeting
```

## 🚫 Common Mistakes to Avoid

### Don't Do This
```python
# ❌ No blacklist check
async def command(self, interaction):
    # Missing blacklist check
    pass

# ❌ No permission check
async def command(self, interaction):
    # Missing permission validation
    pass

# ❌ No error handling
async def command(self, interaction):
    # No try-catch block
    result = some_operation()
    await interaction.send(result)

# ❌ Wrong response order
async def command(self, interaction):
    await interaction.send(embed=embed)
    await self.bot.maybe_send_ad(interaction)  # Wrong order!

# ❌ Hardcoded values
embed.set_footer(text="© Ryujin Bot | System")  # Missing year and logo

# ❌ Inconsistent naming
class userInfoCog(commands.Cog):  # Wrong naming convention
    pass
```

### Do This Instead
```python
# ✅ Proper blacklist check
async def command(self, interaction):
    user_id = interaction.user.id
    is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
    
    if is_blacklisted:
        embed = self.create_blacklist_embed(blacklist_reason)
        await interaction.send(embed=embed, ephemeral=True)
        return

# ✅ Proper permission check
async def command(self, interaction):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.send("❌ You don't have permission.", ephemeral=True)
        return

# ✅ Proper error handling
async def command(self, interaction):
    try:
        result = some_operation()
        embed = create_success_embed(result)
        await self.bot.maybe_send_ad(interaction)
        await interaction.send(embed=embed, ephemeral=True)
    except Exception as e:
        await interaction.send(f"❌ Error: `{e}`", ephemeral=True)

# ✅ Correct response order
async def command(self, interaction):
    await self.bot.maybe_send_ad(interaction)
    await interaction.send(embed=embed, ephemeral=True)

# ✅ Proper footer
embed.set_footer(
    text="© Ryujin Bot (2023-2025) | System Name",
    icon_url=self.RYUJIN_LOGO
)

# ✅ Consistent naming
class UserInfoCog(commands.Cog):  # Correct naming convention
    pass
```

## 🎯 Quality Checklist

Before submitting your code, ensure:
- [ ] All naming follows conventions
- [ ] Error handling is comprehensive
- [ ] Security measures are in place
- [ ] Performance is acceptable
- [ ] Documentation is clear
- [ ] Code is readable and maintainable
- [ ] All tests pass
- [ ] No hardcoded values
- [ ] Consistent formatting throughout

**Remember: Quality code is maintainable code!** 🚀 