from rich.console import Console
from rich.text import Text

from naked.models.search_result import ResultStatus, SearchResult
from naked.models.search_session import SearchSession
from naked.models.profiles.github import GithubProfile
from naked.models.profiles.reddit import RedditProfile

console = Console()

SNAKE = """\
\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800
\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u28c0\u28ff\u28ff\u28ff\u28c4\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800
\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2820\u28c4\u28f6\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28d7\u28c4\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800
\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2820\u28b4\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u2846\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800
\u2800\u2800\u2800\u28b0\u2846\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2820\u28b4\u28ff\u28ff\u28ff\u28ff\u28bf\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u2847\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800
\u2800\u2800\u2800\u289f\u2882\u2846\u2800\u2800\u2800\u2800\u2800\u28a1\u28ff\u28ff\u28ff\u28bf\u2818\u2801\u28b6\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28f7\u28c6\u28c0\u28c0\u28c0\u2800\u2800\u2800\u2800\u2800
\u2800\u2800\u289e\u28c0\u28f6\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28bf\u2800\u2800\u2800\u28a0\u28b4\u289f\u2882\u2846\u2800\u2800\u2800\u2808\u28ff\u2882\u28ff\u28ff\u28ff\u2800\u2800\u2809\u2809\u2809\u2873\u2846\u2800\u2800
\u2800\u2800\u28ff\u28ff\u28ff\u28ff\u28ff\u28bf\u2882\u28ff\u28ff\u28ff\u28ff\u2803\u2800\u2800\u28a1\u289e\u2801\u2800\u2800\u289b\u2862\u2846\u2800\u2800\u2800\u2800\u28ff\u28ff\u28ff\u2800\u2800\u2820\u2846\u2800\u2800\u2819\u2846\u2800
\u2800\u2820\u28ff\u288b\u2800\u2819\u288b\u2801\u2882\u28ff\u28ff\u28ff\u28ff\u2846\u2800\u28b4\u2801\u2800\u2800\u2800\u2800\u2800\u2800\u2808\u28d7\u2846\u2800\u2800\u28ff\u28ff\u28ff\u2800\u2800\u2800\u28ff\u2800\u2800\u2800\u28b9\u2800
\u2800\u28b8\u2809\u2800\u28c0\u28c0\u28c0\u2846\u2882\u28ff\u28ff\u28ff\u28ff\u2883\u280c\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2808\u2847\u2800\u2800\u28ff\u28ff\u288f\u2846\u2800\u2800\u2882\u2847\u28a4\u2800\u2800\u2846
\u2800\u2803\u2800\u28bc\u2801\u2800\u2800\u2801\u2808\u28ff\u28ff\u28ff\u28ef\u288e\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2847\u2800\u2882\u28ff\u28ff\u2830\u28ff\u2846\u2800\u2882\u28ff\u28ff\u2800\u2800\u2847
\u28c0\u28bf\u2819\u2801\u2800\u2800\u2800\u2800\u2800\u2818\u28ff\u28ff\u28ff\u2847\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u28b0\u28a7\u2846\u2818\u28bf\u28ff\u2846\u2819\u2800\u2820\u28bf\u28ff\u28ff\u28f7\u2820\u2847
\u2801\u2800\u2800\u2800\u2800\u2800\u28a4\u28c0\u2800\u28c7\u28b8\u28ff\u28ff\u28a7\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2820\u2819\u28a6\u28bc\u28ff\u28ff\u2846\u2820\u28bc\u28ff\u28ff\u28ff\u28a7\u28be\u2803
\u2800\u2800\u2800\u2800\u2800\u2800\u28b9\u28ff\u28d7\u28be\u2846\u2882\u28ff\u28ff\u28a0\u28a6\u2800\u2800\u2800\u2800\u2800\u2800\u2820\u2800\u2824\u28be\u28ff\u28a6\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u280f\u2800
\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2882\u28ff\u28eb\u289f\u2800\u2882\u28ff\u28ff\u28ff\u2800\u2800\u2800\u2800\u2820\u2820\u28c0\u28c4\u28a4\u28ed\u2819\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28bf\u2803\u2800\u2800
\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2882\u28ba\u2800\u2800\u2800\u2882\u28ff\u288b\u28ff\u2847\u2800\u2800\u28a0\u28bf\u289f\u28ff\u28bf\u2819\u2882\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u288b\u2801\u2800\u2800\u2800\u2800
\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2803\u2800\u2800\u2800\u2800\u2800\u2818\u28ff\u2800\u2800\u2808\u2800\u2800\u28b0\u280f\u2800\u2820\u28ff\u28ff\u280f\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800
\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2882\u28a6\u2800\u2800\u2800\u2820\u288b\u2800\u2800\u28bc\u28ff\u28d7\u289e\u2801\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800
\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u28a7\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2809\u28bc\u288b\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800
\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2818\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2820\u2803\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800
\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2801\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800\u2800"""

NAKED_TEXT = """\
             _            _ 
            | |          | |
 _ __   __ _| | _____  __| |
| '_ \\ / _` | |/ / _ \\/ _` |
| | | | (_| |   <  __/ (_| |
|_| |_|\\__,_|_|\\_\\___|\\_,_|"""


def _header() -> None:
    snake_lines = SNAKE.splitlines()
    naked_lines = NAKED_TEXT.splitlines()

    # Pad snake lines to consistent width before placing naked text beside it
    snake_width = max(len(l) for l in snake_lines)

    # naked text starts at line 6 (0-indexed) to align with mid-body
    naked_start = 6

    for i, line in enumerate(snake_lines):
        naked_idx = i - naked_start
        if 0 <= naked_idx < len(naked_lines):
            suffix = "  " + naked_lines[naked_idx]
        else:
            suffix = ""
        t = Text()
        t.append(line.ljust(snake_width), style="color(208)")
        t.append(suffix, style="bold white")
        console.print(t)


def _divider() -> None:
    console.print("─" * 44, style="dim")


def _render_result(result: SearchResult) -> None:
    _divider()

    # Provider name
    console.print(result.provider.upper(), style="bold green")

    # Status
    if result.status.value == "found":
        console.print("✓ FOUND", style="bold green")
    elif result.status.value == "not_found":
        console.print("✗ NOT FOUND", style="dim")
    else:
        console.print("! ERROR", style="bold red")
        if result.error:
            console.print(f"  {result.error}", style="red")
        return

    # Score
    if result.score:
        console.print(
            f"Score: {result.score.score}/100",
            style="bold color(208)",
        )

        console.print("\nEvidence", style="dim")
        for ev in result.score.evidences:
            if ev.passed:
                console.print(
                    f"  ✓ {ev.description} (+{ev.points})",
                    style="green",
                )
            else:
                console.print(
                    f"  ✗ {ev.description}",
                    style="dim",
                )

    # Profile fields
    if result.profile:
        console.print()
        p = result.profile

        if isinstance(p, GithubProfile):
            if p.repositories is not None:
                console.print(f"Repositories : {p.repositories}")
            if p.followers is not None:
                console.print(f"Followers    : {p.followers}")

        elif isinstance(p, RedditProfile):
            if p.karma_post is not None:
                console.print(f"Post karma   : {p.karma_post}")
            if p.karma_comment is not None:
                console.print(f"Comment karma: {p.karma_comment}")

    if result.url:
        console.print(result.url, style="blue underline")


def render_session(session: SearchSession) -> None:
    console.print()
    _header()
    console.print()
    console.print(f"Searching: {session.username}", style="bold")

    for result in session.results:
        _render_result(result)

    _divider()
    console.print(
        f"Completed in {session.duration_ms} ms",
        style="dim",
    )
    console.print()
