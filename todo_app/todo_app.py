import reflex as rx
from rxconfig import config
from sqlmodel import select
from .models import Todo

# 1. State class to manage todos
class State(rx.State):
    todos: list[dict] = []  # Store todos as plain dictionaries
    new_todo: str = ""      # Current input value

    def set_new_todo(self, value: str):
        self.new_todo = value

    def load_todos(self):
        with rx.session() as session:
            self.todos = [
                {"id": todo.id, "text": todo.text, "completed": todo.completed}
                for todo in session.exec(select(Todo)).all()
            ]

    def add_todo(self):
        if self.new_todo.strip():
            with rx.session() as session:
                session.add(Todo(text=self.new_todo.strip(), completed=False))
                session.commit()
            self.new_todo = ""
            self.load_todos()

    def remove_todo(self, index: int):
        if 0 <= index < len(self.todos):
            todo_id = self.todos[index]["id"]
            with rx.session() as session:
                todo = session.get(Todo, todo_id)
                if todo:
                    session.delete(todo)
                    session.commit()
            self.load_todos()

    def on_mount(self):
        self.load_todos()

# 2. Main UI for the todo app
def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("My Todo List", size="8"),
            # Input and Add button
            rx.hstack(
                rx.input(
                    placeholder="Enter a todo...",
                    value=State.new_todo,
                    on_change=lambda e: State.set_new_todo(e),
                    width="300px",
                ),
                rx.button(
                    "Add",
                    on_click=State.add_todo,
                    color_scheme="green",
                ),
            ),
            # Todo list display
            rx.vstack(
                rx.foreach(
                    State.todos,
                    lambda todo, i: rx.hstack(
                        rx.text(todo["text"], size="5"),
                        rx.button(
                            "Remove",
                            on_click=lambda: State.remove_todo(i),
                            color_scheme="red",
                            size="2",
                        ),
                        spacing="3",
                    ),
                ),
                spacing="2",
                align_items="start",
                margin_top="20px",
            ),
            spacing="6",
            align_items="center",
            min_height="85vh",
        ),
        on_mount=State.on_mount,
    )

# 3. Register the page
app = rx.App()
app.add_page(index, title="Todo App")