from datetime import datetime
from ..models import Task
from ..repositories.task_repository import TaskRepository

class TaskService:
    def __init__(self):
        self.repo = TaskRepository()

    def get_all_tasks(self):
        try:
            tasks = self.repo.get_all_tasks()
            return [{
                'id': task.id,
                'code': task.code,
                'title': task.title,
                'description': task.description,
                'deadline': task.deadline.isoformat(),
                'status': task.status,
                'created_by': task.created_by,
                'created_at': task.created_at.isoformat()
            } for task in tasks]
        except Exception as e:
            raise Exception(f"Error fetching tasks: {str(e)}")

    def create_task(self, data):
        try:
            # Validate required fields
            required_fields = ['code', 'title', 'deadline', 'created_by']
            for field in required_fields:
                if field not in data or not data[field]:
                    raise ValueError(f"Missing required field: {field}")

            # Validate deadline
            try:
                deadline = datetime.fromisoformat(data['deadline'])
            except ValueError:
                raise ValueError("Invalid deadline format. Use ISO format (e.g., 2025-04-21T15:30:00)")

            # Validate status
            valid_statuses = ['assigned', 'in_progress', 'completed']
            status = data.get('status', 'assigned')
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")

            # Prepare task data
            task_data = {
                'code': data['code'],
                'title': data['title'],
                'description': data.get('description'),
                'deadline': deadline,
                'status': status,
                'created_by': data['created_by']
            }

            # Create task
            new_task = self.repo.create_task(task_data)
            return {
                'id': new_task.id,
                'code': new_task.code,
                'title': new_task.title,
                'description': new_task.description,
                'deadline': new_task.deadline.isoformat(),
                'status': new_task.status,
                'created_by': new_task.created_by,
                'created_at': new_task.created_at.isoformat()
            }
        except Exception as e:
            raise Exception(f"Error creating task: {str(e)}")

    def update_task(self, task_id, data):
        try:
            task = self.repo.get_task_by_id(task_id)
            if not task:
                raise ValueError("Task not found")

            # Update fields if provided
            if 'code' in data:
                task.code = data['code']
            if 'title' in data:
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            if 'deadline' in data:
                try:
                    task.deadline = datetime.fromisoformat(data['deadline'])
                except ValueError:
                    raise ValueError("Invalid deadline format. Use ISO format (e.g., 2025-04-21T15:30:00)")
            if 'status' in data:
                valid_statuses = ['Đã giao', 'Đang thực hiện', 'Đã hoàn thành']
                if data['status'] not in valid_statuses:
                    raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
                task.status = data['status']
            if 'created_by' in data:
                task.created_by = data['created_by']

            # Save changes
            updated_task = self.repo.update_task(task)
            return {
                'id': updated_task.id,
                'code': updated_task.code,
                'title': updated_task.title,
                'description': updated_task.description,
                'deadline': updated_task.deadline.isoformat(),
                'status': updated_task.status,
                'created_by': updated_task.created_by,
                'created_at': updated_task.created_at.isoformat()
            }
        except Exception as e:
            raise Exception(f"Error updating task: {str(e)}")

    def delete_task(self, task_id):
        try:
            task = self.repo.get_task_by_id(task_id)
            if not task:
                raise ValueError("Task not found")
            self.repo.delete_task(task)
        except Exception as e:
            raise Exception(f"Error deleting task: {str(e)}")