import os
import time
import requests
from pyfiglet import Figlet
from rich.console import Console
from rich.text import Text
from rich.style import Style

# ===============  COLOR UTILS ===============
def gradient_color(start_hex, end_hex, steps):
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2 ,4))
    
    def rgb_to_hex(rgb_color):
        return "#{:02x}{:02x}{:02x}".format(*rgb_color)

    start_rgb = hex_to_rgb(start_hex)
    end_rgb = hex_to_rgb(end_hex)
    gradient = []

    for i in range(steps):
        ratio = i / (steps - 1)
        interpolated = tuple(
            int(start_rgb[j] + (end_rgb[j] - start_rgb[j]) * ratio) for j in range(3)
        )
        gradient.append(rgb_to_hex(interpolated))

    return gradient

# ===============  ANIMATED TITLE ===============
def animate_title():
    console = Console()
    fig = Figlet(font="slant")
    title_text = "Spamhook"

    colors = [
        ("#a020f0", "#ff8c00"),
        ("#ff8c00", "#ffff00"),
        ("#ffff00", "#a020f0"),
    ]

    for start, end in colors:
        ascii_art = fig.renderText(title_text)
        flat_text = ascii_art.replace("\n", "")
        gradient = gradient_color(start, end, len(flat_text))

        styled_text = Text()
        char_index = 0
        for line in ascii_art.splitlines():
            for char in line:
                if char != ' ':
                    styled_text.append(char, style=Style(color=gradient[char_index], bold=True))
                    char_index += 1
                else:
                    styled_text.append(" ")
            styled_text.append("\n")

        console.clear()
        console.print(styled_text)
        time.sleep(0.2)

# ===============  MAIN FUNCTION ===============
def main():
    animate_title()

    if not os.path.exists("messages.txt"):
        print("[!] Oops! An error occurred, do you have a txt in the same folder?")
        input("Press Enter to exit...")
        return

    with open("messages.txt", "r", encoding="utf-8") as file:
        ascii_content = file.read()

    use_mentions = input("Include '@everyone' at the top? (y/n): ").strip().lower() == 'y'
    if use_mentions:
        formatted_message = "@everyone\n" + ascii_content
    else:
        formatted_message = ascii_content

    webhook_url = input("Enter your Discord Webhook URL: ").strip()
    if not webhook_url.startswith("https://discord.com/api/webhooks/"):
        print("[!] Invalid webhook URL. Exiting.")
        input("Press Enter to exit...")
        return

    try:
        count = int(input("How many messages to send? "))
    except ValueError:
        print("[!] Invalid number. Exiting.")
        input("Press Enter to exit...")
        return

    print(f"\n[+] Sending {count} message(s)...\n")

    for i in range(count):
        response = requests.post(webhook_url, json={"content": formatted_message})
        if response.status_code == 204:
            print(f"[{i + 1}]  Sent Successfully")
        else:
            print(f"[{i + 1}]  Failed (Status: {response.status_code})")
        time.sleep(0.1)

    print("\n[!] Done.")
    input("Press Enter to exit...")

# ===============  START ===============
if __name__ == "__main__":
    main()
