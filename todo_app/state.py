import reflex as rx
from sqlmodel import select
from .models import Todo
import os


# This is the main class that keeps track of all the app's data and logic.
class State(rx.State):
    # List of all tasks (each task is a dictionary)
    todos: list[dict] = []
    # The text for a new task being typed
    new_todo: str = ""
    # Index of the task being edited
    edit_index: int = -1
    # Text for the task being edited
    edit_text: str = ""
    # The currently selected task for viewing/editing
    selected_todo: dict | None = None
    # Message to show when something is successfully done
    success_message: str = ""

    # Update the text for a new task
    def set_new_todo(self, value: str):
        self.new_todo = value

    # Update the text for the task being edited
    def set_edit_text(self, value: str):
        self.edit_text = value

    # Change the title of the selected task
    def set_selected_text(self, value: str):
        if self.selected_todo:
            self.selected_todo["text"] = value

    # Change the description of the selected task
    def set_selected_description(self, value: str):
        if self.selected_todo:
            self.selected_todo["description"] = value

    # Mark the selected task as completed or not
    def set_selected_completed(self, value: bool):
        if self.selected_todo:
            self.selected_todo["completed"] = value

    # Save an uploaded image for the selected task
    def set_selected_image(self, file):
        if self.selected_todo and file:
            assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
            os.makedirs(assets_dir, exist_ok=True)
            file_path = os.path.join(assets_dir, file.name)
            with open(file_path, "wb") as f:
                f.write(file.content)
            self.selected_todo["image"] = file.name

    # Load all tasks from the database and update the list
    def load_todos(self):
        with rx.session() as session:
            self.todos = [
                {
                    "id": todo.id,
                    "text": todo.text,
                    "description": todo.description,
                    "completed": todo.completed,
                    "image": getattr(todo, "image", "")
                }
                for todo in session.exec(select(Todo)).all()
            ]

    # Add a new task to the database and update the list
    def add_todo(self):
        if self.new_todo.strip():
            with rx.session() as session:
                session.add(Todo(text=self.new_todo.strip(), description="", completed=False))
                session.commit()
            self.new_todo = ""
            self.load_todos()

    # Remove a task from the database and update the list
    def remove_todo(self, index: int):
        if 0 <= index < len(self.todos):
            todo_id = self.todos[index]["id"]
            with rx.session() as session:
                todo = session.get(Todo, todo_id)
                if todo:
                    session.delete(todo)
                    session.commit()
            self.load_todos()

    # Start editing a task (store its index and text)
    def start_edit(self, index: int):
        self.edit_index = index
        self.edit_text = self.todos[index]["text"]

    # Save changes to a task being edited
    def save_edit(self):
        if 0 <= self.edit_index < len(self.todos):
            todo_id = self.todos[self.edit_index]["id"]
            with rx.session() as session:
                todo = session.get(Todo, todo_id)
                if todo:
                    todo.text = self.edit_text
                    session.commit()
            self.edit_index = -1
            self.edit_text = ""
            self.load_todos()

    # Cancel editing a task
    def cancel_edit(self):
        self.edit_index = -1
        self.edit_text = ""

    # Toggle a task's completed status
    def toggle_complete(self, index: int):
        todo_id = self.todos[index]["id"]
        with rx.session() as session:
            todo = session.get(Todo, todo_id)
            if todo:
                todo.completed = not todo.completed
                session.commit()
        self.load_todos()

    # Load a task's details for viewing or editing
    def view_details(self, todo_id: int):
        with rx.session() as session:
            todo = session.get(Todo, todo_id)
            if todo:
                self.selected_todo = {
                    "id": todo.id,
                    "text": todo.text,
                    "description": todo.description,
                    "completed": todo.completed,
                    "image": getattr(todo, "image", "")
                }

    # Save changes to the selected task
    def save_selected_todo(self):
        if self.selected_todo:
            with rx.session() as session:
                todo = session.get(Todo, self.selected_todo["id"])
                if todo:
                    todo.text = self.selected_todo["text"]
                    todo.description = self.selected_todo["description"]
                    todo.completed = self.selected_todo["completed"]
                    todo.image = self.selected_todo.get("image", "")
                    session.commit()
            self.selected_todo = None
            self.success_message = "✅ Todo updated successfully!"
            return rx.redirect("/")

    # Delete the selected task
    def delete_selected_todo(self):
        if self.selected_todo:
            with rx.session() as session:
                todo = session.get(Todo, self.selected_todo["id"])
                if todo:
                    session.delete(todo)
                    session.commit()
            self.selected_todo = None
            rx.redirect("/")

    # When the page loads, clear any messages and load all tasks
    def on_mount(self):
        self.success_message = ""
        self.load_todos()
