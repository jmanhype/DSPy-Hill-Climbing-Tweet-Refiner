import reflex as rx
from app.states.dspy_state import DSPyState
from app.components.sidebar import sidebar
from app.components.main_content import main_content


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        main_content(),
        class_name="flex min-h-screen bg-black font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)