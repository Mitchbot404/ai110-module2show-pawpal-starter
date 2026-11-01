# Six-phase walkthrough and evidence

The detailed course instructions supplied in chat are the source for this map.

## Phase 1 — System design and UML

Read docs/design.md and diagrams/uml_draft.mmd. Three actions: add a pet,
schedule a task, and view/complete today's tasks. Owner manages Pets, each Pet
contains Tasks, and Scheduler retrieves associations through Owner.all_tasks().
A readable skeleton is in docs/class_skeletons.py.txt; the live implementation is
pawpal_system.py.

Explain: Why does Scheduler receive an Owner rather than separate copies of
every pet's tasks? Why does each dataclass list use default_factory?

**Workflow difference:** The first baseline was built before the detailed rubric
arrived. The assignment-aligned draft and learning skeleton were then saved
during revision. There was no earlier skeleton-only commit; do not claim one.

## Phase 2 — Core implementation and CLI

Read Task, Pet, Owner, then Scheduler in pawpal_system.py. Run python main.py.
The demo constructs two pets and four deliberately unsorted tasks. The Task
completion and Pet task-addition tests are in tests/test_pawpal.py.

Explain: How does a task's stable ID differ from its description? Why does the
CLI receive the same backend classes as the browser UI?

## Phase 3 — UI/backend integration

Read app.py. The Owner lives in st.session_state.owner. Add-pet and add-task forms
call Owner.add_pet() and Pet.add_task(). Reruns retain the owner and its nested
pets/tasks. Editing uses Pet.update_task() with validation before replacement.

Try: add two pets, assign a task to each, change a filter, and check that tasks
remain. Explain why creating a fresh Owner on every rerun would lose the data.

## Phase 4 — Algorithmic layer

Trace sort_by_time(), filter_tasks(), mark_task_complete(), and detect_conflicts().
Validated HH:MM strings sort chronologically within a date. Filtering uses
optional pet/status/date criteria. Recurrence creates a new occurrence after the
later of due date and completion date. Warnings compare pending time intervals.

Try: overlapping tasks for different pets, tasks touching at an endpoint, and a
daily completion. Explain why duplicate-start-only detection misses partial overlap.

sort_by_priority() is optional Challenge 3. It orders priority before date/time;
it changes the view, not the appointments.

## Phase 5 — Testing and verification

Read docs/test-plan.md. Run python -m pytest. Explain one recurrence test, one
conflict test, and the difference between their happy paths and edge cases.
Read docs/verification.md for actual results and limits.

## Phase 6 — Final UI, UML, documentation, reflection

The UI exposes all required algorithms. Compare diagrams/uml_final.mmd to the
classes and methods in pawpal_system.py. Follow the README demo and write your
personal answers in reflection.md using actual observations.

**Chat-session difference:** Work was organized using files, explicit updates,
and test plans inside one continuing chat. Separate phase chats were not used.
Discuss that actual experience rather than claiming the course's suggested
separate-chat workflow occurred.

See docs/submission-checklist.md for the remaining GitHub and reflection steps.
