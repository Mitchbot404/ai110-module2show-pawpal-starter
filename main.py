"""Reproducible CLI demo: python main.py."""
from datetime import date
from pawpal_system import Owner, Pet, Scheduler, Task

DEMO_DATE = date(2026, 11, 2)


def build_demo_owner(on_date: date = DEMO_DATE) -> Owner:
    """Build two pets with deliberately unsorted and conflicting tasks."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)
    mochi.add_task(Task("Morning walk", "09:00", "daily", on_date, 30, "high"))
    mochi.add_task(Task("Breakfast", "08:00", "daily", on_date, 10, "medium"))
    luna.add_task(Task("Grooming", "18:00", "weekly", on_date, 15, "low"))
    luna.add_task(Task("Medication", "08:00", "daily", on_date, 5, "high"))
    return owner


def print_schedule(entries: list[tuple[Pet, Task]]) -> None:
    """Print task associations in a readable fixed-width table."""
    print("Time   Pet      Task             Min  Priority  Status")
    for pet, task in entries:
        status = "done" if task.completed else "pending"
        print(f"{task.time}  {pet.name:<7}  {task.description:<16} {task.duration_minutes:>3}  {task.priority:<8}  {status}")


def main() -> None:
    """Demonstrate sorting, filtering, warnings, priority, and recurrence."""
    owner = build_demo_owner()
    scheduler = Scheduler(owner)
    print(f"Today's Schedule — {DEMO_DATE} (fixed demo date)")
    print_schedule(scheduler.sort_by_time(on_date=DEMO_DATE))
    print("\nPending tasks for Mochi")
    print_schedule(scheduler.sort_by_time(pet_name="Mochi", completed=False, on_date=DEMO_DATE))
    print("\nConflict warnings")
    for warning in scheduler.detect_conflicts(DEMO_DATE):
        print(warning)
    print("\nPriority-first view")
    print_schedule(scheduler.sort_by_priority(on_date=DEMO_DATE))
    breakfast = owner.get_pet("Mochi").tasks[1]
    successor = scheduler.mark_task_complete("Mochi", breakfast.task_id, completed_on=DEMO_DATE)
    print(f"\nCompleted: Mochi — {breakfast.description}")
    print(f"Next daily occurrence: {successor.due_date} {successor.time}")
    print(f"Pending on demo date: {len(scheduler.filter_tasks(completed=False, on_date=DEMO_DATE))}")
    print(f"Completed on demo date: {len(scheduler.filter_tasks(completed=True, on_date=DEMO_DATE))}")


if __name__ == "__main__":
    main()
