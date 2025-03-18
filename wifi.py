import tkinter as tk
from tkinter import messagebox
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Gen Z Color Palette
BG_COLOR = "#F5F5F5"  # Light Gray
PRIMARY_COLOR = "#FF6F61"  # Coral
SECONDARY_COLOR = "#6B5B95"  # Lavender
TEXT_COLOR = "#2E2E2E"  # Dark Gray
ACCENT_COLOR = "#88B04B"  # Moss Green

# AWS IoT Configuration
AWS_ACCESS_KEY = "AKIA47CR32WJBZP3RJLG"
AWS_SECRET_KEY = "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"
AWS_REGION = "ap-south-1"
IOT_TOPIC = "pi/wifi-config"

# Function to send Wi-Fi credentials to AWS IoT
def send_credentials():
    ssid = ssid_entry.get()
    password = password_entry.get()

    if not ssid or not password:
        messagebox.showerror("Error", "Please enter both SSID and Password.")
        return

    try:
        # Initialize AWS IoT Data client
        client = boto3.client(
            "iot-data",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION,
        )

        # Publish Wi-Fi credentials to AWS IoT
        payload = f'{{"ssid":"{ssid}", "password":"{password}"}}'
        client.publish(topic=IOT_TOPIC, qos=1, payload=payload)

        messagebox.showinfo("Success", "Wi-Fi credentials sent successfully!")
    except (NoCredentialsError, PartialCredentialsError):
        messagebox.showerror("Error", "AWS credentials are missing or invalid.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Wi-Fi Configurator")
root.geometry("500x400")
root.configure(bg=BG_COLOR)

# Main Container
container = tk.Frame(root, bg="white", padx=20, pady=20)
container.pack(expand=True, fill="both", padx=20, pady=20)

# App Title
title_label = tk.Label(
    container,
    text="Wi-Fi Configurator",
    font=("Helvetica", 24, "bold"),
    fg=TEXT_COLOR,
    bg="white",
)
title_label.pack(pady=(0, 20))

# SSID Input
ssid_label = tk.Label(
    container,
    text="SSID",
    font=("Helvetica", 14),
    fg=TEXT_COLOR,
    bg="white",
)
ssid_label.pack(anchor="w", pady=(10, 5))

ssid_entry = tk.Entry(
    container,
    font=("Helvetica", 14),
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    relief="flat",
    borderwidth=1,
)
ssid_entry.pack(fill="x", pady=(0, 10))

# Password Input
password_label = tk.Label(
    container,
    text="Password",
    font=("Helvetica", 14),
    fg=TEXT_COLOR,
    bg="white",
)
password_label.pack(anchor="w", pady=(10, 5))

password_entry = tk.Entry(
    container,
    font=("Helvetica", 14),
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    relief="flat",
    borderwidth=1,
    show="*",
)
password_entry.pack(fill="x", pady=(0, 20))

# Send Button
send_button = tk.Button(
    container,
    text="Send",
    font=("Helvetica", 16, "bold"),
    bg=PRIMARY_COLOR,
    fg="white",
    activebackground=SECONDARY_COLOR,
    activeforeground="white",
    relief="flat",
    borderwidth=0,
    cursor="hand2",
    command=send_credentials,
)
send_button.pack(pady=(10, 0))

# Run the app
root.mainloop()