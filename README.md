# DSPy Tweet Optimizer 🐦

A sophisticated tweet optimization tool that uses DSPy with Claude Sonnet 4.5 (via OpenRouter) to iteratively improve tweets using a hill climbing algorithm. Features a pop-punk themed interface with real-time progress tracking.

![Pop-Punk Edition](https://img.shields.io/badge/style-pop--punk-red?style=flat-square)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)
![Reflex](https://img.shields.io/badge/reflex-0.8.15a1-purple?style=flat-square)

## ✨ Features

- **Hill Climbing Optimization**: Iteratively generates and evaluates tweets to find the best version
- **Customizable Scoring**: Define your own evaluation categories (clarity, engagement, hashtag relevance, etc.)
- **Real-Time Progress**: Watch the optimization process with live updates
- **Patience Parameter**: Stop optimization after N iterations without improvement
- **Persistent Categories**: Your custom categories are saved in browser local storage
- **Pop-Punk UI**: Black/white/red aesthetic with smooth animations
- **DSPy + Claude Sonnet 4.5**: Powered by state-of-the-art language models

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenRouter API key ([get one here](https://openrouter.ai/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/DSPy-Hill-Climbing-Tweet-Refiner.git
   cd DSPy-Hill-Climbing-Tweet-Refiner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   ```bash
   export OPENROUTER_API_KEY="your-api-key-here"
   ```

4. **Run the application**
   ```bash
   reflex run
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

## 📖 Usage

### Basic Workflow

1. **Enter your input text**: Type or paste the text you want to turn into a tweet
2. **Configure parameters**:
   - **Iterations**: How many refinement cycles to run (1-20)
   - **Patience**: Stop after N iterations without improvement (1-20)
3. **Customize scoring categories**: Add or remove evaluation criteria
4. **Start optimizing**: Click "Start Optimizing" and watch the magic happen!
5. **View results**: See the best tweet with category-wise scores

### Scoring Categories

The optimizer evaluates each generated tweet across multiple categories (1-9 scale). Default categories include:

- **Clarity and conciseness**: How clear and to-the-point is the tweet?
- **Engagement and hook**: Does it grab attention?
- **Hashtag relevance**: Are hashtags used effectively?

You can add custom categories like "Brand voice", "Call-to-action strength", "Humor", etc.

### How Hill Climbing Works

1. Generate an initial tweet from your input text
2. Evaluate it on all categories
3. For each iteration:
   - Generate a new tweet variant
   - Evaluate the new tweet
   - If the total score improves → keep it as the new best
   - If no improvement → increment patience counter
4. Stop when patience threshold is reached or max iterations completed

## 🏗️ Architecture

```
app/
├── app.py                    # Main application entry point
├── dspy_modules.py          # DSPy generator and evaluator modules
├── states/
│   └── dspy_state.py        # State management and optimization logic
└── components/
    ├── sidebar.py           # Config panel and category manager
    └── main_content.py      # Tweet display and score visualization
```

### Key Components

- **TweetGeneratorSignature**: DSPy module for generating engaging tweets (max 280 chars)
- **TweetEvaluatorSignature**: DSPy module for scoring tweets on custom categories
- **DSPyState**: Reflex state with hill climbing logic and local storage persistence
- **Background Processing**: Async event handler for non-blocking optimization

## 🎨 Design System

The UI follows a pop-punk aesthetic:

- **Colors**: Black background, white text, red accents (#dc2626)
- **Typography**: Inter font family (400-900 weights)
- **Layout**: Responsive flexbox with sidebar toggle
- **Animations**: Smooth transitions for sidebar and state changes

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | ✅ Yes |

### Model Configuration

By default, the app uses `openai/anthropic/claude-3.5-sonnet` via OpenRouter. You can modify this in `app/dspy_modules.py`:

```python
_lm = dspy.LM(
    model="openai/anthropic/claude-3.5-sonnet",  # Change model here
    api_key=api_key,
    api_base="https://openrouter.ai/api/v1",
    headers={"HTTP-Referer": "http://localhost:3000"},
    cache=False,
)
```

## 🧪 Development

### Project Structure

- `rxconfig.py`: Reflex framework configuration
- `requirements.txt`: Python dependencies
- `plan.md`: Detailed project implementation notes
- `CLAUDE.md`: AI-assisted development guardrails

### Adding New Features

1. **New scoring category**: Just add it in the sidebar - it's automatically saved!
2. **Custom UI components**: Add to `app/components/`
3. **State management**: Extend `DSPyState` in `app/states/dspy_state.py`

## 🐛 Troubleshooting

### "OPENROUTER_API_KEY environment variable not set"
Make sure you've exported the environment variable before running `reflex run`:
```bash
export OPENROUTER_API_KEY="your-key"
```

### Slow generation
- Reduce the number of iterations
- Increase patience parameter (stops sooner)
- Check your OpenRouter API rate limits

### Categories not persisting
- Make sure you're using the same browser
- Check browser console for local storage errors
- Clear local storage and re-add categories

## 📝 License

This project is provided as-is for educational and personal use.

## 🙏 Acknowledgments

- Built with [Reflex](https://reflex.dev/) - Pure Python web framework
- Powered by [DSPy](https://github.com/stanfordnlp/dspy) - Programming with language models
- Uses [Claude Sonnet 4.5](https://www.anthropic.com/claude) via [OpenRouter](https://openrouter.ai/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

**Made with ❤️ and a lot of ☕ | Pop-Punk Edition 🎸**
