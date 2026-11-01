"""Integration checks for session memory and all required UI features."""
from datetime import date, timedelta
from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def widget(elements, label):
    return next(item for item in elements if item.label == label)


def start():
    return AppTest.from_file(str(APP), default_timeout=15).run()


def test_add_two_pets_and_task_persists_across_reruns():
    app = start()
    widget(app.text_input, "Pet name").set_value("Biscuit")
    widget(app.button, "Add pet").click().run()
    widget(app.text_input, "Pet name").set_value("Luna")
    widget(app.button, "Add pet").click().run()
    assert len(app.session_state["owner"].pets) == 2
    widget(app.selectbox, "Pet for task").select("Biscuit").run()
    widget(app.button, "Add task").click().run()
    owner = app.session_state["owner"]
    assert len(owner.get_pet("Biscuit").tasks) == 1
    widget(app.selectbox, "Filter by pet").select("Luna").run()
    assert len(app.session_state["owner"].get_pet("Biscuit").tasks) == 1
    assert any("No tasks match" in item.value for item in app.info)
    assert not app.exception


def test_example_sorting_filtering_and_conflict_warning():
    app = start()
    widget(app.button, "Load example pets and tasks").click().run()
    assert len(app.warning) == 1
    assert "Breakfast" in app.warning[0].value
    assert "Medication" in app.warning[0].value
    table = app.table[0].value
    assert list(table["Time"]) == ["08:00", "08:00", "09:00", "18:00"]
    widget(app.selectbox, "Filter by pet").select("Luna").run()
    assert list(app.table[0].value["Pet"]) == ["Luna", "Luna"]
    # The warning must retain conflicts with pets outside the display filter.
    assert len(app.warning) == 1
    widget(app.selectbox, "Sort schedule").select("Priority, then time").run()
    assert list(app.table[0].value["Priority"]) == ["high", "low"]
    assert not app.exception


def test_edit_delete_and_completion_create_next_occurrence():
    app = start()
    widget(app.text_input, "Pet name").set_value("Mochi")
    widget(app.button, "Add pet").click().run()
    widget(app.selectbox, "Frequency").select("daily")
    widget(app.button, "Add task").click().run()
    original_id = app.session_state["owner"].get_pet("Mochi").tasks[0].task_id
    widget(app.selectbox, "Task to add or edit").select(original_id).run()
    widget(app.text_input, "Description").set_value("Evening walk")
    widget(app.number_input, "Duration (minutes)").set_value(25)
    widget(app.button, "Save task").click().run()
    assert app.session_state["owner"].get_pet("Mochi").tasks[0].description == "Evening walk"
    widget(app.button, "Mark complete").click().run()
    tasks = app.session_state["owner"].get_pet("Mochi").tasks
    assert tasks[0].completed
    assert len(tasks) == 2
    assert tasks[1].due_date == date.today() + timedelta(days=1)
    assert tasks[1].duration_minutes == 25
    widget(app.selectbox, "Filter by status").select("Completed").run()
    assert list(app.table[0].value["Status"]) == ["✅ Complete"]
    widget(app.selectbox, "Task to add or edit").select(tasks[1].task_id).run()
    widget(app.button, "Delete task").click().run()
    assert len(app.session_state["owner"].get_pet("Mochi").tasks) == 1
    assert not app.exception


def test_validation_is_visible_without_losing_session_data():
    app = start()
    widget(app.button, "Add pet").click().run()
    assert "must not be blank" in app.error[0].value
    widget(app.text_input, "Owner name").set_value(" ")
    widget(app.button, "Save owner").click().run()
    assert "Owner name" in app.error[0].value
    assert app.session_state["owner"].name == "Jordan"
    widget(app.text_input, "Pet name").set_value("Mochi")
    widget(app.button, "Add pet").click().run()
    widget(app.text_input, "Pet name").set_value("MOCHI")
    widget(app.button, "Add pet").click().run()
    assert "already exists" in app.error[0].value
    widget(app.text_input, "Description").set_value(" ")
    widget(app.button, "Add task").click().run()
    assert "Task description" in app.error[0].value
    assert app.session_state["owner"].get_pet("Mochi").tasks == []
    assert not app.exception
