import zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5316")

    while True:
        print("\n=== Task Manager ===")
        print("1. Create a new task")
        print("2. Edit task start time")
        print("3. Edit task duration")
        print("4. Undo last change")
        print("5. Help")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_task_prompt(socket)
        elif choice == "2":
            edit_task_start_time_prompt(socket)
        elif choice == "3":
            edit_task_duration_prompt(socket)
        elif choice == "4":
            undo_last_change(socket)
        elif choice == "5":
            show_help()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

def create_task_prompt(socket):
    print("\n--- Create Task ---")
    task_name = input("Step 1 of 3 - Task name: ")

    while True:
        start_time = input("Step 2 of 3 - Start time (HH:MM): ")
        if validate_time_format(start_time):
            break
        else:
            print("Invalid time format. Please use HH:MM.")

    while True:
        duration_input = input("Step 3 of 3 - Duration (minutes): ")
        if duration_input.isdigit():
            duration = int(duration_input)
            break
        else:
            print("Please enter a valid number.")

    task = {
        "type": "create_task",
        "task_name": task_name,
        "start_time": start_time,
        "duration": duration
    }

    socket.send_json(task)
    response = socket.recv_json()
    print(response.get("message"))

def edit_task_start_time_prompt(socket):
    print("\n--- Edit Start Time ---")
    task_name = input("Step 1 of 3 - Task name: ")

    while True:
        new_start_time = input("Step 2 of 3 - New start time (HH:MM): ")
        if validate_time_format(new_start_time):
            break
        else:
            print("Invalid time format. Please use HH:MM.")

    while True:
        confirm = input(f"Step 3 of 3 - Confirm changing start time of '{task_name}' to {new_start_time}? (yes/no): ").strip().lower()
        if confirm in ('yes', 'no'):
            break
        else:
            print("Please type 'yes' or 'no'.")

    if confirm == 'yes':
        task = {
            "type": "edit_start_time",
            "task_name": task_name,
            "new_start_time": new_start_time
        }
        socket.send_json(task)
        response = socket.recv_json()
        print(response.get("message"))
    else:
        print("Edit cancelled.")

def edit_task_duration_prompt(socket):
    print("\n--- Edit Duration ---")
    task_name = input("Step 1 of 3 - Task name: ")

    while True:
        new_duration = input("Step 2 of 3 - New duration (minutes): ")
        if new_duration.isdigit():
            new_duration = int(new_duration)
            break
        else:
            print("Please enter a valid number.")

    while True:
        confirm = input(f"Step 3 of 3 - Confirm changing duration of '{task_name}' to {new_duration} minutes? (yes/no): ").strip().lower()
        if confirm in ('yes', 'no'):
            break
        else:
            print("Please type 'yes' or 'no'.")

    if confirm == 'yes':
        task = {
            "type": "edit_duration",
            "task_name": task_name,
            "new_duration": new_duration
        }
        socket.send_json(task)
        response = socket.recv_json()
        print(response.get("message"))
    else:
        print("Edit cancelled.")

def undo_last_change(socket):
    task = {"type": "undo"}
    socket.send_json(task)
    response = socket.recv_json()
    print(response.get("message"))

def show_help():
    print("""
Help - Features and Benefits:

- Create a new task: Easily add a task with a start time and duration, so you never miss important work.
- Edit start time: Adjust when a task begins, giving you flexibility to change plans.
- Edit duration: Modify how long a task lasts to better fit your schedule.
- Undo last change: Revert your most recent edit if you made a mistake.
- Step-by-step prompts: The app guides you through each step to reduce confusion and make it easy to use.

Use the menu options by entering the number corresponding to your choice.
""")

def validate_time_format(time_str):
    try:
        hour, minute = map(int, time_str.split(":"))
        return 0 <= hour <= 23 and 0 <= minute <= 59
    except:
        return False

if __name__ == "__main__":
    main()

