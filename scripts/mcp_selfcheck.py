#!/usr/bin/env python
"""Probe whether the live agent<->notebook bridge is ready.

This does NOT depend on Claude Code's MCP layer, so it works in the SAME
session that just wrote `.mcp.json` (Claude Code only loads MCP servers at
startup). The `course-setup` skill runs this via Bash to verify the
infrastructure before telling you to restart Claude Code for the real
end-to-end MCP round-trip.

Four checks, each with a pass/fail line and a fix hint:
  (a) `uvx jupyter-mcp-server` resolves (and warms the uvx cache)
  (b) the RTC extension `jupyter_collaboration` is installed AND enabled
  (c) JupyterLab is reachable at JUPYTER_URL using JUPYTER_TOKEN
  (d) the `geo-graph` kernelspec is registered

Reads JUPYTER_URL / JUPYTER_TOKEN from the environment, falling back to a
`.env.local` file in the repo root if present. Exits non-zero on any failure.

Usage:
    uv run python scripts/mcp_selfcheck.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

MCP_PIN = "jupyter-mcp-server@1.0.2"
DEFAULT_URL = "http://localhost:8888"


def load_env_local() -> None:
    """Populate os.environ from .env.local (does not override real env vars)."""
    env_file = Path(__file__).resolve().parent.parent / ".env.local"
    if not env_file.exists():
        return
    for raw in env_file.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _run(cmd: list[str], timeout: int = 180) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        return proc.returncode, (proc.stdout + proc.stderr)
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s: {' '.join(cmd)}"


def check_uvx() -> tuple[bool, str]:
    code, out = _run(["uvx", MCP_PIN, "--help"])
    if code == 0:
        return True, "uvx can resolve & run jupyter-mcp-server (cache warmed)"
    if code == 127:
        return False, "`uvx` not found — install uv (see SETUP.md), it ships with uv"
    return False, (
        f"`uvx {MCP_PIN} --help` failed (exit {code}). "
        "Check your network; first run downloads the package."
    )


def check_rtc() -> tuple[bool, str]:
    code, out = _run(["jupyter", "server", "extension", "list"])
    if code != 0:
        return False, (
            "could not run `jupyter server extension list` — is jupyterlab "
            "installed in this env? Run `uv sync --extra local`."
        )
    low = out.lower()
    if "jupyter_collaboration" not in low:
        return False, (
            "jupyter_collaboration (RTC) is NOT installed — the agent and you "
            "would collide on saves. Run `uv sync --extra local`."
        )
    # The extension lists a line like "jupyter_collaboration ... enabled"
    enabled = any(
        "jupyter_collaboration" in ln.lower() and "enabled" in ln.lower()
        for ln in out.splitlines()
    )
    if not enabled:
        return False, (
            "jupyter_collaboration is installed but DISABLED. Enable with "
            "`uv run jupyter server extension enable jupyter_collaboration`."
        )
    return True, "RTC extension jupyter_collaboration is installed and enabled"


def check_lab_reachable() -> tuple[bool, str]:
    url = os.environ.get("JUPYTER_URL", DEFAULT_URL).rstrip("/")
    token = os.environ.get("JUPYTER_TOKEN", "")
    if not token:
        return False, (
            "JUPYTER_TOKEN is not set. The setup skill writes it to .env.local "
            "and exports it; ensure it is in your shell before launching Claude Code."
        )
    req = urllib.request.Request(
        f"{url}/api/status",
        headers={"Authorization": f"token {token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                return True, f"JupyterLab reachable at {url} with the token"
            return False, f"{url}/api/status returned HTTP {resp.status}"
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            return False, (
                f"auth rejected at {url} (HTTP {exc.code}) — JUPYTER_TOKEN does "
                "not match the token JupyterLab was launched with."
            )
        return False, f"{url}/api/status HTTP error {exc.code}"
    except urllib.error.URLError as exc:
        return False, (
            f"cannot reach {url} ({exc.reason}). Is `jupyter lab` running on "
            "that port? Check for a port clash or a firewall."
        )


def check_kernelspec() -> tuple[bool, str]:
    code, out = _run(["jupyter", "kernelspec", "list"])
    if code != 0:
        return False, "could not run `jupyter kernelspec list`"
    if "geo-graph" in out:
        return True, "the `geo-graph` kernel is registered"
    return False, (
        "the `geo-graph` kernel is not registered. Run: `uv run python -m "
        "ipykernel install --user --name geo-graph --display-name \"Geo-Graph (uv)\"`"
    )


CHECKS = [
    ("uvx / jupyter-mcp-server", check_uvx),
    ("RTC (jupyter_collaboration)", check_rtc),
    ("JupyterLab reachable", check_lab_reachable),
    ("geo-graph kernelspec", check_kernelspec),
]


def main() -> int:
    load_env_local()
    print("MCP bridge self-check\n" + "-" * 60)
    all_ok = True
    for label, fn in CHECKS:
        ok, msg = fn()
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {label}: {msg}")
        all_ok = all_ok and ok
    print("-" * 60)
    if all_ok:
        print(
            "All checks passed. Restart Claude Code so it loads .mcp.json, "
            "approve the `jupyter` server on first use, then ask the agent to "
            "verify the bridge (it will insert + run a test cell)."
        )
        return 0
    print(
        "One or more checks failed — fix the items marked FAIL above, then "
        "re-run this self-check. See unit-1-graph-substrate/KNOWN_ISSUES.md."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
