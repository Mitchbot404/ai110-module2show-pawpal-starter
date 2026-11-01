# Test plan

1. **Object ownership and completion:** adding pets/tasks, independent default
   lists, stable IDs, one-time completion, and preservation of history.
2. **Sorting and filtering:** out-of-order times, different dates, multiple pets,
   completion status, empty results, chronological and priority-first ordering.
3. **Recurrence:** daily/weekly successors, no duplicate successor on repeated
   completion, late completion, year rollover, and invalid/overflow dates.
4. **Conflicts:** identical times for one or multiple pets, partial duration
   overlap, nonoverlapping adjacent intervals, completed tasks, other dates,
   cross-midnight overlap, and exactly one warning per conflicting pair.
5. **UI integration and validation:** adding multiple pets, session persistence,
   adding/editing/deleting/completing tasks, date/status/pet filters, priority
   view, conflict display, and invalid input without losing valid state.

Backend tests are in tests/test_pawpal.py. UI integration tests are in
tests/test_app.py and execute the actual Streamlit app through AppTest.
Tests check externally meaningful behavior rather than matching source text.
