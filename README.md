# GuardianEye
GuardianEye: A Python-based real-time theft detection system using OpenCV. Features automated object monitoring, motion/displacement sensing, and instant alerts via Email (with image attachments) and SMS (Twilio integration).
🛡️ GuardianEye: Theft Alert Detector
  GuardianEye is a smart physical security application built with Python. It allows users to monitor specific objects in a video feed. If a selected object is moved, removed, or tampered with, the system triggers   an immediate alert via Email (including a snapshot of the event) and SMS.

✨ Features
  Real-Time Object Selection: Select any object within the camera frame using a simple drag-and-drop ROI (Region of Interest) selector.

  Template Matching: Uses OpenCV's matchTemplate to track the presence of the object with a confidence threshold.

  Multi-Channel Alerts:

  Email: Sends an alert message and an image attachment of the "theft" scene using smtplib.

  SMS: Sends a text notification via the Twilio API.

  Two-Factor Verification: Integrated OTP (One-Time Password) system to verify user credentials before monitoring begins.

  Modern UI: Styled with sv_ttk for a sleek, dark-themed interface.

🚀 Getting Started
  Prerequisites
  Python 3.x

  A webcam

  A Twilio account (for SMS)

  An App Password for your Gmail account (for Email)

  Installation
  Clone the repository:

  Bash
  git clone https://github.com/yourusername/GuardianEye.git
  cd GuardianEye
  Install dependencies:
  
  Bash
  pip install opencv-python numpy twilio sv-ttk pillow
  Configuration
  Open theft1.py and update the following credentials:
  
  Python
  # Twilio Credentials
  TWILIO_SID = "your_sid_here"
  TWILIO_AUTH_TOKEN = "your_auth_token_here"
  TWILIO_PHONE_NUMBER = "your_twilio_number"
  
  # Email Credentials
  EMAIL_SENDER = "your_email@gmail.com"
  EMAIL_PASSWORD = "your_app_password" 
  Note: For Gmail, you must use an App Password, not your regular login password.

🛠️ Usage
  Run the application:
  
  Bash
  python theft1.py
  Enter your Email and Phone Number.
  
  Click Send Verification Code and enter the OTP received in your email.
  
  Click Select Object to Monitor. A camera window will open.
  
  Draw a box around the object you want to protect and press ENTER or SPACE.
  
  The system is now live! If the object is moved, you will receive an alert.
