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

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
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



