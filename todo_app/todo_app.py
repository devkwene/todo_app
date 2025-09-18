
# app.py
# This file brings together all the parts of the app and registers the pages.

import reflex as rx
from rxconfig import config
from sqlmodel import select
from .models import Todo  # The data model for tasks
from .pages.index import index  # The main page (task list)
from .state import State  # The app's logic and state

# Page for editing a task's details
def edit_details() -> rx.Component:
    return rx.container(
        rx.heading("Edit Details", size="7"),
        # Show a success message if there is one
        rx.cond(
            State.success_message != "",
            rx.fragment(
                rx.text(State.success_message, color="green", font_weight="bold"),
                rx.script("setTimeout(() => window.location.href = '/', 1500);")
            ),
        ),
        # If a task is selected, show its details for editing
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
                    rx.button("Back", on_click=lambda: rx.redirect("/"), color_scheme="gray"),
                ),
                spacing="4"
            ),
            rx.text("No task selected.")
        )
    )

# Page for viewing a task's details
def view_details() -> rx.Component:
    return rx.container(
        rx.heading("View Details", size="7"),
        # If a task is selected, show its details
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

# Register all pages with the app so users can navigate between them
app = rx.App()
app.add_page(index, title="Todo App")  # Main page
app.add_page(edit_details, route="/edit_details", title="Edit Details")  # Edit page
app.add_page(view_details, route="/view_details", title="View Details")  # View page