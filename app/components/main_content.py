import reflex as rx
from app.states.dspy_state import DSPyState


def score_display(
    scores: rx.Var[list[dict]], title: str, color_class: str
) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name=f"text-lg font-semibold mb-3 {color_class}"),
        rx.el.div(
            rx.cond(
                scores.length() > 0,
                rx.foreach(
                    scores,
                    lambda score: rx.el.div(
                        rx.el.p(
                            score["category"],
                            class_name="text-sm text-gray-400 flex-1 truncate",
                        ),
                        rx.el.p(
                            score["score"], class_name="text-lg font-bold text-white"
                        ),
                        class_name="flex justify-between items-center p-3 bg-gray-800 rounded-lg",
                    ),
                ),
                rx.el.p(
                    "No scores yet.",
                    class_name="text-sm text-gray-500 text-center py-4",
                ),
            ),
            class_name="space-y-2",
        ),
        class_name="bg-black/50 p-4 rounded-xl border border-gray-800",
    )


def main_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.button(
                rx.icon(
                    tag=rx.cond(
                        DSPyState.sidebar_open, "chevrons-left", "chevrons-right"
                    ),
                    size=20,
                ),
                on_click=DSPyState.toggle_sidebar,
                class_name="absolute top-6 left-6 text-gray-400 hover:text-white",
            ),
            rx.el.h1(
                "Tweet Optimizer",
                class_name="text-4xl font-bold text-white tracking-tighter",
            ),
            rx.el.p(
                "Generate and refine tweets using DSPy.",
                class_name="text-gray-400 mt-1",
            ),
            class_name="text-center mb-8",
        ),
        rx.el.div(
            rx.el.h2("Input Text", class_name="text-xl font-semibold text-white mb-3"),
            rx.el.textarea(
                default_value=DSPyState.input_text,
                on_change=DSPyState.set_input_text.debounce(300),
                placeholder="Enter the base text for your tweet here...",
                class_name="w-full p-4 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-all h-32",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        DSPyState.processing, "Stop Processing", "Start Optimizing"
                    ),
                    on_click=rx.cond(
                        DSPyState.processing,
                        DSPyState.stop_processing,
                        DSPyState.start_processing,
                    ),
                    class_name=rx.cond(
                        DSPyState.processing,
                        "w-full py-3 px-4 bg-gray-600 text-white font-semibold rounded-lg hover:bg-gray-700 flex items-center justify-center space-x-2",
                        "w-full py-3 px-4 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 flex items-center justify-center space-x-2",
                    ),
                ),
                class_name="mt-4",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Current Tweet", class_name="text-xl font-semibold text-white mb-3"
                ),
                rx.el.div(
                    rx.el.p(
                        rx.cond(
                            DSPyState.current_tweet,
                            DSPyState.current_tweet,
                            "Waiting to generate...",
                        ),
                        class_name="text-gray-300 leading-relaxed",
                    ),
                    class_name="p-4 bg-gray-900 border border-gray-700 rounded-lg min-h-[100px]",
                ),
            ),
            rx.el.div(
                rx.el.h2(
                    "Best Tweet", class_name="text-xl font-semibold text-white mb-3"
                ),
                rx.el.div(
                    rx.el.p(
                        rx.cond(
                            DSPyState.best_tweet,
                            DSPyState.best_tweet,
                            "No improved tweet yet.",
                        ),
                        class_name="text-green-400 leading-relaxed font-medium",
                    ),
                    class_name="p-4 bg-gray-900 border border-green-800 rounded-lg min-h-[100px]",
                ),
            ),
            class_name="grid md:grid-cols-2 gap-8 mb-8",
        ),
        rx.el.div(
            score_display(DSPyState.current_scores, "Current Scores", "text-red-400"),
            score_display(DSPyState.best_scores, "Best Scores", "text-green-400"),
            class_name="grid md:grid-cols-2 gap-8",
        ),
        class_name="flex-1 p-8 overflow-y-auto bg-gray-900",
    )