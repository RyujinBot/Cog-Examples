# 🚀 Ryujin Bot - Developer Guide

## ⚡ Quick Start for GitHub Contributors

**Just want to contribute a command?** Check out [QUICK_START.md](QUICK_START.md) for a fast guide!

---

## 📋 Table of Contents
- [Introduction](#introduction)
- [Cog Structure](#cog-structure)
- [Required Imports](#required-imports)
- [Standard Methods](#standard-methods)
- [Command Structure](#command-structure)
- [Best Practices](#best-practices)
- [Examples](#examples)
- [Database Integration](#database-integration)
- [Testing](#testing)

## 🎯 Introduction

Welcome to the Ryujin Bot development guide! This document will help you understand how to create cogs (command modules) for the bot following our established patterns and standards.

### What is a Cog?
A cog is a Python class that contains related commands and functionality. Each cog should be focused on a specific category (e.g., moderation, information, media tools).

## 📁 Cog Structure

### File Location
```
cogs/commands/[category]/[command_name].py
```

### Categories Available:
- `moderation/` - Server management commands
- `information/` - Info and utility commands
- `mediatools/` - Media processing commands
- `mediaprocessing/` - Audio/video processing
- `aftereffects/` - After Effects resources
- `development/` - Developer/admin commands
- `socialandcommunity/` - Community features

## 📦 Required Imports

```python
import nextcord
from nextcord.ext import commands
# Add other imports as needed for your specific functionality
```

## 🔧 Standard Methods

Every cog MUST include these standard methods:

### 1. Blacklist Check Methods
```python
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
```

### 2. Constructor
```python
def __init__(self, bot):
    self.bot = bot
    self.RYUJIN_LOGO = "https://cdn.discordapp.com/avatars/1059400568805785620/63a77f852ea29f37961f458c53fb5a97.png"
```

## ⚡ Command Structure

### Basic Command Template
```python
@nextcord.slash_command(
    name="command_name",
    description="Description of what the command does.",
    default_member_permissions=nextcord.Permissions(permission_name=True)  # Optional
)
async def command_name(
    self,
    interaction: nextcord.Interaction,
    # Add your parameters here
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

    # 3. Your command logic here
    try:
        # Your code here
        
        # 4. Create response embed
        embed = nextcord.Embed(
            title="✅ Success Title",
            description="Your description here",
            color=nextcord.Color.green()
        )
        
        # 5. Set footer and author
        embed.set_footer(
            text="© Ryujin Bot (2023-2025) | Category System",
            icon_url=self.RYUJIN_LOGO
        )
        
        embed.set_author(
            name="Ryujin",
            icon_url=self.RYUJIN_LOGO
        )

        # 6. Send response (order matters!)
        await self.bot.maybe_send_ad(interaction)
        await interaction.send(embed=embed, ephemeral=True)

    except Exception as e:
        await interaction.send(f"❌ An error occurred: `{e}`", ephemeral=True)
```

## 🎨 Embed Guidelines

### Colors
- 🟢 `nextcord.Color.green()` - Success actions
- 🔴 `nextcord.Color.red()` - Errors, bans, blacklist
- 🟡 `nextcord.Color.yellow()` - Warnings
- 🟠 `nextcord.Color.orange()` - Softbans, special actions
- 🔵 `nextcord.Color.blue()` - Information
- ⚫ `nextcord.Color.dark_grey()` - Neutral actions

### Footer Text Format
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

## 📊 Database Integration

### Using Database Functions
```python
from cogs.utils.db import your_function_name

# Example for warnings
from cogs.utils.db import add_warning, get_warning_count

# Use in your command
warning_id = await add_warning(
    self.bot.connection,
    interaction.guild.id,
    user.id,
    interaction.user.id,
    reason
)
```

### Creating New Database Functions
1. Add your function to `cogs/utils/db.py`
2. Follow the existing pattern
3. Use proper error handling
4. Return meaningful values

## 🔍 Best Practices

### 1. Error Handling
- Always use try-catch blocks
- Provide meaningful error messages
- Log errors appropriately

### 2. Permission Checks
- Check user permissions before executing
- Check bot permissions
- Verify role hierarchy when needed

### 3. Response Order
```python
# CORRECT ORDER:
await self.bot.maybe_send_ad(interaction)
await interaction.send(embed=embed, ephemeral=True)

# WRONG ORDER:
await interaction.send(embed=embed, ephemeral=True)
await self.bot.maybe_send_ad(interaction)
```

### 4. Embed Consistency
- Always include footer and author
- Use consistent colors
- Format descriptions properly

### 5. Parameter Validation
- Validate all user inputs
- Check for edge cases
- Provide helpful error messages

## 📝 Examples

### Simple Information Command
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

### Moderation Command
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

## 🧪 Testing

### Before Submitting
1. ✅ Test your command thoroughly
2. ✅ Check all permission scenarios
3. ✅ Verify error handling
4. ✅ Test with different user roles
5. ✅ Ensure embed formatting is correct
6. ✅ Verify database operations (if applicable)

### Testing Checklist
- [ ] Command works with valid inputs
- [ ] Command handles invalid inputs gracefully
- [ ] Permission checks work correctly
- [ ] Blacklist system works
- [ ] Embed displays correctly
- [ ] Error messages are helpful
- [ ] Database operations succeed/fail appropriately

## 📞 Support

If you need help creating cogs:
1. Check existing cogs for examples
2. Review this documentation
3. Ask in the development channel
4. Check the template files

## 🎉 Final Notes

Remember:
- **Consistency is key** - Follow the established patterns
- **Security first** - Always check permissions
- **User experience** - Provide clear feedback
- **Maintainability** - Write clean, readable code
- **Documentation** - Comment complex logic

Happy coding! 🚀 