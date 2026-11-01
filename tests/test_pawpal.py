"""Required model and algorithm tests, including boundary behavior."""
from datetime import date, timedelta
import pytest
from pawpal_system import Owner, Pet, Scheduler, Task

DAY = date(2026, 11, 2)


def task(description="Walk", time="09:00", **kwargs):
    return Task(description, time, due_date=DAY, **kwargs)


def system():
    owner = Owner("Jordan")
    owner.add_pet(Pet("Mochi", "dog"))
    owner.add_pet(Pet("Luna", "cat"))
    return owner, Scheduler(owner)


def test_task_completion_changes_status():
    activity = task()
    assert activity.mark_complete(DAY) is None
    assert activity.completed is True


def test_adding_task_increases_pet_count():
    pet = Pet("Mochi", "dog")
    pet.add_task(task())
    assert len(pet.tasks) == 1


def test_multiple_pets_and_all_tasks():
    owner, scheduler = system()
    owner.get_pet("Mochi").add_task(task("Walk"))
    owner.get_pet("Luna").add_task(task("Feed"))
    assert len(owner.all_tasks()) == 2
    assert {pet.name for pet, _ in scheduler.filter_tasks()} == {"Mochi", "Luna"}


def test_independent_default_lists():
    first, second = Pet("A", "dog"), Pet("B", "cat")
    first.add_task(task())
    assert second.tasks == []
    one, two = Owner("A"), Owner("B")
    one.add_pet(first)
    assert two.pets == []


def test_sort_by_time_with_out_of_order_tasks_and_multiple_dates():
    owner, scheduler = system()
    pet = owner.get_pet("Mochi")
    late, early = task(time="18:00"), task(time="08:05")
    tomorrow = Task("Tomorrow", "06:00", due_date=DAY + timedelta(days=1))
    for activity in [tomorrow, late, early]:
        pet.add_task(activity)
    before = pet.tasks.copy()
    assert [t for _, t in scheduler.sort_by_time()] == [early, late, tomorrow]
    assert pet.tasks == before


def test_filter_by_pet_status_and_date():
    owner, scheduler = system()
    done = task("Done")
    done.mark_complete(DAY)
    owner.get_pet("Mochi").add_task(done)
    owner.get_pet("Mochi").add_task(task("Pending"))
    owner.get_pet("Luna").add_task(task("Other pet"))
    assert [t.description for _, t in scheduler.filter_tasks("mochi", False, DAY)] == ["Pending"]
    assert [t.description for _, t in scheduler.filter_tasks(completed=True)] == ["Done"]
    assert scheduler.filter_tasks(on_date=DAY + timedelta(days=1)) == []


@pytest.mark.parametrize("frequency,days", [("daily", 1), ("weekly", 7)])
def test_completion_automatically_adds_next_occurrence(frequency, days):
    owner, scheduler = system()
    pet = owner.get_pet("Mochi")
    original = task(frequency=frequency, priority="high", duration_minutes=30)
    pet.add_task(original)
    successor = scheduler.mark_task_complete("Mochi", original.task_id, DAY)
    assert original.completed
    assert len(pet.tasks) == 2
    assert successor in pet.tasks
    assert successor.due_date == DAY + timedelta(days=days)
    assert successor.time == original.time
    assert successor.priority == "high"
    assert successor.duration_minutes == 30
    assert successor.frequency == frequency
    assert successor.task_id != original.task_id
    assert not successor.completed
    assert scheduler.mark_task_complete("Mochi", original.task_id, DAY) is None
    assert len(pet.tasks) == 2


def test_one_time_completion_does_not_add_task():
    owner, scheduler = system()
    activity = task()
    owner.get_pet("Mochi").add_task(activity)
    scheduler.mark_task_complete("Mochi", activity.task_id, DAY)
    assert len(owner.all_tasks()) == 1


def test_late_completion_creates_future_occurrence():
    activity = task(frequency="daily")
    successor = activity.mark_complete(DAY + timedelta(days=4))
    assert successor.due_date == DAY + timedelta(days=5)


def test_future_occurrence_is_not_moved_backward():
    activity = task(frequency="weekly")
    successor = activity.mark_complete(DAY - timedelta(days=5))
    assert successor.due_date == DAY + timedelta(days=7)


def test_recurrence_handles_year_boundary():
    activity = Task("Feed", "08:00", "daily", date(2026, 12, 31))
    assert activity.mark_complete(date(2026, 12, 31)).due_date == date(2027, 1, 1)


def test_recurrence_overflow_does_not_complete_original():
    activity = Task("Feed", "08:00", "daily", date.max)
    with pytest.raises(ValueError, match="supported date"):
        activity.mark_complete(date.max)
    assert not activity.completed


@pytest.mark.parametrize("same_pet", [True, False])
def test_duplicate_times_warn_for_same_or_different_pets(same_pet):
    owner, scheduler = system()
    owner.get_pet("Mochi").add_task(task("Walk", "08:00"))
    owner.get_pet("Mochi" if same_pet else "Luna").add_task(task("Feed", "08:00"))
    warnings = scheduler.detect_conflicts(DAY)
    assert len(warnings) == 1
    assert "Walk" in warnings[0] and "Feed" in warnings[0]


def test_overlap_detected_but_touching_endpoints_are_allowed():
    owner, scheduler = system()
    pet = owner.get_pet("Mochi")
    pet.add_task(task("Walk", "08:00", duration_minutes=30))
    pet.add_task(task("Feed", "08:20", duration_minutes=10))
    pet.add_task(task("Play", "08:30", duration_minutes=10))
    assert len(scheduler.detect_conflicts(DAY)) == 1


def test_conflicts_ignore_completed_tasks_and_other_dates():
    owner, scheduler = system()
    first, done = task("Walk", "08:00"), task("Done", "08:00")
    done.mark_complete(DAY)
    owner.get_pet("Mochi").add_task(first)
    owner.get_pet("Luna").add_task(done)
    owner.get_pet("Luna").add_task(Task("Tomorrow", "08:00", due_date=DAY + timedelta(days=1)))
    assert scheduler.detect_conflicts(DAY) == []
    assert scheduler.detect_conflicts() == []


def test_conflicts_include_previous_day_tasks_crossing_midnight():
    owner, scheduler = system()
    owner.get_pet("Mochi").add_task(task("Late walk", "23:50", duration_minutes=30))
    owner.get_pet("Luna").add_task(Task("Feed", "00:05", due_date=DAY + timedelta(days=1)))
    assert len(scheduler.detect_conflicts(DAY + timedelta(days=1))) == 1
    assert scheduler.detect_conflicts(DAY) == []
    assert len(scheduler.detect_conflicts()) == 1


def test_conflicts_report_each_pair_once():
    owner, scheduler = system()
    for name in ["A", "B", "C"]:
        owner.get_pet("Mochi").add_task(task(name, "08:00"))
    assert len(scheduler.detect_conflicts(DAY)) == 3


def test_priority_first_then_time():
    owner, scheduler = system()
    pet = owner.get_pet("Mochi")
    for activity in [task("Low", "07:00", priority="low"),
                     task("High late", "10:00", priority="high"),
                     task("High early", "09:00", priority="high")]:
        pet.add_task(activity)
    assert [t.description for _, t in scheduler.sort_by_priority()] == ["High early", "High late", "Low"]


def test_empty_owner_and_pet():
    owner = Owner("Jordan")
    scheduler = Scheduler(owner)
    assert scheduler.sort_by_time() == []
    owner.add_pet(Pet("Mochi", "dog"))
    assert scheduler.filter_tasks("Mochi") == []
    assert scheduler.detect_conflicts(DAY) == []


def test_edit_validates_before_replacing_and_preserves_id():
    pet = Pet("Mochi", "dog")
    activity = task()
    pet.add_task(activity)
    pet.update_task(activity.task_id, time="11:00", description="Long walk")
    assert pet.tasks[0].time == "11:00"
    assert pet.tasks[0].task_id == activity.task_id
    with pytest.raises(ValueError):
        pet.update_task(activity.task_id, time="25:00")
    assert pet.tasks[0].time == "11:00"
    with pytest.raises(ValueError):
        pet.update_task(activity.task_id, completed=True)
    pet.tasks[0].mark_complete(DAY)
    with pytest.raises(ValueError, match="history"):
        pet.update_task(activity.task_id, time="12:00")
    pet.remove_task(activity.task_id)
    assert pet.tasks == []


def test_membership_validation():
    owner, _ = system()
    with pytest.raises(ValueError, match="already exists"):
        owner.add_pet(Pet(" moCHI ", "cat"))
    with pytest.raises(ValueError):
        owner.add_pet("Luna")
    with pytest.raises(ValueError):
        owner.get_pet("Unknown")
    pet = owner.get_pet("Mochi")
    activity = task()
    pet.add_task(activity)
    with pytest.raises(ValueError):
        pet.add_task(activity)
    with pytest.raises(ValueError):
        pet.add_task("Walk")
    with pytest.raises(ValueError):
        pet.get_task("missing")
    with pytest.raises(ValueError):
        Pet("A", "dog", [activity, activity])
    with pytest.raises(ValueError):
        Pet("A", "dog", ["Walk"])
    with pytest.raises(ValueError):
        Owner("A", [pet, Pet("mochi", "dog")])
    with pytest.raises(ValueError):
        Owner("A", ["Pet"])


@pytest.mark.parametrize("time", ["8:00", "24:00", "12:60", "", "08:00:00", None])
def test_invalid_clock_strings(time):
    with pytest.raises(ValueError, match="HH:MM"):
        task(time=time)


@pytest.mark.parametrize("changes", [
    {"description": " "}, {"duration_minutes": 0}, {"duration_minutes": True},
    {"duration_minutes": 2.5}, {"duration_minutes": 1441},
    {"frequency": "monthly"}, {"priority": "urgent"}, {"due_date": "2026-11-02"},
    {"completed": "yes"}, {"task_id": ""},
])
def test_invalid_task_data(changes):
    details = dict(description="Walk", time="08:00", due_date=DAY)
    details.update(changes)
    with pytest.raises(ValueError):
        Task(**details)


def test_invalid_names_and_completion_date():
    for factory in [lambda: Owner(" "), lambda: Pet("", "dog"), lambda: Pet("A", "")]:
        with pytest.raises(ValueError):
            factory()
    activity = task(frequency="daily")
    with pytest.raises(ValueError):
        activity.mark_complete("Monday")
    assert not activity.completed
