# Photo Curator - Roadmap

## What We Proved (Feb 7, 2026)
- Tested 3 AI models on same photos with same "score like a parent" prompt
- **Claude Sonnet** = best match with human taste (picked the "cheeky" photo as #1)
- **GPT-4o** = close second (ranked it #2)
- **Gemini** = consistently wrong for personal/emotional photos (ranked favorite dead last 3x)
- **Decision: Use Claude Sonnet as the scoring engine going forward**

## Next: Web App (Priority)
Turn the Python script into a proper web app with drag-and-drop UI.

**Core flow:**
1. User drags in a folder of photos
2. App groups by event, names them
3. Shows top photos from each group
4. User approves/rejects (training the model over time)
5. Output: curated photos ready for Instagram or keeping

**Stack:** Next.js + Tailwind + shadcn/ui (Eric's standard stack), Claude API on backend

## Future: Purge Folder (Safety Net)
Instead of deleting "rejected" photos, move them to a review/purge folder. User does a quick scan before permanent deletion. Hypothesis: even reviewing the purge folder is faster than manually sorting 1TB of photos from scratch.

## Future: Preference Learning
- Save user's approve/reject decisions over time
- Build a "taste profile" as a system instruction
- The more you use it, the better it knows your preferences
- Like training a model, but through a system prompt that evolves

## Future: "Year in Photos" Wrapped
Generate a year-end summary - like Spotify Wrapped but for your photo library.
- Best photo from each event across the year
- AI-written prose narrative of the year's highlights
- Month-by-month storytelling with embedded photos
- Stats: X events, Y photos curated, top moments

## Big Vision
"Sell it to Apple" - this should be a feature built into iPhotos/Apple Photos. Until then, build the standalone tool that proves the concept.
