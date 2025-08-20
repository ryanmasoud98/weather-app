import sys
import os
from colorama import Fore

# Add project root to sys.path to fix ModuleNotFoundError
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from auth.user_auth import signup, login, ensure_users_table

def main():
    ensure_users_table()
    while True:
        print("\n1. Signup\n2. Login\n3. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            print(Fore.CYAN + "👋 Goodbye! Stay safe and take care!")
            break
        else:
            print(Fore.RED + "⚠ Invalid choice.")

if __name__ == "__main__":
    main()

