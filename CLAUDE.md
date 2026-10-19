# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A training/demo IT PMO Kanban board for a fictitious bank. The entire app is one file, `index.html`, with all markup, a `<style>` block and a `<script>` block. There is no build, no package manager, no tests and no linter.

## Hard constraints (from the original spec — keep them)

- Vanilla HTML/CSS/JS only: no frameworks, libraries, CDNs, web fonts or image files. Use the system font stack and inline SVG/Unicode for icons.
- Must keep working when opened directly from disk (`file://`). Don't introduce ES modules, `fetch` of local files, or anything else that needs a server.
- **No persistence.** No localStorage, sessionStorage, IndexedDB or cookies. Every refresh resets to the seed data. This is intended, and the page shows a note saying so.
- Branding: neutral "IT PMO" text wordmark, corporate blue palette. Never use or imitate a real bank's logo or systems. The `UOB-ITPM-####` ID format and the `[UOB IT PMO]` email subject prefix were explicitly requested.
- No `alert()` / `confirm()`. Errors show inline and deletes are confirmed with an inline "Delete? Yes / No".
- No `!important`. Colours and spacing come from the CSS custom properties on `:root`.

## Running

- Quick check: open `index.html` in a browser.
- To exercise FormSubmit email delivery, serve it over http, because FormSubmit rejects `file://` origins:

```bash
python -m http.server 8000
```

## Architecture (script block)

- **Single source of truth.** Everything lives in `state = { tasks, filters, ui }`.
  - `ui` holds transient per-card UI state: `openMoveId`, `pendingDeleteId`, `draggingId`.
  - The flow is always: change `state` → call `renderBoard()`.
  - Card markup is built only in `renderCard()` and inserted only by `renderBoard()`. Don't touch card DOM directly anywhere else.
- **Focus after re-render.** `renderBoard(focusSelector)` re-renders all columns and the header summary (`renderSummary()`), then focuses the element matching `focusSelector`. Use this to keep keyboard focus after any re-render.
- **Reference data.** `STATUSES`, `PROJECTS`, `CATEGORIES` and `PRIORITIES` drive the columns, the `<select>` options (filled in `init()` via `fillSelect`) and validation. Change them there, not in markup.
- **Actions.** `addTask()`, `moveTask()` and `deleteTask()` are the only functions that modify `state.tasks`.
  - Board clicks are handled by one delegated listener (`handleBoardClick`) that dispatches on `data-action` attributes.
  - Drag-and-drop uses delegated native HTML5 DnD handlers on `#board`.
- **IDs.** Generated from the `nextIdNumber` counter via `formatId()`. The seed data uses IDs 0001–0008.
- **Dates.** Dates are local `YYYY-MM-DD` strings from `isoDate()` / `todayISO()`, so they're compared as plain strings. Don't use `toISOString()` for dates: it converts to UTC and can shift the day. Seed due dates are relative to today, so some cards are always overdue.
- **Escaping.** Every user-supplied value inserted into HTML must go through `escapeHtml()`.
- **Add Task form.**
  - `handleSubmit` runs `validateTask()`, which returns a `{field: message}` map shown with `setFieldError`.
  - On success it adds the task optimistically, then awaits `notifyNewTask()` inside try/catch.
  - A notification failure only shows a warning toast. It must never break the board.
- **FormSubmit.** The `FORMSUBMIT_ENDPOINT` constant at the top of the script is the only place the destination email is set. It is a placeholder by default. Activation is one-time: the first submission emails a confirmation link.
  - `notifyNewTask()` treats as failures: a non-OK HTTP status, a JSON body with `success: "false"`, or a 10 s timeout.
