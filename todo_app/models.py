import reflex as rx

class Todo(rx.Model, table=True):
    text: str
    completed: bool = False