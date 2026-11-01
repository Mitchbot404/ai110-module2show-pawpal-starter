# Review against the supplied grading rubric

Reviewed November 1, 2026, using the two rubric screenshots supplied by the
student. This is an evidence map, not an instructor's grade.

## Required features: 20 points

| Rubric category | Points | Evidence | Status |
| --- | --- | --- | --- |
| Clear OOP UML | 4 | `diagrams/uml_final.mmd`: Owner, Pet, Task, Scheduler; attributes, methods, and ownership relationships match the backend | Supported |
| Core class implementation | 4 | `pawpal_system.py`: Task completion; Pet task management; Owner pet collection; Scheduler operating across pets | Supported |
| Two meaningful algorithms | 3 | Chronological and priority sorting, pet/status/date filtering, recurring occurrences, and duration conflict warnings across pets | Supported |
| End-to-end CLI demo | 3 | `main.py` creates one owner, two pets, and four tasks; uses Scheduler; actual readable CLI output in README | Supported |
| Basic pytest suite | 3 | `tests/test_pawpal.py` and `tests/test_app.py`; final recorded result: 44 passing tests | Supported |
| Documentation and AI reflection | 3 | README includes architecture, algorithms, run/test instructions, coverage summary, and passing test output; reflection includes factual design and verification notes | README criteria supported; personal reflection unfinished |

The remaining core submission gap is the student's reflection: the file still
contains personal prompts. Complete the account of accepted/rejected suggestions
and verification with actual experience before submitting. Do not count the
assistant's decisions as evidence of the student's own review.

## Stretch features: up to 10 points

| Feature | Points | Evidence and remaining work |
| --- | --- | --- |
| Advanced algorithm via agent mode | +2 | More than two algorithms exist, and `ai_interactions.md` has an Agent Workflow section. Whether the additional algorithms meet the rubric's advanced-capability threshold is for the grader; no separate advanced-extension credit is assumed. Student manual corrections remain to be recorded if any occurred. |
| Data persistence | +2 | Not implemented. Session state preserves widget reruns but does not save between application runs. |
| Advanced scheduling | +2 | `Scheduler.sort_by_priority()` sorts by priority, then date/time; tested and demonstrated in the README CLI output. |
| Professional UI/output formatting | +2 | `main.print_schedule()` uses aligned columns; Streamlit tables, warning/success messages, and emoji status labels are documented in the README Output formatting section. |
| Model or prompt comparison | +2 | Not performed. No structured comparison is claimed. |

The priority and formatting categories have direct implementation and README
evidence. Do not claim persistence, a prompt comparison, or a guaranteed score.
