---
name: course-setup
description: One-time environment setup for a student of the Geospatial Graph Learning course. Use when the student says "make full setup", "set up my environment", "get jupyter running", "install the course", "/setup", or otherwise asks to get up and running on a unit. Installs unit dependencies with uv, registers a Jupyter kernel, smoke-tests the stack, and (recommended, local only) installs + tests the live agent↔notebook bridge so the agent can write and run cells while the student watches.
---

# Course setup

Your job: take a student from a fresh fork/clone to a working, kernel-ready,
smoke-tested Jupyter, with the **minimum manual steps**. Narrate what you do.
Read-only checks you run yourself; **state-changing commands you confirm once**
before running. Cross-platform: macOS, Windows (PowerShell), Linux.

This is a **recommendation, not a forced path** — ask the student how they want
to run and adapt. Nothing you set up here is a precondition for doing the course;
it just makes the practice hour smoother.

## Step 0 — ask how they want to run

> "Will you run **locally** (recommended for repeat work — persistent env, your
> own files) or on **Colab** (zero install, resets each session)? And do you want
> the **live agent-driven notebook** bridge, where I write and run cells while you
> watch and talk to me? (local only)"

Branch on the answer.

## Colab branch (zero local install)

Nothing to install. Tell the student:
- Open any demo notebook via its **"Open in Colab"** badge; the first cell runs
  `setup_colab.py` and installs that unit's deps.
- To keep edits, `File → Save a copy in GitHub` into their fork (see `SETUP.md`).
- For the practice hour, they talk to you and you hand them cells to paste/run —
  you cannot drive Colab directly. (That's the `practice-tutor` Colab mode.)

Stop here for Colab — there is no kernel/MCP to install.

## Local branch

Pick the unit (default **unit-1**; infer from the cwd if they're inside a
`unit-N-*` folder). Then:

### 1. Preflight (read-only — run without asking)
- Confirm repo root: `pyproject.toml` exists here.
- `uv --version` — if missing, show the platform install command from `SETUP.md`
  (§4) and ask the student to run it (don't pipe-to-shell for them).
- `node --version` (≥18) and `claude --version` — usually already true.

### 2. Install dependencies (confirm once — large download, mutates `.venv/`)
Run, with `<N>` = the unit:
```bash
uv sync --extra unit-<N> --extra local
```
`--extra local` adds the JupyterLab + RTC stack used by the bridge. Offer
`--extra all --extra local` if they want every unit.

> **CRITICAL — every `uv run` AFTER this sync must carry `--no-sync`.** A bare
> `uv run …` re-syncs the env to the *default* extras (none) first, which
> **uninstalls the unit + local libs you just installed**. So steps 3–5 below
> all use `uv run --no-sync …`. (Equivalently, repeat the full
> `--extra unit-<N> --extra local` list on every `uv run` — but `--no-sync` is
> shorter and can't drift out of step with step 2.)

### 3. Register a named kernel (idempotent — run after sync)
```bash
uv run --no-sync python -m ipykernel install --user \
  --name geo-graph --display-name "Geo-Graph (uv)"
```
So any Jupyter / VS Code sees the synced env as a selectable kernel.

### 4. Smoke-test the stack (run it — read-only w.r.t. notebooks)
```bash
uv run --no-sync python scripts/smoke.py --unit <N>
```
This imports every library the unit needs and applies version gates **without
touching the demo notebook**. On failure, surface the exact failed import and
point at `unit-<N>-*/KNOWN_ISSUES.md`. Do not proceed to the bridge until smoke
passes. (If smoke fails with `ModuleNotFoundError` for libs you just installed,
a stray bare `uv run` resynced the env down — re-run step 2, then keep
`--no-sync` on every command.)

### 5. Offer + install + TEST the live agent↔notebook bridge (recommended)

Only if the student said yes in Step 0. This is the part that lets you write and
run cells while they watch in the browser. Because **Claude Code loads MCP
servers at startup**, a freshly written config is not callable in this session —
so verify in **two phases** and tell the student exactly when to restart.

**Phase A — install + infrastructure test (this session, all via Bash):**
1. Warm the server package (first run downloads ~1–2 min):
   ```bash
   uvx jupyter-mcp-server@1.0.2 --help
   ```
2. Generate a token, write the gitignored `.env.local`, and launch JupyterLab
   (RTC on) in the background:
   ```bash
   uv run --no-sync python scripts/start_lab.py --launch
   ```
   Run this with `run_in_background: true`. Capture the printed
   `http://localhost:8888/lab?token=…` URL and give it to the student to open.
3. Tell the student to load the token into the shell **where Claude Code runs**:
   ```bash
   set -a; source .env.local; set +a     # macOS / Linux
   # Windows PowerShell: see the lines start_lab.py printed
   ```
4. Run the real install test (it loads `.env.local` itself):
   ```bash
   uv run --no-sync python scripts/mcp_selfcheck.py
   ```
   This checks: uvx resolves, RTC enabled, lab reachable with the token, and the
   `geo-graph` kernel exists. If any check FAILs, **stop** and walk the student
   through that specific fix (token mismatch, port in use, RTC not enabled,
   firewall) before continuing. Re-run until all four pass.
5. Confirm `.mcp.json` is present at the repo root (it is committed).

**Phase B — true MCP round-trip (after the student restarts Claude Code):**
Tell the student, in these words:
> "Now **restart Claude Code** so it loads `.mcp.json`, make sure `JUPYTER_TOKEN`
> is in that shell, **approve the `jupyter` server** when prompted, then say
> *'verify the jupyter bridge'*."

When they come back, check whether the `jupyter` MCP tools are available
(`list_notebooks` etc.). If not, they didn't restart / approve / export the
token — re-point them at Phase B. When the tools ARE available, run the
end-to-end test yourself:
1. `list_notebooks`.
2. Create/open `unit-<N>-*/student-work/working.ipynb` (this is inside
   `student-work/`, which is the student's space — allowed to create).
3. `insert_cell` a one-liner like `print("bridge ok", 1 + 1)`.
4. `execute_code` / run it, then `read_cell` the output.
5. Confirm with the student that the cell **appeared and ran live in their
   browser** and that there was **no "File Changed" prompt** (RTC autosave).

On success: "The bridge is ready — when you want to work, say *let's work on the
practice of unit <N>* and I'll drive the notebook while you direct."

### 6. Report
Summarize: deps synced, kernel registered, smoke passed, bridge status. For any
failure, link the relevant `KNOWN_ISSUES.md` entry. Remind them of the two launch
options if they skip the bridge: `uv run --extra unit-<N> jupyter lab`, or VS
Code + the "Geo-Graph (uv)" kernel.

## Guardrails
- Confirm before any state-changing command (`uv sync`, installing tools,
  `ipykernel install`, launching lab). Read-only checks run freely.
- Never edit upstream files. The only thing you create is inside `student-work/`.
- Don't commit anything. `.env.local` is gitignored — never print its contents
  back into a committed file.
