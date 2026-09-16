# SecureBank Lab 🔐

## Overview

SecureBank Lab is a deliberately vulnerable banking web application built in a controlled virtualized environment for practicing Web Application Penetration Testing.

The project is designed to simulate a realistic security assessment workflow, from reconnaissance and enumeration to vulnerability discovery, exploitation, impact analysis, and documentation.

## Objectives

- Practice web application penetration testing
- Understand authentication and authorization mechanisms
- Identify access control vulnerabilities
- Analyze HTTP requests and user-controlled parameters
- Document security findings and proof of concept
- Understand the impact of vulnerable application logic

## Technologies

- Python
- Flask
- SQLite
- HTML
- Linux
- Nmap
- Git / GitHub

## Pentesting Methodology

```text
Reconnaissance
      ↓
Enumeration
      ↓
Vulnerability Discovery
      ↓
Exploitation
      ↓
Impact Analysis
      ↓
Documentation
      ↓
Remediation
Security Findings
IDOR / Broken Access Control

An IDOR vulnerability was identified in the user profile functionality.

The application uses a user-controlled id parameter:

/user?id=1

By modifying the identifier, an authenticated user can access another user's information without proper authorization checks.

This demonstrates a Broken Access Control vulnerability.

Controlled Environment

This application is intentionally vulnerable and is used exclusively in a controlled laboratory environment for educational and cybersecurity training purposes.

Project Status

The laboratory is being continuously expanded with additional security testing, vulnerability analysis, and documentation.


### 3️⃣ Save

Hbet lta7t w klik:

**Commit changes**

Commit message khallih:

```text
Add project documentation
