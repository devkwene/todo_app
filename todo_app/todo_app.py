# app.py

import reflex as rx
from rxconfig import config
from sqlmodel import select
from .models import Todo
from .pages.index import index

from .state import State

# 3. Edit Details Page
def edit_details() -> rx.Component:
    return rx.container(
        rx.heading("Edit Details", size="7"),
        rx.cond(
            State.success_message != "",
            rx.fragment(
                rx.text(State.success_message, color="green", font_weight="bold"),
                rx.script("setTimeout(() => window.location.href = '/', 1500);")
            ),
        ),
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