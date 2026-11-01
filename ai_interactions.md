# AI Interactions Log

## Agent Workflow

**Tool:** Codex. One continuing chat; no separate phase chats, independent agents,
or multi-model comparison.

**Actual request:** The user asked for help completing all six phases of AI110
Project 2, supplied CodePath's starter repository, then supplied the detailed
phase instructions. The user then created a personal fork under Mitchbot404 and
provided its URL. The assistant redirected the local origin, pushed the verified
implementation, and checked the uploaded backend file through GitHub.

**Files modified:** pawpal_system.py, main.py, app.py, tests/test_pawpal.py,
tests/test_app.py, diagrams/uml_draft.mmd, diagrams/uml_final.mmd, README.md,
reflection.md, requirements.txt, pytest.ini, .gitignore, this log, and docs/.
The earlier generated pawpal.py and its scheduler tests were replaced.

**What the assistant completed:** Inspected and cloned the starter, drafted UML
and a first baseline, revised the system to the required four-class multi-pet
architecture, added a deterministic CLI demo, wired Streamlit session state,
implemented sorting/filtering/recurrence/conflict warnings, and added and ran
automated tests. Optional Challenge 3 priority ordering was implemented and
demonstrated in the CLI. The README records actual output.

**Correction during review:** The first baseline used a single-pet, time-budget
planner. The detailed assignment required clock-time scheduling, multiple pets,
completion status, and successor occurrences. The assistant replaced that design
and updated the tests rather than retaining an incompatible backend.

**Algorithm evaluation:** Duplicate-start detection was considered as a simpler
alternative. Interval overlap checks were retained because different start times
can still overlap. Sorted pairs allow early stopping once later tasks start
after the current task ends. This keeps the implementation readable for small
household schedules; worst-case work remains O(n²).

**Verification:** The CLI ran successfully and the final suite passed all 44
cases. Backend statement coverage was 100%; app coverage 98%. Total coverage
including CLI printing was 92%. The first baseline's Streamlit test startup
timeout was increased from 3 to 15 seconds. Local socket access was required
for the approved UI test execution.

**Workflow differences:** The detailed rubric arrived after the first baseline.
The assignment-aligned skeleton was saved as a learning reference during revision;
no earlier skeleton-only commit was fabricated. The phase tasks were handled in
one chat, so no separate-chat experience is claimed.

**Student reflection choice:** The student selected the session-memory
limitation as a point that stood out and chose save-and-load functionality as a
future improvement. Their proposed tests would check that dates, completion
status, and recurring tasks survive saving and loading. These responses were
added to reflection.md; persistence has not been implemented.

**Student manual verification:** Not yet recorded. Add what you actually
verified, modified, or rejected and explain your reasoning. Selecting a future
improvement is not a claim of having run tests or rejected an AI suggestion.

## Optional extensions

Implemented: Challenge 3, priority-first then date/time ordering, documented with
CLI output in the README. Structured CLI tables and UI status labels were also
used. JSON persistence and a multi-model comparison were not attempted.
