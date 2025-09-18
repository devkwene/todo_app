import reflex as rx
from ..state import State

# This is the main page of the app. It shows the todo list and lets you add, edit, delete, and view tasks.
def index() -> rx.Component:
    return rx.container(
        # Theme toggle button in the top right
        rx.color_mode.button(position="top-right"),
        # Main vertical stack for the page content
        rx.vstack(
            # Big heading for the app title
            rx.heading("My Todo List", size="8"),
            # Show a success message if there is one
            rx.cond(
                State.success_message != "",
                rx.text(State.success_message, color="green", font_weight="bold", margin_bottom="10px"),
                rx.fragment()
            ),
            # Input box and add button for new tasks
            rx.hstack(
                rx.input(
                    placeholder="Enter a todo...",
                    value=State.new_todo,
                    on_change=lambda e: State.set_new_todo(e),
                    width="300px",
                ),
                rx.button("Add", on_click=State.add_todo, color_scheme="green"),
            ),
            # List of all tasks with up/down buttons for reordering
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
                            # Up button
                            rx.button("↑", on_click=lambda: State.move_todo_up(i), is_disabled=(i == 0), size="2"),
                            # Down button
                            rx.button("↓", on_click=lambda: State.move_todo_down(i), is_disabled=(i == State.todos.length() - 1), size="2"),
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
            # Space and alignment for the whole page
            spacing="6",
            align_items="center",
            min_height="85vh",
        ),
        # When the page loads, get all tasks
        on_mount=State.on_mount,
    )
