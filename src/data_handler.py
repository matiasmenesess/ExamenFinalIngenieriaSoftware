import json

class DataHandler:
    def __init__(self, filename='data.json'):
        self.filename = filename
        self.tasks = []
        self.users = []
        self.load_data()
    
    def save_data(self):
        data = {
            'tasks': self.tasks,
            'users': self.users
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.tasks = data.get('tasks', [])
                self.users = data.get('users', [])
        except FileNotFoundError:
            self.tasks = []
            self.users = []
    
    def get_user_by_alias(self, alias):
        for user in self.users:
            if user.get('email') == alias:
                return user
        return None
    
    def add_user(self, user):
        self.users.append(user)
        self.save_data()
    
    def get_tasks_by_user_alias(self, alias):
        assigned_tasks = []
        for task in self.tasks:
            task_users = task.get('usuarios', [])
            for user in task_users:
                if user.get('alias') == alias:
                    task_info = {
                        'id': task.get('id'),
                        'nombre': task.get('nombre'),
                        'descripcion': task.get('descripcion'),
                        'estado': task.get('estado'),
                        'rol': user.get('rol')
                    }
                    assigned_tasks.append(task_info)
                    break
        return assigned_tasks
    
    def add_task(self, task):
        self.tasks.append(task)
        self.save_data()
    
    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.get('id') == task_id:
                return task
        return None
    
    def update_task_state(self, task_id, new_state):
        for task in self.tasks:
            if task.get('id') == task_id:
                task['estado'] = new_state
                self.save_data()
                return True
        return False
    
    def user_has_role_in_task(self, task_id, user_alias, rol):
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        
        task_users = task.get('usuarios', [])
        for user in task_users:
            if user.get('alias') == user_alias and user.get('rol') == rol:
                return True
        return False
    
    def add_user_to_task(self, task_id, user_alias, rol):
        task = self.get_task_by_id(task_id)
        if task:
            if 'usuarios' not in task:
                task['usuarios'] = []
            task['usuarios'].append({'alias': user_alias, 'rol': rol})
            self.save_data()
            return True
        return False
    
    def remove_user_from_task(self, task_id, user_alias, rol):
        task = self.get_task_by_id(task_id)
        if task:
            task_users = task.get('usuarios', [])
            for i, user in enumerate(task_users):
                if user.get('alias') == user_alias and user.get('rol') == rol:
                    task_users.pop(i)
                    self.save_data()
                    return True
        return False
    
    def dependency_exists(self, task_id, dependency_task_id):
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        
        dependencies = task.get('dependencies', [])
        return dependency_task_id in dependencies
    
    def add_dependency(self, task_id, dependency_task_id):
        task = self.get_task_by_id(task_id)
        if task:
            if 'dependencies' not in task:
                task['dependencies'] = []
            task['dependencies'].append(dependency_task_id)
            self.save_data()
            return True
        return False
    
    def remove_dependency(self, task_id, dependency_task_id):
        task = self.get_task_by_id(task_id)
        if task:
            dependencies = task.get('dependencies', [])
            if dependency_task_id in dependencies:
                dependencies.remove(dependency_task_id)
                self.save_data()
                return True
        return False