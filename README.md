# GuardianEye - Theft Alert Detector 🛡️👁️

GuardianEye is a real-time security application built with Python and OpenCV. It allows users to select a specific object via a camera feed and monitors it. If the object is moved or removed, the system immediately triggers an alert via Email (with a snapshot) and SMS.

## 🚀 Features
* **Live Object Tracking:** Uses OpenCV's template matching to detect if an object has been displaced.
* **Instant Email Alerts:** Sends a notification to your email with an attached image of the theft incident.
* **SMS Integration:** Delivers real-time text alerts to your mobile phone via Twilio.
* **Modern GUI:** A sleek, user-friendly interface built with `tkinter` and the `sv-ttk` dark theme.
* **Two-Factor Prep:** Includes an OTP-style verification simulation for user sessions.

---

## 🛠️ Installation

1. Clone the Repository

        bash
        git clone [https://github.com/YOUR_USERNAME/GuardianEye.git](https://github.com/YOUR_USERNAME/GuardianEye.git)
        cd GuardianEye

3. Install Dependencies
    Ensure you have Python 3.x installed. Install the required libraries using:

        Bash
        pip install -r requirements.txt

4. Configuration
    For security, this project uses environment variables. Create a .env file in the root directory and add your credentials:

        Plaintext
        TWILIO_SID=your_twilio_sid
        TWILIO_AUTH_TOKEN=your_twilio_auth_token
        TWILIO_PHONE_NUMBER=your_twilio_phone_number
        EMAIL_SENDER=your_gmail_address
        EMAIL_PASSWORD=your_gmail_app_password


🖥️ Usage

    1. Run the application:
        Bash
        python theft1.py
    2. Enter your Email and Phone Number.
    
    3. Click Send Verification Code (check your email for the 6-digit code).

    4. Once verified, click Select Object to Monitor.

    5. A camera window will open. Draw a rectangle around the object you want to protect and press ENTER or SPACE.

    6. The system is now live! If the object is removed, alerts will be sent.

    7. Press Q in the camera window to stop monitoring.

📦 Dependencies

    opencv-python - Computer vision and camera handling.
    Pillow - Image processing for the GUI.
    twilio - SMS gateway integration.
    sv-ttk - Modern visual styling.
    numpy - Array processing for image frames.
