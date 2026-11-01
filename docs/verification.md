# Verification record

Verified November 1, 2026, on Windows using Python 3.14.2, Streamlit 1.66.1,
pytest 9.2.0, and pytest-cov 7.1.0.

## CLI demonstration

Ran .venv/Scripts/python.exe main.py successfully. The CLI created two pets and
four tasks, printed chronological and filtered schedules, warned about the two
08:00 tasks, demonstrated priority ordering, completed Breakfast, and created
its November 3 successor. Full actual output appears in README.md.

## Required standard test run

Command: .venv/Scripts/python.exe -m pytest

```text
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.2.0, pluggy-1.7.0
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.16.0, cov-7.1.0
collected 44 items

tests\test_app.py ....                                                   [  9%]
tests\test_pawpal.py ........................................            [100%]

============================= 44 passed in 3.68s ==============================
```

The machine-specific root directory line is omitted.

## Coverage run

Command: .venv/Scripts/python.exe -m pytest --cov=pawpal_system --cov=app --cov=main --cov-report=term-missing -q

```text
Name               Stmts   Miss  Cover   Missing
------------------------------------------------
app.py                99      2    98%   24-25
main.py               39     22    44%   24-27, 32-48, 52
pawpal_system.py     147      0   100%
------------------------------------------------
TOTAL                285     24    92%
44 passed in 4.37s
```

There are 40 backend cases, including parameterized cases, and 4 UI integration
tests. The latter drive the real app through Streamlit AppTest, including forms,
reruns, table contents, warnings, state, editing, deletion, and recurrence.

The UI test runner requires local sockets and used the approved execution
environment. The tests allow 15 seconds per app run for initial dependency loads.

## Student browser check

The student supplied before-and-after screenshots of the running app. The first
shows Mochi's Breakfast and Luna's Medication both at 08:00 with a conflict
warning. The second shows Medication at 08:15 and the no-pending-conflicts
confirmation while the table is filtered to Luna. This provides manual evidence
for displaying a cross-pet warning and clearing it after a manual time edit.

## Limits

Coverage measures executed statements, not proof of correctness. The Owner rename
success path was not exercised by the UI tests. CLI printing was verified by the
separate main.py run rather than the automated coverage run. The student browser
check above covers one conflict-resolution flow; a full accessibility audit
was not performed. Permanent storage, free-time suggestions, and reminders are
outside the current implementation.
