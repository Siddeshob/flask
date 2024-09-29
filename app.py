from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(255),nullable=False)
    completed=db.Column(db.Integer,default=0)
    date_created=db.Column(db.DateTime,default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id
@app.route("/",methods=['GET','POST'])
def hello():
    if request.method=='POST':
        task_content=request.form['content']
        new_task=todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print('something went wrong')
        finally:
            print(">>>>>>>>>>>>>>>>>>>Done")
    else:
        data = todo.query.all()
        print(data)
        return render_template('index.html',tasks=data)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_Delete=todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_Delete)
        db.session.commit()
        return redirect("/")
    except:
        return "not-Done"

@app.route("/update/<int:id>",methods=['GET','POST'])
def update(id):
    tasks=todo.query.get_or_404(id)
    if request.method=="POST":
        pass
    else:
        return render_template("update.html",task=tasks)



if __name__=="__main__":
    app.run(debug=True)