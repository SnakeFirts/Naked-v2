```
                                              __
                                             / _)
                                      .-^^^-/ /
                                   __/       /
                                  <__.|_|-|_|

     _   _    _    _  _______ ____
    | \ | |  / \  | |/ / ____|  _ \
    |  \| | / _ \ | ' /|  _| | | | |
    | |\  |/ ___ \| . \| |___| |_| |
    |_| \_/_/   \_\_|\_\_____|____/
```

> Username correlation and identity research framework.

NAKED is an OSINT tool for username intelligence: given a single
username, it queries multiple providers concurrently and returns not
just *whether* an account exists, but how confident you should be
about it.

---

## Why NAKED

Most username-checking tools give you a binary answer:

```
[+] github.com/snakefirts        FOUND
[-] tiktok.com/@snakefirts        NOT FOUND
```

That's not enough for real research. "Not found" and "I couldn't
verify this" are two completely different things, and conflating them
produces false negatives. NAKED treats them as such:

```
github
------------------------------
status        : FOUND
naked score   : 100/100

reasons
  + Official API
  + Username exact match
  + Public profile
  + Profile URL verified

reddit
------------------------------
status        : ERROR
error         : Reddit returned 403 (suspended, private, or blocked)
```

Every result carries a `status` (`FOUND` / `NOT_FOUND` / `ERROR`) and,
when found, a NAKED Score with the reasons behind it -- not just a
number pulled out of nowhere.

---

## Architecture

```
naked/
|
|-- core/                  engine, plugin loader, cache, logging
|
|-- intelligence/          scoring engine
|     |-- score.py           ScoreCalculator
|     '-- rules.py           per-provider scoring rules
|
|-- models/                pydantic models (SearchResult, profiles, score)
|
|-- providers/             one folder per source
|     |-- github/
|     |-- reddit/
|     '-- examples/dummy/
|
'-- main.py                CLI entrypoint (typer)
```

Providers are auto-discovered: drop a folder under `providers/` with a
`provider.py` that defines a `Provider` subclass, and the
`PluginManager` picks it up at runtime. No manual registration needed.

### Result lifecycle

```
                +------------------+
   username --> |  Provider.search |
                +------------------+
                         |
            +------------+------------+
            |            |            |
          200          404        429 / 5xx / timeout
            |            |            |
            v            v            v
        FOUND       NOT_FOUND       ERROR
            |
            v
     ScoreCalculator
            |
            v
     IntelligenceScore
```

Errors (rate limits, timeouts, ambiguous blocks) never get silently
turned into "not found." They're surfaced as `ERROR` with a reason, so
you always know what NAKED actually verified versus what it couldn't.

---

## Installation

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/SnakeFirts/NAKED.git
cd NAKED
uv sync
```

## Usage

```bash
uv run python main.py <username>
```

```bash
uv run python main.py --help
```

---

## Providers

| Provider | Source                          | Auth required |
|----------|----------------------------------|----------------|
| github   | api.github.com (official API)    | No             |
| reddit   | reddit.com/user/<x>/about.json   | No             |

More providers are added incrementally; see `naked/providers/` for the
plugin interface.

## Scoring

Each provider defines its own rules in `naked/intelligence/rules.py`.
Points are awarded for things like using an official API, an exact
username match, a public profile, or a verified account -- and the
total is capped at 100. The calculator lives independently from the
providers, so scoring logic can evolve without touching provider code.

---

## Testing

```bash
uv run pytest tests/ -v
```

Tests cover scoring logic and error classification (including mocked
rate-limit and ambiguous-block scenarios) without depending on live
network calls.

---

## Roadmap

```
[x] Plugin-based provider architecture
[x] GitHub provider
[x] Reddit provider
[x] Intelligence scoring engine
[x] FOUND / NOT_FOUND / ERROR result classification
[x] CLI with username argument
[ ] Additional providers (scraping-based)
[ ] Cross-provider correlation / overall identity score
[ ] Rich-formatted terminal output
```

---

## License

TBD.
