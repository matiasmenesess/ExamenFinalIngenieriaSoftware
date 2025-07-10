from flask import Flask, jsonify, request
from data_handler import DataHandler
import uuid

app = Flask(__name__)
data_handler = DataHandler()

class TaskController:
    def __init__(self, data_handler):
        self.data_handler = data_handler

@app.route('/dummy', methods=['GET'])
def dummy_endpoint():
    return jsonify({"message": "This is a dummy endpoint!"})

@app.route('/usuarios', methods=['GET'])
def get_user_by_alias():
    alias = request.args.get('mialias')
    if not alias:
        return jsonify({"error": "Falta el alias"}), 400
    
    user = data_handler.get_user_by_alias(alias)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    assigned_tasks = data_handler.get_tasks_by_user_alias(alias)
    
    user_data = {
        "id": user.get('id'),
        "name": user.get('name'),
        "email": user.get('email'),
        "assigned_tasks": assigned_tasks
    }
    
    return jsonify(user_data), 200

@app.route('/usuarios', methods=['POST'])
def create_user():
    try:
        
        data = request.get_json()
        
        if not data or 'contacto' not in data or 'nombre' not in data:
            return jsonify({"error": "Both 'Falta o el contacto (email) o el nombre "}), 422
        
        contacto = data['contacto']
        nombre = data['nombre']
        
        if data_handler.get_user_by_alias(contacto):
            return jsonify({"error": "Usuario ya existe"}), 403
        
        user_id = str(uuid.uuid4())
        new_user = {
            "id": user_id,
            "name": nombre,
            "email": contacto
        }
        
        data_handler.add_user(new_user)
        
        return jsonify({"id": user_id, "message": "Usuario creado exitosamente"}), 201
        
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return jsonify({"error": "Contenido no procesable"}), 422

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['nombre', 'descripcion', 'usuario', 'rol']):
            return jsonify({"error": "Se requieren los siguientes campos: nombre, descripcion, usuario, rol"}), 422
        
        nombre = data['nombre']
        descripcion = data['descripcion']
        usuario = data['usuario']
        rol = data['rol']
        
        valid_roles = ['programador', 'pruebas', 'infra']
        if rol not in valid_roles:
            return jsonify({"error": f"Rol invalido, el rol debe ser uno de estos: {', '.join(valid_roles)}"}), 422
        
        if not data_handler.get_user_by_alias(usuario):
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        task_id = str(uuid.uuid4())
        new_task = {
            "id": task_id,
            "nombre": nombre,
            "descripcion": descripcion,
            "estado": "Nueva",
            "usuarios": [{"alias": usuario, "rol": rol}],
            "dependencies": []
        }
        
        data_handler.add_task(new_task)
        
        return jsonify({"id": task_id}), 201
        
    except Exception as e:
        return jsonify({"error": "Invalid JSON data"}), 422

@app.route('/tasks/<task_id>', methods=['POST'])
def change_state(task_id):
    try:
        data = request.get_json()
        
        if not data or 'estado' not in data:
            return jsonify({"error": "Falta el campo'estado'."}), 422
        
        nuevo_estado = data['estado']
        
        task = data_handler.get_task_by_id(task_id)
        if not task:
            return jsonify({"error": "Task no encontrada"}), 404
        
        valid_states = ['Nueva', 'En Progreso', 'Finalizada']
        if nuevo_estado not in valid_states:
            return jsonify({"error": f"Estado invalido, debe ser uno de estos: {', '.join(valid_states)}"}), 422
        
        if task.get('estado') == 'Finalizada' and nuevo_estado == 'Nueva':
            return jsonify({"error": "No se puede cambiar el estado de 'Finalizada' a 'Nueva'"}), 422
        
        data_handler.update_task_state(task_id, nuevo_estado)
        
        return jsonify({"message": "Tarea actualizada exitosamente"}), 200
        
    except Exception as e:
        return jsonify({"error": "Json invalido"}), 422

@app.route('/tasks/<task_id>/users', methods=['POST'])
def manage_task_users(task_id):
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['usuario', 'rol', 'accion']):
            return jsonify({"error": "Se requieren estos campos: usuario, rol, accion"}), 422
        
        usuario = data['usuario']
        rol = data['rol']
        accion = data['accion']
        
        valid_roles = ['programador', 'pruebas', 'infra']
        if rol not in valid_roles:
            return jsonify({"error": f"Rol invalido, debe ser uno de estos: {', '.join(valid_roles)}"}), 422
        
        valid_actions = ['adicionar', 'remover']
        if accion not in valid_actions:
            return jsonify({"error": f"Accion invalido, debe ser uno de estos: {', '.join(valid_actions)}"}), 422

        task = data_handler.get_task_by_id(task_id)
        if not task:
            return jsonify({"error": "Task no encontrada"}), 404
        
        if not data_handler.get_user_by_alias(usuario):
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        if accion == 'adicionar':
            if data_handler.user_has_role_in_task(task_id, usuario, rol):
                return jsonify({"error": "El usuario ya tiene este rol en la task."}), 422
            
            data_handler.add_user_to_task(task_id, usuario, rol)
            return jsonify({"message": "Usuario añadido a la task exitosamente."}), 200
            
        elif accion == 'remover':
            if not data_handler.user_has_role_in_task(task_id, usuario, rol):
                return jsonify({"error": "El usuario no tiene este rol en la task"}), 422
            
            data_handler.remove_user_from_task(task_id, usuario, rol)
            return jsonify({"message": "Usuario removido de la task exitosamente"}), 200
        
    except Exception as e:
        return jsonify({"error": "Json invalido"}), 422

@app.route('/tasks/<task_id>/dependencies', methods=['POST'])
def add_dependency(task_id):
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['dependencytaskid', 'accion']):
            return jsonify({"error": "Todos los campos son requeridos: dependencytaskid, accion"}), 422
        
        dependency_task_id = data['dependencytaskid']
        accion = data['accion']
        
        valid_actions = ['adicionar', 'remover']
        if accion not in valid_actions:
            return jsonify({"error": f"Accion invalida, debe ser una de estas: {', '.join(valid_actions)}"}), 422
        
        task = data_handler.get_task_by_id(task_id)
        if not task:
            return jsonify({"error": "Task no encontrada"}), 404
        
        dependency_task = data_handler.get_task_by_id(dependency_task_id)
        if not dependency_task:
            return jsonify({"error": "Dependencias de tareas no encontradas"}), 404
        
        if task_id == dependency_task_id:
            return jsonify({"error": "Una task no puede depender de si misma"}), 422
        
        if accion == 'adicionar':
            if data_handler.dependency_exists(task_id, dependency_task_id):
                return jsonify({"error": "Dependencia ya existe"}), 422
            
            data_handler.add_dependency(task_id, dependency_task_id)
            return jsonify({"message": "Dependencia añadida exitosamente"}), 200
            
        elif accion == 'remover':
            if not data_handler.dependency_exists(task_id, dependency_task_id):
                return jsonify({"error": "La dependencia no existe"}), 422
            
            data_handler.remove_dependency(task_id, dependency_task_id)
            return jsonify({"message": "Dependencia removida exitosamente"}), 200
        
    except Exception as e:
        return jsonify({"error": "Json invalido"}), 422

if __name__ == '__main__':
    app.run(debug=True)