# DSPy-Hill-Climbing-Tweet-Refiner

A tweet optimization tool built with DSPy and Reflex. Uses hill climbing to iteratively generate and score tweet variants, keeping the highest-scoring version.

## How it works

1. Generate an initial tweet from input text using DSPy + Claude Sonnet (via OpenRouter)
2. Score it across configurable categories (1-9 scale)
3. For each iteration, generate a variant and compare scores
4. Keep the variant if total score improves; otherwise increment a patience counter
5. Stop when patience runs out or max iterations reached

## Stack

| Component | Technology |
|---|---|
| Frontend/backend | Reflex 0.8.15a1 (Python full-stack framework) |
| LLM orchestration | DSPy |
| Model | Claude Sonnet 3.5 via OpenRouter |
| State persistence | Browser localStorage (for custom categories) |

## Requirements

- Python >= 3.8
- OpenRouter API key

## Setup

```bash
git clone https://github.com/jmanhype/DSPy-Hill-Climbing-Tweet-Refiner.git
cd DSPy-Hill-Climbing-Tweet-Refiner
pip install -r requirements.txt
export OPENROUTER_API_KEY="your-key"
reflex run
# Open http://localhost:3000
```

## Configuration

| Variable | Description | Required |
|---|---|---|
| `OPENROUTER_API_KEY` | OpenRouter API key | Yes |

To change the model, edit `app/dspy_modules.py`:

```python
_lm = dspy.LM(
    model="openai/anthropic/claude-3.5-sonnet",  # change here
    api_key=api_key,
    api_base="https://openrouter.ai/api/v1",
)
```

## Parameters

| Parameter | Range | Description |
|---|---|---|
| Iterations | 1-20 | Number of refinement cycles |
| Patience | 1-20 | Stop after N iterations without improvement |
| Categories | Custom | Evaluation criteria (clarity, engagement, hashtag relevance, etc.) |

## Default scoring categories

- Clarity and conciseness
- Engagement and hook
- Hashtag relevance

Custom categories can be added in the sidebar and are persisted in browser localStorage.

## Project structure

```
app/
  app.py              # Entry point
  dspy_modules.py     # DSPy generator and evaluator signatures
  states/
    dspy_state.py     # Hill climbing logic, state management
  components/
    sidebar.py        # Config panel, category manager
    main_content.py   # Tweet display, score visualization
```

## Limitations

- Depends on OpenRouter availability and rate limits
- No server-side persistence of optimization history
- Single-user (no auth or multi-tenancy)
- The Reflex version pinned (0.8.15a1) is an alpha release

## License

Provided as-is for educational and personal use.
