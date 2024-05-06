from flask import Flask, render_template, request, redirect, url_for
from turbo_flask import Turbo
from todos_model import Todo

app = Flask(__name__, template_folder = "templates")
turbo = Turbo(app) #NEW ADD

todos = [Todo(task="Piemēra uzdevums", status=False), 
         Todo(task="Izdarīts piemēra uzdevums", status=True)]

def get_todo_by_id(id):
    todo = [todo for todo in todos if todo.id == id]
    if todo:
        return todo[0]
    else:
        return None 
    
# Return None if no todo item with the specified id is found


#defining the root endpoint as in what opens first in the app/open the link
@app.route("/") 
def index():
    return render_template("layout.html", todos=todos) #passing the html file for the root, passing the todo list so it can render and display them

#defining add function with POST method
@app.route("/todo/add", methods=["POST"]) 
def add():
    todo = Todo(request.form['task'])
    todos.append(todo)
    return redirect(url_for("index"))

#defining edit function
@app.route("/todo/<id>/edit", methods=["GET", "POST"]) 
def edit(id):
    todo = get_todo_by_id(id)
    if request.method == "POST":
        todo.task = request.form['task']
        return redirect(url_for('index'))
    else:
        return render_template("todo_edit.html", todo=todo)
    
#defining check function 
@app.route("/todo/<id>/check", methods=["PATCH"])
def check(id):
    todo = get_todo_by_id(id)
    todo.status = not todo.status
    return render_template("todo_task.html", todo=todo)

#defining delete function
@app.route("/todo/<id>", methods=["DELETE"]) #bc of htmx can use delete method
def delete(id):
    todo = get_todo_by_id(id)
    todos.remove(todo)
    return redirect(url_for("index"), 303) #The response code is now a 303. it will issue a GET to the new location.
#if i dont use 303, even if i click delete, the task doesnt dissapier until i refresh the page
if __name__ == '__main__':
    app.run(debug=True)