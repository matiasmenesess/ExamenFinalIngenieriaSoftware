import unittest
from models.usuario import Usuario
from models.tarea import Tarea
from models.asignacion import Asignacion

class TestModelos(unittest.TestCase):

    # ---------- PRUEBAS PARA USUARIO ----------

    def test_usuario_info(self):
        """
        ÉXITO:
        Verifica que get_user_info retorne los datos correctos
        """
        usuario = Usuario("U001", "Luis", "luis@test.com")
        info = usuario.get_user_info()
        self.assertEqual(info["id"], "U001")
        self.assertEqual(info["name"], "Luis")
        self.assertEqual(info["email"], "luis@test.com")

    def test_usuario_email_vacio(self):
        """
        ERROR:
        Se crea un usuario sin email y se verifica que esté vacío
        """
        usuario = Usuario("U002", "Ana", "")
        self.assertEqual(usuario.email, "")

    def test_usuario_acceso_directo(self):
        """
        COMPLEMENTARIO:
        Accede directamente a los atributos del usuario
        """
        usuario = Usuario("U003", "Carlos", "carlos@mail.com")
        self.assertEqual(usuario.id, "U003")
        self.assertEqual(usuario.name, "Carlos")

    def test_usuario_get_user_info_completo(self):
        """
        COMPLEMENTARIO:
        Verifica estructura completa retornada por get_user_info
        """
        usuario = Usuario("U004", "Julia", "julia@mail.com")
        expected = {
            "id": "U004",
            "name": "Julia",
            "email": "julia@mail.com"
        }
        self.assertEqual(usuario.get_user_info(), expected)

    # ---------- PRUEBAS PARA TAREA ----------

    def test_tarea_marcar_completada(self):
        """
        ÉXITO:
        Se marca una tarea como completada
        """
        tarea = Tarea("T001", "Test Tarea", "Descripción de prueba")
        tarea.mark_complete()
        self.assertEqual(tarea.status, "completed")

    def test_tarea_estado_invalido_manual(self):
        """
        ERROR:
        Se asigna manualmente un estado inválido
        """
        tarea = Tarea("T002", "Otra Tarea", "Detalle")
        tarea.status = "desconocido"
        self.assertNotIn(tarea.status, ["pending", "completed"])

    def test_tarea_datos_iniciales(self):
        """
        COMPLEMENTARIO:
        Verifica los datos iniciales de una tarea
        """
        tarea = Tarea("T003", "Inicial", "Algo")
        self.assertEqual(tarea.id, "T003")
        self.assertEqual(tarea.title, "Inicial")
        self.assertEqual(tarea.description, "Algo")
        self.assertEqual(tarea.status, "pending")

    def test_tarea_status_personalizado(self):
        """
        COMPLEMENTARIO:
        Crea tarea con estado personalizado
        """
        tarea = Tarea("T004", "Título", "Desc", status="en progreso")
        self.assertEqual(tarea.status, "en progreso")

    # ---------- PRUEBAS PARA ASIGNACIÓN ----------

    def test_asignacion_detalles(self):
        """
        ÉXITO:
        Verifica que get_assignment_details funcione correctamente
        """
        asignacion = Asignacion("T001", "U001")
        detalles = asignacion.get_assignment_details()
        self.assertEqual(detalles["task_id"], "T001")
        self.assertEqual(detalles["user_id"], "U001")

    def test_asignacion_ids_vacios(self):
        """
        ERROR:
        Se crean IDs vacíos en asignación
        """
        asignacion = Asignacion("", None)
        detalles = asignacion.get_assignment_details()
        self.assertEqual(detalles["task_id"], "")
        self.assertIsNone(detalles["user_id"])

    def test_asignacion_directa_acceso(self):
        """
        COMPLEMENTARIO:
        Accede directamente a los atributos de asignación
        """
        asignacion = Asignacion("T789", "U123")
        self.assertEqual(asignacion.task_id, "T789")
        self.assertEqual(asignacion.user_id, "U123")

    def test_asignacion_detalles_estructura(self):
        """
        COMPLEMENTARIO:
        Verifica estructura del diccionario retornado
        """
        asignacion = Asignacion("T555", "U999")
        expected = {"task_id": "T555", "user_id": "U999"}
        self.assertEqual(asignacion.get_assignment_details(), expected)

if __name__ == "__main__":
    unittest.main()
