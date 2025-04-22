from app.models import db, Task_Detail

def get_task_details_by_task_id(task_id):
    return Task_Detail.query.filter_by(task_id=task_id).all()

def get_all_task_details():
    return Task_Detail.query.all()

def get_task_detail_by_id(task_detail_id):
    return Task_Detail.query.get(task_detail_id)

def add_task_detail(task_detail):
    db.session.add(task_detail)
    db.session.commit()
    return task_detail

def update_task_detail():
    db.session.commit()

def delete_task_detail(task_detail):
    db.session.delete(task_detail)
    db.session.commit()
