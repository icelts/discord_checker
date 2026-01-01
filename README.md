# Discord Token Checker

A Discord token checker that categorizes tokens into banned, phone verification required, and valid accounts.

## Features

- Check Discord tokens efficiently
- Categorize results into:
  - **Banned** - Tokens that have been banned by Discord
  - **Phone Verification Required** - Tokens that require phone number verification
  - **Valid** - Normal, working tokens
- Simple and clean web interface
- Progress tracking with JSON file
- Easy to use

## Usage Options

### Option 1: Run Locally

#### Requirements

- Python 3.x
- Required Python packages

#### Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app/main.py
   ```

3. Open your browser and navigate to the web interface URL.

### Option 2: Use Online Checker

If you prefer not to configure your local environment, you can run the checker directly on our website:

**https://www.discordtokenchecker.com/**

Simply visit the website and follow the instructions to check your tokens online.

## Project Structure

```
discord_checker/
├── app/
│   ├── checker.py      # Core checking logic
│   ├── main.py         # Main application entry
│   └── utils.py        # Utility functions
├── static/
│   └── frontend.html   # Web interface
└── result/
    └── progress.json   # Progress tracking data
```

## License

This project is open source and available for educational purposes.

## Disclaimer

This tool is for educational purposes only. Use responsibly and respect Discord's Terms of Service.
