import requests, os, random, string, time, pyfiglet
from colorama import Fore, init

init(autoreset=True)
BASE_URL = "https://inboxes.com"
HEADERS = {
    "authority": "inboxes.com", "accept": "*/*", "accept-language": "en-US,en;q=0.9", 
    "referer": "https://inboxes.com/", "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"', 
    "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": '"Android"', "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", 
    "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
}

def clear_terminal(): os.system("cls" if os.name == "nt" else "clear")
def print_banner(): print(Fore.GREEN + pyfiglet.figlet_format("TMP-mail by mowhn", font="slant"))

def fetch_domains_mowhn():
    response = requests.get(f"{BASE_URL}/api/v2/domain", headers=HEADERS)
    return [domain["qdn"] for domain in response.json().get("domains", [])] if response.status_code == 200 else []

def create_temp_mail_mowhn(username, domain):
    email = f"{username}@{domain}"
    response = requests.get(f"{BASE_URL}/api/v2/inbox/{email}", headers=HEADERS)
    return email if response.status_code == 200 else None

def generate_random_username_mowhn(length=8): return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def get_emails_mowhn(email):
    response = requests.get(f"{BASE_URL}/api/v2/inbox/{email}", headers=HEADERS)
    return response.json().get("msgs", []) if response.status_code == 200 else []

def fetch_email_content_mowhn(uid):
    response = requests.get(f"{BASE_URL}/api/v2/message/{uid}", headers=HEADERS)
    return response.json() if response.status_code == 200 else None

def delete_email_mowhn(email):
    response = requests.delete(f"{BASE_URL}/api/v2/inbox/{email}", headers=HEADERS)
    if response.status_code == 200:
        print(f"{Fore.YELLOW}Temporary email '{email}' deleted successfully.")

def prompt_for_choice_mowhn(options, prompt_message):
    while True:
        print(f"\n{Fore.CYAN}{prompt_message}")
        for idx, option in enumerate(options, 1): print(f"{Fore.GREEN}{idx}. {option}")
        try:
            choice = int(input(f"{Fore.MAGENTA}Choose an option: ").strip())
            if 1 <= choice <= len(options): return choice
        except ValueError: print(f"{Fore.RED}Invalid input. Please enter a number between 1 and {len(options)}.")

def handle_generate_email_mowhn(temp_email):
    # Delete old email if it exists
    if temp_email:
        delete_email_mowhn(temp_email)

    domains = fetch_domains_mowhn()
    if not domains: return None
    print(f"\n{Fore.YELLOW}Available domains:")
    
    # Provide 20+ domains
    available_domains = domains[:20]  # Adjust number based on actual response
    for idx, domain in enumerate(available_domains, 1): print(f"{Fore.CYAN}{idx}. {domain}")
    
    domain_choice = int(input(f"{Fore.MAGENTA}Choose a domain (1-{len(available_domains)}): ").strip()) - 1
    if domain_choice < 0 or domain_choice >= len(available_domains): return None
    selected_domain = available_domains[domain_choice]
    choice = prompt_for_choice_mowhn(["Randomly generate username", "Custom username"], f"{Fore.GREEN}How would you like to generate your temporary email with domain '{selected_domain}'?")
    if choice == 1: return create_temp_mail_mowhn(generate_random_username_mowhn(), selected_domain)
    elif choice == 2: return create_temp_mail_mowhn(input(f"{Fore.MAGENTA}Enter your custom username: ").strip(), selected_domain)

def handle_view_email_content_mowhn(messages):
    if not messages: 
        print(f"{Fore.RED}No messages to view.")
        return
    
    for i, msg in enumerate(messages, 1):
        print(f"{Fore.GREEN}{i}. {Fore.YELLOW}From: {msg['f']} {Fore.YELLOW}Subject: {msg['s']}")
    
    try:
        msg_num = int(input(f"\n{Fore.MAGENTA}Enter the message number to view full content: ").strip())
        if 1 <= msg_num <= len(messages): 
            email_content = fetch_email_content_mowhn(messages[msg_num - 1]["uid"])
            if email_content:
                print(f"\n{Fore.CYAN}Full Email Content:\n{Fore.YELLOW}From: {email_content['f']}\n{Fore.YELLOW}Subject: {email_content['s']}\n{Fore.WHITE}Text: {email_content['text']}")
                
                # Pause and let the user decide to go back or view another message
                input(f"\n{Fore.MAGENTA}Press Enter to go back to the menu.")
        else:
            print(f"{Fore.RED}Invalid message number.")
    except ValueError:
        print(f"{Fore.RED}Invalid input.")

def main_mowhn():
    clear_terminal()
    print_banner()

    temp_email, messages = None, []
    try:
        while True:
            menu_message = f"Your Mail: {temp_email}" if temp_email else "Mail: No temporary email generated"
            choice = prompt_for_choice_mowhn(
                ["Generate Temporary Email", "Fetch Emails", "View Email Content", "Delete Email", "Exit"],
                f"{menu_message}\n\nWelcome to TMP-mail tool by mowhn! Please select an option:"
            )

            if choice == 1:
                temp_email = handle_generate_email_mowhn(temp_email)
                if temp_email: messages = get_emails_mowhn(temp_email)
            elif choice == 2:
                if temp_email: messages = get_emails_mowhn(temp_email)
                else: print(f"{Fore.RED}You need to generate an email first.")
            elif choice == 3:
                if temp_email: handle_view_email_content_mowhn(messages)
                else: print(f"{Fore.RED}You need to generate an email first.")
            elif choice == 4:
                if temp_email: delete_email_mowhn(temp_email); temp_email = None; messages = []
                else: print(f"{Fore.RED}No email to delete.")
            elif choice == 5: break

            time.sleep(2)
            clear_terminal()
    finally:
        if temp_email: delete_email_mowhn(temp_email)

if __name__ == "__main__":
    main_mowhn()
