===========================================
OFFLINE PASSWORD MANAGER — DESIGN DOCUMENT
===========================================

📌 PROJECT GOAL:
Build a lightweight, offline password manager using Python and Tkinter that securely stores and retrieves encrypted login credentials locally.

-------------------------------------------
🎯 USE CASE
-------------------------------------------
User: Security-conscious individual who:
- Does not trust cloud-based password managers
- Wants full control over their credential storage
- Needs a lightweight desktop app for daily use

-------------------------------------------
🧩 FEATURES
-------------------------------------------
1. Add new credentials
2. Store credentials securely (encrypted)
3. Decrypt vault after entering master password
4. Search or filter stored entries
5. Copy username/password to clipboard
6. Automatically clear clipboard after timeout
7. No cloud storage – all local