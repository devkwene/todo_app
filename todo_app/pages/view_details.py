import reflex as rx
from ..state import State

# This page lets you view all the details of a selected task.
def view_details() -> rx.Component:
    return rx.container(
        # Heading for the page
        rx.heading("View Details", size="7"),
        # If a task is selected, show its details
        rx.cond(
            State.selected_todo is not None,
                rx.vstack(
                    # Show the task's title
                    rx.text(f"Title: {State.selected_todo['text']}", size="5"),
                    # Show the task's description
                    rx.text(f"Description: {State.selected_todo['description']}", size="4"),
                    # If there is an image, show it
                    rx.cond(
                        State.selected_todo.get("image", "") != "",
                        rx.image(src=f"/assets/{State.selected_todo['image']}", width="200px", margin_top="10px"),
                        rx.fragment()
                    ),
                    # Show if the task is completed
                    rx.text(
                        rx.cond(
                            State.selected_todo["completed"],
                            "Completed: ✅",
                            "Completed: ❌"
                        ),
                        size="4",
                        color="gray"
                    ),
                    # Button to go back to the main page
                    rx.button("Back", on_click=lambda: rx.redirect("/"), color_scheme="gray"),
                    spacing="4"
                ),
            # If no task is selected, show a message
            rx.text("No task selected.")
        )
    )
