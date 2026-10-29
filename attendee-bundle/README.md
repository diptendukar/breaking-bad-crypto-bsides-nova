# Breaking Bad Crypto — hands-on labs

Welcome. This repo is seven small, deliberately broken systems. In the workshop
you will attack each one from a starter script, get a flag, then watch a one-line
fix kill your own exploit.

## Setup (do this before the workshop)

```bash
pip install -r requirements.txt
python labcheck.py        #  ->  ALL CHECKS PASSED
```

Python 3.9+ and any OS. If `labcheck.py` is not green, message the instructor in
the workshop Slack channel before the day.

## How a lab works

The challenge **servers run on the instructor's laptop**, on the room network.
You do not run the servers. For each lab you:

1. Open the lab's `challenge/` folder and read its short `README.md`.
2. Open `challenge/client.py` — the plumbing is written; one piece is missing (a `TODO`).
   (The `ecb-penguin` lab is a demo you run yourself, `ecb_penguin.py`, not a client — just follow its README.)
3. Fill in the `TODO`, run it against the instructor's server, and get your `flag{...}`.
4. Stuck? `hints.md` unlocks progressively. Raise a hand — someone is roaming.

You will be told each lab's server address and port on the day
(`http://<instructor-ip>:<port>`).

## The seven labs (in order)

| # | Folder | What you break |
|---|--------|----------------|
| 0 | `ecb-penguin` | See through "encrypted" images (demo — watch this one) |
| 1 | `cbc-bit-flip` | Turn `role=user` into `role=root` with no key |
| 2 | `ecdsa-nonce-reuse` | Steal a signing key from two signatures (the Sony PS3 bug) |
| 3 | `jwt-alg-confusion` | Forge an admin JWT with `alg=none` |
| 4 | `lcg-prediction` | Predict the next "random" password-reset token |
| 5 | `signature-forgery-missing-check` | A signature that validates for any message |
| 6 | `cbc-padding-oracle` | Read a secret one byte at a time from a yes/no answer |

## The takeaway

`checklist.md` is the whole workshop on one page: six questions you can run
against any codebase. The crypto was never the problem — the code around it was.

*No solvers are in this repo during the class. They are published here after the workshop.*
