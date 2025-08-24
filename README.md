# Cookie Clicker AI Automation

An intelligent automation system for Cookie Clicker that combines computer vision, AI decision-making, and web APIs to optimize gameplay strategy.

## 🚀 Features

- **Computer Vision Cookie Detection**: Uses OpenCV to automatically locate and click the cookie
- **AI-Powered Strategy**: Integrates Google's Gemini AI for optimal purchase decisions
- **Real-time Game State Analysis**: Captures game data via browser injection
- **Smart Pause/Resume Controls**: Keyboard shortcuts for manual control
- **Rate Limit Handling**: Graceful fallback when AI API limits are reached
- **Visual Feedback**: Saves screenshots with detected cookie boundaries

## 🛠 Technologies Used

- **Python**: Main automation logic
- **OpenCV**: Computer vision for cookie detection
- **Flask**: Web API for game state management
- **Google Gemini AI**: Strategic decision making
- **PyAutoGUI**: Mouse automation
- **JavaScript**: Browser userscript for game data extraction

## 📋 Prerequisites

- Python 3.7+
- Google Gemini API key
- Violentmonkey or Tampermonkey browser extension
- Cookie Clicker game (https://orteil.dashnet.org/cookieclicker/)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cookie_automation.git
   cd cookie_automation
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "API_KEY=your_google_gemini_api_key_here" > .env
   ```

4. **Install the userscript**
   - Install Violentmonkey browser extension
   - Copy the contents of `userscript.js`
   - Create new script in Violentmonkey and paste the code
   - Enable the script

## 🎮 Usage

### Step 1: Start the Flask Server
```bash
python server.py
```
The server will run on `http://localhost:5000`

### Step 2: Open Cookie Clicker
Navigate to https://orteil.dashnet.org/cookieclicker/ in your browser

### Step 3: Run the Main Bot
```bash
python main_bot.py
```

### Step 4: Take Initial Screenshot
- Press `S` key to capture a screenshot of the cookie
- The system will detect the cookie location automatically

### Step 5: Start Automation
- Press `C` key to begin automated clicking
- Press `P` key to pause (press `C` again to resume)
- Press `U` key to stop the automation

## 🎯 How It Works

### Computer Vision Pipeline
1. **Screenshot Capture**: Takes screenshot when `S` is pressed
2. **Color Detection**: Converts image to HSV and detects brown cookie color
3. **Contour Analysis**: Finds the largest brown contour (the cookie)
4. **Centroid Calculation**: Determines exact click coordinates

### AI Strategy System
1. **Game State Capture**: Browser userscript extracts current game data
2. **Data Processing**: Flask API receives and processes game state
3. **AI Analysis**: Gemini AI analyzes available purchases and recommends strategy
4. **Decision Execution**: System executes recommended purchases

### Control Flow
```
Browser Userscript → Flask API → Gemini AI → Strategic Decisions
                ↓
Screenshot → OpenCV Detection → PyAutoGUI Clicks
```

## 🎛 Keyboard Controls

| Key | Action |
|-----|--------|
| `S` | Take screenshot and detect cookie |
| `C` | Start/Resume automated clicking |
| `P` | Pause automation |
| `U` | Stop automation completely |

## 📊 Performance

- **Test Duration**: 55 minutes continuous operation
- **Peak Performance**: 5,900+ cookies per second
- **AI Integration**: ~15 minutes before rate limiting
- **Fallback Mode**: Smooth operation when AI unavailable

## 🏗 Project Structure

```
cookie-clicker-automation/
├── main_bot.py          # Main automation script with computer vision
├── server.py            # Flask API server for AI recommendations
├── userscript.js        # Browser script for game data extraction
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── screenshots/         # Generated screenshots and detection images
└── README.md           # This file
```

## 🔍 API Endpoints

- `POST /save-game-state` - Receives game state from browser
- `GET /recommend` - Returns AI-powered purchase recommendations

## 🚨 Rate Limiting

The system handles Google Gemini API rate limits gracefully:
- Continues clicking automation even without AI recommendations
- Maintains performance through fallback mechanisms
- Resumes AI guidance when rate limits reset

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This project is for educational purposes only. Use responsibly and in accordance with Cookie Clicker's terms of service.

## 🙋‍♂️ Support

If you have questions or run into issues:
1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Include screenshots and error messages when possible

---

**Built with ❤️ for learning automation, computer vision, and AI integration**
