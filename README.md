# 🔐 SecureBank Lab

## 📌 Overview

SecureBank Lab is a deliberately vulnerable banking web application
built in a controlled virtualized environment for practicing
Web Application Penetration Testing.

The objective is to reproduce a realistic penetration testing workflow:
reconnaissance, enumeration, vulnerability discovery, exploitation,
impact analysis and documentation.

## 🏗️ Lab Environment

- Virtualized Linux environment
- Flask web application
- SQLite database
- Controlled laboratory environment

## 🛠️ Technologies

- Python
- Flask
- SQLite
- HTML
- Linux
- Nmap
- Git / GitHub

## 🔎 Pentesting Methodology

```text
Reconnaissance
      ↓
Enumeration
      ↓
Vulnerability Discovery
      ↓
Validation / Exploitation
      ↓
Impact Analysis
      ↓
Documentation
      ↓
Remediation
🧪 Security Testing
IDOR / Broken Access Control

During testing, an IDOR vulnerability was identified in the
user profile functionality.

The application uses a user-controlled identifier:

/user?id=1

By modifying the identifier, an authenticated user can access
another user's information without an appropriate authorization check.

This demonstrates an access control vulnerability.

📸 Screenshots

Screenshots documenting the security testing process are available
in the screenshots/ directory.

⚠️ Disclaimer

This project is intentionally vulnerable and is used exclusively
for educational purposes in a controlled laboratory environment.

It must not be deployed on or used against systems without
explicit authorization.

🚀 Project Status

The laboratory is continuously being expanded with additional
security testing, vulnerability analysis and documentation.


ومن بعد:
