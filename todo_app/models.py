import reflex as rx

class Todo(rx.Model, table=True):
    text: str
    description: str = ""  # Optional field for task details
    completed: bool = False