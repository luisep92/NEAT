# NEAT — grid-maze RL with NeuroEvolution

A weekend RL experiment: train a tiny neural network with **NEAT** (NeuroEvolution of Augmenting Topologies) to navigate a 10×10 grid maze in pygame. Walls force a detour, the agent has to learn it.

It worked partway. The place where it stopped working is, honestly, the most interesting part of the project.

---

## What you'll see

Two pygame demos and a baseline:

- **`test.py`** — manual play with arrow keys, the no-NEAT baseline you can poke at to feel the maze.
- **`neat_train.py`** — trains a population of 50 genomes for 50 generations and saves the best one.
- **`replay.py`** — loads the best agent and runs it in pygame at 10 fps. A 10×10 grid with a blue square (player), a yellow square (goal), and white walls. On a win, the screen flashes green.

The agent observes seven features (position + goal + delta + Manhattan distance, all normalised) and picks one of four actions (up / down / left / right).

## Why I built it

I'd been watching [Argonaut Code's RL videos](https://www.youtube.com/@argonautcode) and wanted the under-the-hood understanding that watching alone doesn't give. NEAT is a good entry point because the algorithm is conceptually clean (genome = network, fitness drives selection, structural mutations grow the topology over time) and the library [`neat-python`](https://github.com/CodeReclaimers/neat-python) handles the heavy lifting — leaving you to focus on the environment, the observation, and the reward.

The longer-term ambition was to point the same approach at **Hollow Knight: Silksong**. That didn't materialise — see [What came next](#what-came-next).

## Run it

Tested on Python 3.10+.

```bash
pip install neat-python pygame
cd pygame/

# Train: creates neat-config.ini and best-genome.pkl. ~50 generations.
python neat_train.py

# Replay the best agent in pygame
python replay.py

# Or play manually with arrow keys (no NEAT)
python test.py
```

`neat_train.py` writes `neat-config.ini` on first run if it isn't there, so a clean clone trains out of the box.

## The wall I hit

The maze starts the player top-left and puts the goal bottom-right, with two horizontal walls offset on rows 2 and 4 — wall on `[2][0..4]` blocks the left half of row 2, wall on `[4][6..9]` blocks the right half of row 4. To get from start to goal the agent has to zigzag: right past the first wall, down, left past the second, down again, right again to the goal. **It has to move away from the goal at multiple points.**

The reward is shaped by Manhattan distance: every step that increases distance is a small negative. That's exactly the wrong signal for this maze. Every necessary detour-step looks locally bad, and selection pressure favours genomes that find the easy half of the maze and stall against a wall. The agent gets close to the goal as long as the path is convex, then stops.

The fixes are well known — sparser rewards (only the `+5` on win, no per-step shaping), curiosity-driven bonuses, or a richer observation that includes nearby walls so the agent can learn local geometry — but I parked the project here. The point of the weekend was to *feel* why naive shaping fails on non-convex paths, and at that point I had felt it.

---

## Stack

Python 3.10+ · [neat-python](https://github.com/CodeReclaimers/neat-python) (NEAT implementation) · pygame (rendering) · pickle (genome serialisation)

## How it's structured

All sources are under `pygame/` — the directory name is a leftover and slightly confusing; everything inside *uses* pygame, it isn't pygame itself.

- `MyGame.py` — `Map` and `Cell` classes. 10×10 grid with hardcoded walls; render via pygame primitives.
- `env.py` — `SimpleGridEnv` with the standard `reset` / `step` / observation interface NEAT expects. 7-D observation (position, goal, delta, Manhattan distance, all normalised). Reward shaping detailed in [The wall I hit](#the-wall-i-hit).
- `neat_train.py` — NEAT config (50 population, structural mutation enabled, sigmoid activations) and the genome evaluator (3 episodes per genome, averaged). Saves the best genome to `best-genome.pkl`.
- `replay.py` — loads `best-genome.pkl` and runs the agent in pygame at 10 fps.
- `test.py` — manual-play baseline. Useful for sanity-checking the maze itself before reasoning about why training fails.
- `Colors.py` — palette constants.

## What came next

The original ambition was to scale this up to **Hollow Knight: Silksong** — get an agent to play it. That specific goal didn't happen, but reverse-engineering the game's runtime to figure out how an agent might even *interact* with it ended up producing two BepInEx mods that did ship: [**QuickWarp**](https://github.com/luisep92/QuickWarp) (~3.5k Nexus downloads) and [**UnlockAllTools**](https://github.com/luisep92/UnlockAllTools) (~10k). Side projects compound in directions you don't predict.

## License

[MIT](LICENSE).
