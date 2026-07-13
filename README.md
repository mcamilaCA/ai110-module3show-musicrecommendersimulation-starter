# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

The system aims to recommend songs to user's based on their preferences & likings. For each song, details like genre, mood, energy and acousticness are translated into a score with the end goal of achieving a high compatibililty with a user's profile, the higher the score, the more likely a song is to be liked by the user.

For this, user statistics will be used to define: favorite mood, their most frequently listened energy levels and whether or not they like acoustic music. 

Instead of using thresholds, recommender calculates distance-based rewards prioritizing answering "how close is this feature to what the user wants to hear?". Once each weighted score is calculated, a ranking of all songs scores is computed to decide which songs are the ones with higher likelihood to be liked by the user and they are returned. If there is a tie of songs with the same score, danceability preferences are used to determine the one to be given to the user.

This being said, the weights that will be used for each attribute are:
1. genre: 35%
2. mood: 30%
3. energy: 20%
4. acousticness: 15% 

As seen by the weigthts above, the system has a bias for genre and mood - since it assumes every user gives a higher priority to genre than to mood or any of the other atributes. In an ideal system, it might ask for users preference, update the weights accordingly and store that data internally.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
``` 
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
======================================================================
🎵  YOUR TOP SONG RECOMMENDATIONS  🎵
======================================================================
👤 Profile: genre=pop | mood=happy | energy=0.8 | accousticness=0.2
======================================================================

🥇 #1  Sunrise City — Neon Echo
   ⭐ Score: 94.8/100
   🎸 Genre   ✅ match (pop vs pop): +35.0 pts
   🎭 Mood    ✅ match (happy vs happy): +30.0 pts
   ⚡ Energy  similarity 0.98 (song 0.82 vs target 0.80): +19.6 pts
   🎻 Acoustic similarity 0.68 (song 0.18 vs target 0.50): +10.2 pts
----------------------------------------------------------------------
🥈 #2  Rooftop Lights — Indigo Parade
   ⭐ Score: 61.9/100
   🎸 Genre   ❌ no match (indie pop vs pop): +0.0 pts
   🎭 Mood    ✅ match (happy vs happy): +30.0 pts
   ⚡ Energy  similarity 0.96 (song 0.76 vs target 0.80): +19.2 pts
   🎻 Acoustic similarity 0.85 (song 0.35 vs target 0.50): +12.8 pts
----------------------------------------------------------------------
🥉 #3  Gym Hero — Max Pulse
   ⭐ Score: 60.7/100
   🎸 Genre   ✅ match (pop vs pop): +35.0 pts
   🎭 Mood    ❌ no match (intense vs happy): +0.0 pts
   ⚡ Energy  similarity 0.87 (song 0.93 vs target 0.80): +17.4 pts
   🎻 Acoustic similarity 0.55 (song 0.05 vs target 0.50): +8.2 pts
----------------------------------------------------------------------
🎶 #4  Night Drive Loop — Neon Echo
   ⭐ Score: 29.8/100
   🎸 Genre   ❌ no match (synthwave vs pop): +0.0 pts
   🎭 Mood    ❌ no match (moody vs happy): +0.0 pts
   ⚡ Energy  similarity 0.95 (song 0.75 vs target 0.80): +19.0 pts
   🎻 Acoustic similarity 0.72 (song 0.22 vs target 0.50): +10.8 pts
----------------------------------------------------------------------
🎶 #5  Island Drift — Solar Tide
   ⭐ Score: 29.5/100
   🎸 Genre   ❌ no match (reggae vs pop): +0.0 pts
   🎭 Mood    ❌ no match (carefree vs happy): +0.0 pts
   ⚡ Energy  similarity 0.80 (song 0.60 vs target 0.80): +16.0 pts
   🎻 Acoustic similarity 0.90 (song 0.40 vs target 0.50): +13.5 pts
----------------------------------------------------------------------

🎧 Enjoy the music!

```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



