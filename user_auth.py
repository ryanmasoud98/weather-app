import sys
from colorama import Fore, Style
from db.db_config import connect_db
from weather.display_utils import weather_loop

# For password masking
if sys.platform == "win32":
    import msvcrt
else:
    import tty, termios

# ---------------- PASSWORD INPUT ----------------
def input_password(prompt="Password: "):
    print(prompt, end="", flush=True)
    password = ""
    if sys.platform == "win32":
        while True:
            ch = msvcrt.getch()
            if ch in {b'\r', b'\n'}:
                print("")
                break
            elif ch == b'\x08':  # Backspace
                if len(password) > 0:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            elif ch in {b'\x03', b'\x1a'}:  # Ctrl+C or Ctrl+Z
                raise KeyboardInterrupt
            else:
                password += ch.decode("utf-8")
                print("*", end="", flush=True)
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in {"\r", "\n"}:
                    print("")
                    break
                elif ch == "\x7f":  # Backspace
                    if len(password) > 0:
                        password = password[:-1]
                        print("\b \b", end="", flush=True)
                else:
                    password += ch
                    print("*", end="", flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return password

# ---------------- USERS TABLE ----------------
def ensure_users_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# ---------------- SIGNUP ----------------
def signup():
    conn = connect_db()
    cur = conn.cursor()
    email = input("Enter email: ").strip()
    password = input_password("Enter password: ").strip()
    try:
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        print(Fore.GREEN + Style.BRIGHT + "✅ Signup successful!")
    except Exception as e:
        print(Fore.RED + "⚠ Email already exists or error occurred.", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

# ---------------- LOGIN ----------------
def login():
    conn = connect_db()
    cur = conn.cursor()
    email = input("Enter email: ").strip()
    password = input_password("Enter password: ").strip()
    cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        print(Fore.GREEN + Style.BRIGHT + "✅ Login successful!")
        weather_loop()
        return True
    else:
        print(Fore.RED + "❌ Invalid email or password.")
        return False
