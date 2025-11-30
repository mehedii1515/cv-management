# Resume Parser - User Instructions

## 🚀 Quick Start (30 seconds)

1. **Extract** the Resume_Parser_Portable.zip file to any folder on your PC
2. **Open** the extracted folder and double-click `START_RESUME_PARSER.bat`
3. **Add API keys** when the notepad opens (see below for how to get them)
4. **Run again** - the application will open in your browser automatically!

## 🔑 Getting API Keys (Required)

You need at least one API key to use the AI features:

### OpenAI API Key (Recommended)
1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with sk-...)

### Google Gemini API Key (Alternative)
1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API key"
4. Copy the key

### Adding Keys to the Application
1. When you first run START_RESUME_PARSER.bat, notepad will open
2. Replace `your_openai_key_here` with your actual OpenAI key
3. Replace `your_gemini_key_here` with your actual Gemini key
4. Save the file and close notepad
5. Run START_RESUME_PARSER.bat again

## 📱 Using the Application

Once started, the application will open in your browser at:
- **Main App**: http://localhost:3000/
- **Admin Panel**: http://localhost:8000/admin/

## 💻 System Requirements

- Windows 7/8/10/11 (64-bit)
- No software installation required
- Internet connection for AI processing
- ~500MB free disk space

## 🆘 Troubleshooting

**Problem: Application won't start**
- Make sure ports 3000 and 8000 are not in use
- Try running as administrator
- Check that you have internet connection

**Problem: Can't parse resumes**
- Verify your API keys are correct in the .env file
- Make sure you have internet connection
- Check that you have credits/quota on your API account

**Problem: API key errors**
- Double-check your API keys are entered correctly
- Ensure no extra spaces in the keys
- Verify your API account has available credits

## 🛑 Stopping the Application

- Close the command window that opened when you started the app
- Or press Ctrl+C in the command window

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure you have valid API keys
3. Try running as administrator
4. Contact your IT support or the person who provided this software

---

**Note**: This is a portable application - you can copy the entire folder to any Windows PC and it will work without installation!
