import reflex as rx
from rxconfig import config
from sqlmodel import select
from .models import Todo

# 1. State class to manage todos
class State(rx.State):
    todos: list[dict] = []
    new_todo: str = ""

    edit_index: int = -1
    edit_text: str = ""

    selected_todo: dict | None = None

    def set_new_todo(self, value: str):
        self.new_todo = value

    def set_edit_text(self, value: str):
        self.edit_text = value

    def set_selected_text(self, value: str):
        if self.selected_todo:
            self.selected_todo["text"] = value

    def set_selected_description(self, value: str):
        if self.selected_todo:
            self.selected_todo["description"] = value

    def set_selected_completed(self, value: bool):
        if self.selected_todo:
            self.selected_todo["completed"] = value

    def load_todos(self):
        with rx.session() as session:
            self.todos = [
                {
                    "id": todo.id,
                    "text": todo.text,
                    "description": todo.description,
                    "completed": todo.completed
                }
                for todo in session.exec(select(Todo)).all()
            ]

    def add_todo(self):
        if self.new_todo.strip():
            with rx.session() as session:
                session.add(Todo(text=self.new_todo.strip(), description="", completed=False))
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

    def start_edit(self, index: int):
        self.edit_index = index
        self.edit_text = self.todos[index]["text"]

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

    def cancel_edit(self):
        self.edit_index = -1
        self.edit_text = ""

    def toggle_complete(self, index: int):
        todo_id = self.todos[index]["id"]
        with rx.session() as session:
            todo = session.get(Todo, todo_id)
            if todo:
                todo.completed = not todo.completed
                session.commit()
        self.load_todos()

    def view_details(self, todo_id: int):
        with rx.session() as session:
            todo = session.get(Todo, todo_id)
            if todo:
                self.selected_todo = {
                    "id": todo.id,
                    "text": todo.text,
                    "description": todo.description,
                    "completed": todo.completed
                }

    def save_selected_todo(self):
        if self.selected_todo:
            with rx.session() as session:
                todo = session.get(Todo, self.selected_todo["id"])
                if todo:
                    todo.text = self.selected_todo["text"]
                    todo.description = self.selected_todo["description"]
                    todo.completed = self.selected_todo["completed"]
                    session.commit()
            self.selected_todo = None
            rx.redirect("/")

    def delete_selected_todo(self):
        if self.selected_todo:
            with rx.session() as session:
                todo = session.get(Todo, self.selected_todo["id"])
                if todo:
                    session.delete(todo)
                    session.commit()
            self.selected_todo = None
            rx.redirect("/")

    def on_mount(self):
        self.load_todos()

# 2. Main UI
def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("My Todo List", size="8"),
            rx.hstack(
                rx.input(
                    placeholder="Enter a todo...",
                    value=State.new_todo,
                    on_change=lambda e: State.set_new_todo(e),
                    width="300px",
                ),
                rx.button("Add", on_click=State.add_todo, color_scheme="green"),
            ),
            rx.vstack(
                rx.foreach(
                    State.todos,
                    lambda todo, i: rx.vstack(
                        rx.hstack(
                            rx.text(
                                todo["text"],
                                size="5",
                                text_decoration=rx.cond(todo["completed"], "line-through", "none"),
                                color=rx.cond(todo["completed"], "gray", "black")
                            ),
                            rx.button("Edit", on_click=lambda: [State.view_details(todo["id"]), rx.redirect("/edit_details")], color_scheme="yellow", size="2"),
                            rx.button("View", on_click=lambda: [State.view_details(todo["id"]), rx.redirect("/view_details")], color_scheme="blue", size="2"),
                            rx.button("Remove", on_click=lambda: State.remove_todo(i), color_scheme="red", size="2"),
                            rx.button("Toggle", on_click=lambda: State.toggle_complete(i), color_scheme="purple", size="2"),
                            spacing="3"
                        ),
                        rx.cond(
                            todo["completed"],
                            rx.text("Completed: ✅", size="3", color="gray"),
                            rx.text("Completed: ❌", size="3", color="gray")
                        )
                    )
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

# 3. Edit Details Page
def edit_details() -> rx.Component:
    return rx.container(
        rx.heading("Edit Details", size="7"),
        rx.cond(
            State.selected_todo.is_not_none(),
            rx.vstack(
                rx.input(
                    value=State.selected_todo["text"],
                    on_change=lambda e: State.set_selected_text(e),
                    placeholder="Task title",
                    width="100%"
                ),
                rx.text_area(
                    value=State.selected_todo["description"],
                    on_change=lambda e: State.set_selected_description(e),
                    placeholder="Task description",
                    width="100%",
                    height="100px"
                ),
                rx.checkbox(
                    label="Completed",
                    is_checked=State.selected_todo["completed"],
                    on_change=lambda e: State.set_selected_completed(e)
                ),
                rx.hstack(
                    rx.button("Save", on_click=State.save_selected_todo, color_scheme="blue"),
                    rx.button("Delete", on_click=State.delete_selected_todo, color_scheme="red"),
                    rx.button("Back", on_click=lambda: rx.redirect("/"), color_scheme="gray")
                ),
                spacing="4"
            ),
            rx.text("No task selected.")
        )
    )

# 4. View Details Page
def view_details() -> rx.Component:
    return rx.container(
        rx.heading("View Details", size="7"),
        rx.cond(
            State.selected_todo.is_not_none(),
            rx.vstack(
                rx.text(f"Title: {State.selected_todo['text']}", size="5"),
                rx.text(f"Description: {State.selected_todo['description']}", size="4"),
                rx.text(
                    rx.cond(
                        State.selected_todo["completed"],
                        "Completed: ✅",
                        "Completed: ❌"
                    ),
                    size="4",
                    color="gray"
                ),
                rx.button("Back", on_click=lambda: rx.redirect("/"), color_scheme="gray"),
                spacing="4"
            ),
            rx.text("No task selected.")
        )
    )

# 5. Register pages
app = rx.App()
app.add_page(index, title="Todo App")
app.add_page(edit_details, route="/edit_details", title="Edit Details")
app.add_page(view_details, route="/view_details", title="View Details")