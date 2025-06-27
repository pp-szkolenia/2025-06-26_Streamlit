import streamlit as st
from datetime import datetime

from db_connector import DatabaseConnector
from languages import translate


if "language" not in st.session_state:
    st.session_state.language = "en"
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in.")
    st.stop()
if "tasks" not in st.session_state:
    connector = DatabaseConnector("database/users.json", "database/tasks.json")
    st.session_state.tasks = connector.load_tasks()
if "users" not in st.session_state:
    connector = DatabaseConnector("database/users.json", "database/tasks.json")
    st.session_state.users = connector.load_users()

with st.sidebar:
    lang_in_session = st.session_state.get("language")
    index = ["en", "pl"].index(lang_in_session) if lang_in_session else 0
    lang = st.selectbox("", ["en", "pl"], index=index,
                        format_func=lambda x: "English" if x == "en" else "Polski", key="language_users")
    st.session_state.language = lang

    if st.session_state.user:
        st.markdown(f"**{translate('logged_in_as', lang)}:** {st.session_state.user['display_name']}")


user = st.session_state.user
is_admin = user["role"] == "admin"

# Filters
user_options = [u for u in st.session_state.users]

col1, col2 = st.columns(2)

user_multiselect = col1.multiselect(
    translate("filter_by_user", lang), [u["id"] for u in user_options],
    format_func=lambda uid: next(u["display_name"] for u in user_options if u["id"] == uid)
)

priority_multiselect = col2.multiselect(
    translate("filter_by_priority", lang), ["HIGH", "MEDIUM", "LOW", "none"],
    format_func=lambda p: translate(p.lower() if p != "none" else "none", lang)
)

col3, col4 = st.columns(2)
date_from = col3.date_input(translate("filter_by_due_date", lang) + " (from)", value=None)
date_to = col4.date_input(translate("filter_by_due_date", lang) + " (to)", value=None)

col5, col6 = st.columns([1, 3])
sort_by = col5.selectbox(translate("sort_by", lang), ["description", "priority", "assigned_user"],
                         format_func=lambda x: translate(x, lang), key="sort_by"
)


def filter_tasks(tasks):
    filtered = tasks.copy()
    if user_multiselect:
        filtered = [t for t in filtered if t["assigned_user_id"] in user_multiselect]
    if priority_multiselect:
        filtered = [t for t in filtered if (t["priority"] if t["priority"] else "none") in priority_multiselect]
    if date_from:
        filtered = [t for t in filtered if t["due_date"] >= date_from.strftime("%Y-%m-%d")]
    if date_to:
        filtered = [t for t in filtered if t["due_date"] <= date_to.strftime("%Y-%m-%d")]
    return filtered


def sort_tasks(tasks):
    if sort_by == "description":
        return sorted(tasks, key=lambda x: x["description"])
    elif sort_by == "priority":
        priority_order = {
            None: 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3
        }
        return sorted(tasks, key=lambda x: priority_order[x["priority"]])
    elif sort_by == "assigned_user":
        return sorted(tasks, key=lambda x: next(
            (u["display_name"] for u in st.session_state.users if u["id"] == x["assigned_user_id"]),
            "-"))
    else:
        return tasks


tasks = st.session_state.tasks
filtered_tasks = filter_tasks(tasks)
sorted_tasks = sort_tasks(filtered_tasks)
pinned_tasks = [t for t in sorted_tasks if t["pinned"]]
other_tasks = [t for t in sorted_tasks if not t["pinned"]]


def display_task_card(task):
    assigned_user = next((u["display_name"] for u in st.session_state.users if u["id"] == task["assigned_user_id"]), "-")
    can_edit = is_admin or task["assigned_user_id"] == user["id"]
    with st.container():
        st.divider()
        if task["pinned"]:
            st.markdown("📌")
        st.markdown(f"**{translate('description', lang)}:** {task['description']}")
        st.markdown(f"**{translate('assigned_user', lang)}:** {assigned_user}")
        st.markdown(f"**{translate('priority', lang)}:** {translate(task['priority'].lower() if task['priority'] else 'none', lang)}")
        st.markdown(f"**{translate('due_date', lang)}:** {task['due_date']}")
        cols = st.columns([1, 1])
        if can_edit:
            if cols[0].button(translate("edit_task", lang), key=f"edit_{task['id']}"):
                st.session_state.edit_task_id = task["id"]
                st.session_state.edit_task = task

                with st.form("edit_task_form"):
                    st.subheader(translate("edit_task", lang))
                    description = st.text_input(translate("description", lang), value=task["description"], key="edit_task_desc")
                    assigned_user_id = st.selectbox(translate("assigned_user", lang), [u["id"] for u in st.session_state.users], format_func=lambda uid: next(u["display_name"] for u in st.session_state.users if u["id"] == uid), index=[u["id"] for u in st.session_state.users].index(task["assigned_user_id"]), key="edit_task_user")
                    priority = st.selectbox(translate("priority", lang), ["HIGH", "MEDIUM", "LOW", "none"], format_func=lambda p: translate(p.lower() if p != "none" else "none", lang), index=["HIGH", "MEDIUM", "LOW", "none"].index(task["priority"] if task["priority"] else "none"), key="edit_task_priority")
                    due_date = st.date_input(translate("due_date", lang), value=datetime.strptime(task["due_date"], "%Y-%m-%d"), key="edit_task_due")
                    pinned = st.checkbox(translate("pinned", lang), value=task["pinned"], key="edit_task_pinned")
                    submitted = st.form_submit_button(translate("save", lang))
                    if submitted:
                        task["description"] = description
                        task["assigned_user_id"] = assigned_user_id
                        task["priority"] = priority if priority != "none" else None
                        task["due_date"] = due_date.strftime("%Y-%m-%d")
                        task["pinned"] = pinned
                        for i, t in enumerate(st.session_state.tasks):
                            if t["id"] == task["id"]:
                                st.session_state.tasks[i] = task
                                break
                        connector = DatabaseConnector("database/users.json", "database/tasks.json")
                        connector.save_tasks(st.session_state.tasks)
                        st.success(translate("task_updated", lang))
                        st.session_state.edit_task_id = None
                        st.session_state.edit_task = None
                        st.rerun()
            if cols[1].button(translate("delete_task", lang), key=f"delete_{task['id']}"):
                st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task["id"]]
                connector = DatabaseConnector("database/users.json", "database/tasks.json")
                connector.save_tasks(st.session_state.tasks)
                st.rerun()
        st.divider()


st.header(translate("tasks", lang))

col1, _, col2 = st.columns([1, 0.5, 1])

for i, task in enumerate(pinned_tasks + other_tasks):
    if i % 2 == 0:
        with col1:
            display_task_card(task)
    else:
        with col2:
            display_task_card(task)


with st.expander(translate("add_task", lang)):
    description = st.text_input(translate("description", lang), key="new_task_desc")
    assigned_user_id = st.selectbox(translate("assigned_user", lang), [u["id"] for u in st.session_state.users], format_func=lambda uid: next(u["display_name"] for u in st.session_state.users if u["id"] == uid), key="new_task_user")
    priority = st.selectbox(translate("priority", lang), ["HIGH", "MEDIUM", "LOW", "none"], index=3,
                            format_func=lambda p: translate(p.lower() if p != "none" else "none", lang), key="new_task_priority")
    due_date = st.date_input(translate("due_date", lang), key="new_task_due")
    pinned = st.checkbox(translate("pinned", lang), key="new_task_pinned")
    if st.button(translate("add_task", lang), key="add_task_btn"):
        new_id = max([t["id"] for t in st.session_state.tasks], default=0) + 1
        st.session_state.tasks.append({
            "id": new_id,
            "description": description,
            "assigned_user_id": assigned_user_id,
            "priority": priority if priority != "none" else None,
            "due_date": due_date.strftime("%Y-%m-%d"),
            "pinned": pinned,
            "created_by": user["id"]
        })
        connector = DatabaseConnector("database/users.json", "database/tasks.json")
        connector.save_tasks(st.session_state.tasks)
        st.success(translate("task_created", lang))
        st.rerun()
