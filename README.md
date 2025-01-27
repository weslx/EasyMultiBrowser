# Selenium Multi-Browser Manager

A Python application that manages multiple Chrome instances with automated cookie persistence and profile management using Selenium.

## Features

- 🚀 Multi-Instance Management: Launch 3 concurrent browser instances
- 🔒 Cookie Persistence: Automatically saves/loads cookies per profile
- 👤 Profile Isolation: Separate sessions using named profiles
- 🌐 Predefined URLs: Opens YouTube and Gmail by default
- 🤖 Stealth Mode: Basic anti-detection configurations
- ⚙️ Auto Driver Management: Handles ChromeDriver automatically via webdriver-manager

## Project Structure

```
selenium-browser-manager/
├── profiles/                   # Cookie storage directory
│   └── [profile_name]/         # Individual profiles
│       ├── cookies_1.pkl       # Cookies for instance 1
│       ├── cookies_2.pkl       # Cookies for instance 2
│       └── cookies_3.pkl       # Cookies for instance 3
├── main.py                     # Main application script
├── requirements.txt            # Dependency list
└── README.md                   # Documentation
```

## Prerequisites

- Python 3.7+
- Google Chrome (latest version recommended)
- Stable internet connection

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/weslx/EasyMultiBrowser
cd EasyMultiBrowser
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Choose a profile when prompted:
```bash
Select profile: work  # Type your profile name and press Enter
```

5. Interact with the opened browsers normally

6. Press Enter in the terminal when done to save cookies and exit

### Customizing URLs
Modify the PREDEFINED_URLS list in the code to open different websites:
PREDEFINED_URLS = [
    "https://www.youtube.com",
    "https://mail.google.com/mail",
    "https://github.com"
]

### Changing Browser Count
Adjust the NUM_BROWSERS value in the code to control the number of instances:
NUM_BROWSERS = 5  # Opens 5 concurrent browsers

### Profile Management
- New profiles are created automatically when entered
- Delete profile folders manually to remove associated cookies
- Profile data stored in: profiles/[your_profile_name]/

## FAQ

Q: How are cookies managed?  
A: Cookies are saved when you exit using Enter. Each instance in a profile has its own cookie file.

Q: Can I use different browsers?  
A: Currently only Chrome is supported. Modify the driver initialization for other browsers.

Q: Why am I getting detected as automation?  
A: The basic stealth settings help but aren't foolproof. Consider adding more advanced anti-detection measures.

## Troubleshooting

Issue: ChromeDriver compatibility errors  
Solution: Ensure Chrome is updated, then run:
pip install --upgrade webdriver-manager

Issue: Cookies not persisting  
Solution:
1. Wait for all sites to load completely
2. Ensure you exit using Enter in the console
3. Check write permissions for the profiles directory

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (git checkout -b feature/improvement)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request