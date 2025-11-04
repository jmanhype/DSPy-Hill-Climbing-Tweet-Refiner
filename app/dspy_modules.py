import dspy
import os
from typing import Optional

_lm: Optional[dspy.LM] = None


def _get_lm() -> dspy.LM:
    """
    Get or create a cached DSPy language model instance configured for OpenRouter.

    Returns:
        dspy.LM: Configured language model instance using Claude Sonnet 4.5 via OpenRouter.

    Raises:
        ValueError: If OPENROUTER_API_KEY environment variable is not set.
    """
    global _lm
    if _lm is None:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY environment variable not set. "
                "Please set it with: export OPENROUTER_API_KEY='your-key-here'"
            )
        _lm = dspy.LM(
            model="openai/anthropic/claude-3.5-sonnet",
            api_key=api_key,
            api_base="https://openrouter.ai/api/v1",
            headers={"HTTP-Referer": "http://localhost:3000"},
            cache=False,
        )
    return _lm


class TweetGeneratorSignature(dspy.Signature):
    """Generate an engaging, concise, and well-structured tweet from input text."""

    input_text: str = dspy.InputField(
        desc="The base text or idea to convert into a tweet."
    )
    tweet: str = dspy.OutputField(
        desc="Generated tweet (max 280 characters). Should be catchy and include relevant hashtags."
    )


class TweetEvaluatorSignature(dspy.Signature):
    """Evaluate a tweet based on a set of categories, providing a score from 1 to 9 for each."""

    tweet: str = dspy.InputField(desc="The tweet to evaluate.")
    categories: str = dspy.InputField(
        desc="A semicolon-separated list of categories to score the tweet on."
    )
    scores: str = dspy.OutputField(
        desc="A JSON list of objects, each with a 'category' and a 'score' (integer 1-9)."
    )


_generator: Optional[dspy.ChainOfThought] = None
_evaluator: Optional[dspy.ChainOfThought] = None


def get_generator() -> dspy.ChainOfThought:
    """
    Get a cached instance of the tweet generator predictor.

    The generator uses DSPy's ChainOfThought module to convert input text
    into engaging, concise tweets (max 280 characters) with relevant hashtags.

    Returns:
        dspy.ChainOfThought: Configured tweet generator instance.
    """
    global _generator
    if _generator is None:
        dspy.configure(lm=_get_lm())
        _generator = dspy.ChainOfThought(TweetGeneratorSignature)
    return _generator


def get_evaluator() -> dspy.ChainOfThought:
    """
    Get a cached instance of the tweet evaluator predictor.

    The evaluator uses DSPy's ChainOfThought module to score tweets
    on custom categories (1-9 scale) and return structured JSON results.

    Returns:
        dspy.ChainOfThought: Configured tweet evaluator instance.
    """
    global _evaluator
    if _evaluator is None:
        dspy.configure(lm=_get_lm())
        _evaluator = dspy.ChainOfThought(TweetEvaluatorSignature)
    return _evaluator