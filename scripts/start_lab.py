#!/usr/bin/env python
"""Prepare (and optionally launch) JupyterLab for the agent<->notebook bridge.

What it does:
  1. Reuses or generates a stable JupyterLab token.
  2. Writes it to a gitignored `.env.local` (JUPYTER_TOKEN, JUPYTER_URL) so the
     committed `.mcp.json` can interpolate it and `mcp_selfcheck.py` can read it.
  3. Prints the one line you must run in your shell (export) and the exact
     `jupyter lab` command — or, with --launch, starts JupyterLab itself
     (RTC on by default via jupyter-collaboration).

The `course-setup` skill calls this with --launch in the background. You can
also run it by hand.

Usage:
    uv run python scripts/start_lab.py            # write env + print commands
    uv run python scripts/start_lab.py --launch   # also start jupyter lab
    uv run python scripts/start_lab.py --port 8889
"""
from __future__ import annotations

import argparse
import os
import secrets
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = REPO_ROOT / ".env.local"


def read_env_local() -> dict[str, str]:
    out: dict[str, str] = {}
    if ENV_FILE.exists():
        for raw in ENV_FILE.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def write_env_local(values: dict[str, str]) -> None:
    lines = [
        "# Local-only secrets for the agent<->notebook bridge. NOT committed.",
        "# Re-source after editing:  set -a; source .env.local; set +a",
    ]
    for key, value in values.items():
        lines.append(f"{key}={value}")
    ENV_FILE.write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8888)
    parser.add_argument(
        "--launch", action="store_true", help="start jupyter lab now"
    )
    args = parser.parse_args()

    existing = read_env_local()
    token = existing.get("JUPYTER_TOKEN") or secrets.token_hex(24)
    url = f"http://localhost:{args.port}"

    write_env_local({"JUPYTER_TOKEN": token, "JUPYTER_URL": url})
    print(f"Wrote {ENV_FILE.relative_to(REPO_ROOT)} (gitignored).")
    print()
    print("In the shell where you run Claude Code, load these env vars:")
    print("  set -a; source .env.local; set +a       # macOS / Linux")
    print('  # Windows PowerShell: $env:JUPYTER_TOKEN="%s"; $env:JUPYTER_URL="%s"'
          % (token, url))
    print()
    # `--no-sync`: a bare `uv run` would re-sync to the default (no-extra) env
    # first, uninstalling the `local` extra (JupyterLab + jupyter-collaboration
    # RTC) that the bridge depends on. Keep the env exactly as `uv sync
    # --extra unit-<N> --extra local` left it.
    launch_cmd = (
        f"uv run --no-sync jupyter lab --port {args.port} "
        f"--IdentityProvider.token {token} --no-browser"
    )
    print("Launch JupyterLab (RTC enabled via jupyter-collaboration) with:")
    print(f"  {launch_cmd}")
    print(f"Then open: {url}/lab?token={token}")

    if args.launch:
        print("\nLaunching JupyterLab now...\n", flush=True)
        os.environ["JUPYTER_TOKEN"] = token
        os.environ["JUPYTER_URL"] = url
        # Replace this process with jupyter lab so background managers can
        # track it directly.
        os.execvp(
            "uv",
            [
                "uv", "run", "--no-sync", "jupyter", "lab",
                "--port", str(args.port),
                "--IdentityProvider.token", token,
                "--no-browser",
            ],
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
