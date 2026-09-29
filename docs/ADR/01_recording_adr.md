## Architecture Decision Record (ADR)
## Recording protocol for labelled CSI dataset

### This document is resposible for a decision I made that explains, Why? where should i use? what follows from it?

## Status
Accepted, 29-09-2026

## Context
M2 needs a labelled dataset to detect the binary presence. The CSI is board sensitive detects(furnitures, fan oscillation and window movements.....) and witout fixed placements, the model could learn the side effects instead of human presence. 

## Decision
- **Labels:** represents the choices of a person is (in or not) inside a room.
- **Activity:** describes what the person does?
- **Duration:** to describe how mauch time does the script should record the data
- **Session:** one recording sitting under unchanged conditions. Defaults tothe date; a suffix is added if recording twice in a day.
- **Train/test split:** by session, never by row. Neighbouring rows are nearly identical, so a random row split would leak test data into training.
- **Hardware placement:** B1 (sender) and B2 (receiver) at 2m distance.
- **Target size:** at least 30 captures per class across at least 3 different days.
  
## Consequences
- Labelling is simple and reliable (per file, no timestamps needed).
- Evaluation reflects generalisation to a new day, not memorised conditions.
- Moving the boards or changing the room invalidates comparability; any
  change must be noted in `--note` and the lab notebook.
- Finer classes (activity, location) are possible later without re-recording,
  since activity is already stored.
- The step-by-step procedure lives in `docs/protocol.md`.



