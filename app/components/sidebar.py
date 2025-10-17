import reflex as rx
from app.states.dspy_state import DSPyState


def config_slider(
    label: str, value: rx.Var[int], on_change: rx.event.EventHandler
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-300"),
        rx.el.div(
            rx.el.input(
                type="range",
                min=1,
                max=20,
                key=label,
                default_value=value.to_string(),
                on_change=on_change.throttle(100),
                class_name="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-red-600",
            ),
            rx.el.span(value, class_name="text-sm font-bold text-white ml-4"),
            class_name="flex items-center mt-2",
        ),
        class_name="w-full",
    )


def category_manager() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Scoring Categories", class_name="text-md font-semibold text-white mb-3"
        ),
        rx.el.div(
            rx.foreach(
                DSPyState.categories,
                lambda category, index: rx.el.div(
                    rx.el.span(
                        category["description"],
                        class_name="text-gray-300 text-sm flex-grow truncate",
                    ),
                    rx.el.button(
                        rx.icon(
                            "x", size=14, class_name="text-gray-500 hover:text-red-500"
                        ),
                        on_click=lambda: DSPyState.remove_category(index),
                        class_name="p-1 rounded-full",
                    ),
                    class_name="flex items-center justify-between bg-gray-800 p-2 rounded-md mb-2",
                ),
            ),
            class_name="space-y-2 mb-4",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="New category description...",
                on_change=DSPyState.set_new_category,
                on_key_down=lambda key: rx.cond(
                    key == "Enter", DSPyState.add_category, rx.noop()
                ),
                class_name="flex-grow bg-gray-700 border border-gray-600 text-white text-sm rounded-l-md p-2 focus:ring-red-500 focus:border-red-500 outline-none",
                default_value=DSPyState.new_category,
            ),
            rx.el.button(
                rx.icon("plus", size=18),
                on_click=DSPyState.add_category,
                class_name="bg-red-600 text-white p-2 rounded-r-md hover:bg-red-700",
            ),
            class_name="flex",
        ),
        class_name="mt-6 border-t border-gray-700 pt-6",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.h2(
                "DSPy Tweeter",
                class_name="text-2xl font-bold text-white tracking-tighter",
            ),
            rx.el.p(
                "Pop-Punk Edition", class_name="text-xs text-red-400 font-mono -mt-1"
            ),
            class_name="p-6 border-b border-gray-700",
        ),
        rx.el.div(
            rx.el.h3("Config", class_name="text-md font-semibold text-white mb-4"),
            rx.el.div(
                config_slider(
                    "Iterations (n)", DSPyState.iterations, DSPyState.set_iterations
                ),
                config_slider("Patience", DSPyState.patience, DSPyState.set_patience),
                class_name="space-y-4",
            ),
            category_manager(),
            class_name="p-6",
        ),
        class_name=rx.cond(
            DSPyState.sidebar_open,
            "w-80 bg-black text-white h-screen flex flex-col border-r border-gray-800 transition-all duration-300 ease-in-out",
            "w-0 -translate-x-full transition-all duration-300 ease-in-out",
        ),
    )