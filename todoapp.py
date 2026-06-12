from flask import Flask, request, render_template, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    slno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(600), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.slno} - {self.title}"

@app.route("/",methods=["GET","POST"])
def home():
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo=Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo=Todo.query.all()
    return render_template("home.html",allTodo=allTodo)

@app.route("/update/<int:slno>",methods=["POST","GET"])
def update(slno):
    todo=Todo.query.filter_by(slno=slno).first()
    if request.method=="POST":
        todo.title = request.form["title"]
        todo.desc = request.form["desc"]
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo)

@app.route("/delete/<int:slno>",methods=["POST","GET"])
def delete(slno):
    todo=Todo.query.filter_by(slno=slno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 