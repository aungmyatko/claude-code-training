# IT PMO Kanban Board (Demo)

An IT PMO Kanban board demo for a fictitious bank, built as a single file of vanilla HTML, CSS and JavaScript.

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](index.html)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)](index.html)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](index.html)
![No dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![Zero build](https://img.shields.io/badge/build-zero-brightgreen)
[![Deploy to GitHub Pages](https://github.com/aungmyatko/claude-code-training/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/aungmyatko/claude-code-training/actions/workflows/deploy-pages.yml)
[![CI](https://github.com/aungmyatko/claude-code-training/actions/workflows/ci.yml/badge.svg)](https://github.com/aungmyatko/claude-code-training/actions/workflows/ci.yml)
[![Live demo](https://img.shields.io/badge/demo-live-0a66c2)](https://aungmyatko.github.io/claude-code-training/)

## Live demo

**<https://aungmyatko.github.io/claude-code-training/>**

## Features

- **Four status columns:** Backlog, In Progress, Blocked and Done, with per-column counts and a live summary in the header.
- **Add Task form with validation:** title, project, category, priority, assignee and due date. Errors show inline next to each field. Each new task gets an ID in the format `UOB-ITPM-####`.
- **Move tasks** with a per-card "Move to…" menu (keyboard friendly) or by native drag and drop between columns.
- **Inline delete confirmation:** "Delete? Yes / No" on the card. There are no browser pop-ups.
- **Filters** by project, assignee (contains) and priority, plus a "Clear filters" button.
- **Overdue highlighting:** cards past their due date that aren't Done are flagged.
- **Optional email notification** for new tasks through [FormSubmit](https://formsubmit.co/). A failed notification only shows a warning toast and never breaks the board.

## Installation

```bash
git clone https://github.com/aungmyatko/claude-code-training.git
cd claude-code-training
```

There's nothing to install. You don't need Node, npm or any packages.

## How to run

**Quick:** open `index.html` in a browser. It works straight from disk (`file://`).

**Local server** (needed for FormSubmit email, because FormSubmit rejects `file://` origins):

```bash
python -m http.server 8000
```

Then open <http://localhost:8000>.

## Configuration

Email notifications are off until you set the destination address. The only place it's set is the `FORMSUBMIT_ENDPOINT` constant at the top of the `<script>` block in `index.html`:

```js
const FORMSUBMIT_ENDPOINT = "https://formsubmit.co/ajax/YOUR_EMAIL@example.com";
```

1. Replace `YOUR_EMAIL@example.com` with your address.
2. Serve the page over http (see above) and add a task.
3. FormSubmit sends a **one-time activation email** to that address. Click the link in it, and later submissions are delivered. Email subjects start with `[UOB IT PMO]`.

> **Do not commit a real email address to a public repository.** It would be published on the GitHub Pages site. Keep the placeholder here, and set a real address only in a local copy or a private fork.

## Notes

- **No persistence, by design.** Tasks live in memory only. Refreshing the page resets the board to the seed data, and the page shows a note saying so.
- Seed due dates are relative to today, so some cards are always overdue.
- All names, projects and tasks are **fictitious demo data**. This project isn't affiliated with, endorsed by or connected to any real bank. It uses a neutral "IT PMO" wordmark and no real logos or systems.

## Deployment / CI-CD

Two GitHub Actions workflows live in `.github/workflows/`:

- **`ci.yml`** runs on every push and pull request with read-only permissions. It has three jobs:
  - HTML validation (`html-validate@8`, configured in `.htmlvalidate.json`).
  - A full-history secret scan with Gitleaks.
  - A constraints check that fails if `index.html` uses `localStorage`, `sessionStorage`, `indexedDB`, `document.cookie`, `alert(`, `confirm(`, `!important`, `<script src=` or `type="module"`.
- **`deploy-pages.yml`** runs on every push to `main` and on manual dispatch. It runs CI first, so a failing check blocks the deploy. It then copies **only `index.html`** into the Pages artifact and deploys it to GitHub Pages.

## Project structure

```text
.
├── index.html                  # The whole app: markup, <style> and <script>
├── README.md
├── CLAUDE.md                   # Guidance for Claude Code
├── .gitignore
├── .htmlvalidate.json          # html-validate config used by CI
└── .github/
    └── workflows/
        ├── ci.yml              # Validation, secret scan, constraints check
        └── deploy-pages.yml    # CI + deploy index.html to GitHub Pages
```
