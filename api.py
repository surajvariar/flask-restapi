from flask import Flask 
from flask_restful import Resource,Api,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
api=Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db=SQLAlchemy(app)

class ToDoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(50))
    summary = db.Column(db.String(255))


#uncomment this while running the application for the first time
#db.create_all()

resouce_fields={
    'id':fields.Integer,
    'task':fields.String,
    'summary':fields.String
}

task_post_args=reqparse.RequestParser()

task_post_args.add_argument("task",type=str,help="This field is required",required=True)
task_post_args.add_argument("summary",type=str,help="This field is required",required=True)

task_put_args=reqparse.RequestParser()

task_put_args.add_argument("task",type=str)
task_put_args.add_argument("summary",type=str)

class ToDoList(Resource):
    
    def get(self):
        tasks=ToDoModel.query.all()
        todos={}
        for task in tasks:
            todos[task.id]={"task":task.task,"summary":task.summary}
        return todos

class ToDo(Resource):
    @marshal_with(resouce_fields)
    def get(self,todo_id):
        task=ToDoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(403,descrption="Bad Request")
        return task

    @marshal_with(resouce_fields)
    def post(self,todo_id):
        args=task_post_args.parse_args()
        task=ToDoModel.query.filter_by(id=todo_id).first()
        if task:
            abort(409,descrption="This task already exits")
        todos=ToDoModel(id=todo_id,task=args["task"],summary=args["summary"])
        db.session.add(todos)
        db.session.commit()
        return todos
    @marshal_with(resouce_fields)
    def put(self,todo_id):
        args=task_put_args.parse_args()
        task=ToDoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(403, message="Todo Id doesnt exist")
        if args["task"]:
            task.task=args["task"]
        if args["summary"]:
            task.summary=args["summary"]
        db.session.commit()
        return task
    def delete(self,todo_id):
        task=ToDoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(403,message="Todo id doesnt exist")
        db.session.delete(task)
        return 'Todo Deleted Successfully'


api.add_resource(ToDoList,'/todo')
api.add_resource(ToDo,'/todo/<int:todo_id>')

if __name__=='__main__':
    app.run(debug=True) 
