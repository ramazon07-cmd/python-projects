import sys
import json
from colorama import init, Fore, Style

init(autoreset=True)

TASKS_FILE = "tasks.json"
PRIORITIES = {"past": 1, "o'rtacha": 2, "yuqori": 3}
tasks = []

def load_tasks():
    global tasks
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

def save_tasks():
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def show_tasks(filter_status=None, sort_priority=False):
    if not tasks:
        print(Fore.YELLOW + "Vazifalar ro'yxati bo'sh.")
        return
    filtered = tasks
    if filter_status is not None:
        filtered = [t for t in tasks if t["done"] == filter_status]
    if sort_priority:
        filtered = sorted(filtered, key=lambda t: PRIORITIES[t["priority"]])
    for i, task in enumerate(filtered, 1):
        status = Fore.GREEN + "✅" if task["done"] else Fore.RED + "❌"
        pr_color = {
            "past": Fore.CYAN,
            "o'rtacha": Fore.YELLOW,
            "yuqori": Fore.MAGENTA
        }[task["priority"]]
        print(f"{i}. {task['text']} [{status}{Style.RESET_ALL}] {pr_color}({task['priority']}){Style.RESET_ALL}")

def add_task():
    text = input("Yangi vazifa kiriting: ")
    while True:
        pr = input("Ustuvorlik darajasi (past/o'rtacha/yuqori): ").lower()
        if pr in PRIORITIES:
            break
        print(Fore.RED + "Noto'g'ri ustuvorlik. Qayta kiriting.")
    tasks.append({"text": text, "done": False, "priority": pr})
    save_tasks()
    print(Fore.GREEN + "Vazifa qo'shildi.")

def delete_task():
    show_tasks()
    try:
        idx = int(input("O'chirmoqchi bo'lgan vazifa raqamini kiriting: ")) - 1
        if 0 <= idx < len(tasks):
            tasks.pop(idx)
            save_tasks()
            print(Fore.GREEN + "Vazifa o'chirildi.")
        else:
            print(Fore.RED + "Noto'g'ri raqam.")
    except ValueError:
        print(Fore.RED + "Raqam kiriting.")

def edit_task():
    show_tasks()
    try:
        idx = int(input("Tahrirlamoqchi bo'lgan vazifa raqamini kiriting: ")) - 1
        if 0 <= idx < len(tasks):
            new_text = input("Yangi matnni kiriting: ")
            while True:
                pr = input("Yangi ustuvorlik (past/o'rtacha/yuqori): ").lower()
                if pr in PRIORITIES:
                    break
                print(Fore.RED + "Noto'g'ri ustuvorlik. Qayta kiriting.")
            tasks[idx]["text"] = new_text
            tasks[idx]["priority"] = pr
            save_tasks()
            print(Fore.GREEN + "Vazifa tahrirlandi.")
        else:
            print(Fore.RED + "Noto'g'ri raqam.")
    except ValueError:
        print(Fore.RED + "Raqam kiriting.")

def mark_done():
    show_tasks()
    try:
        idx = int(input("Bajarilgan vazifa raqamini kiriting: ")) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]["done"] = True
            save_tasks()
            print(Fore.GREEN + "Vazifa bajarildi deb belgilandi.")
        else:
            print(Fore.RED + "Noto'g'ri raqam.")
    except ValueError:
        print(Fore.RED + "Raqam kiriting.")

def filter_tasks():
    print("1. Faqat bajarilganlar\n2. Faqat bajarilmaganlar")
    choice = input("Tanlang: ")
    if choice == '1':
        show_tasks(filter_status=True)
    elif choice == '2':
        show_tasks(filter_status=False)
    else:
        print(Fore.RED + "Noto'g'ri tanlov.")

def sort_tasks():
    show_tasks(sort_priority=True)

def main_menu():
    print(Fore.CYAN + "\n1. Vazifalarni ko'rish\n2. Vazifa qo'shish\n3. Vazifani o'chirish\n4. Vazifani tahrirlash\n5. Vazifani bajarilgan deb belgilash\n6. Filtrlash\n7. Ustuvorlik bo'yicha tartiblash\n8. Chiqish")

def main():
    load_tasks()
    while True:
        main_menu()
        choice = input("Tanlang: ")
        if choice == '1':
            show_tasks()
        elif choice == '2':
            add_task()
        elif choice == '3':
            delete_task()
        elif choice == '4':
            edit_task()
        elif choice == '5':
            mark_done()
        elif choice == '6':
            filter_tasks()
        elif choice == '7':
            sort_tasks()
        elif choice == '8':
            print(Fore.CYAN + "Dasturdan chiqildi.")
            sys.exit()
        else:
            print(Fore.RED + "Noto'g'ri tanlov.")

if __name__ == "__main__":
    main()

tasks = []

def show_tasks():
    if not tasks:
        print("Vazifalar ro'yxati bo'sh.")
    else:
        for i, (task, done) in enumerate(tasks, 1):
            status = "✅" if done else "❌"
            print(f"{i}. {task} [{status}]")

def add_task():
    task = input("Yangi vazifa kiriting: ")
    tasks.append((task, False))
    print("Vazifa qo'shildi.")

def delete_task():
    show_tasks()
    try:
        idx = int(input("O'chirmoqchi bo'lgan vazifa raqamini kiriting: ")) - 1
        if 0 <= idx < len(tasks):
            tasks.pop(idx)
            print("Vazifa o'chirildi.")
        else:
            print("Noto'g'ri raqam.")
    except ValueError:
        print("Raqam kiriting.")

def mark_done():
    show_tasks()
    try:
        idx = int(input("Bajarilgan vazifa raqamini kiriting: ")) - 1
        if 0 <= idx < len(tasks):
            task, _ = tasks[idx]
            tasks[idx] = (task, True)
            print("Vazifa bajarildi deb belgilandi.")
        else:
            print("Noto'g'ri raqam.")
    except ValueError:
        print("Raqam kiriting.")

def main():
    while True:
        print("\n1. Vazifalarni ko'rish\n2. Vazifa qo'shish\n3. Vazifani o'chirish\n4. Vazifani bajarilgan deb belgilash\n5. Chiqish")
        choice = input("Tanlang: ")
        if choice == '1':
            show_tasks()
        elif choice == '2':
            add_task()
        elif choice == '3':
            delete_task()
        elif choice == '4':
            mark_done()
        elif choice == '5':
            print("Dasturdan chiqildi.")
            sys.exit()
        else:
            print("Noto'g'ri tanlov.")

if __name__ == "__main__":
    main()