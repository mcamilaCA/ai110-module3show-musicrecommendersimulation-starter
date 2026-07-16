# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

The agent helped expand the dataset and update the functions to implement relevant new features

**Prompts used:**

Act as a data expert and help me introduce 5 complex attributes to the dataset ( @data/songs.csv ) that are not currently present, such as Song Popularity (0-100), Release Decade, or Detailed Mood Tags (e.g., "nostalgic," "aggressive," "euphoric"). Then, help me update @src/recommender.py  to have in mind the new data when scoring songs

**What did the agent generate or change?**

The agent editted: src/recommender.py and songs.csv.
Changes made:
- UserProfile incorporated new fields
- _score_core now has instrumentalness and release_decade as new weighted dimensions (each weighting 0.10)
- explicit_content acts as pre-scoring filter and popularity is used alongside danceability as tiebreaker

**What did you verify or fix manually?**

I double checked all the code and updated the profiles in main.py to verify output match as well - and apply modifications as needed. 

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
