from datetime import datetime
from app.models import Task_Detail, Task
from app.repositories.task_detail_repo import (
    get_task_details_by_task_id,
    get_all_task_details,
    get_task_detail_by_id,
    add_task_detail,
    update_task_detail,
    delete_task_detail
)

def fetch_task_details_by_task_id(task_id):
    return get_task_details_by_task_id(task_id)

def fetch_all_task_details():
    return get_all_task_details()

def create_task_detail(data):
    task_id = data.get('task_id')
    title = data.get('title')
    description = data.get('description', '')
    status = 'Đã giao'

    if not all([task_id, title, status]):
        raise ValueError("Các trường task_id, title và status là bắt buộc")

    task = Task.query.get(task_id)
    if not task:
        raise LookupError(f"Task với id {task_id} không tồn tại")

    new_detail = Task_Detail(
        task_id=task_id,
        title=title,
        description=description,
        status=status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    add_task_detail(new_detail)
    return new_detail, task.title

def modify_task_detail(task_detail_id, data):
    task_detail_record = get_task_detail_by_id(task_detail_id)
    if not task_detail_record:
        raise LookupError("Task detail không tồn tại")

    task_detail_record.title = data.get('title', task_detail_record.title)
    task_detail_record.description = data.get('description', task_detail_record.description)
    task_detail_record.status = data.get('status', task_detail_record.status)
    task_detail_record.updated_at = datetime.utcnow()

    update_task_detail()
    return task_detail_record

def remove_task_detail(task_detail_id):
    task_detail = get_task_detail_by_id(task_detail_id)
    if not task_detail:
        raise LookupError("Task detail không tồn tại")
    delete_task_detail(task_detail)
