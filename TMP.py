import requests, os, random, string, time, pyfiglet
from colorama import Fore, init
import locale

init(autoreset=True)

# Language configurations
LANGUAGES = {
    "en": {
        "menu_title": "Welcome to TMP-mail tool by mowhn! Please select an option:",
        "current_mail": "Your Mail: {}",
        "no_mail": "Mail: No temporary email generated",
        "menu_options": [
            "Generate Temporary Email",
            "Fetch Emails",
            "View Email Content", 
            "Delete Email",
            "Exit"
        ],
        "available_domains": "Available domains:",
        "choose_domain": "Choose a domain (1-{}):",
        "email_gen_options": [
            "Randomly generate username",
            "Custom username"
        ],
        "email_gen_prompt": "How would you like to generate your temporary email with domain '{}'?",
        "enter_username": "Enter your custom username:",
        "email_deleted": "Temporary email '{}' deleted successfully.",
        "no_messages": "No messages to view.",
        "message_list_format": "{}. From: {} Subject: {}",
        "view_message_prompt": "Enter the message number to view full content:",
        "email_content_header": "Full Email Content:",
        "press_enter": "Press Enter to go back to the menu.",
        "invalid_message": "Invalid message number.",
        "invalid_input": "Invalid input.",
        "generate_first": "You need to generate an email first.",
        "no_email_delete": "No email to delete.",
        "invalid_choice": "Invalid input. Please enter a number between 1 and {}.",
        "choose_option": "Choose an option:"
    },
    "zh": {
        "menu_title": "欢迎使用 TMP-mail 工具！请选择一个选项：",
        "current_mail": "当前邮箱: {}",
        "no_mail": "邮箱: 尚未生成临时邮箱",
        "menu_options": [
            "生成临时邮箱",
            "获取邮件",
            "查看邮件内容",
            "删除邮箱",
            "退出"
        ],
        "available_domains": "可用域名：",
        "choose_domain": "请选择域名 (1-{})：",
        "email_gen_options": [
            "随机生成用户名",
            "自定义用户名"
        ],
        "email_gen_prompt": "请选择如何生成域名为 '{}' 的临时邮箱？",
        "enter_username": "请输入自定义用户名：",
        "email_deleted": "临时邮箱 '{}' 已成功删除。",
        "no_messages": "没有可查看的邮件。",
        "message_list_format": "{}. 发件人: {} 主题: {}",
        "view_message_prompt": "请输入要查看的邮件编号：",
        "email_content_header": "邮件完整内容：",
        "press_enter": "按回车键返回菜单。",
        "invalid_message": "无效的邮件编号。",
        "invalid_input": "无效的输入。",
        "generate_first": "请先生成一个临时邮箱。",
        "no_email_delete": "没有可删除的邮箱。",
        "invalid_choice": "无效的输入。请输入1到{}之间的数字。",
        "choose_option": "请选择一个选项："
    }
}

BASE_URL = "https://inboxes.com"
HEADERS = {
    "authority": "inboxes.com", "accept": "*/*", "accept-language": "en-US,en;q=0.9", 
    "referer": "https://inboxes.com/", "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"', 
    "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": '"Android"', "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", 
    "sec-fetch-site": "same-origin", "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
}

def clear_terminal(): 
    os.system("cls" if os.name == "nt" else "clear")

def print_banner(): 
    print(Fore.GREEN + pyfiglet.figlet_format("TMP-mail by mowhn", font="slant"))

def get_language():
    clear_terminal()
    print_banner()
    print(f"{Fore.CYAN}Please select language / 请选择语言:")
    print(f"{Fore.GREEN}1. English")
    print(f"{Fore.GREEN}2. 中文")
    
    while True:
        try:
            choice = int(input(f"{Fore.MAGENTA}Enter choice / 输入选项 (1-2): ").strip())
            if choice == 1:
                return "en"
            elif choice == 2:
                return "zh"
            else:
                print(f"{Fore.RED}Invalid choice / 无效选项")
        except ValueError:
            print(f"{Fore.RED}Invalid input / 无效输入")

CURRENT_LANG = get_language()
TEXTS = LANGUAGES[CURRENT_LANG]

def fetch_domains_mowhn():
    try:
        response = requests.get(f"{BASE_URL}/api/v2/domain", headers=HEADERS)
        if response.status_code == 200:
            domains = response.json().get("domains", [])
            return [domain["qdn"] for domain in domains]
        return []
    except Exception:
        return []

def create_temp_mail_mowhn(username: str, domain: str) -> str | None:
    try:
        email = f"{username}@{domain}"
        response = requests.get(f"{BASE_URL}/api/v2/inbox/{email}", headers=HEADERS)
        return email if response.status_code == 200 else None
    except Exception:
        return None

def generate_random_username_mowhn(length: int = 8) -> str:
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def get_emails_mowhn(email: str) -> list:
    try:
        response = requests.get(f"{BASE_URL}/api/v2/inbox/{email}", headers=HEADERS)
        return response.json().get("msgs", []) if response.status_code == 200 else []
    except Exception:
        return []

def fetch_email_content_mowhn(uid: str) -> dict | None:
    try:
        response = requests.get(f"{BASE_URL}/api/v2/message/{uid}", headers=HEADERS)
        return response.json() if response.status_code == 200 else None
    except Exception:
        return None

def delete_email_mowhn(email):
    response = requests.delete(f"{BASE_URL}/api/v2/inbox/{email}", headers=HEADERS)
    if response.status_code == 200:
        print(f"{Fore.YELLOW}{TEXTS['email_deleted'].format(email)}")

def prompt_for_choice_mowhn(options, prompt_message):
    while True:
        print(f"\n{Fore.CYAN}{prompt_message}")
        for idx, option in enumerate(options, 1): print(f"{Fore.GREEN}{idx}. {option}")
        try:
            choice = int(input(f"{Fore.MAGENTA}{TEXTS['choose_option']} ").strip())
            if 1 <= choice <= len(options): return choice
        except ValueError: 
            print(f"{Fore.RED}{TEXTS['invalid_choice'].format(len(options))}")

def handle_generate_email_mowhn(temp_email):
    if temp_email:
        delete_email_mowhn(temp_email)

    domains = fetch_domains_mowhn()
    if not domains: return None
    print(f"\n{Fore.YELLOW}{TEXTS['available_domains']}")
    
    available_domains = domains[:20]
    for idx, domain in enumerate(available_domains, 1): 
        print(f"{Fore.CYAN}{idx}. {domain}")
    
    domain_choice = int(input(f"{Fore.MAGENTA}{TEXTS['choose_domain'].format(len(available_domains))}: ").strip()) - 1
    if domain_choice < 0 or domain_choice >= len(available_domains): return None
    
    selected_domain = available_domains[domain_choice]
    choice = prompt_for_choice_mowhn(
        TEXTS['email_gen_options'],
        f"{Fore.GREEN}{TEXTS['email_gen_prompt'].format(selected_domain)}"
    )
    
    if choice == 1: 
        return create_temp_mail_mowhn(generate_random_username_mowhn(), selected_domain)
    elif choice == 2:
        return create_temp_mail_mowhn(
            input(f"{Fore.MAGENTA}{TEXTS['enter_username']} ").strip(),
            selected_domain
        )

def handle_view_email_content_mowhn(messages):
    if not messages: 
        print(f"{Fore.RED}{TEXTS['no_messages']}")
        return
    
    for i, msg in enumerate(messages, 1):
        print(TEXTS['message_list_format'].format(
            f"{Fore.GREEN}{i}",
            f"{Fore.YELLOW}{msg['f']}",
            f"{Fore.YELLOW}{msg['s']}"
        ))
    
    try:
        msg_num = int(input(f"\n{Fore.MAGENTA}{TEXTS['view_message_prompt']} ").strip())
        if 1 <= msg_num <= len(messages): 
            email_content = fetch_email_content_mowhn(messages[msg_num - 1]["uid"])
            if email_content:
                print(f"\n{Fore.CYAN}{TEXTS['email_content_header']}\n"
                      f"{Fore.YELLOW}From: {email_content['f']}\n"
                      f"{Fore.YELLOW}Subject: {email_content['s']}\n"
                      f"{Fore.WHITE}Text: {email_content['text']}")
                
                input(f"\n{Fore.MAGENTA}{TEXTS['press_enter']}")
        else:
            print(f"{Fore.RED}{TEXTS['invalid_message']}")
    except ValueError:
        print(f"{Fore.RED}{TEXTS['invalid_input']}")

def main_mowhn():
    clear_terminal()
    print_banner()

    temp_email, messages = None, []
    try:
        while True:
            menu_message = (TEXTS['current_mail'].format(temp_email) 
                          if temp_email else TEXTS['no_mail'])
            choice = prompt_for_choice_mowhn(
                TEXTS['menu_options'],
                f"{menu_message}\n\n{TEXTS['menu_title']}"
            )

            if choice == 1:
                temp_email = handle_generate_email_mowhn(temp_email)
                if temp_email: messages = get_emails_mowhn(temp_email)
            elif choice == 2:
                if temp_email: messages = get_emails_mowhn(temp_email)
                else: print(f"{Fore.RED}{TEXTS['generate_first']}")
            elif choice == 3:
                if temp_email: handle_view_email_content_mowhn(messages)
                else: print(f"{Fore.RED}{TEXTS['generate_first']}")
            elif choice == 4:
                if temp_email: 
                    delete_email_mowhn(temp_email)
                    temp_email = None
                    messages = []
                else: print(f"{Fore.RED}{TEXTS['no_email_delete']}")
            elif choice == 5: 
                if temp_email:
                    # 静默删除，不显示消息
                    requests.delete(f"{BASE_URL}/api/v2/inbox/{temp_email}", headers=HEADERS)
                break

            time.sleep(2)
            clear_terminal()
    finally:
        if temp_email:
            # 静默删除，不显示消息
            requests.delete(f"{BASE_URL}/api/v2/inbox/{temp_email}", headers=HEADERS)

if __name__ == "__main__":
    main_mowhn()
