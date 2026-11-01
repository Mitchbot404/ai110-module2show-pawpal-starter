# System design and review

## Three core user actions

1. Add a pet under the owner's account.
2. Schedule or edit a dated care task for a selected pet.
3. View a sorted daily schedule, see conflicts, and complete tasks.

## Assignment-aligned building blocks

An Owner holds a list of Pets; a Pet holds a list of Tasks. Scheduler receives an
Owner in its constructor and retrieves associations through Owner.all_tasks().
Returning (pet, task) pairs preserves identity when task descriptions repeat.

Task stores description, HH:MM time, frequency, due date, duration, priority,
completion status, and a stable ID. Computed start/end datetimes support interval
checks. The final UML documents these methods and relationships.

## Review of missing relationships and bottlenecks

The first AI baseline had one pet per generated plan and did not implement the
course's Owner–Pets–Tasks hierarchy. Reviewing the supplied assignment identified
the missing multi-pet ownership, occurrence completion, and recurrence creation.
The replacement uses four required classes; plan-result helper classes were
removed because dated occurrences already provide the needed schedule data.

For small household schedules, explicit conflict comparisons are readable and
sufficient. Sorting allows early stopping after later tasks no longer overlap.
The worst case is O(n²), including O(n²) output if every task overlaps every
other task. A sweep-line index would add complexity for little benefit here.

## Algorithm evaluation

Sorting by a validated date and zero-padded HH:MM string is clearer than manually
parsing times in the sorting key. For conflicts, raw time strings are insufficient
because durations can cross midnight; start/end datetimes are used instead.

One alternative would check only duplicate start times using a dictionary.
That is simpler and often O(n), but misses 08:00–08:30 versus 08:20–08:40.
The implementation keeps the interval comparison to warn about both.

Recurring-task creation stays in Task.mark_complete(), while Scheduler attaches
the returned successor to the original pet. Repeating completion returns None,
preventing duplicate occurrences. Validation and successor creation occur before
changing completion status so an invalid date cannot partially complete a task.

## Decisions and limits

- One pet name per owner, matched without case sensitivity.
- Per-occurrence IDs distinguish equal descriptions and successive occurrences.
- Lists use default_factory, preventing shared state between instances.
- Pending tasks can be edited; completed ones remain history.
- Dates are exact occurrence dates, with no automatic overdue carryover.
- Late completion schedules the next occurrence after completion.
- Warnings cover all pets; table filters never hide the owner's conflicts.
- Session state preserves objects across widget reruns, not permanent restarts.
- No persistence or external AI API is required.
