"""PawPal+ logic layer: owners contain pets, pets contain scheduled tasks."""
from dataclasses import dataclass, field, replace
from datetime import date, datetime, timedelta
import re
from uuid import uuid4

PRIORITIES = {"high": 3, "medium": 2, "low": 1}
FREQUENCIES = ("once", "daily", "weekly")


def require_text(value: str, label: str) -> None:
    """Reject empty or non-text labels."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must not be blank.")


@dataclass
class Task:
    """One dated occurrence of a pet-care activity."""

    description: str
    time: str
    frequency: str = "once"
    due_date: date = field(default_factory=date.today)
    duration_minutes: int = 15
    priority: str = "medium"
    completed: bool = False
    task_id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self) -> None:
        """Validate fields so clock strings sort chronologically."""
        require_text(self.description, "Task description")
        if not isinstance(self.time, str) or not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", self.time):
            raise ValueError("Time must use 24-hour HH:MM format, such as 08:30.")
        if self.frequency not in FREQUENCIES:
            raise ValueError("Frequency must be once, daily, or weekly.")
        if type(self.due_date) is not date:
            raise ValueError("Due date must be a date.")
        if type(self.duration_minutes) is not int or not 1 <= self.duration_minutes <= 1440:
            raise ValueError("Duration must be a whole number from 1 to 1440.")
        if self.priority not in PRIORITIES:
            raise ValueError("Priority must be low, medium, or high.")
        if type(self.completed) is not bool:
            raise ValueError("Completion status must be true or false.")
        require_text(self.task_id, "Task ID")

    @property
    def start(self) -> datetime:
        """Return the occurrence's local start datetime."""
        return datetime.combine(self.due_date, datetime.strptime(self.time, "%H:%M").time())

    @property
    def end(self) -> datetime:
        """Return the end, including a next-day endpoint when necessary."""
        return self.start + timedelta(minutes=self.duration_minutes)

    def mark_complete(self, completed_on: date | None = None) -> "Task | None":
        """Complete once and return a new daily/weekly occurrence, if any."""
        if self.completed:
            return None
        completed_on = date.today() if completed_on is None else completed_on
        if type(completed_on) is not date:
            raise ValueError("Completion date must be a date.")
        successor = None
        if self.frequency != "once":
            days = 1 if self.frequency == "daily" else 7
            try:
                next_date = max(self.due_date, completed_on) + timedelta(days=days)
            except OverflowError as error:
                raise ValueError("The next occurrence falls outside the supported date range.") from error
            successor = replace(self, due_date=next_date, completed=False, task_id=uuid4().hex)
        self.completed = True
        return successor


@dataclass
class Pet:
    """A pet and the task occurrences belonging to it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate identity and initial task membership."""
        require_text(self.name, "Pet name")
        require_text(self.species, "Species")
        if any(not isinstance(task, Task) for task in self.tasks):
            raise ValueError("Pets may contain only Task objects.")
        if len({task.task_id for task in self.tasks}) != len(self.tasks):
            raise ValueError("Task IDs must be unique within a pet.")

    def add_task(self, task: Task) -> None:
        """Attach a task while preventing duplicate occurrences."""
        if not isinstance(task, Task):
            raise ValueError("Add a Task object.")
        if any(existing.task_id == task.task_id for existing in self.tasks):
            raise ValueError("This task is already assigned to the pet.")
        self.tasks.append(task)

    def get_task(self, task_id: str) -> Task:
        """Find an occurrence by its stable identifier."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        raise ValueError("Task not found.")

    def update_task(self, task_id: str, **changes) -> None:
        """Validate edits before replacing an incomplete task."""
        task = self.get_task(task_id)
        if task.completed:
            raise ValueError("Completed tasks are history and cannot be edited.")
        allowed = {"description", "time", "frequency", "due_date", "duration_minutes", "priority"}
        if set(changes) - allowed:
            raise ValueError("Only task scheduling details can be edited.")
        updated = replace(task, **changes)
        index = next(i for i, current in enumerate(self.tasks) if current.task_id == task_id)
        self.tasks[index] = updated

    def remove_task(self, task_id: str) -> None:
        """Delete the selected occurrence."""
        task = self.get_task(task_id)
        self.tasks.remove(task)


@dataclass
class Owner:
    """An owner who manages multiple pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate the owner and case-insensitively unique pet names."""
        require_text(self.name, "Owner name")
        if any(not isinstance(pet, Pet) for pet in self.pets):
            raise ValueError("Owners may contain only Pet objects.")
        if len({pet.name.strip().casefold() for pet in self.pets}) != len(self.pets):
            raise ValueError("Pet names must be unique for this owner.")

    def add_pet(self, pet: Pet) -> None:
        """Attach a pet with a unique name."""
        if not isinstance(pet, Pet):
            raise ValueError("Add a Pet object.")
        if any(existing.name.strip().casefold() == pet.name.strip().casefold() for existing in self.pets):
            raise ValueError("A pet with that name already exists.")
        self.pets.append(pet)

    def get_pet(self, name: str) -> Pet:
        """Find a pet by name without case sensitivity."""
        for pet in self.pets:
            if pet.name.strip().casefold() == name.strip().casefold():
                return pet
        raise ValueError("Pet not found.")

    def all_tasks(self) -> list[tuple[Pet, Task]]:
        """Flatten pet-task associations without losing pet identity."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


@dataclass
class Scheduler:
    """Coordinate sorting, filtering, recurrence, and warnings across pets."""

    owner: Owner

    def filter_tasks(self, pet_name: str | None = None, completed: bool | None = None,
                     on_date: date | None = None) -> list[tuple[Pet, Task]]:
        """Filter by pet, status, and exact occurrence date without mutation."""
        tasks = self.owner.all_tasks()
        if pet_name is not None:
            pet = self.owner.get_pet(pet_name)
            tasks = [(p, task) for p, task in tasks if p is pet]
        if completed is not None:
            tasks = [(pet, task) for pet, task in tasks if task.completed == completed]
        if on_date is not None:
            tasks = [(pet, task) for pet, task in tasks if task.due_date == on_date]
        return tasks

    def sort_by_time(self, pet_name: str | None = None, completed: bool | None = None,
                     on_date: date | None = None) -> list[tuple[Pet, Task]]:
        """Return chronological tasks using validated HH:MM strings."""
        return sorted(self.filter_tasks(pet_name, completed, on_date),
                      key=lambda entry: (entry[1].due_date, entry[1].time))

    def sort_by_priority(self, pet_name: str | None = None, completed: bool | None = None,
                         on_date: date | None = None) -> list[tuple[Pet, Task]]:
        """Offer priority-first ordering, then date/time, as an optional view."""
        return sorted(self.filter_tasks(pet_name, completed, on_date),
                      key=lambda entry: (-PRIORITIES[entry[1].priority],
                                         entry[1].due_date, entry[1].time))

    def mark_task_complete(self, pet_name: str, task_id: str,
                           completed_on: date | None = None) -> Task | None:
        """Complete the occurrence and automatically attach its successor."""
        pet = self.owner.get_pet(pet_name)
        successor = pet.get_task(task_id).mark_complete(completed_on)
        if successor is not None:
            pet.add_task(successor)
        return successor

    def detect_conflicts(self, on_date: date | None = None) -> list[str]:
        """Warn about overlapping pending tasks across all pets."""
        entries = self.sort_by_time(completed=False)
        warnings = []
        for i, (pet, task) in enumerate(entries):
            for other_pet, other in entries[i + 1:]:
                if other.start >= task.end:
                    break
                # Half-open intervals: one task may start when another ends.
                if task.start < other.end and other.start < task.end:
                    if on_date is not None:
                        day_start = datetime.combine(on_date, datetime.min.time())
                        day_end = day_start + timedelta(days=1)
                        if max(task.start, other.start, day_start) >= min(task.end, other.end, day_end):
                            continue
                    warnings.append(
                        f"Conflict: {pet.name} — {task.description} "
                        f"({task.due_date} {task.time}) overlaps "
                        f"{other_pet.name} — {other.description} "
                        f"({other.due_date} {other.time})."
                    )
        return warnings
