import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyautogui
import time
import json
import sv_ttk


class ActionExecutorApp:
    def __init__(self, root):
        """Initialize the ActionExecutorApp class."""
        self.root = root
        self.root.title("TaskBot")
        self.root.geometry("700x500")
        sv_ttk.set_theme("dark")  # Set the theme to dark

        # Initialize variables
        self.actions = []
        self.action_file = None

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        """Create and layout the widgets in the application."""
        # File loading section
        self.file_frame = ttk.Frame(self.root)
        self.file_frame.pack(pady=10)

        self.file_label = ttk.Label(self.file_frame, text="JSON File:")
        self.file_label.pack(side=tk.LEFT, padx=5)

        self.file_entry = ttk.Entry(self.file_frame, width=50)
        self.file_entry.pack(side=tk.LEFT, padx=5)

        self.load_button = ttk.Button(
            self.file_frame, text="Load", command=self.load_file
        )
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(
            self.file_frame, text="Save", command=self.save_file
        )
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Action display section
        self.action_listbox = tk.Listbox(self.root, width=80, height=15)
        self.action_listbox.pack(pady=10)

        # Action control buttons
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(pady=5)

        self.add_button = ttk.Button(
            self.control_frame, text="Add Action", command=self.add_action
        )
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(
            self.control_frame, text="Edit Action", command=self.edit_action
        )
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(
            self.control_frame, text="Delete Action", command=self.delete_action
        )
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Execute button
        self.execute_button = ttk.Button(
            self.root, text="Execute Actions", command=self.execute_actions
        )
        self.execute_button.pack(pady=10)

        # Status bar
        self.status_label = ttk.Label(self.root, text="Status: Idle", anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=10, pady=5)

    def load_file(self):
        """Open a file dialog to load a JSON file containing actions."""
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filepath:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filepath)
            self.action_file = filepath
            self.load_actions(filepath)

    def save_file(self):
        """Save the current actions to the previously loaded file or prompt for a new file."""
        if self.action_file:
            with open(self.action_file, "w") as file:
                json.dump(self.actions, file)
            messagebox.showinfo("Info", "Actions saved successfully.")
        else:
            self.save_file_as()

    def save_file_as(self):
        """Prompt the user to save the current actions to a new JSON file."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )
        if filepath:
            self.action_file = filepath
            self.save_file()

    def load_actions(self, filepath):
        """Load actions from the specified JSON file."""
        try:
            with open(filepath, "r") as file:
                self.actions = json.load(file)
            self.populate_listbox()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load actions: {e}")

    def populate_listbox(self):
        """Clear the listbox and populate it with the current actions."""
        self.action_listbox.delete(0, tk.END)
        for action in self.actions:
            action_desc = (
                f"{action['type'].capitalize()} - {action.get('description', '')} "
                f"({action.get('position', '') if 'position' in action else ''} "
                f"{action.get('duration', '') if 'duration' in action else ''} "
                f"{action.get('keys', '') if 'keys' in action else ''})"
            )
            self.action_listbox.insert(tk.END, action_desc)

    def execute_actions(self):
        """Execute the loaded actions sequentially."""
        self.status_label.config(text="Status: Executing...")
        for action in self.actions:
            self.perform_action(action)
            time.sleep(1)  # Adding a small delay between actions
        self.status_label.config(text="Status: Idle")

    def perform_action(self, action):
        """Perform a single action based on its type."""
        try:
            if action["type"] == "click":
                self.perform_click(
                    action["position"], action.get("description", "click")
                )
            elif action["type"] == "wait":
                self.wait_for(action["duration"])
            elif action["type"] == "hotkey":
                pyautogui.hotkey(*action["keys"])
            elif action["type"] == "type":
                pyautogui.typewrite(action["text"])
            elif action["type"] == "move":
                pyautogui.moveTo(action["position"])
            else:
                print(f"Unknown action type: {action['type']}")
        except Exception as e:
            print(f"Failed to perform action {action}: {e}")

    def perform_click(self, position, description="click"):
        """Perform a click action at the specified position."""
        if position:
            pyautogui.click(position)
            print(f"Performed {description} at {position}.")
        else:
            print(f"Failed to perform {description}. Position not found.")

    def wait_for(self, seconds):
        """Pause for a given number of seconds."""
        time.sleep(seconds)

    def add_action(self):
        """Open a dialog to add a new action."""
        self.edit_action(new=True)

    def edit_action(self, new=False):
        """Open a dialog to edit an existing action or add a new one."""
        selected_index = self.action_listbox.curselection()
        if not new and not selected_index:
            messagebox.showwarning("Warning", "Please select an action to edit.")
            return

        action_window = tk.Toplevel(self.root)
        action_window.title("Edit Action")

        # Action type
        ttk.Label(action_window, text="Action Type:").grid(
            row=0, column=0, padx=5, pady=5
        )
        action_type = ttk.Combobox(
            action_window, values=["click", "wait", "hotkey", "type", "move"]
        )
        action_type.grid(row=0, column=1, padx=5, pady=5)

        # Description
        ttk.Label(action_window, text="Description:").grid(
            row=1, column=0, padx=5, pady=5
        )
        description = ttk.Entry(action_window)
        description.grid(row=1, column=1, padx=5, pady=5)

        # Position
        ttk.Label(action_window, text="Position (x, y):").grid(
            row=2, column=0, padx=5, pady=5
        )
        position = ttk.Entry(action_window)
        position.grid(row=2, column=1, padx=5, pady=5)

        # Duration
        ttk.Label(action_window, text="Duration (seconds):").grid(
            row=3, column=0, padx=5, pady=5
        )
        duration = ttk.Entry(action_window)
        duration.grid(row=3, column=1, padx=5, pady=5)

        # Keys
        ttk.Label(action_window, text="Hotkeys (comma separated):").grid(
            row=4, column=0, padx=5, pady=5
        )
        keys = ttk.Entry(action_window)
        keys.grid(row=4, column=1, padx=5, pady=5)

        # Text for typing
        ttk.Label(action_window, text="Text:").grid(row=5, column=0, padx=5, pady=5)
        text = ttk.Entry(action_window)
        text.grid(row=5, column=1, padx=5, pady=5)

        def save_action():
            """Save the current action to the list."""
            action = {
                "type": action_type.get(),
                "description": description.get(),
                "position": eval(position.get()) if position.get() else None,
                "duration": float(duration.get()) if duration.get() else None,
                "keys": keys.get().split(",") if keys.get() else None,
                "text": text.get() if text.get() else None,
            }

            if new:
                self.actions.append(action)
            else:
                index = selected_index[0]
                self.actions[index] = action

            self.populate_listbox()
            action_window.destroy()

        ttk.Button(action_window, text="Save", command=save_action).grid(
            row=6, column=0, columnspan=2, pady=10
        )

    def delete_action(self):
        """Delete the selected action from the list."""
        selected_index = self.action_listbox.curselection()
        if selected_index:
            self.actions.pop(selected_index[0])
            self.populate_listbox()
        else:
            messagebox.showwarning("Warning", "Please select an action to delete.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ActionExecutorApp(root)
    root.mainloop()
