import reflex as rx

# This class defines what a task looks like in the database.
# Each field is a piece of information about the task.
class Todo(rx.Model, table=True):
    text: str  # The name/title of the task
    description: str = ""  # Extra details about the task
    completed: bool = False  # True if the task is done
    order: int = 0  # The position of the task in the list (for drag-and-drop)