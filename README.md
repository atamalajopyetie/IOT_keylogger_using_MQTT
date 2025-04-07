# IoT-Based Keylogger Using Raspberry Pi & Client-Server Architecture

This project is an IoT-based keylogger that uses a **Raspberry Pi as the server** and a **laptop as the client** to capture and log keystrokes in real-time over a secure, encrypted communication channel. The system is built on a **Client-Server architecture** and utilizes **RSA encryption** for secure key transmission.

---
## 🔐 File Structure
├── client.py
├── server.py
├── key_generation.py
├── public_key.pem
├── private_key.pem
├── keylogs.txt
├── decrypted_keylogs.txt

---

## 🛠️ Components

- **client.py** - Runs on the laptop to capture keystrokes and send them to the Raspberry Pi server.
- **server.py** - Runs on the Raspberry Pi to receive, decrypt, and log keystrokes.
- **key_generation.py** - Generates RSA public and private keys.
- **public_key.pem** - The RSA public key used by the client for encryption.
- **private_key.pem** - The RSA private key used by the server for decryption.
- **keylogs.txt** - Encrypted keystroke log file.
- **decrypted_keylogs.txt** - Decrypted keystrokes, readable format.
The sample keys are provided to you and the sample textfiles are provided as well.
---

## 🔐 Features

- Real-time keylogging with secure data transmission.
- RSA encryption and decryption for secure communication.
- Client-server model using sockets.
- Keys are displayed live in the terminal and stored in log files.
- Modular design for easy customization and scalability.

---

## 🚀 How to Run
On Raspberry Pi:
`python3 key_generation.py    # (Run once)`
`python3 server.py`

On Laptop:
Ensure public_key.pem from Raspberry Pi is available.
Install pynput and cryptography if not installed:
`pip install pynput cryptography`
`python3 client.py`

Transfer public_key.pem to the client (laptop) via SCP, USB, etc.

## ⚠️ Disclaimer
This tool is created strictly for educational and ethical research purposes only. Unauthorized keylogging or surveillance without explicit permission is illegal and unethical. Use responsibly.

[Video of working model](https://drive.google.com/file/d/1SvaFqat4ApiX03u0O4HUiX92ge7rPDVk/view?usp=drive_link "Video of working model")
