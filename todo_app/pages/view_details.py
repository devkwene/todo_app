import reflex as rx
from ..state import State

def view_details() -> rx.Component:
    return rx.container(
        rx.heading("View Details", size="7"),
        rx.cond(
            State.selected_todo is not None,
                rx.vstack(
                    rx.text(f"Title: {State.selected_todo['text']}", size="5"),
                    rx.text(f"Description: {State.selected_todo['description']}", size="4"),
                    rx.cond(
                        State.selected_todo.get("image", "") != "",
                        rx.image(src=f"/assets/{State.selected_todo['image']}", width="200px", margin_top="10px"),
                        rx.fragment()
                    ),
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
