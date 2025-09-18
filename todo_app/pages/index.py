import reflex as rx
from ..state import State

def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("My Todo List", size="8"),
            rx.cond(
                State.success_message != "",
                rx.text(State.success_message, color="green", font_weight="bold", margin_bottom="10px"),
                rx.fragment()
            ),
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
