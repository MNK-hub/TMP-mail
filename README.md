
# TMP-mail

TMP-mail is a Python-based utility for creating temporary email addresses, managing inboxes, and interacting with messages seamlessly. By leveraging reverse-engineering techniques, TMP-mail provides an unofficial API for **inboxes.com**, offering powerful capabilities to access temporary email services via a terminal interface.

---

## Features

- **Generate Temporary Emails**: Create email addresses with random or custom usernames.
- **Fetch Emails**: Refresh the inbox.
- **View Email Content**: Display the full content of received emails, including attachments.
- **Delete Inboxes**: Safely delete temporary inboxes when no longer needed.
- **Custom Domains**: Choose from over 20 domain options for your temporary address.
- **Unofficial API Integration**: Access temporary email services using reverse-engineered API endpoints.
- **User-Friendly Terminal Interface**: Intuitive interface with color-coded responses for ease of use.

---

## Prerequisites

- **Python 3.x**
- Required Python libraries (listed in `requirements.txt`):
  - `requests`
  - `pyfiglet`
  - `colorama`

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mowhn/TMP-mail.git
   cd TMP-mail
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Run the tool:
   ```bash
   python TMP.py
   ```

2. Follow the on-screen prompts to:
   - Generate a temporary email address (random or custom).
   - Fetch and refresh the inbox to check for new emails.
   - Access the full content of messages.
   - Delete temporary inboxes when done.

---

## Options

### 1. Generate Temporary Email
Create a disposable email with customizable username options. 

### 2. Fetch Emails
Refresh the inbox to check for new emails.

### 3. View Email Content
Open and display the body and metadata of a selected email.

### 4. Delete Inbox
Permanently remove the temporary email inbox.

---

## Disclaimer

**Important**: TMP-mail uses reverse engineering to interact with the unofficial API of **inboxes.com**. This tool is not officially affiliated with or supported by **inboxes.com**, and its usage may violate the website's terms of service. Users are responsible for using this tool ethically and in compliance with applicable laws.

---

## License

This project is licensed under the [MIT License](LICENSE).
