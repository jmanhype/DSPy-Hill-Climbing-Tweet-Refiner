import reflex as rx
from typing import TypedDict
import json
import logging
import asyncio
from app.dspy_modules import get_generator, get_evaluator


class Category(TypedDict):
    description: str


class Score(TypedDict):
    category: str
    score: int


class DSPyState(rx.State):
    categories_json: str = rx.LocalStorage(name="tweet_optimizer_categories")
    sidebar_open: bool = True
    new_category: str = ""
    processing: bool = False
    input_text: str = (
        "Reflex is a web framework that allows you to build web apps in pure Python."
    )
    iterations: int = 10
    patience: int = 3
    current_tweet: str = ""
    best_tweet: str = ""
    current_scores: list[Score] = []
    best_scores: list[Score] = []
    iteration_count: int = 0
    patience_counter: int = 0

    @rx.var
    def categories(self) -> list[Category]:
        """Get categories from JSON string or return default."""
        if self.categories_json:
            try:
                return json.loads(self.categories_json)
            except json.JSONDecodeError as e:
                logging.exception(
                    f"Could not decode categories_json: {e}, returning default."
                )
                return self._default_categories()
        return self._default_categories()

    def _default_categories(self) -> list[Category]:
        """Return default categories."""
        return [
            {"description": "Clarity and conciseness"},
            {"description": "Engagement and hook"},
            {"description": "Hashtag relevance"},
        ]

    def _save_categories(self, new_categories: list[Category]):
        """Save categories to local storage as a JSON string."""
        self.categories_json = json.dumps(new_categories)

    @rx.event
    def add_category(self):
        """Add a new category from the input field."""
        if self.new_category.strip():
            current_categories = self.categories
            current_categories.append({"description": self.new_category.strip()})
            self._save_categories(current_categories)
            self.new_category = ""

    @rx.event
    def remove_category(self, index: int):
        """Remove a category by its index."""
        current_categories = self.categories
        if 0 <= index < len(current_categories):
            current_categories.pop(index)
            self._save_categories(current_categories)

    @rx.event(background=True)
    async def start_processing(self):
        """Starts the tweet optimization hill climbing process."""
        async with self:
            if self.processing:
                return
            self.processing = True
            self.iteration_count = 0
            self.patience_counter = 0
            self.best_tweet = ""
            self.best_scores = []
        generator = get_generator()
        evaluator = get_evaluator()
        category_str = "; ".join([cat["description"] for cat in self.categories])
        async with self:
            self.current_tweet = "Generating initial tweet..."
        yield
        try:
            initial_result = await asyncio.to_thread(
                generator, input_text=self.input_text
            )
            initial_tweet = initial_result.tweet
            eval_result = await asyncio.to_thread(
                evaluator, tweet=initial_tweet, categories=category_str
            )
            initial_scores = json.loads(eval_result.scores)
            async with self:
                self.best_tweet = self.current_tweet = initial_tweet
                self.best_scores = self.current_scores = initial_scores
            best_total_score = sum((s.get("score", 0) for s in initial_scores))
            for i in range(self.iterations):
                if not self.processing:
                    break
                async with self:
                    self.iteration_count = i + 1
                yield
                new_result = await asyncio.to_thread(
                    generator, input_text=self.best_tweet
                )
                new_tweet = new_result.tweet
                eval_result = await asyncio.to_thread(
                    evaluator, tweet=new_tweet, categories=category_str
                )
                new_scores = json.loads(eval_result.scores)
                new_total_score = sum((s.get("score", 0) for s in new_scores))
                async with self:
                    self.current_tweet = new_tweet
                    self.current_scores = new_scores
                    if new_total_score > best_total_score:
                        self.best_tweet = new_tweet
                        self.best_scores = new_scores
                        best_total_score = new_total_score
                        self.patience_counter = 0
                    else:
                        self.patience_counter += 1
                    if self.patience_counter >= self.patience:
                        self.processing = False
                        break
                yield
        except Exception as e:
            logging.exception(f"Error during DSPy processing: {e}")
            async with self:
                self.current_tweet = f"Error: {e}"
        finally:
            async with self:
                self.processing = False

    @rx.event
    def stop_processing(self):
        """Stops the tweet optimization process."""
        self.processing = False

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    @rx.event
    def set_input_text(self, text: str):
        """Set the input text for tweet generation."""
        self.input_text = text

    @rx.event
    def set_iterations(self, value: str):
        """Set the number of iterations from the slider."""
        self.iterations = int(value)

    @rx.event
    def set_patience(self, value: str):
        """Set the patience value from the slider."""
        self.patience = int(value)

    @rx.event
    def set_new_category(self, text: str):
        """Update the new category input field."""
        self.new_category = text