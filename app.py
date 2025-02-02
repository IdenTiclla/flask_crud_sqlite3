from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database/tasks.db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    done = db.Column(db.Boolean)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@app.route('/create_task',methods=['POST'])
def create():
    if request.method == 'POST':
        content = request.form.get("content")
        task = Task(content=content, done=False)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("index"))

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/done/<int:id>')
def done(id):
    task = Task.query.filter_by(id=id).first()
    task.done = not(task.done)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)