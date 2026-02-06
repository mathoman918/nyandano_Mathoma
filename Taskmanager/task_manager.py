from datetime import datetime


# ================= FILE HANDLING =================

def load_users():
    """Load users from user.txt into a dictionary."""
    try:
        with open("user.txt", "r") as f:
            users = {}
            for line in f:
                username, password = line.strip().split(", ")
                users[username] = password
            return users
    except FileNotFoundError:
        with open("user.txt", "w") as f:
            f.write("admin, adm1n\n")
        return {"admin": "adm1n"}


def save_users(users):
    """Save users to user.txt."""
    with open("user.txt", "w") as f:
        for username, password in users.items():
            f.write(f"{username}, {password}\n")


def load_tasks():
    """Load tasks from tasks.txt."""
    try:
        with open("tasks.txt", "r") as f:
            tasks = [line.strip().split(", ") for line in f]
            return tasks
    except FileNotFoundError:
        open("tasks.txt", "w").close()
        return []


def save_tasks(tasks):
    """Save tasks to tasks.txt."""
    with open("tasks.txt", "w") as f:
        for task in tasks:
            f.write(", ".join(task) + "\n")


# ================= CORE FUNCTIONS =================

def reg_user(users):
    """Register a new user (admin only)."""
    new_user = input("Enter new username: ")
    if new_user in users:
        print("Error: Username already exists.")
        return users

    new_pass = input("Enter new password: ")
    confirm_pass = input("Confirm password: ")

    if new_pass == confirm_pass:
        users[new_user] = new_pass
        save_users(users)
        print("New user registered successfully.")
    else:
        print("Error: Passwords do not match.")
    return users


def add_task(users, tasks):
    """Add a new task if the username exists."""
    username = input("Enter the username to assign the task to: ")
    if username not in users:
        print("Error: This username does not exist.")
        return

    title = input("Enter the task title: ")
    description = input("Enter the task description: ")
    due_date_input = input("Enter the due date (DD Mon YYYY, e.g. 20 Sep 2025): ")

    try:
        due_date = datetime.strptime(due_date_input, "%d %b %Y")
    except ValueError:
        print("Invalid date format. Use DD Mon YYYY (e.g. 20 Sep 2025).")
        return

    assigned_date = datetime.today().strftime("%d %b %Y")
    task = [
        username,
        title,
        description,
        assigned_date,
        due_date.strftime("%d %b %Y"),
        "No",
    ]

    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully.")


def view_all(tasks):
    """View all tasks."""
    if not tasks:
        print("No tasks available.")
        return

    for task in tasks:
        print(f"Task: {task[1]}")
        print(f"Assigned to: {task[0]}")
        print(f"Date Assigned: {task[3]}")
        print(f"Due Date: {task[4]}")
        print(f"Task Complete? {task[5]}")
        print(f"Description: {task[2]}")
        print()

def get_valid_task_number(max_task_num):
    """Recursively get a valid task number or return -1 to exit."""
    try:
        choice = int(input("Enter task number to select or -1 to return: "))
        if choice == -1 or (1 <= choice <= max_task_num):
            return choice
        else:
            print("Invalid task number. Please try again.")
            return get_valid_task_number(max_task_num)  # recursive call
    except ValueError:
        print("Invalid input. Please enter a number.")
        return get_valid_task_number(max_task_num)  # recursive call
    
def view_mine(username, tasks):
    """View tasks assigned to the logged-in user, with edit/complete options."""
    user_tasks = [t for t in tasks if t[0] == username]

    if not user_tasks:
        print("No tasks assigned to you.")
        return

    for i, task in enumerate(user_tasks, 1):
        print(f"[{i}] {task[1]}")
        print(f"Date Assigned: {task[3]}")
        print(f"Due Date: {task[4]}")
        print(f"Completed: {task[5]}")
        print(f"Description: {task[2]}")
        print()

    try:
        choice = int(input("Select a task number to manage (-1 to return): "))
    except ValueError:
        print("Invalid input. Returning to menu.")
        return

    if choice == -1:
        return
    if not (1 <= choice <= len(user_tasks)):
        print("Invalid task number.")
        return

    selected_task = user_tasks[choice - 1]
    print(f"You selected: {selected_task[1]}")

    action = input("Do you want to (c)complete or (e)edit this task? ").lower()

    if action == "c":
        selected_task[5] = "Yes"
        print("Task marked as complete.")

    elif action == "e":
        if selected_task[5] == "Yes":
            print("Cannot edit a completed task.")
            return

        new_user = input("Reassign task to (leave blank to keep current): ")
        if new_user and new_user in load_users():
            selected_task[0] = new_user
        elif new_user:
            print("Invalid username. Task not reassigned.")

        new_due_date = input(
            "Enter new due date (DD Mon YYYY) (leave blank to keep current): "
        )
        if new_due_date:
            try:
                due_date = datetime.strptime(new_due_date, "%d %b %Y")
                selected_task[4] = due_date.strftime("%d %b %Y")
            except ValueError:
                print("Invalid date format. Keeping current due date.")

        print("Task updated.")

    save_tasks(tasks)


def view_completed(tasks):
    """Admin only: view completed tasks."""
    completed = [t for t in tasks if t[5] == "Yes"]
    if not completed:
        print("No completed tasks.")
        return

    for task in completed:
        print(f"Task: {task[1]}")
        print(f"Assigned to: {task[0]}")
        print(f"Date Assigned: {task[3]}")
        print(f"Due Date: {task[4]}")
        print(f"Description: {task[2]}")
        print()


def delete_task(tasks):
    """Admin only: delete task by title."""
    title = input("Enter the title of the task to delete: ")
    for task in tasks:
        if task[1].lower() == title.lower():
            tasks.remove(task)
            save_tasks(tasks)
            print("Task deleted successfully.")
            return
    print("Task not found.")


def generate_reports(tasks, users):
    """Generate reports for tasks and users."""
    total_tasks = len(tasks)
    completed = sum(1 for t in tasks if t[5] == "Yes")
    uncompleted = total_tasks - completed

    overdue = 0
    for t in tasks:
        try:
            due_date = datetime.strptime(t[4], "%d %b %Y")
        except ValueError:
            continue
        if t[5] == "No" and due_date < datetime.today():
            overdue += 1

    perc_incomplete = (uncompleted / total_tasks * 100) if total_tasks else 0
    perc_overdue = (overdue / total_tasks * 100) if total_tasks else 0

    with open("task_overview.txt", "w") as f:
        f.write(f"Total tasks: {total_tasks}\n")
        f.write(f"Completed tasks: {completed}\n")
        f.write(f"Uncompleted tasks: {uncompleted}\n")
        f.write(f"Overdue tasks: {overdue}\n")
        f.write(f"Percentage incomplete: {perc_incomplete:.2f}%\n")
        f.write(f"Percentage overdue: {perc_overdue:.2f}%\n")

    with open("user_overview.txt", "w") as f:
        f.write(f"Total users: {len(users)}\n")
        f.write(f"Total tasks: {total_tasks}\n\n")
        for user in users:
            user_tasks = [t for t in tasks if t[0] == user]
            user_total = len(user_tasks)
            user_completed = sum(1 for t in user_tasks if t[5] == "Yes")
            user_uncompleted = user_total - user_completed
            user_overdue = 0
            for t in user_tasks:
                try:
                    due_date = datetime.strptime(t[4], "%d %b %Y")
                except ValueError:
                    continue
                if t[5] == "No" and due_date < datetime.today():
                    user_overdue += 1

            perc_assigned = (
                (user_total / total_tasks * 100) if total_tasks else 0
            )
            perc_completed = (
                (user_completed / user_total * 100) if user_total else 0
            )
            perc_incomplete = (
                (user_uncompleted / user_total * 100) if user_total else 0
            )
            perc_overdue = (
                (user_overdue / user_total * 100) if user_total else 0
            )

            f.write(f"User: {user}\n")
            f.write(f"  Total tasks: {user_total}\n")
            f.write(f"  % of total tasks: {perc_assigned:.2f}%\n")
            f.write(f"  % completed: {perc_completed:.2f}%\n")
            f.write(f"  % incomplete: {perc_incomplete:.2f}%\n")
            f.write(f"  % overdue: {perc_overdue:.2f}%\n\n")

    print("Reports generated successfully.")


def display_statistics():
    """Display statistics from report files."""
    try:
        with open("task_overview.txt", "r") as f:
            print(f.read())
        with open("user_overview.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Reports not found. Generating reports now...")
        generate_reports(load_tasks(), load_users())
        display_statistics()


# ================= MAIN =================

def main():
    users = load_users()
    tasks = load_tasks()

    print("Welcome to Task Manager")
    username = None

    while not username:
        uname = input("Username: ")
        pword = input("Password: ")
        if uname in users and users[uname] == pword:
            username = uname
            print(f"Login successful. Welcome, {username}!")
        else:
            print("Invalid login, try again.")

    while True:
        if username == "admin":
            menu = input(
                "\nSelect an option:\n"
                "r - register user\n"
                "a - add task\n"
                "va - view all tasks\n"
                "vm - view my tasks\n"
                "vc - view completed tasks\n"
                "del - delete a task\n"
                "ds - display statistics\n"
                "gr - generate reports\n"
                "e - exit\n: "
            ).lower()
        else:
            menu = input(
                "\nSelect an option:\n"
                "a - add task\n"
                "va - view all tasks\n"
                "vm - view my tasks\n"
                "e - exit\n: "
            ).lower()

        if menu == "r" and username == "admin":
            users = reg_user(users)
        elif menu == "a":
            add_task(users, tasks)
        elif menu == "va":
            view_all(tasks)
        elif menu == "vm":
            view_mine(username, tasks)
        elif menu == "vc" and username == "admin":
            view_completed(tasks)
        elif menu == "del" and username == "admin":
            delete_task(tasks)
        elif menu == "gr" and username == "admin":
            generate_reports(tasks, users)
        elif menu == "ds" and username == "admin":
            display_statistics()
        elif menu == "e":
            print("Goodbye.")
            break
        else:
            print("Invalid choice, try again.")


