import reflex as rx
from ..state import State

def edit_details() -> rx.Component:
    return rx.container(
        rx.heading("Edit Details", size="7"),
        rx.cond(
            State.success_message != "",
            rx.fragment(
                rx.text(State.success_message, color="green", font_weight="bold"),
                rx.script("setTimeout(() => window.location.href = '/', 1500);")
            ),
            rx.fragment()
        ),
        rx.cond(
            State.selected_todo is not None,
            rx.container(
                rx.color_mode.button(position="top-right"),
                rx.vstack(
                    rx.heading("Edit Todo Details", size="8"),
                    rx.input(
                        placeholder="Edit todo text...",
                        value=State.edit_todo_text,
                        on_change=lambda e: State.set_edit_todo_text(e),
                        width="300px",
                    ),
                    rx.text_area(
                        placeholder="Edit description...",
                        value=State.edit_todo_description,
                        on_change=lambda e: State.set_edit_todo_description(e),
                        width="300px",
                        min_height="80px",
                    ),
                    rx.hstack(
                        rx.checkbox(
                            checked=State.edit_todo_completed,
                            on_change=lambda e: State.set_edit_todo_completed(e),
                            label="Completed?",
                        ),
                        rx.button("Save", on_click=State.save_edit, color_scheme="green"),
                        rx.button("Back", on_click=lambda: rx.redirect("/"), color_scheme="gray"),
                    ),
                    rx.upload(
                        accept="image/*",
                        max_files=1,
                        on_upload=State.handle_upload,
                        children=rx.button("Upload Image", color_scheme="blue"),
                    ),
                    rx.cond(
                        State.edit_todo_image != "",
                        rx.image(src=State.edit_todo_image, width="200px", margin_top="10px"),
                        rx.fragment()
                    ),
                    spacing="6",
                    align_items="center",
                    min_height="85vh",
                ),
            ),
            rx.text("No task selected.")
        )
    )
