# PawPal+ Project Reflection

This document contains verified project facts and clearly marked personal
prompts. Complete the personal responses after running and reviewing the app.

## 1. System Design

### 1a. Initial design

**Three core user actions:** add a pet, schedule or edit its care tasks, and view
a sorted daily schedule with completion controls and conflict warnings.

**Assignment-aligned design:** Owner stores multiple Pets and exposes all their
task associations. Pet stores identity and its task list. Task stores the
description, time, frequency, date, duration, priority, and completion status.
Scheduler receives the Owner and handles filtering, ordering, completion, and
warnings. All four classes are dataclasses.

**Your response:** Explain why you agree with these responsibilities and which
relationship in the draft UML helped you understand the system.

### 1b. Design changes

The first AI-generated baseline supported one pet per plan and used a time-budget
selection algorithm. Once the detailed assignment arrived, the implementation
was revised to Owner–Pets–Tasks, scheduled clock times, completion history, and
completion-triggered recurrence. The backend was renamed to pawpal_system.py,
and the Task class replaced CareTask. Stable IDs were added so identical task
descriptions and recurring occurrences can be edited independently.

**Your response:** Describe a specific decision you personally reviewed or
changed. Do not describe the later learning skeleton as an earlier commit.

## 2. Scheduling Logic and Tradeoffs

### 2a. Constraints and priorities

The scheduler sorts by exact date and HH:MM time, filters by pet/status/date,
and detects conflicts using pending task durations. An optional priority view
orders high before medium before low, then date/time. Completion creates the
next daily or weekly occurrence, retaining the original as history.

**Your response:** Explain which of these behaviors matters most for your
example pet owner and why.

### 2b. Tradeoffs

Interval comparisons detect partial overlaps that an exact-start-time check
would miss. The pairwise implementation can take O(n²) time, a reasonable cost
for a small household schedule; a more complex index could help at larger scale.
Warnings let the owner decide what to reschedule. They do not automatically move
time-sensitive appointments. Late recurring-task completion creates one future
occurrence rather than generating every missed occurrence.

**Your response:** Choose one tradeoff and defend or revise it with an example.

## 3. AI Collaboration

### 3a. How AI was used

Codex inspected the starter, drafted designs, edited multiple project files,
implemented the models and UI, generated tests, ran the CLI and pytest, and
prepared documentation. The user supplied the detailed phase instructions after
the first baseline; these instructions exposed the gaps in that baseline.

All work in this chat used one continuing conversation, organized with files and
progress updates. Separate phase chats and a multi-model comparison were not used.

**My experience with AI assistance:** Work mode helped produce a complete
project structure and documented its limitations. One limitation that stood out
to me was that session memory keeps data during interaction but does not
permanently save pets and tasks between application runs.

**Still to reflect on:** Did maintaining one chat help or make it harder to
track the phases? Explain your actual experience.

### 3b. Judgment and verification

A concrete correction was replacing the first AI design's single-pet/time-budget
behavior with the course's multi-pet/time-based task model. The final tests verify
observable behavior, including automatic recurrence and duplicate-time warnings.

**Your response:** Identify a suggestion you personally rejected or modified,
why, and the evidence you used. If you have not done that yet, review the
recurrence and conflict policies and make an actual decision before answering.
The assistant's revisions alone are not evidence of your personal judgment.

## 4. Testing and Verification

### 4a. What was tested

The final suite has 44 passing cases covering ownership, completion, sorting,
filters, daily/weekly recurrence, repeated completion, date boundaries, invalid
inputs, overlap warnings, and Streamlit UI/session integration. Core Task
completion and Pet task-addition tests are included. See docs/test-plan.md and
docs/verification.md for details.

**Your response:** Explain one test's inputs, expected result, and the bug it
would detect. Why is that behavior important?

### 4b. Confidence

The documented engineering assessment is 4/5 based on tests and the CLI demo.
The backend has 100% statement coverage, but this does not prove every possible
behavior. Browser visual/accessibility checks, permanent storage, and reminders
were outside this implementation.

**Your response:** Give your own 1–5 rating after reviewing the results, and name
one edge case or next feature you would test.

## 5. Reflection

### 5a. What went well

**Your response:** What are you most satisfied with, and what did you observe
when you ran it?

### 5b. What to improve

In another iteration, I would add a save-and-load feature. A pet owner should
be able to reopen the app without entering everything again. I would also test
that dates, completion status, and recurring tasks survive saving and loading.

### 5c. Key takeaway

**Your response:** What did you learn about being the lead architect when AI
can edit many files quickly? Support your answer with an actual project decision.
