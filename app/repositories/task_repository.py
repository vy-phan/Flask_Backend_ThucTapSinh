from ..models import db, Task

class TaskRepository:
    def get_all_tasks(self):
        return Task.query.all()

    def get_task_by_id(self, task_id):
        return Task.query.get(task_id)

    def create_task(self, task_data):
        new_task = Task(**task_data)
        db.session.add(new_task)
        db.session.commit()
        return new_task

    def update_task(self, task):
        db.session.commit()
        return task

    def delete_task(self, task):
        db.session.delete(task)
        db.session.commit()