# PawPal+ Project Reflection

*Draft prepared with Codex assistance from this project's recorded work, my
stated design choices, and my browser checks. I will review the wording before
submission, particularly the personal takeaways and confidence rating.*

## 1. System Design

### 1a. Initial design

The three main actions are adding a pet, scheduling or editing its care tasks,
and viewing today's schedule with completion controls and conflict warnings.

The assignment-aligned design uses four classes. Owner stores multiple pets.
Pet holds identifying information and a list of tasks. Task represents one
scheduled occurrence, including its description, time, date, frequency, duration,
priority, and completion status. Scheduler retrieves tasks from the Owner's pets
and handles sorting, filtering, recurrence, and conflicts.

The Owner–Pet–Task relationship reflects how someone would organize care in real
life: one owner can have several pets, and each pet has its own activities.
Keeping scheduling logic separate from the interface also lets the terminal
demo and Streamlit app use the same backend.

### 1b. Design changes

The first AI-generated baseline focused on one pet and a time-budget plan.
After I supplied the detailed phase instructions, the implementation changed to
support multiple pets, explicit clock times, task completion, and recurring
occurrences. The backend became pawpal_system.py, using the required Task class.
Stable task IDs distinguish activities with identical descriptions.

My own design decision came from trying the conflict workflow. I chose to keep
warnings instead of having the app automatically move appointments. I proposed
adding suggested free times so the owner could choose a fix without changing
other pets' schedules. That suggestion feature is a future improvement, not
part of the current implementation.

The workflow did not follow the assignment's suggested order exactly: the first
baseline existed before the full instructions arrived. The later skeleton is a
learning reference, not evidence of an earlier skeleton-only commit.

## 2. Scheduling Logic and Tradeoffs

### 2a. Constraints and priorities

The scheduler considers each task's date, time, duration, pet, and completion
status. It can show tasks chronologically or filter them by pet and status.
The optional priority view puts high-priority tasks first, then orders by date
and time. It changes the display order without changing appointment times.

Conflict detection matters because one owner may need to care for different pets
at the same time. A task's duration matters as well as its starting time: tasks
starting at 08:00 and 08:05 could still overlap. Completing a daily or weekly
task creates its next occurrence while keeping the completed one as history.

### 2b. Tradeoffs

I would keep the warning and let the owner choose what to change. Automatic
rescheduling might remove a conflict but move a task to a time the owner did
not intend. The tradeoff is that the owner must take an extra step to fix it.

My preferred improvement is a quick-fix list of suggested times. Each suggestion
should fit the full duration around pending tasks for all pets, and applying
one should move only the selected task. This would reduce manual effort while
preserving the owner's control.

The current conflict algorithm compares overlapping intervals and can take
O(n²) time. That is reasonable for a small household schedule. An exact-start-only
check would be simpler but would miss tasks that overlap despite starting at
different times.

## 3. AI Collaboration

### 3a. How I used AI

This was my first official experience using Work mode. Codex helped inspect the
starter, draft the design and UML, edit the Python files, connect the interface,
create tests, run the demo, and organize the documentation. I supplied the
assignment details, created my GitHub fork, ran the app, and gave feedback on
the behavior I wanted.

Work mode helped produce a complete project structure and documented its
limitations. One limitation that stood out was that session memory preserves
data during interaction but does not permanently save pets and tasks between
application runs.

We used one continuing chat rather than separate chats for each phase. This
kept the files, troubleshooting, and design discussion together, although the
conversation became long. The phase guide and checklists provided structure.
Because I did not try separate phase chats, I cannot compare the two approaches
from experience.

### 3b. Judgment and verification

When the assistant asked whether I wanted warnings or automatic rescheduling,
I chose warnings. I modified the proposed direction by asking for suggested
alternative times that would not interfere with existing appointments for the
same or different pets. The owner should choose the change.

I tested conflict detection by changing Luna's Medication from 08:00 to 08:15.
The conflict warning disappeared, confirming that the app recognized the
updated schedule. As a future improvement, I would add suggested available
times so the owner could resolve conflicts more easily without affecting other
scheduled tasks.

I also encountered a startup issue: Streamlit was waiting for input at an
optional email prompt. Pressing Enter without entering an email allowed the app
to start. That experience showed why looking at the actual terminal state is
useful when troubleshooting.

## 4. Testing and Verification

### 4a. What was tested

Codex ran the automated suite, which finished with 44 passing cases. These cover
adding tasks, task completion, multiple pets, sorting, filtering, daily and weekly
recurrence, repeated completion, date boundaries, invalid inputs, conflicts, and
Streamlit session behavior.

For example, the recurrence test completes a daily task and checks that the
original is marked complete and a new pending occurrence is added for the next
day with a different ID. It then completes the original again and checks that
another copy is not created. This detects a bug that could duplicate tasks when
the same action is repeated.

My browser check complemented the automated results: I saw the cross-pet
conflict and confirmed that moving Medication cleared it. Checking both the
warning and its removal helps catch stale or incorrectly calculated warnings.

### 4b. Confidence

Based on the documented test results and my conflict-resolution check, I would
rate this version 4 out of 5. The backend has 100% statement coverage, but that
does not mean every possible input or user interaction has been verified.

I would next test saved data and suggested free times if those features were
added. Important cases include preserving dates and completion status after
loading, finding a slot that fits a task's full duration, and handling a day with
no available slot. A suggestion should also avoid tasks that cross midnight.

## 5. Reflection

### 5a. What went well

A useful result was seeing the conflict workflow operate in the browser. The
warning identified tasks belonging to different pets, and it cleared after I
changed the time. That gave me something concrete to evaluate beyond reading
code or seeing a test summary.

The project also brought the UML, Python classes, terminal demo, interface, and
tests into one structure. The written walkthrough made it easier to connect
the assignment requirements to specific files and behaviors.

### 5b. What I would improve

In another iteration, I would add a save-and-load feature. A pet owner should
be able to reopen the app without entering everything again. I would test that
dates, completion status, and recurring tasks survive saving and loading.

I would also add quick-fix suggestions for conflicts. Each suggested time should
fit the task's full duration without overlapping another pet's tasks or moving
any existing appointments. The owner would choose whether to apply a suggestion.

### 5c. Key takeaway

AI can make changes quickly, but I still need to provide the requirements,
try the result, and decide whether its behavior makes sense. The first baseline
needed revision once the detailed instructions were available, which shows why
working code alone does not establish that an assignment is complete.

My decision about conflict handling is an example of that responsibility:
I want help finding a free time while keeping control over which appointment
moves. Being the lead architect means making those choices and checking the
result, even when AI writes much of the implementation.
