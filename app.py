"""Streamlit UI backed by the same four classes as the CLI demo."""
from datetime import date, datetime
import streamlit as st
from main import build_demo_owner
from pawpal_system import FREQUENCIES, PRIORITIES, Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.write("Care for all your pets in one schedule.")
st.caption("Data stays in this session. It is not saved after the session ends.")
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner = st.session_state.owner
scheduler = Scheduler(owner)
if "notice" in st.session_state:
    st.success(st.session_state.pop("notice"))

with st.form("owner_form"):
    owner_name = st.text_input("Owner name", owner.name)
    if st.form_submit_button("Save owner"):
        try:
            # Validate before changing the existing session object.
            Owner(owner_name.strip())
            owner.name = owner_name.strip()
            st.success("Owner updated.")
        except ValueError as error:
            st.error(str(error))

st.subheader("Pets")
with st.form("pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        try:
            owner.add_pet(Pet(pet_name.strip(), species))
            st.session_state.notice = "Pet added."
            st.rerun()
        except ValueError as error:
            st.error(str(error))
if st.button("Load example pets and tasks", disabled=bool(owner.pets)):
    demo = build_demo_owner(date.today())
    for pet in demo.pets:
        owner.add_pet(pet)
    st.rerun()

if not owner.pets:
    st.info("Add a pet or load the example to start planning.")
else:
    st.write("Your pets: " + ", ".join(f"{pet.name} ({pet.species})" for pet in owner.pets))
    st.subheader("Add or manage a task")
    selected_pet = st.selectbox("Pet for task", [pet.name for pet in owner.pets])
    pet = owner.get_pet(selected_pet)
    task_ids = ["new"] + [task.task_id for task in pet.tasks]
    labels = {"new": "Add new task"}
    labels.update({task.task_id: f"{task.description} — {task.due_date} {task.time}"
                   + (" · completed" if task.completed else "") for task in pet.tasks})
    task_id = st.selectbox("Task to add or edit", task_ids,
                          format_func=lambda value: labels[value], key=f"task_choice_{pet.name}")
    existing = pet.get_task(task_id) if task_id != "new" else None
    # The stable ID gives each occurrence its own editor state.
    with st.form(f"task_form_{pet.name}_{task_id}"):
        description = st.text_input("Description", existing.description if existing else "Morning walk")
        task_time = st.time_input("Task time",
            datetime.strptime(existing.time if existing else "09:00", "%H:%M").time(), step=60)
        due_date = st.date_input("Due date", existing.due_date if existing else date.today())
        duration = st.number_input("Duration (minutes)", 1, 1440, existing.duration_minutes if existing else 20)
        frequencies = list(FREQUENCIES)
        frequency = st.selectbox("Frequency", frequencies,
            index=frequencies.index(existing.frequency) if existing else 0)
        priorities = list(PRIORITIES)
        priority = st.selectbox("Priority", priorities,
            index=priorities.index(existing.priority) if existing else 1)
        if existing and existing.completed:
            st.caption("Completed tasks are retained as history. You can delete this occurrence.")
        save = st.form_submit_button("Save task" if existing else "Add task",
                                     disabled=bool(existing and existing.completed))
        complete = st.form_submit_button("Mark complete", disabled=existing.completed) if existing else False
        delete = st.form_submit_button("Delete task") if existing else False
    try:
        if save:
            details = dict(description=description.strip(), time=task_time.strftime("%H:%M"),
                           frequency=frequency, due_date=due_date,
                           duration_minutes=int(duration), priority=priority)
            if existing:
                pet.update_task(task_id, **details)
            else:
                pet.add_task(Task(**details))
            st.session_state.notice = "Task saved."
            st.rerun()
        if complete:
            successor = scheduler.mark_task_complete(pet.name, task_id)
            st.session_state.notice = (
                f"Completed. Next occurrence: {successor.due_date} at {successor.time}."
                if successor else "Task completed.")
            st.rerun()
        if delete:
            pet.remove_task(task_id)
            st.session_state.notice = "Task deleted."
            st.rerun()
    except ValueError as error:
        st.error(str(error))

    st.subheader("Today's schedule")
    selected_date = st.date_input("Schedule date", date.today())
    pet_filter = st.selectbox("Filter by pet", ["All pets"] + [pet.name for pet in owner.pets])
    status = st.selectbox("Filter by status", ["Pending", "Completed", "All"])
    ordering = st.selectbox("Sort schedule", ["Time", "Priority, then time"])
    completed = {"Pending": False, "Completed": True, "All": None}[status]
    sort = scheduler.sort_by_time if ordering == "Time" else scheduler.sort_by_priority
    entries = sort(pet_name=None if pet_filter == "All pets" else pet_filter,
                   completed=completed, on_date=selected_date)
    if entries:
        st.table([{
            "Time": task.time, "Pet": pet.name, "Task": task.description,
            "Minutes": task.duration_minutes, "Frequency": task.frequency,
            "Priority": task.priority,
            "Status": "✅ Complete" if task.completed else "⏳ Pending",
        } for pet, task in entries])
    else:
        st.info("No tasks match this date and these filters.")
    st.caption("Warnings include every pet's pending tasks, regardless of the display filters. "
               "Edit a task time to resolve a conflict.")
    warnings = scheduler.detect_conflicts(selected_date)
    if warnings:
        for warning in warnings:
            st.warning(warning)
    else:
        st.success("No pending task conflicts on this date.")
