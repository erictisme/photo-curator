# Episode 01: "My AI Picked the Wrong Photo"
### How a Non-Technical Builder Used Claude Code to Build an AI Photo Curator in 60 Minutes — and What It Teaches About Building with AI

*A podcast script in the style of How I AI. Written for Eric + Yaohong to riff on. Adapt freely.*

---

## COLD OPEN (2 min)

**ERIC:**
Here's a question. You have 10,000 photos on your phone. Your kid's first year. Birthdays, holidays, random Tuesday mornings. You *know* there are amazing photos buried in there. But you will never, ever sort through them.

So I asked an AI to pick the best ones. And it picked wrong. Dead last. The photo my friend would frame on the wall — the AI scored it the lowest out of 17 photos. Three times in a row.

And that failure is the most interesting thing that happened. Because what we did next — rewriting one paragraph of instructions, and then testing three different AI models head-to-head — taught me more about building with AI than any tutorial I've ever watched.

I'm Eric. I don't write code. I build software by talking to AI. And today I'm going to walk you through exactly what happened, step by step.

---

## ACT 1: THE PROBLEM NOBODY SOLVES (8 min)
*Theme: Start with a real person's real pain. Not a hypothesis.*

**ERIC:**
So this started because I was hanging out with a couple — the husband is a software engineer. Infosys background. Used to work in tech at one of the largest sovereign wealth funds in the world. His wife has a problem with her photos. Apple Photos. Over a terabyte. And the duplicate-finder in Apple Photos? She's tried it. It catches *identical* copies. But that's not her problem.

Her problem is she has seventeen photos of the same moment. Her baby eating a muffin. Slightly different angles, slightly different expressions. She wants to keep the best one or two, not all seventeen. But she'll never sit down and do that manually for a terabyte of photos.

And here's what makes this interesting: her husband is a *technical* guy. He could probably build something to solve this. But he hasn't. Because the problem isn't technical skill — it's that life is busy, nobody has the motivation to sit down and build a photo sorter on a Saturday afternoon. This is the kind of problem that doesn't get solved because it's not urgent enough to prioritize, but painful enough to complain about.

**[YAOHONG — tech context]:**
*This is actually a harder problem than it sounds. Finding identical photos is a solved problem — you compare the file data. Finding the "best" photo from a group of similar-but-different photos? That's a judgment call. That's taste. And taste is subjective.*

**ERIC:**
Right. And here's the insight that changed how I think about this. The problem isn't "too many photos." The problem is: **she can't relive her memories easily.**

Think about Instagram. Why do people post there? It forces you to pick your best photos. It displays them beautifully. It becomes this curated timeline of your life. Instagram is accidentally the best photo curation tool most people have.

But your private photo library? It's just a dump. You never look back. It's mental load — you *know* you should organize it, you never do, and so those memories just... sit there.

**[Principle #1: Spend more time on problem discovery than diving in. The customer interview IS the product work.]**

---

## ACT 2: BUILD THE SIMPLEST THING (10 min)
*Theme: Don't build an app. Build a script. Prove the concept first.*

**ERIC:**
So here's what we did. And I want to be really transparent about the messy process, because I think that's what's valuable.

I opened Claude Code — which is a terminal tool, you type to it and it builds things — and I said, basically: "Build me a Python script that takes a folder of photos, groups them by when they were taken, sends each group to an AI that can see images, and asks it to score them."

Fifteen minutes later, we had a working script. Drop photos in a folder, run one command, get results.

**[YAOHONG — tech context]:**
*What happened under the hood: Claude Code wrote a Python script that reads the timestamp from each photo's metadata — every photo has hidden data saying when and where it was taken — groups photos taken within 30 minutes of each other as one "event," then sends each group to an AI vision model to name and score.*

**ERIC:**
The first version used Google's Gemini model. It looked at our 17 baby photos and came back with:

- Event name: **"Baby Eating Muffin"** — accurate, and pretty cute
- Best photo: **IMG_5870** — scored 88 out of 100
- Ranked all 17 from best to worst

And we were like, cool, it works! Let's check if the AI agrees with a real human.

**[Principle #2: Build the simplest thing that could possibly work. A Python script you run from the terminal. Not an app. Not a website. One command, one result. Prove the concept before you build the product.]**

---

## ACT 3: THE HUMAN TEST (10 min)
*Theme: The moment everything got interesting. AI meets human taste.*

**ERIC:**
So here's where it gets good. I showed my friend the ranked results and asked: "Which one would *you* frame on the wall?"

She immediately pointed to **IMG_5875**. A photo where the baby has this cheeky, mischievous expression — looking right at the camera with this little smirk. She said, "That one. That's the one that captures who he is."

I looked at the scores. IMG_5875 was scored **55 out of 100.** Dead last out of 17 photos.

**[Pause for effect]**

The photo a mother would frame on the wall — the AI put it at the very bottom.

**[YAOHONG — tech context]:**
*This is actually a really important moment, and it happens all the time in AI products. The AI was scoring "correctly" by its own criteria — sharp focus, good lighting, composition. But the human was scoring on something completely different: personality. Expression. The feeling of the photo. The AI was a photography judge. The mother was... a mother.*

**ERIC:**
Exactly. And this is where the methodology kicks in. We didn't throw out the tool. We didn't say "AI is useless." We said: **the instructions are wrong.**

**[Principle #3: When the AI gets it wrong, the first question is always: "Did I ask for the right thing?" Not "is the AI broken?" Your instructions are the product.]**

---

## ACT 4: THE PROMPT REWRITE (8 min)
*Theme: One paragraph changed everything. Prompt engineering is product design.*

**ERIC:**
So we rewrote the instructions. And I want to show you the before and after, because this is probably the most valuable part of the whole session.

**Before — the default instruction was basically:**
> Score each photo on quality, composition, sharpness, and visual appeal.

Standard photography criteria. Technical. Objective. And totally wrong for what we wanted.

**After — the rewritten instruction:**
> You are a PARENT picking your favorite photos to frame on the wall — NOT a photography contest judge. You care about the FEELING of the photo, not whether it's technically perfect.
>
> Score based on priorities:
> 1. EXPRESSION & PERSONALITY (highest weight) — cheeky smiles, genuine laughs, playful looks
> 2. EMOTIONAL STORYTELLING — captures a feeling you'd want to remember
> 3. CUTENESS & CHARM — the 'aww' factor
> 4. TECHNICAL QUALITY (lowest weight, tiebreaker only)
>
> IMPORTANT: A slightly blurry photo of a genuinely funny expression beats a perfectly sharp photo of a neutral face.

**[YAOHONG — tech context]:**
*Notice what Eric did here. He didn't change any code. He didn't change the model. He changed one paragraph of text — the system prompt. This is the closest thing to "product design" in AI development. You're literally writing the personality and judgment criteria of your product in plain English. No code required.*

**ERIC:**
We re-ran it with the new prompt. Same 17 photos. Same Gemini model.

IMG_5875 — the cheeky photo — scored **40.** Still dead last.

**[YAOHONG:]**
*Wait, it got worse?*

**ERIC:**
It got worse. We ran it again. Same thing. Gemini just... doesn't get it. Even when you explicitly tell it "personality over perfection," it keeps defaulting to technical quality.

And that's when we decided to do something I'd never done before.

**[Principle #4: If your prompt is right but the output is still wrong, the model might be the problem. Not all AI models are interchangeable. They have different "personalities."]**

---

## ACT 5: THE EVAL TABLE (12 min)
*Theme: Testing three AI models head-to-head. The moment this became real engineering.*

**ERIC:**
We took the exact same 17 photos, the exact same "score like a parent" prompt, and ran it through three different AI models:

1. **Gemini** (Google) — the one that kept failing
2. **Claude Sonnet** (Anthropic) — the model I use for coding
3. **GPT-4o** (OpenAI) — the one everyone talks about

Same photos, same instructions, three different judges. And here's what came back:

| Model | Where it ranked IMG_5875 (the cheeky photo) | Score |
|-------|------|-------|
| **Claude Sonnet** | **#1 out of 17** | **95** |
| **GPT-4o** | #2 out of 17 | 90 |
| **Gemini** | #17 out of 17 (dead last) | 40 |

**[Let that sink in.]**

Claude didn't just rank it well. It ranked it *first.* The exact photo the mother would frame on the wall. Score of 95.

GPT-4o was close — second place, score of 90. Respectable.

Gemini? Dead. Last. For the third time. Even with the emotional prompt.

**[YAOHONG — tech context]:**
*OK, so this is genuinely fascinating from a technical perspective. All three models received identical input — same images, same text prompt. The difference is in how each model was trained. Google optimized Gemini heavily for factual accuracy and structured analysis. It interprets "score like a parent" and still defaults to technical metrics. Claude was trained with a different emphasis — understanding human intent, nuance, what you actually mean versus what you literally said. When you say "score like a parent," Claude understands the spirit of that instruction. It's not just reading the words — it's reading the intent.*

**ERIC:**
And here's the thing — I would never have known this if I hadn't tested. If I'd just used Gemini (because I had a Google API key handy) and never compared, I would've thought AI just can't do this. I would've given up.

The eval table took maybe 15 minutes to set up. Claude Code created the two extra scripts in parallel. And those 15 minutes completely changed my conclusion from "AI can't understand taste" to "the right AI absolutely can."

**[Principle #5: Always eval. Always compare. The difference between "AI doesn't work for this" and "this specific model doesn't work for this" is the difference between giving up and shipping a product.]**

---

## ACT 6: THE BIGGER PICTURE (5 min)
*Theme: What this session revealed about building with AI as a non-technical person.*

**ERIC:**
So let me zoom out. What actually happened in this 60-minute session?

1. **We started with a real person and a real problem** — not a feature idea, not a spec. A friend sitting next to me saying "I can't deal with my photos." That's the customer interview.

2. **We built the simplest possible thing** — a Python script. Not an app. Not a website. One command, one result. Took 15 minutes.

3. **We tested with a real human** — showed the results to the person with the problem. She immediately found the flaw.

4. **We iterated on the instructions, not the code** — the rewrite was one paragraph. Plain English. No programming knowledge needed.

5. **When the instructions were right but the output was still wrong, we compared models** — 15 minutes, three models, one table. Clear winner.

6. **We let the customer interview shape the product vision** — the friend started riffing on ideas. Purge folder. Preference learning. "Year in Photos" like Spotify Wrapped. Instagram for your private library. These ideas came from the conversation, not from a whiteboard.

The whole thing — from "I have too many photos" to "Claude Sonnet picks the exact photo I'd frame on my wall" — was about an hour.

**[YAOHONG:]**
*And the interesting thing is, none of this required reading or writing code. Eric was directing the AI the entire time. "Build me this." "Change this instruction." "Now test it against these other models." That's it. The skill isn't coding. The skill is knowing what to build, how to test it, and when to change direction.*

---

## THE METHODOLOGY — EXTRACTED (3 min)
*For the podcast series going forward.*

**ERIC:**
So if we're going to do this regularly — build things live, on camera — here's the methodology that emerged naturally from today. We didn't plan this. It just happened. But I think it's repeatable.

**Step 1: Customer Interview (10-15 min)**
- Sit with a real person who has a real problem
- Use voice transcription (I used Whisper Flow) so you can talk naturally
- Let them describe the pain in their own words
- Don't propose solutions yet. Just listen.

**Step 2: Build the Simplest Thing (15-20 min)**
- Python script, not an app
- One input, one output
- Direct the AI tool to build it. Don't overthink architecture.
- The goal is a working prototype you can show to the person in the same session.

**Step 3: The Human Test (5 min)**
- Show the output to the real human
- Ask: "Does this match what you'd do?"
- Listen for where it disagrees. That's the gold.

**Step 4: Iterate on Instructions (10 min)**
- When it disagrees, rewrite the prompt — the instructions you gave the AI
- This is product design in plain English
- Test again. Did it get closer?

**Step 5: Eval if Needed (15 min)**
- If the instructions are right but the output is still wrong, test other AI models
- Same input, same prompt, different model
- Build a comparison table. Let the data decide.

**Step 6: Capture the Vision (5 min)**
- After the build, the customer will naturally start riffing on ideas
- Write these down. This is your roadmap.
- Don't build them yet. Just capture.

**Total: ~60 minutes from problem to proof-of-concept.**

---

## CLOSE (2 min)

**ERIC:**
The thing I keep coming back to is: my friend will never learn to code. She doesn't want to. She shouldn't have to. But she has a real problem — a terabyte of memories she can't access — and in one hour, sitting on a couch, talking to me while I talked to an AI, we proved that the problem is solvable.

That's what I want to show people. Not "learn to code." Not "AI will take your job." Just: **there are things you've given up on solving because you thought they required a developer. They don't anymore.**

And if the AI picks the wrong photo? You rewrite one paragraph and try again.

**[YAOHONG:]**
*From the technical side — what impressed me is the eval. Most people, technical or not, don't compare models. They use whatever's default and assume the results are representative. Eric's instinct to say "let me test three models side by side" is actually what professional ML engineers do. He just did it without knowing the jargon.*

**ERIC:**
See? I'm accidentally an engineer. Don't tell anyone.

---

## MOMENTS THAT LANDED IN THE ROOM

*These are the moments during the live session where people leaned in, laughed, or said "wait, what?" — the stuff that makes good content.*

1. **The eval table.** When the three-model comparison appeared on screen — Claude #1, GPT-4o #2, Gemini dead last — there was a visible "oh shit" moment. The table made it undeniable. It wasn't opinion. It was data. A technical SWE and his wife both understood it instantly.

2. **Reading Claude's "reason" out loud.** After Claude scored the cheeky photo #1 with a 95, it also wrote a one-sentence reason explaining *why* — something about the expression capturing genuine personality. Reading that out loud to the room, people went quiet. The AI articulated why the photo mattered *better than the humans had.*

3. **The prompt rewrite side-by-side.** Showing the before prompt ("score on quality and composition") next to the after prompt ("you are a PARENT picking photos to frame on the wall") — that was the "aha" moment. The non-technical people in the room realized: this isn't coding. This is *writing.* You're writing a brief, like for a creative agency. And that's accessible to everyone.

4. **"Baby Eating Muffin."** When Gemini named the event "Baby Eating Muffin," the room laughed. It was accurate, charming, and made the tech feel human. Naming things is one of AI's underrated superpowers.

5. **Mom's taste vs AI's taste.** The whole dynamic of a mother's instinctive "that one, that's my kid" versus the AI's clinical "this one has better exposure" — that tension was the emotional core of the session. It made everyone think about what "intelligence" actually means.

6. **The technical husband hadn't built this.** The unspoken subtext: a software engineer with SWF-tier credentials could have built this himself. But he hadn't. Because the tool that matters isn't the one you *can* build — it's the one you *actually* build. Claude Code collapsed the activation energy to zero.

---

## EPISODE NOTES

**What was built:** Photo Curator — groups photos by event, scores them using AI vision, picks the best one
**Time:** ~60 minutes
**Code written by Eric:** Zero
**Models tested:** Gemini, Claude Sonnet, GPT-4o
**Winner:** Claude Sonnet (matched human taste perfectly)
**GitHub:** github.com/erictisme/photo-curator

**Key moments:**
- 0:00 — Cold open: "The AI picked wrong"
- 2:00 — The problem: 1TB of photos, can't relive memories
- 10:00 — Building the first script in 15 minutes
- 20:00 — The human test: friend picks her favorite, AI disagrees
- 28:00 — The prompt rewrite: "score like a parent"
- 36:00 — The eval table: three models, one winner
- 48:00 — The methodology: 6 steps from problem to proof
- 55:00 — What this means for non-technical builders

---

## GUIDING PRINCIPLES FOR THE SERIES

Extracted from today's session and Eric's notes to Yaohong:

1. **Problem-first, not tool-first.** We don't demo Claude Code features. We solve someone's actual problem using Claude Code. The tool is invisible. The solution is the star.

2. **Time to value under 1 hour.** Every episode should go from "I have this problem" to "holy shit it works" in under 60 minutes. If it takes longer, the problem is too big or we're overbuilding.

3. **The non-technical person leads.** Eric drives product requirements, asks "dumb" questions, represents the audience. Yaohong explains what's happening technically and why it matters. The audience should see themselves in Eric, not Yaohong.

4. **Show the failures.** The Gemini failure was more educational than the Claude success. Debugging, wrong turns, and "that didn't work" moments are the content. Polished demos are boring. Messy builds are relatable.

5. **Always eval.** Compare models, compare approaches. Make a table. This is the one habit that separates "vibing" from actually building something that works.

6. **Enhance work, don't remove it.** The positioning isn't "AI replaces your job." It's "AI does work nobody would ever do" — like sorting through 10,000 photos. The friend was never going to do that manually. This isn't automation replacing labor. This is unlocking value that didn't exist before.

7. **Capture, don't build.** When the customer starts riffing on ideas ("what about Spotify Wrapped for photos?"), write it down, don't build it. The roadmap comes from the conversation. The build comes later.

8. **ICP: "From my mum to pastors to doctors."** Everyday people. White-collar workers. The vast majority of the world who will never write a line of code but who have problems worth solving.
