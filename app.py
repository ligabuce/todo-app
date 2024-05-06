from flask import Flask, render_template, request, redirect, url_for
from turbo_flask import Turbo
from todos_model import Todo

app = Flask(__name__, template_folder="templates")
turbo = Turbo(app)

todos = [Todo(task="Piemēra uzdevums", status=False),
         Todo(task="Izdarīts piemēra uzdevums", status=True)]

def get_todo_by_id(id):
    todo = [todo for todo in todos if todo.id == id]
    if todo:
        return todo[0]
    else:
        return None

@app.route("/")
def index():
    return render_template("layout.html", todos=todos)

@app.route("/todo/add", methods=["POST"])
def add():
    todo = Todo(request.form['task'])
    todos.append(todo)
    return redirect(url_for("index"))

@app.route("/todo/<id>/edit", methods=["GET", "POST"])
def edit(id):
    todo = get_todo_by_id(id)
    if request.method == "POST":
        todo.task = request.form['task']
        return redirect(url_for('index'))
    else:
        return render_template("todo_edit.html", todo=todo)

@app.route("/todo/<id>/check", methods=["PATCH"])
def check(id):
    todo = get_todo_by_id(id)
    todo.status = not todo.status
    return render_template("todo_task.html", todo=todo)

@app.route("/todo/<id>", methods=["DELETE"])
def delete(id):
    todo = get_todo_by_id(id)
    todos.remove(todo)
    return redirect(url_for("index"), 303)

if __name__ == '__main__':
    app.run(debug=True)
