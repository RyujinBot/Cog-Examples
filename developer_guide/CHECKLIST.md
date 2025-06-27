# ✅ Developer Checklist

## 🚀 Pre-Development Checklist

### Before Starting
- [ ] **Read the README.md** thoroughly
- [ ] **Choose the right template** for your cog type
- [ ] **Plan your command structure** and parameters
- [ ] **Understand the category** you're working in
- [ ] **Check existing cogs** for similar functionality

## 📝 Code Structure Checklist

### Required Elements
- [ ] **Import statements** are correct
- [ ] **Class name** follows naming convention (`YourCogNameCog`)
- [ ] **Constructor** includes bot and RYUJIN_LOGO
- [ ] **Blacklist methods** are implemented:
  - [ ] `check_blacklist(self, user_id)`
  - [ ] `create_blacklist_embed(self, reason)`
- [ ] **Command decorators** are properly formatted
- [ ] **Setup function** is present at the end

### Command Structure
- [ ] **Blacklist check** is the first thing in every command
- [ ] **Permission checks** are implemented where needed
- [ ] **Role hierarchy checks** are included for moderation commands
- [ ] **Parameter validation** is thorough
- [ ] **Error handling** with try-catch blocks
- [ ] **Embed creation** follows guidelines
- [ ] **Footer and author** are set correctly
- [ ] **Response order** is correct: `maybe_send_ad()` then `interaction.send()`

## 🔒 Security Checklist

### Permission Checks
- [ ] **User permissions** are verified
- [ ] **Bot permissions** are checked
- [ ] **Role hierarchy** is respected
- [ ] **Self-moderation** is prevented
- [ ] **Bot protection** is implemented

### Input Validation
- [ ] **All parameters** are validated
- [ ] **Edge cases** are handled
- [ ] **Invalid inputs** return helpful error messages
- [ ] **SQL injection** is prevented (if using database)
- [ ] **Rate limiting** is considered (if needed)

## 🎨 UI/UX Checklist

### Embed Design
- [ ] **Title** is descriptive and uses appropriate emoji
- [ ] **Description** is clear and informative
- [ ] **Color** matches the action type:
  - 🟢 Green for success
  - 🔴 Red for errors/bans
  - 🟡 Yellow for warnings
  - 🟠 Orange for special actions
  - 🔵 Blue for information
- [ ] **Fields** are organized logically
- [ ] **Footer text** uses correct system name
- [ ] **Author** is set to "Ryujin" with logo

### User Experience
- [ ] **Error messages** are helpful and specific
- [ ] **Success messages** provide useful information
- [ ] **Loading states** are handled (if needed)
- [ ] **Confirmation** is requested for destructive actions
- [ ] **DM notifications** are sent when appropriate

## 📊 Database Checklist (if applicable)

### Database Integration
- [ ] **Import statements** include database functions
- [ ] **Connection** is accessed via `self.bot.connection`
- [ ] **Error handling** for database operations
- [ ] **Data validation** before database operations
- [ ] **Transaction handling** for complex operations
- [ ] **Connection cleanup** is handled properly

### Data Management
- [ ] **Server-specific data** is properly scoped
- [ ] **User data** is handled securely
- [ ] **Data retrieval** is efficient
- [ ] **Data formatting** is consistent
- [ ] **Empty results** are handled gracefully

## 🧪 Testing Checklist

### Functionality Testing
- [ ] **Command works** with valid inputs
- [ ] **Command handles** invalid inputs gracefully
- [ ] **Permission checks** work correctly
- [ ] **Blacklist system** works as expected
- [ ] **Error scenarios** are handled properly
- [ ] **Database operations** succeed and fail appropriately

### User Role Testing
- [ ] **Admin users** can use the command
- [ ] **Moderator users** can use the command (if applicable)
- [ ] **Regular users** are blocked appropriately
- [ ] **Users without permissions** get proper error messages
- [ ] **Bot permissions** are verified

### Edge Case Testing
- [ ] **Self-targeting** is prevented
- [ ] **Bot-targeting** is prevented
- [ ] **Role hierarchy** is respected
- [ ] **Invalid user IDs** are handled
- [ ] **Network errors** are handled
- [ ] **Database connection issues** are handled

## 📋 Final Review Checklist

### Code Quality
- [ ] **Code is readable** and well-commented
- [ ] **Variable names** are descriptive
- [ ] **Functions** are properly structured
- [ ] **No hardcoded values** (use constants)
- [ ] **No unused imports** or variables
- [ ] **Consistent formatting** throughout

### Documentation
- [ ] **Docstrings** are present for complex functions
- [ ] **Comments** explain complex logic
- [ ] **Command descriptions** are clear and helpful
- [ ] **Parameter descriptions** are informative
- [ ] **Usage examples** are provided (if needed)

### Performance
- [ ] **Database queries** are optimized
- [ ] **API calls** are handled efficiently
- [ ] **Memory usage** is reasonable
- [ ] **Response times** are acceptable
- [ ] **No infinite loops** or blocking operations

## 🚀 Submission Checklist

### Before Submitting
- [ ] **All tests pass** locally
- [ ] **Code is reviewed** by yourself
- [ ] **Template is followed** correctly
- [ ] **No sensitive data** is included
- [ ] **File is placed** in correct directory
- [ ] **Setup function** is properly named

### Final Checks
- [ ] **Command name** is unique and descriptive
- [ ] **File name** matches the command
- [ ] **Category placement** is correct
- [ ] **Import statements** are complete
- [ ] **Error handling** is comprehensive
- [ ] **User experience** is smooth

## 🎯 Quality Assurance

### Code Review Questions
- [ ] Would another developer understand this code?
- [ ] Is the error handling comprehensive?
- [ ] Are the security measures adequate?
- [ ] Is the user experience intuitive?
- [ ] Does it follow the established patterns?
- [ ] Is it maintainable and scalable?

### Performance Questions
- [ ] Will this work efficiently with many users?
- [ ] Are database queries optimized?
- [ ] Is memory usage reasonable?
- [ ] Are API calls minimized?
- [ ] Is the response time acceptable?

## 📞 Getting Help

If you're stuck on any of these items:
1. **Check existing cogs** for examples
2. **Review the README.md** again
3. **Look at the templates** for guidance
4. **Ask in the development channel**
5. **Test with a simple version first**

## 🎉 Success Criteria

Your cog is ready when:
- ✅ All checkboxes are completed
- ✅ Code follows established patterns
- ✅ Security measures are in place
- ✅ User experience is smooth
- ✅ Error handling is comprehensive
- ✅ Performance is acceptable

**Remember: Quality over speed! Take your time to do it right.** 🚀 