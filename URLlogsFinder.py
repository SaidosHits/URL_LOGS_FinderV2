import os
from colorama import init, Fore
from time import sleep, strftime, localtime
from tkinter import Tk, filedialog

init(autoreset=True)
sleep(2)
# Colorful welcome text
print("")
print("")
welcome_text = """



██╗░░░░░░█████╗░░██████╗░░██████╗██╗░░░██╗██████╗░██╗░░░░░███████╗██╗███╗░░██╗██████╗░███████╗██████╗░
██║░░░░░██╔══██╗██╔════╝░██╔════╝██║░░░██║██╔══██╗██║░░░░░██╔════╝██║████╗░██║██╔══██╗██╔════╝██╔══██╗
██║░░░░░██║░░██║██║░░██╗░╚█████╗░██║░░░██║██████╔╝██║░░░░░█████╗░░██║██╔██╗██║██║░░██║█████╗░░██████╔╝
██║░░░░░██║░░██║██║░░╚██╗░╚═══██╗██║░░░██║██╔══██╗██║░░░░░██╔══╝░░██║██║╚████║██║░░██║██╔══╝░░██╔══██╗
███████╗╚█████╔╝╚██████╔╝██████╔╝╚██████╔╝██║░░██║███████╗██║░░░░░██║██║░╚███║██████╔╝███████╗██║░░██║
╚══════╝░╚════╝░░╚═════╝░╚═════╝░░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░░░░╚═╝╚═╝░░╚══╝╚═════╝░╚══════╝╚═╝░░╚═╝ V 0.2

Telegram ========> @SaidosHits


"""
print("")

# Define colors
colors = [Fore.RED]

# Print colorful welcome text
lines = welcome_text.strip().split('\n')
for i, line in enumerate(lines):
    print(colors[i % len(colors)] + line)
sleep(1)

# User input
print("")
print("")
domain_to_search = input("Enter the domain you want to search for: ")

def extract_country_code(folder_path):
    # Extracts the country code from the folder name
    return os.path.basename(folder_path)[:2]

def create_output_folder():
    # Creates an output folder with the current date and time
    current_datetime = strftime("%Y.%m.%d %H.%M.%S", localtime())
    output_folder_name = f"Result [{current_datetime}]"
    return output_folder_name

def get_root_folder_path():
    # Opens a dialog to select the root folder path
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Root Folder")
    root.destroy()
    return folder_path

def search_and_extract_credentials(root_path, keyword, output_root):
    output_folder_name = create_output_folder()
    output_root_folder = os.path.join(output_root, output_folder_name)
    os.makedirs(output_root_folder)

    for foldername, subfolders, filenames in os.walk(root_path):
        for filename in filenames:
            if filename == "Passwords.txt":
                file_path = os.path.join(foldername, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        lines = file.readlines()
                        found_domain = False
                        for i, line in enumerate(lines):
                            if keyword in line:
                                found_domain = True
                            elif found_domain:
                                if "Username:" in line:
                                    username = line.strip().replace("Username:", "").replace(" ", "")
                                if "Password:" in line:
                                    password = line.strip().replace("Password:", "").replace(" ", "")
                                    country_code = extract_country_code(foldername)

                                    # Create country-specific folder if not exists
                                    country_folder = os.path.join(output_root_folder, country_code)
                                    if not os.path.exists(country_folder):
                                        os.makedirs(country_folder)

                                    # Write credentials to a file in the country folder
                                    output_file_path = os.path.join(country_folder, "result.txt")
                                    with open(output_file_path, "a", encoding='utf-8') as output_file:
                                        output_file.write(f"{username}:{password}\n")
                                    found_domain = False
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

def main():
    keyword = domain_to_search
    output_root_folder = "Result"

    # Get root folder path using dialog
    root_path = get_root_folder_path()

    print("Searching for credentials...")
    search_and_extract_credentials(root_path, keyword, output_root_folder)
    print(f"Search completed. Results saved in '{output_root_folder}' folder.")
    input()

if __name__ == "__main__":
    main()