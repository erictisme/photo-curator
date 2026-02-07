# Episode 01: "The AI Picked the Wrong Photo"
### A family, a laptop, and one hour to prove that AI can understand a mother's taste in photos

*A sample episode script for Eric + Yaohong's content series. Written to show the concept, not to be read word-for-word. Adapt freely.*

---

## WHAT ACTUALLY HAPPENED

Five people in a living room. Eric (doesn't code, builds apps by directing AI). His brother (software engineer, ex-Infosys, worked in tech at one of the world's largest sovereign wealth funds). Brother's wife (the one with the photo problem). Eric's wife. Eric's mum. A MacBook running Claude Code. And Whisper Flow turning everyone's conversation into text that Eric fed into the terminal.

Nobody planned this as a "demo." It started as a family hangout. Someone mentioned photos. The brother's wife said she had over a terabyte of photos she couldn't manage. Eric said, "Let me try something."

What followed was an hour of everyone talking — to each other and through Eric to Claude Code — that went from "I have too many photos" to "this AI understands which photo I'd frame on my wall" to "wait, we should build this into a real product."

This script reconstructs that session. Some context was lost (the conversation compacted twice as it got long), but the key moments survived.

---

## THE SCENE (5 min)

The brother's wife explains the problem. It's not about duplicates — Apple Photos already handles that. It's about having seventeen photos of the same moment. Her baby eating a muffin. Seventeen slightly different angles and expressions. She wants the best one or two. She doesn't want to manually compare seventeen photos for every event across a terabyte of memories.

The brother — who could literally build this himself — nods. He hasn't built it. Not because he can't. Because nobody sits down on a Saturday to build a photo sorting tool. The activation energy is too high. The problem isn't urgent enough to prioritize, but it's painful enough to complain about every time you open your photo library.

Eric's mum is there too. She doesn't know what Claude Code is. She's about to watch her son talk to a terminal and have it build software in front of her.

Eric opens his laptop. "Let me see if we can solve this right now."

---

## THE BUILD (10 min)

Eric isn't thinking "I need to build a Python script." He's thinking: **can I prove this is solvable before everyone gets bored and moves on?**

He starts talking to Claude Code through Whisper Flow — speaking naturally, describing the problem as the family discussed it. The room's conversation becomes the product requirements. No spec document. No wireframes. Just: "She has a folder of photos. Group them by when they were taken. Send each group to an AI that can see images. Ask it to name the event and pick the best photo."

Claude Code starts building. Files appear. The brother leans in — he notices file extensions, syntax, the structure. At one point he points out something about `.tsx` files and Eric has no idea what that means. This becomes a running joke. Eric is directing AI to write code in languages he can't read. And it's working.

Fifteen minutes in, there's a working script. Drop photos in a folder, run one command, get results.

The first run comes back. Gemini (Google's AI) looked at the 17 baby photos and named the event: **"Baby Eating Muffin."**

The room laughs. It's accurate. It's charming. It already feels like magic — an AI looked at a pile of unnamed image files and understood what was happening in them.

Best photo: IMG_5870. Score: 88 out of 100. All 17 ranked from best to worst.

Everyone leans in to look at the results.

---

## THE MOMENT IT GOT INTERESTING (5 min)

Eric asks his sister-in-law: "Which one would *you* frame on the wall?"

She doesn't hesitate. **IMG_5875.** The baby has this cheeky, mischievous expression — looking right at the camera with a little smirk. "That one. That's him. That's who he is."

Eric scrolls to find IMG_5875 in the rankings.

Score: **55 out of 100.** Dead last out of 17 photos.

The room goes quiet for a second. Then everyone starts talking at once. The photo a mother would frame on the wall — the AI put it at the very bottom. The AI was judging like a photography contest. The mother was judging like... a mother.

The brother immediately gets it from a technical angle: the AI was optimizing for the wrong objective. Sharp focus, good lighting, composition — that's what it was scoring. But personality, expression, the *feeling* of the photo? It wasn't even looking at that.

---

## THE REWRITE (10 min)

This is where it gets good. Eric doesn't change any code. He doesn't touch the script. He rewrites **one paragraph** — the instructions he gave the AI about how to score.

Before, the instruction was basically: *score on quality, composition, sharpness, and visual appeal.*

After — and this was shaped by the room's conversation, everyone chiming in about what matters in a family photo:

> You are a PARENT picking your favorite photos to frame on the wall — NOT a photography contest judge. You care about the FEELING of the photo, not whether it's technically perfect.
>
> 1. EXPRESSION & PERSONALITY (highest weight) — cheeky smiles, genuine laughs, playful looks
> 2. EMOTIONAL STORYTELLING — captures a feeling you'd want to remember
> 3. CUTENESS & CHARM — the 'aww' factor
> 4. TECHNICAL QUALITY (lowest weight, tiebreaker only)
>
> IMPORTANT: A slightly blurry photo of a genuinely funny expression beats a perfectly sharp photo of a neutral face.

The non-technical people in the room had a visible reaction to this. This isn't code. It's a creative brief. It's writing. It's something a mother, a pastor, an admin assistant could write. You're describing what you care about in plain English and the AI reshapes its judgment around your values.

They re-ran it. Same 17 photos, same Gemini model, new instructions.

IMG_5875 — the cheeky photo — scored **40.** Still dead last. It actually got *worse.*

The brother: "The model might just not be capable of this."

---

## THE EVAL (10 min)

Eric decides to test other models. Same 17 photos. Same "score like a parent" prompt. Three AI models head-to-head:

Claude Code spins up two additional scripts in parallel — one for Claude Sonnet (Anthropic), one for GPT-4o (OpenAI). The brother watches this happen in real time. Three scripts running simultaneously, three different AI companies scoring the same photos with identical instructions.

Results come back. Eric pulls up the comparison.

| Model | Where it ranked the cheeky photo | Score |
|-------|------|-------|
| **Claude Sonnet** | **#1 out of 17** | **95** |
| **GPT-4o** | #2 out of 17 | 90 |
| **Gemini** | #17 out of 17 (dead last) | 40 |

The room reacts. Even Eric's mum understands this table. The brother — a professional software engineer — is impressed. Not by the code, but by the methodology. He says something to the effect of: "That's what ML engineers do. You just did model evaluation without knowing the term."

Claude didn't just rank the cheeky photo well. It ranked it **first.** Score of 95. And it wrote a reason — something about the expression capturing genuine personality and mischief. When Eric read Claude's reason out loud, the room went quiet. The AI articulated *why* the photo mattered better than anyone in the room had.

The sister-in-law: "That's exactly right. That's exactly why I love that photo."

---

## WHAT HAPPENED AFTER (5 min)

The energy in the room shifted. The sister-in-law started riffing on ideas. What about a "purge folder" — instead of deleting rejected photos, move them somewhere for a quick review before permanent deletion? What about the AI learning her taste over time? What about a "Year in Photos" — like Spotify Wrapped, but for your photo library?

Eric captured all of this in a roadmap file. None of it got built that day. The point wasn't to build a product. The point was to prove the problem was solvable. And it was — in under an hour, with zero code written by a human.

The brother's takeaway was different. He'd been watching a non-technical person direct AI to build working software, evaluate multiple models, and arrive at a defensible technical decision — all without understanding what `.tsx` means. The activation energy problem he'd never solved for himself got solved in front of him by someone who doesn't code.

Eric's mum's takeaway: "So the computer can pick which photo is the nice one?"

Yes. That's exactly what it does.

---

## MOMENTS THAT LANDED

*The stuff that makes good content — when people in the room leaned in, laughed, or said "wait, what?"*

1. **"Baby Eating Muffin."** The AI naming the event. The room laughed. It felt human and charming. First moment of "oh, this thing *understands.*"

2. **Mom's taste vs AI's taste.** The emotional core. A mother's instinctive "that one, that's my kid" versus the AI's clinical "this one has better exposure." Made everyone think about what intelligence actually means.

3. **The prompt rewrite — reading it out loud.** When Eric read the rewritten prompt, the non-technical people realized: *I could write this. This is a creative brief, not code.* That was the accessibility moment.

4. **The eval table.** When the three-model comparison appeared. Claude #1, GPT-4o #2, Gemini dead last. A technical SWE and his mum both understood it instantly. Data, not opinion.

5. **Claude's "reason."** The AI explaining *why* the cheeky photo was the best — articulating the emotional quality better than the humans had. The sister-in-law saying "that's exactly right." An AI understanding a mother's taste.

6. **Eric not knowing what .tsx is.** The brother pointing it out, half-amused, half-amazed. The person directing the build doesn't understand the file extensions of the code being written. And it doesn't matter. The skill isn't reading code — it's knowing what to build and how to test it.

7. **The SWE who hadn't built it.** The unspoken subtext: a software engineer with world-class credentials could have built this himself. But he hadn't. The tool that matters isn't the one you *can* build — it's the one you *actually* build. Claude Code collapsed the gap between "I could" and "I did."

---

## EPISODE NOTES

**Setting:** Family living room, 5 people, 1 laptop
**Time:** ~60 minutes
**Code written by Eric:** Zero
**Code understood by Eric:** Also zero
**Models tested:** Gemini, Claude Sonnet, GPT-4o
**Winner:** Claude Sonnet (matched human taste perfectly)
**GitHub:** github.com/erictisme/photo-curator

---

## WHAT THIS EPISODE DEMONSTRATES

For Yaohong and anyone producing this content — this is what the format looks like:

**It's not a tutorial.** Nobody follows along on their own laptop. It's a screen shared in a room (or on a call) where the non-technical person drives and the conversation shapes what gets built.

**It's not a demo.** It's a discovery session. Nobody knew in advance that Gemini would fail, that the prompt rewrite wouldn't fix it, or that Claude would nail it. The failures are the content.

**The dynamic is 3+ people, not 2.** The person with the problem. The person directing the AI. The technical person observing and explaining. Maybe others watching and reacting. The conversation between them IS the product requirements — fed through Whisper Flow into Claude Code.

**Time to value is the proof.** Under 1 hour from "I have this problem" to "holy shit, the AI picked the exact photo I would have picked." That's the moment that convinces people this is real.

---

## GUIDING PRINCIPLES FOR THE SERIES

*Aligned with Eric's notes to Yaohong, Feb 7 2026:*

1. **Problem-first, not tool-first.** We don't demo Claude Code features. We solve someone's actual problem. The tool is invisible. The solution is the star.

2. **Time to value under 1 hour.** From "I have this problem" to "it works" in under 60 minutes. If it takes longer, the problem is too big or we're overbuilding. The goal isn't shipping a product — it's proving the problem is solvable. Enough to build trust that it's worth investing more time.

3. **Build tools nobody would build for them.** The positioning isn't "automate your job." It's "solve problems nobody would ever build a tool for" — like sorting through 10,000 family photos. These problems don't get solved because they're not big enough for a startup, not urgent enough for an engineer, and too tedious for a human. AI changes the economics.

4. **Enhance work, don't remove it.** Not "AI replaces your job." It's "AI does work that was never going to happen." The sister-in-law was never going to sort a terabyte manually. This isn't automation replacing labor. This is unlocking value that didn't exist before.

5. **The non-technical person leads.** Eric drives. He asks questions, describes problems, represents the audience. The technical person (Yaohong, or the brother in this case) explains what's happening and why it matters. The audience should see themselves in Eric.

6. **Show the failures.** The Gemini failure was more educational than the Claude success. The prompt rewrite that didn't work was more interesting than the one that did. Polished demos are boring. Real discovery is messy and relatable.

7. **Spend more time on problem discovery than building.** The conversation about *why* photos matter — reliving memories, mental load, Instagram as accidental curation — shaped the prompt rewrite, which shaped the product. The customer interview isn't a step before the build. It IS the build.

8. **ICP: "From my mum to pastors to doctors to admin staff."** Everyday white-collar people. People who will never write code. People who have problems they've given up on solving. The technical person in the room is the validator, not the audience.

9. **Capture, don't build.** When the customer starts riffing on ideas ("what about Spotify Wrapped for photos?"), write it down. Don't build it. The roadmap comes from the conversation. The build comes later — or never. The session is about proving value, not shipping features.
