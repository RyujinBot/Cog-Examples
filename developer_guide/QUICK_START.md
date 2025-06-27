# 🚀 Quick Start Guide for Contributors

## 📋 What You Need to Know

### Before You Start
- You need Python 3.12+ installed
- Basic knowledge of Discord.py/Nextcord
- A GitHub account

### How to Contribute
1. **Fork** the repository
2. **Create** your cog in the right folder
3. **Test** your code
4. **Submit** a pull request

## 📁 Where to Put Your Cog

```
cogs/commands/[category]/[command_name].py
```

**Categories:**
- `moderation/` - Ban, kick, timeout, etc.
- `information/` - User info, server info, etc.
- `mediatools/` - Media processing commands
- `mediaprocessing/` - Audio/video processing
- `aftereffects/` - After Effects resources
- `development/` - Admin/developer commands
- `socialandcommunity/` - Community features

## ⚡ Quick Template

Copy this template and modify it for your command:

```python
import nextcord
from nextcord.ext import commands

class YourCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.RYUJIN_LOGO = "https://cdn.discordapp.com/avatars/1059400568805785620/63a77f852ea29f37961f458c53fb5a97.png"

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
        embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)
        return embed

    @nextcord.slash_command(
        name="your_command",
        description="What your command does"
    )
    async def your_command(
        self,
        interaction: nextcord.Interaction,
        # Add your parameters here
    ):
        # 1. ALWAYS check blacklist first
        user_id = interaction.user.id
        is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
        
        if is_blacklisted:
            embed = self.create_blacklist_embed(blacklist_reason)
            await interaction.send(embed=embed, ephemeral=True)
            return

        # 2. Add permission checks if needed
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.send("❌ You don't have permission.", ephemeral=True)
            return

        # 3. Your command logic here
        try:
            # Your code here
            
            # 4. Create response embed
            embed = nextcord.Embed(
                title="✅ Success",
                description="Your success message",
                color=nextcord.Color.green()
            )
            
            # 5. Set footer and author (REQUIRED)
            embed.set_footer(
                text="© Ryujin Bot (2023-2025) | Category System",  # Change category
                icon_url=self.RYUJIN_LOGO
            )
            embed.set_author(name="Ryujin", icon_url=self.RYUJIN_LOGO)

            # 6. Send response (ORDER MATTERS!)
            await self.bot.maybe_send_ad(interaction)
            await interaction.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.send(f"❌ An error occurred: `{e}`", ephemeral=True)

def setup(bot):
    bot.add_cog(YourCommandCog(bot))
```

## 🎨 Embed Colors

```python
# Success
color=nextcord.Color.green()

# Error/Ban
color=nextcord.Color.red()

# Warning
color=nextcord.Color.yellow()

# Special action
color=nextcord.Color.orange()

# Information
color=nextcord.Color.blue()
```

## 🔒 Required Checks

### For ALL Commands
```python
# 1. Blacklist check (ALWAYS FIRST)
user_id = interaction.user.id
is_blacklisted, blacklist_reason = self.check_blacklist(user_id)

if is_blacklisted:
    embed = self.create_blacklist_embed(blacklist_reason)
    await interaction.send(embed=embed, ephemeral=True)
    return
```

### For Moderation Commands
```python
# 2. Permission check
if not interaction.user.guild_permissions.manage_messages:
    await interaction.send("❌ You don't have permission.", ephemeral=True)
    return

# 3. Role hierarchy check
if user.top_role >= interaction.user.top_role:
    await interaction.send("❌ You can't moderate this user.", ephemeral=True)
    return

# 4. Self-targeting check
if user.id == interaction.user.id:
    await interaction.send("❌ You can't target yourself.", ephemeral=True)
    return
```

## 📊 Database Integration

If your command needs database:

```python
from cogs.utils.db import your_function

# Use database
result = await your_function(self.bot.connection, ...)

# Handle errors
if result is None:
    await interaction.send("❌ Database operation failed.", ephemeral=True)
    return
```

## ✅ Checklist Before PR

- [ ] Blacklist check is first in command
- [ ] Permission checks added (if needed)
- [ ] Error handling with try-catch
- [ ] Embed has footer and author
- [ ] Response order: `maybe_send_ad()` then `interaction.send()`
- [ ] Command tested with valid inputs
- [ ] Command tested with invalid inputs
- [ ] No hardcoded values
- [ ] File placed in correct category folder

## 🚫 Common Mistakes

```python
# ❌ Wrong - No blacklist check
async def command(self, interaction):
    # Missing blacklist check
    pass

# ❌ Wrong - Wrong response order
await interaction.send(embed=embed)
await self.bot.maybe_send_ad(interaction)  # Wrong!

# ❌ Wrong - No error handling
result = some_operation()
await interaction.send(result)  # No try-catch

# ✅ Correct
async def command(self, interaction):
    # Blacklist check first
    user_id = interaction.user.id
    is_blacklisted, blacklist_reason = self.check_blacklist(user_id)
    
    if is_blacklisted:
        embed = self.create_blacklist_embed(blacklist_reason)
        await interaction.send(embed=embed, ephemeral=True)
        return

    try:
        # Your logic here
        await self.bot.maybe_send_ad(interaction)
        await interaction.send(embed=embed, ephemeral=True)
    except Exception as e:
        await interaction.send(f"❌ Error: `{e}`", ephemeral=True)
```

## 🎯 Footer Text

Use the correct system name in footer:

```
"© Ryujin Bot (2023-2025) | [Category] System"
```

**Categories:**
- `Moderation System`
- `Information System`
- `Media Tools System`
- `Media Processing System`
- `After Effects System`
- `Development System`
- `Social & Community System`

## 📞 Need Help?

1. Check existing cogs for examples
2. Look at the templates in `developer_guide/templates/`
3. Ask in the development channel
4. Check the full README.md for detailed info

## 🚀 Ready to Submit?

1. Test your command thoroughly
2. Make sure it follows all patterns
3. Create your pull request
4. Describe what your command does

**Good luck! 🎯** 