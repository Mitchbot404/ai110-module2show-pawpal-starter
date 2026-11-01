# PawPal+ — AI110 Project 2

PawPal+ helps one owner manage care tasks across multiple pets. The Streamlit UI
and terminal demo use the same four-class Python backend.

## Features

- Add multiple pets and create, edit, or delete their tasks.
- Schedule dated tasks with a clock time, duration, frequency, priority, and status.
- View tasks in chronological order; filter by pet, date, or completion status.
- Complete tasks and automatically create the next daily or weekly occurrence.
- See warnings for simultaneous or overlapping pending tasks, across all pets.
- Switch to priority-first ordering (optional Challenge 3).
- Keep completed occurrences as history throughout the current session.

## Setup and run

Use Python 3.10 or later. From this project folder in Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The environment is already installed on this computer. Use the last command to
launch the app. If the Microsoft Store opens for `python`, use an installed
Python executable or `py` to create the environment. On macOS/Linux, substitute
`.venv/bin/python` for `.venv\Scripts\python.exe`.

## System design

The required logic layer is `pawpal_system.py`:

| Class | Responsibility |
| --- | --- |
| `Owner` | Store pets; add/find pets; expose all pet-task associations |
| `Pet` | Store pet details; add/find/edit/delete its task occurrences |
| `Task` | Validate task details, track completion, create a recurrence successor |
| `Scheduler` | Retrieve, filter, sort, complete, and check tasks across pets |

`Owner.pets` and `Pet.tasks` use separate lists for each instance. All four
classes are dataclasses. Task IDs let the UI distinguish repeated descriptions.
The UI stores the Owner in `st.session_state.owner`, preserving the entire
object graph across widget reruns.

Mermaid sources: [draft UML](diagrams/uml_draft.mmd) and
[final UML](diagrams/uml_final.mmd). See [design notes](docs/design.md),
[phase walkthrough](docs/phase-guide.md), and the
[learning skeleton](docs/class_skeletons.py.txt).

## Smarter Scheduling

| Feature | Method | Behavior and cost |
| --- | --- | --- |
| Chronological sorting | `Scheduler.sort_by_time()` | Sort by date, then validated HH:MM; O(n log n) |
| Filtering | `Scheduler.filter_tasks()` | Combine pet name, completion status, and exact date; O(n) |
| Completion and recurrence | `Scheduler.mark_task_complete()`, `Task.mark_complete()` | Retain completed occurrence and attach a new daily/weekly task |
| Conflict warnings | `Scheduler.detect_conflicts()` | Check overlapping pending intervals, including across pets and midnight; O(n²) worst case |
| Priority ordering | `Scheduler.sort_by_priority()` | High before medium before low, then date/time; O(n log n) |

A daily recurrence is scheduled one day after the later of its due date and
completion date; weekly recurrence uses seven days. Clock time and other details
are preserved. Repeated completion does not create duplicates. Overdue completion
creates a future occurrence rather than a backlog. Recurrence is triggered by
completion, not a timer. Use the Scheduler method to complete an attached task:
`Task.mark_complete()` alone returns a successor but cannot attach it to a pet.

Conflict intervals are half-open: 08:00–08:15 and 08:15–08:30 do not overlap.
Completed tasks do not block time. Warnings never silently move appointments.
A selected day's warnings include overlapping tasks from the previous night.
All pets' warnings remain visible even when the table is filtered to one pet.

## Demo Walkthrough

1. Launch Streamlit. Save your owner name, then add two pets. Alternatively, click
   **Load example pets and tasks** while the pet list is empty.
2. Choose **Pet for task**. Fill in a description, clock time, due date, duration,
   frequency, and priority. Click **Add task**.
3. The schedule updates immediately. Choose a date and filter by pet or status.
   The default ordering is chronological.
4. With the example loaded, Breakfast and Medication both start at 08:00.
   Read the warning identifying both tasks and pets.
5. Select Luna's Medication in the editor, move its time to 08:15, and save.
   The warning disappears; Breakfast ends at 08:10.
6. Select a daily task and click **Mark complete**. The completed occurrence stays
   in history; a success message identifies the next occurrence.
7. Select tomorrow's date to see the new task. Use **Completed** on the original
   date to see history. Delete or edit pending tasks using the same editor.
8. Select **Priority, then time** to see the optional priority ordering.

### Sample Output

Actual output from `main.py` (November 2, 2026 is a fixed demo date; the UI uses
the current date). Tasks are deliberately added out of order.

```text
Today's Schedule — 2026-11-02 (fixed demo date)
Time   Pet      Task             Min  Priority  Status
08:00  Mochi    Breakfast         10  medium    pending
08:00  Luna     Medication         5  high      pending
09:00  Mochi    Morning walk      30  high      pending
18:00  Luna     Grooming          15  low       pending

Pending tasks for Mochi
Time   Pet      Task             Min  Priority  Status
08:00  Mochi    Breakfast         10  medium    pending
09:00  Mochi    Morning walk      30  high      pending

Conflict warnings
Conflict: Mochi — Breakfast (2026-11-02 08:00) overlaps Luna — Medication (2026-11-02 08:00).

Priority-first view
Time   Pet      Task             Min  Priority  Status
08:00  Luna     Medication         5  high      pending
09:00  Mochi    Morning walk      30  high      pending
08:00  Mochi    Breakfast         10  medium    pending
18:00  Luna     Grooming          15  low       pending

Completed: Mochi — Breakfast
Next daily occurrence: 2026-11-03 08:00
Pending on demo date: 3
Completed on demo date: 1
```

## Output formatting

The terminal demo uses `main.print_schedule()` with Python f-string field widths
to align time, pet, task, duration, priority, and status columns. Section labels
separate the chronological schedule, filtered results, conflict warnings, and
priority view; the sample output above shows the actual result.

The browser UI in `app.py` uses Streamlit's `st.table()` for structured schedules,
`st.warning()` for conflicts, `st.success()` for confirmations, and `st.info()`
for empty results. Status cells use ✅ Complete and ⏳ Pending, so status remains
readable without relying on color. These formatting features use Python and
Streamlit; no additional formatting library is required.

## Testing PawPal+

With the environment activated, run:

```powershell
python -m pytest
python -m pytest --cov=pawpal_system --cov=app --cov=main --cov-report=term-missing
```

Without activation use `.\.venv\Scripts\python.exe` in place of `python`.
The suite checks completion, adding tasks, multiple pets, sorting, filters,
daily/weekly recurrence, duplicate completion, date boundaries, invalid data,
same-pet and cross-pet conflicts, duration overlap, and Streamlit session memory.
See [test plan](docs/test-plan.md) and [verification record](docs/verification.md).

Actual coverage run:

```text
............................................                             [100%]
Name               Stmts   Miss  Cover   Missing
------------------------------------------------
app.py                99      2    98%   24-25
main.py               39     22    44%   24-27, 32-48, 52
pawpal_system.py     147      0   100%
------------------------------------------------
TOTAL                285     24    92%
44 passed in 4.37s
```

**Confidence Level: ★★★★☆ (4/5, engineering assessment).** Required backend
behaviors and UI workflows pass; the CLI was also run separately. Coverage of
the CLI print functions is lower because the automated UI suite imports the demo
factory without executing `main()`. Coverage does not prove correctness, and a
visual browser review and the student's own walkthrough are still useful.

Standard test-run result from `python -m pytest`:

```text
collected 44 items
tests\test_app.py ....                                                   [  9%]
tests\test_pawpal.py ........................................            [100%]
============================= 44 passed in 3.68s ==============================
```

## Scope and submission

Times are local, without timezone or daylight-saving conversion. There is no
permanent storage, login, reminder service, automatic conflict resolution, or
time-budget optimizer. Scheduling is explicit by date/time. The optional priority
view changes display order; it does not move task times. Completed occurrences
cannot be edited, preserving history; deleting a task affects only that occurrence.

Personal reflection prompts are in [reflection.md](reflection.md).
The AI assistance and actual design correction are recorded in
[ai_interactions.md](ai_interactions.md). The workflow differed from the course
sequence: a first baseline existed before the detailed six-phase instructions
arrived. No earlier skeleton-only commit or separate phase chats were fabricated.
Fork/push status and remaining steps are in [submission checklist](docs/submission-checklist.md).
See the [grading rubric review](docs/rubric-review.md) for required and bonus evidence.
