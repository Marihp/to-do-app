# Importar dependencias de Flask
from flask import (
    Flask,
    request,
    redirect,
    render_template,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy


# Crear instancia app Flask
app = Flask(__name__)

# Configurar la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Crear instancia de la base de datos
db = SQLAlchemy(app)


# Crear modelo de la base de datos
class Todo_list(db.Model):
    # Crear columnas de la base de datos
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    completed = db.Column(db.Boolean)


# Crear todas las tablas de la base de datos
with app.app_context():
    db.create_all()


# Ruta principal
@app.route("/")
def index():
    """Página principal de la aplicación.
    Toma todas las tareas de la base de datos

    Retorna:
        HTML: Plantilla index.html
    """

    # Obtener todas las tareas de la base de datos
    todo_list = db.session.query(Todo_list).all()

    # Renderizar la plantilla index.html
    return render_template("index.html", todo_list=todo_list)


# Ruta para agregar tareas
@app.route("/add", methods=["POST"])
def add():
    """Agregar tareas a la base de datos.
    Recibe el contenido de la tarea desde el formulario de la página principal
    y lo agrega a la base de datos.

    Retorna:
        Redireccion: Redirecciona a la página principal
    """

    # Obtener el contenido de la tarea desde el formulario
    todo = request.form.get("todo")

    # Crear una nueva tarea
    new_todo = Todo_list(content=todo, completed=False)

    # Agregar la nueva tarea a la base de datos
    db.session.add(new_todo)

    # Guardar los cambios en la base de datos
    db.session.commit()

    # Redireccionar a la página principal
    return redirect(url_for("index"))


# Ruta para marcar tareas como completadas
@app.route("/complete/<int:todo_id>")
def complete(todo_id):
    """Marcar tareas como completadas.
    Recibe el id de la tarea desde la página principal y lo marca como
    completado en la base de datos.

    Args:
        todo_id (int): Id de la tarea

    Retorna:
        Redireccion: Redirecciona a la página principal
    """

    # Obtener la tarea desde la base de datos
    todo = Todo_list.query.filter_by(id=todo_id).first()

    # Marcar la tarea como completada
    todo.completed = True

    # Guardar los cambios en la base de datos
    db.session.commit()

    # Redireccionar a la página principal
    return redirect(url_for("index"))


# Ruta para eliminar tareas
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    """Eliminar tareas.
    Recibe el id de la tarea desde la página principal y la elimina de la
    base de datos.

    Args:
        todo_id (int): Id de la tarea

    Retorna:
        Redireccion: Redirecciona a la página principal
    """

    # Obtener la tarea desde la base de datos
    todo = Todo_list.query.filter_by(id=todo_id).first()

    # Eliminar la tarea de la base de datos
    db.session.delete(todo)

    # Guardar los cambios en la base de datos
    db.session.commit()

    # Redireccionar a la página principal
    return redirect(url_for("index"))
