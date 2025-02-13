from colorama import Fore, init
import sys
import time
import requests
import os
import json
from options.ipfivem import run as run_fivem
from options.cloner import main as run_cloner
import asyncio
from options.tknchecker import DiscordTokenChecker  # Update the import path

# Initialize colorama
init(autoreset=True)

# VPS IP and port for key management
VPS_IP = '147.93.87.4'
VPS_PORT = 5000

WEBHOOK_URL = "https://discord.com/api/webhooks/1339561445024862218/ArWkZhYNV0NqJN6VyDBKKsG8ZoA6f_tMoaF6suisBxAQX-9ybE5uiF21cVqp8Nfx3qRk"

# Function to generate smooth fade
def get_fade_color(position, total_length):
    # Calculate the gradient position (from 0 to 1)
    gradient_position = position / total_length

    # Choose RGB for color fading effect between lightgreen -> white -> lightgreen
    if gradient_position < 0.5:
        # Fading from lightgreen to white
        r = int(144 + (255 - 144) * (gradient_position * 2))  # From light green to white
        g = int(238 + (255 - 238) * (gradient_position * 2))  # From light green to white
        b = int(144 + (255 - 144) * (gradient_position * 2))  # From light green to white
    else:
        # Fading from white to lightgreen
        r = int(255 - (255 - 144) * ((gradient_position - 0.5) * 2))  # From white to light green
        g = int(255 - (255 - 238) * ((gradient_position - 0.5) * 2))  # From white to light green
        b = int(255 - (255 - 144) * ((gradient_position - 0.5) * 2))  # From white to light green

    return f'\033[38;2;{r};{g};{b}m'

def print_faded_text(text, end='\n'):
    total_length = len(text)
    for i, char in enumerate(text):
        color = get_fade_color(i, total_length)
        sys.stdout.write(color + char)
    sys.stdout.flush()
    sys.stdout.write(end)  # Use the end parameter to control newline

def clear_input_line():
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    sys.stdout.flush()

def get_all_users():
    response = requests.get(f'http://{VPS_IP}:{VPS_PORT}/users')
    if response.status_code == 200:
        return response.json().get('users', [])
    else:
        print("Failed to retrieve users.")
        return []

def send_login_webhook(username):
    embed = {
        "title": "User Login",
        "description": f"User **{username}** has logged in.",
        "color": 0x000000,
        "thumbnail": {
            "url": "https://media.discordapp.net/attachments/1133865773178306620/1339501535213785088/IMG_5723.jpg?ex=67aef384&is=67ada204&hm=97400105948c32870cb7ed7915a5d0023be99fa8483be7691b36df6966a8d9e0&=&format=webp&width=444&height=443"
        }
    }

    data = {
        "embeds": [embed]
    }

    response = requests.post(WEBHOOK_URL, data=json.dumps(data), headers={"Content-Type": "application/json"})

    if response.status_code != 204:
        print("Failed to send webhook notification.")

def login():
    while True:
        os.system('cls')  # Clear the screen on Windows
        print_faded_text("[#] ./777 Services Provided by kirito.011")
        print_faded_text("[%] User: ", end='')  # No newline
        username = input()  # Input on the same line

        response = requests.get(f'http://{VPS_IP}:{VPS_PORT}/check', params={'username': username})
        if response.status_code == 200:
            user = response.json()
            while True:
                os.system('cls')  # Clear the screen on Windows
                print_faded_text("[#] ./777 Services Provided by kirito.011")
                print_faded_text("[%] User: " + username)
                print_faded_text("[%] Key: ", end='')  # No newline
                key = input()  # Input on the same line
                if key == user['message'].split(': ')[1]:
                    print_faded_text("Login successful!")
                    send_login_webhook(username)  # Send webhook notification after successful login
                    time.sleep(1)  # Pause before displaying art again
                    os.system('cls')  # Clear the screen
                    display_ascii_art(username)  # Pass the username to display in the art
                    display_menu(username)  # Display the menu with username
                    return
                else:
                    print_faded_text("Invalid Key!")
                    time.sleep(1)  # Pause before clearing
        else:
            print_faded_text("Invalid User!")
            time.sleep(1)  # Pause before clearing

def display_ascii_art(username, top_padding_factor=10, animate=True):
    art = """
     /$$$$$$$$ /$$$$$$$$ /$$$$$$$$
    |_____ $$/|_____ $$/|_____ $$/ 
         /$$/      /$$/      /$$/  
        /$$/      /$$/      /$$/   
       /$$/      /$$/      /$$/    
  /$$ /$$/      /$$/      /$$/   V1.0  
 |__/|__/      |__/      |__/  Credits: kirito.011
    
    https://discord.gg/k1ngg                              
    """
    os.system('cls' if os.name == 'nt' else 'clear')

    # Calculate vertical centering for the ASCII art
    terminal_height = os.get_terminal_size().lines
    art_height = len(art.splitlines())
    top_padding = (terminal_height - art_height) // top_padding_factor

    # Print blank lines for vertical centering
    print("\n" * top_padding)

    lines = art.splitlines()
    max_length = max(len(line) for line in lines)
    total_length = len(lines) * max_length

    # Adjust horizontal position by adding spaces
    horizontal_padding = 40  # Increase this value to move more right

    for line in lines:
        faded_line = ""
        for i, char in enumerate(line):
            color = get_fade_color(i + (max_length * lines.index(line)), total_length)
            faded_line += color + char
        print(" " * horizontal_padding + faded_line + Fore.RESET)
        if animate:
            time.sleep(0.03)  # Delay for animation effect

def display_menu(username):
    # Create the menu string
    menu = f"""‎ 
                .1 IpFivem           .4 Undefined            .7 Undefined           .10 Undefined
                .2 Cloner            .5 Undefined            .8 Undefined           .11 Undefined
                .3 Checker           .6 Undefined            .9 Undefined           .12 Undefined
           
        ┌──(x@{username})-[~/main]
        └─$ """.strip()  # Remove trailing newline

    # Use the print_faded_text function to display the "Logged in as" part with fade effect
    print_faded_text(f"Logged in as: {username}\n", end='')  # Display the logged-in username with fade

    # Now display the rest of the menu with the fading effect
    print_faded_text(menu, end=' ')  # Print without newline
    handle_choice(username)

def handle_choice(username):
    while True:
        choice = input("Choose an option: ")
        if choice == '1':
            run_fivem()
        elif choice == '2':
            asyncio.run(run_cloner())
        elif choice == '3':
            # Apply the fade color effect to the prompt text
            print_faded_text("Drag and drop the token file here: ", end='')  # This uses the fade color system
            file_path = input().strip().strip('"')  # Input after the faded prompt
            webhook_url = input("Webhook: ").strip()
            token_checker = DiscordTokenChecker(file_path, webhook_url)  # Pass the file path and webhook URL
            token_checker.check_tokens()  # Check the tokens
            token_checker.send_results_to_webhook()  # Send results to the webhook
            input("Press Enter to go back to options...")  # Wait for user input before returning

        # Add more options as needed
        else:
            print("Invalid choice")
        
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        display_ascii_art(username, animate=False)  # Display the ASCII art without animation
        display_menu(username)  # Redisplay the menu after handling the choice


if __name__ == "__main__":
    display_ascii_art("User")  # Temporary value for testing
    login()
