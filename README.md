# Photo Curator

AI-powered photo organizer that groups your photos by event and picks the best shot from each group. Uses Claude's vision to score photos the way a parent would — prioritizing personality and emotion over technical perfection.

## What It Does

1. **Groups photos by timestamp** — Photos taken within 30 minutes of each other are treated as one event
2. **Names each event** — AI looks at the photos and gives each group a descriptive name (e.g. "Baby Eating Muffin", "Window Sill Afternoon")
3. **Scores and ranks** — Each photo gets a 0-100 score based on expression, emotion, and charm
4. **Picks the best** — The top photo from each event is marked as the winner

Built for parents drowning in 10,000+ photos who want to keep the best ones without manually sorting.

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/YOUR_USERNAME/photo-curator.git
cd photo-curator
pip install -r requirements.txt

# 2. Add your API key
cp .env.example .env
# Edit .env and add your Anthropic API key

# 3. Add photos and run
# Drop your photos (JPEG, HEIC, PNG) into the input/ folder
mkdir -p input
python curator_claude.py
```

Results appear in `output_claude/` — organized by event with the best photo ranked #1.

## How Scoring Works

The AI scores like a parent picking photos to frame, not a photography judge:

| Priority | Weight | What It Means |
|----------|--------|---------------|
| Expression & Personality | Highest | Cheeky smiles, genuine laughs, playful looks |
| Emotional Storytelling | High | Captures a feeling you'd want to remember |
| Cuteness & Charm | Medium | The 'aww' factor |
| Technical Quality | Lowest | Sharpness, lighting (tiebreaker only) |

A slightly blurry photo of a genuinely funny expression beats a perfectly sharp photo of a neutral face.

## Scripts

| Script | AI Model | Notes |
|--------|----------|-------|
| `curator_claude.py` | Claude Sonnet | **Recommended** — best match with human taste |
| `curator_openai.py` | GPT-4o | Good alternative, close second |
| `curator.py` | Gemini | Original version, less reliable for emotional scoring |

## Requirements

- Python 3.10+
- [Anthropic API key](https://console.anthropic.com/) (for Claude version)
- Photos in JPEG, HEIC, or PNG format
