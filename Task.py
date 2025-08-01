import zmq
import copy

tasks = {}
undo_stack = []

def handle_create_task(data):
    task_name = data["task_name"]
    start_time = data["start_time"]
    duration = data["duration"]

    # No undo for create task (optional)
    tasks[task_name] = {
        "start_time": start_time,
        "duration": duration
    }
    return {"message": f"Task '{task_name}' created."}

def handle_edit_start_time(data):
    task_name = data["task_name"]
    new_start_time = data["new_start_time"]
    if task_name in tasks:
        # Save current state before change
        undo_stack.append(copy.deepcopy(tasks))
        tasks[task_name]["start_time"] = new_start_time
        return {"message": f"Start time for '{task_name}' updated."}
    return {"message": f"Task '{task_name}' not found."}

def handle_edit_duration(data):
    task_name = data["task_name"]
    new_duration = data["new_duration"]
    if task_name in tasks:
        # Save current state before change
        undo_stack.append(copy.deepcopy(tasks))
        tasks[task_name]["duration"] = new_duration
        return {"message": f"Duration for '{task_name}' updated."}
    return {"message": f"Task '{task_name}' not found."}

def handle_undo(data):
    if undo_stack:
        global tasks
        tasks = undo_stack.pop()
        return {"message": "Last change undone."}
    else:
        return {"message": "No changes to undo."}

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5316")

    print("Task Service running on port 5316...")

    while True:
        message = socket.recv_json()

        if message["type"] == "create_task":
            response = handle_create_task(message)
        elif message["type"] == "edit_start_time":
            response = handle_edit_start_time(message)
        elif message["type"] == "edit_duration":
            response = handle_edit_duration(message)
        elif message["type"] == "undo":
            response = handle_undo(message)
        else:
            response = {"message": "Invalid message type."}

        socket.send_json(response)

if __name__ == "__main__":
    main()