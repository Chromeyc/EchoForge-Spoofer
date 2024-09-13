from pystyle import Colors, Colorate, Center, System, Write
import os
import shutil
import subprocess
import time
import psutil
import threading

# Global flag for stopping the animation
stop_animation = False

# Define console width for centering
CONSOLE_WIDTH = 80  # Adjust this value to match your console width

# Function to update console title
def update_console_title(title):
    System.Title(title)

# Function to animate console title
def animate_console_title(base_title, suffix):
    global stop_animation
    while not stop_animation:
        for i in range(len(suffix) + 1):
            if stop_animation:
                break
            title = f"{base_title}{suffix[:i]}"
            System.Title(title)
            time.sleep(0.2)  # Adjust the speed of the animation

# Function to display progress bar
def display_progress(percent):
    bar_length = 40
    filled_length = int(round(bar_length * percent / 100))
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    print(f'\r[{bar}] {percent:02d}%', end='', flush=True)

# Function to delete directory
def delete_directory(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            return True
        except PermissionError as e:
            print(Colorate.Color(Colors.red, f"Permission error: {e}", True))
            return False
        except Exception as e:
            print(Colorate.Color(Colors.red, f"Error deleting directory {path}: {e}", True))
            return False
    return False

# Function to delete files with a specific extension
def delete_files_with_extension(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                try:
                    os.remove(os.path.join(root, file))
                    count += 1
                except PermissionError as e:
                    print(Colorate.Color(Colors.red, f"Permission error: {e}", True))
                except Exception as e:
                    print(Colorate.Color(Colors.red, f"Error deleting file {file}: {e}", True))
    return count

# Function to close the Roblox player
def close_roblox_player():
    try:
        process_list = [proc.name() for proc in psutil.process_iter()]
        if 'RobloxPlayerBeta.exe' in process_list:
            os.system('taskkill /f /im RobloxPlayerBeta.exe')
            print(Colorate.Color(Colors.green, "Closed RobloxPlayerBeta.exe", True))
        else:
            print(Colorate.Color(Colors.yellow, "RobloxPlayerBeta.exe not found", True))
    except Exception as e:
        print(Colorate.Color(Colors.red, f"Error closing RobloxPlayerBeta.exe: {e}", True))

# Function to install the Roblox player
def install_roblox_player():
    print(Colorate.Color(Colors.yellow, "Downloading Roblox Player...", True))
    download_url = "https://www.roblox.com/download/client?os=win"
    install_path = os.path.join(os.getcwd(), "installs")
    os.makedirs(install_path, exist_ok=True)
    file_name = "RobloxPlayerSetup.exe"
    file_path = os.path.join(install_path, file_name)

    # Simulate download progress
    for percent in range(0, 101, 10):
        display_progress(percent)
        time.sleep(0.01)  # Short update interval
    print()

    print(Colorate.Color(Colors.green, f"\nDownloaded to {file_path}", True))

    # Check if the file exists before attempting to run it
    if not os.path.isfile(file_path):
        print(Colorate.Color(Colors.red, f"File not found: {file_path}", True))
        return

    print(Colorate.Color(Colors.yellow, "Opening installer...", True))
    try:
        subprocess.run([file_path], check=True)
    except Exception as e:
        print(Colorate.Color(Colors.red, f"Error opening installer: {e}", True))
        return

    print(Colorate.Color(Colors.yellow, "Waiting for installer to close...", True))
    while True:
        if not any(process.name() == 'RobloxPlayerSetup.exe' for process in psutil.process_iter()):
            break
        time.sleep(0.1)  # Shorter check interval

    print(Colorate.Color(Colors.green, "Roblox Player installation completed.", True))

# Function to clear the console
def clear_console():
    System.Clear()

# Function to display a message and wait
def display_and_wait(message):
    clear_console()
    print_header()
    print(Colorate.Color(Colors.yellow, message, True))
    print("\nPress Any Key To Continue Spoofing...")
    input()  # Wait for user input

# Function to print the header
def print_header():
    header = """
   ____    __        ____                                             ___       
  / __/___/ /  ___  / __/__  _______ ____         ___ ___  ___  ___  / _/__ ____
 / _// __/ _ \/ _ \/ _// _ \/ __/ _ `/ -_)       (_-</ _ \/ _ \/ _ \/ _/ -_) __/
/___/\__/_//_/\___/_/  \___/_/  \_, /\__/       /___/ .__/\___/\___/_/ \__/_/   
                               /___/               /_/                           
    """
    # Using gradient from blue to purple
    print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(header), 1))

# Main menu function
def main_menu():
    global stop_animation
    clear_console()

    # Stop any previous animation
    stop_animation = True
    time.sleep(0.2)  # Small delay to ensure the previous animation thread stops

    # Start title animation for "Forge - Main"
    stop_animation = False
    title_thread = threading.Thread(target=animate_console_title, args=("Forge - ", "Main"), daemon=True)
    title_thread.start()

    # Print the header and menu
    print_header()

    menu = """
Forge Spoofer
=========================
1. Clean Roblox Files
2. Install Roblox Player
3. Close
    """
    # Apply gradient to menu
    gradient_menu = Colorate.Horizontal(Colors.green_to_cyan, Center.XCenter(menu), 1)
    print(gradient_menu)  # Print menu instantly

    # Adding extra lines to move the prompt down
    print("\n" * 3)  # Three new lines

    # Slight pause to avoid visual overlap with input prompt
    time.sleep(0.1)

    choice = Write.Input("forge@menu$~ → Choice ~ ", Colors.cyan_to_blue, interval=0.001)
    
    if choice == '1':
        clear_console()
        title_change("Clean Roblox Files")
        display_and_wait("Cleaning Roblox files...")
        clean_roblox_files()
    elif choice == '2':
        clear_console()
        title_change("Install Roblox Player")
        display_and_wait("Installing Roblox Player...")
        install_roblox_player()
        print("Thank You For Using Forge Spoofer, Hope It Worked! Leave a Star at the Repo :)")
        print("\nPress Any Key To Go Back...")
        input()
        main_menu()  # Return to main menu after installation
    elif choice == '3':
        print(Colorate.Color(Colors.green, "Exiting the program.", True))
        exit()
    else:
        print(Colorate.Color(Colors.red, "Invalid option.", True))
        main_menu()

# Function to change the title
def title_change(suffix):
    global stop_animation
    stop_animation = True  # Stop the previous title animation
    time.sleep(0.2)  # Ensure the previous thread stops
    stop_animation = False  # Reset flag
    title_thread = threading.Thread(target=animate_console_title, args=("Forge - ", suffix), daemon=True)
    title_thread.start()

# Function to clean Roblox files
def clean_roblox_files():
    user_profiles = get_user_profiles()
    
    directories_to_delete = [
        os.path.join(profile, 'AppData', 'Local', 'Bloxstrap') for profile in user_profiles
    ] + [
        os.path.join(profile, 'AppData', 'Local', 'Roblox') for profile in user_profiles
    ] + [
        'C:\\Program Files (x86)\\Roblox'
    ]

    files_to_delete = [
        os.path.join(profile, 'AppData', 'LocalLow') for profile in user_profiles
    ]

    directories_deleted = 0
    files_deleted = 0

    print(Colorate.Color(Colors.yellow, "Closing Roblox Player...", True))
    close_roblox_player()
    time.sleep(2)  # Wait before continuing

    print(Colorate.Color(Colors.yellow, "Deleting Directories and .rbx Files in LocalLow...", True))

    for directory in directories_to_delete:
        if delete_directory(directory):
            directories_deleted += 1

    for folder in files_to_delete:
        if os.path.isdir(folder):
            count = delete_files_with_extension(folder, '.rbx')
            files_deleted += count

    print(Colorate.Color(Colors.green, f"Deleted Files: {files_deleted}", True))
    print(Colorate.Color(Colors.green, f"Directories Deleted: {directories_deleted}", True))
    
    # Ask for reinstallation
    reinstall = Write.Input("Would you like to reinstall Roblox? (yes/no) ", Colors.cyan, interval=0.001)
    if reinstall.lower() == 'yes':
        install_roblox_player()
    else:
        print("Returning to main menu...")
        time.sleep(1)
        main_menu()

# Function to retrieve user profiles
def get_user_profiles():
    user_profiles = []
    try:
        profiles = os.getenv('USERPROFILE')  # Gets the user's profile path
        for user_profile in os.listdir(profiles):
            user_path = os.path.join(profiles, user_profile)
            if os.path.isdir(user_path):
                user_profiles.append(user_path)
    except Exception as e:
        print(Colorate.Color(Colors.red, f"Error retrieving user profiles: {e}", True))
    return user_profiles

# Run the main menu
if __name__ == "__main__":
    main_menu()
