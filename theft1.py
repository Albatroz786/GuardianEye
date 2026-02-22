import cv2
import numpy as np
import smtplib
import random
from email.message import EmailMessage
import time
import tkinter as tk
from tkinter import ttk, messagebox
from twilio.rest import Client
import threading
from PIL import Image, ImageTk
import sv_ttk  # For modern theme
import os
from dotenv import load_dotenv

load_dotenv()

# Twilio Credentials
TWILIO_SID = os.getenv("TWILIO_SID")  # Replace with your Twilio SID
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")  # Replace with your Twilio Auth Token
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")  # Replace with your Twilio phone number

# Email Credentials
EMAIL_SENDER =os.getenv(" EMAIL_SENDER") # Replace with your Gmail email
EMAIL_PASSWORD =os.getenv("EMAIL_PASSWORD")  # Replace with your Gmail password


class ObjectMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Theft Alert Detector - GuardianEye")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        # Apply modern theme
        sv_ttk.set_theme("dark")

        # App variables
        self.user_email = ""
        self.user_phone = ""
        self.otp_generated = ""
        self.selected_objects = []
        self.status_var = tk.StringVar(
            value="Please enter your email and phone number to begin."
        )
        self.cap = None  # Add this line

        # Load logo
        try:
            self.logo_img = Image.open("logo.png").resize((150, 50))
            self.logo_img = ImageTk.PhotoImage(self.logo_img)
        except:
            self.logo_img = None

        self.create_widgets()

    def create_widgets(self):
        # Header Frame
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=10, fill="x", padx=20)

        if self.logo_img:
            ttk.Label(header_frame, image=self.logo_img).pack(side="left")
        else:
            ttk.Label(
                header_frame, text="GuardianEye", font=("Helvetica", 16, "bold")
            ).pack(side="left")

        ttk.Label(
            header_frame, text="Theft Alert Detector", font=("Helvetica", 12)
        ).pack(side="right")

        # Separator
        ttk.Separator(self.root).pack(fill="x", padx=20, pady=5)

        # Main Container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # User Input Section
        input_frame = ttk.LabelFrame(main_frame, text="User Credentials", padding=15)
        input_frame.pack(fill="x", pady=10)

        ttk.Label(input_frame, text="Email Address:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.email_entry = ttk.Entry(input_frame, width=38)
        self.email_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(input_frame, text="Phone Number ():").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.phone_entry = ttk.Entry(input_frame, width=38)
        self.phone_entry.grid(row=1, column=1, pady=5, padx=5)

        self.otp_button = ttk.Button(
            input_frame,
            text="Send Verification Code",
            command=self.send_otp,
            style="Accent.TButton",
        )
        self.otp_button.grid(row=2, column=0, columnspan=2, pady=15)

        # Verification Section
        verify_frame = ttk.LabelFrame(main_frame, text="Verification", padding=15)
        verify_frame.pack(fill="x", pady=10)

        ttk.Label(verify_frame, text="Enter Verification Code:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.otp_entry = ttk.Entry(verify_frame, width=20)
        self.otp_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        self.verify_button = ttk.Button(
            verify_frame,
            text="Verify Code",
            command=self.verify_otp,
            style="Accent.TButton",
        )
        self.verify_button.grid(row=1, column=1, pady=10, sticky="") # Removed 'ew' sticky

        # Object Selection Section
        self.object_frame = ttk.LabelFrame(main_frame, text="Object Monitoring", padding=15)
        self.object_frame.pack(fill="x", pady=10)

        self.select_button = ttk.Button(
            self.object_frame,
            text="Select Object to Monitor",
            command=self.select_object,
            state="disabled",
            style="Accent.TButton",
        )
        self.select_button.pack(pady=10)

        # Status Section
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill="x", pady=10)

        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            wraplength=400,
            justify="center",
            foreground="#4CAF50",
        )
        self.status_label.pack(fill="x")

        # Footer
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill="x", pady=10)

        ttk.Label(
            footer_frame,
            text="© 2023 Theft Alert Detector-GuardianEye",
            font=("Helvetica", 8),
            foreground="gray",
        ).pack(side="bottom")

        # Center the window
        self.root.eval("tk::PlaceWindow . center")

    def send_otp(self):
        self.user_email = self.email_entry.get()
        self.user_phone = self.phone_entry.get()

        if not self.user_email or not self.user_phone:
            messagebox.showerror("Error", "Both email and phone fields are required.")
            return

        if "@" not in self.user_email or "." not in self.user_email:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        self.otp_generated = str(random.randint(100000, 999999))
        msg = EmailMessage()
        msg.set_content(f"Your GuardianEye verification code is: {self.otp_generated}")
        msg["Subject"] = "GuardianEye Verification Code"
        msg["From"] = EMAIL_SENDER
        msg["To"] = self.user_email

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)

            self.status_var.set(f"Verification code sent to {self.user_email}")
            self.otp_button.config(state="disabled")
            self.root.after(
                30000, lambda: self.otp_button.config(state="normal")
            )  # Re-enable after 30 sec
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to send verification code: {str(e)}"
            )

    def verify_otp(self):
        if not self.otp_entry.get():
            messagebox.showerror("Error", "Please enter the verification code.")
            return

        if self.otp_entry.get() == self.otp_generated:
            self.status_var.set(
                "Verification successful! You can now select an object to monitor."
            )
            self.select_button.config(state="normal")
            self.verify_button.config(state="disabled")
            self.otp_entry.config(state="disabled")
        else:
            messagebox.showerror("Error", "Invalid verification code. Please try again.")

    def select_object(self):
        self.status_var.set("Preparing camera for object selection...")
        threading.Thread(target=self.open_cv_object_selection, daemon=True).start()

    def open_cv_object_selection(self):
        self.cap = cv2.VideoCapture(0)  # Capture video globally
        time.sleep(2)
        ret, frame = self.cap.read()
        # cap.release() # Release inside start_monitoring and here.

        if ret:
            frame = cv2.flip(frame, 1)
            roi = cv2.selectROI(
                "Select Object to Monitor", frame, fromCenter=False, showCrosshair=True
            )
            cv2.destroyAllWindows()

            if roi[2] > 0 and roi[3] > 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                selected = gray[
                    int(roi[1]) : int(roi[1] + roi[3]), int(roi[0]) : int(roi[0] + roi[2])
                ]
                self.selected_objects.clear()
                self.selected_objects.append(selected)
                self.status_var.set(f"Object selected! Monitoring is now active.")
                threading.Thread(target=self.start_monitoring, daemon=True).start()
            else:
                self.status_var.set("Object selection was cancelled.")
                if self.cap.isOpened():
                    self.cap.release()  # Release the camera if no object is selected.
        else:
            self.status_var.set("Error: Could not read frame during object selection.")
            if self.cap and self.cap.isOpened():
                self.cap.release()

    def send_alerts(self, frame):
        image_path = "alert_image.jpg"
        cv2.imwrite(image_path, frame)

        # Email Alert
        msg = EmailMessage()
        msg.set_content("ALERT: Your monitored object has been removed or displaced!")
        msg["Subject"] = "GuardianEye Alert: Object Removed"
        msg["From"] = EMAIL_SENDER
        msg["To"] = self.user_email

        with open(image_path, "rb") as img:
            msg.add_attachment(img.read(), maintype="image", subtype="jpeg", filename="alert.jpg")

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)
        except Exception as e:
            print(f"Email alert failed: {e}")

        # SMS Alert
        try:
            client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
            client.messages.create(
                body="ALERT: Your monitored object has been removed! Check your email for details.",
                from_=TWILIO_PHONE_NUMBER,
                to=self.user_phone,
            )
        except Exception as e:
            print(f"SMS alert failed: {e}")

        self.status_var.set("Alerts sent! Monitoring continues...")

    def start_monitoring(self):
        # cap = cv2.VideoCapture(0) # remove this line
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.status_var.set("Error: Could not open camera for monitoring.")
                return

        object_present = True
        cv2.namedWindow("GuardianEye Monitoring")

        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN and 10 <= x <= 210 and 10 <= y <= 40:
                if self.cap and self.cap.isOpened():  # Check if the camera is open
                    self.cap.release()
                cv2.destroyAllWindows()
                self.status_var.set("Please select a new object to monitor.")
                threading.Thread(target=self.select_object, daemon=True).start()

        cv2.setMouseCallback("GuardianEye Monitoring", mouse_callback)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame")
                self.status_var.set("Error: Could not read frame from camera.")
                break

            frame = cv2.flip(frame, 1)

            # Add UI elements to the camera feed
            cv2.putText(
                frame,
                "Press 'Q' to quit",
                (frame.shape[1] - 200, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

            if self.selected_objects:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                missing = 0
                for obj in self.selected_objects:
                    result = cv2.matchTemplate(gray, obj, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(result)
                    if max_val < 0.5:
                        missing += 1

                if missing == len(self.selected_objects) and object_present:
                    self.status_var.set("ALERT: Object removed! Sending notifications...")
                    self.send_alerts(frame)
                    object_present = False

            cv2.imshow("GuardianEye Monitoring", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        if self.cap and self.cap.isOpened():  # Check if the camera is open before releasing
            self.cap.release()
        cv2.destroyAllWindows()
        self.status_var.set("Monitoring session ended. You may select a new object.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectMonitorApp(root)
    root.mainloop()