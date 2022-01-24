from flask import Flask 
from flask_restful import Resource,Api,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
api=Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
db=SQLAlchemy(app)

class ToDoModel(db.Model):
    pk_bint_employee_master_id = db.Column(db.Integer, primary_key=True)
    vchr_employee_code = db.Column(db.String(5))
    vchr_employee_name = db.Column(db.String(50))
    dat_birth_date =  db.Column(db.String(15))
    vchr_contact_number = db.Column(db.String(15))
    dbl_basic_pay = db.Column(db.Float,nullable=False)
    dbl_basic_percentage = db.Column(db.Float,nullable=True)
    dbl_salary = db.Column(db.Float)

#uncomment this while running the application for the first time
#db.create_all()

resouce_fields={
    'pk_bint_employee_master_id':fields.Integer,
    'vchr_employee_code':fields.String,
    'vchr_employee_name':fields.String,
    'dat_birth_date' :fields.String,
    'vchr_contact_number' :fields.String,
    'dbl_basic_pay' :fields.Float,
    'dbl_basic_percentage' :fields.Float,
    'dbl_salary' :fields.Float 
}


task_post_args=reqparse.RequestParser()  #Fields in which input must be done mandatorily

task_post_args.add_argument("vchr_employee_code",type=str,help="This field is required",required=True)
task_post_args.add_argument("vchr_employee_name",type=str,help="This field is required",required=True)
task_post_args.add_argument("dat_birth_date",type=str,help="This field is required",required=True)
task_post_args.add_argument("vchr_contact_number",type=str,help="This field is required",required=True)
task_post_args.add_argument("dbl_basic_pay",type=float,help="This field is required",required=True)
task_post_args.add_argument("dbl_basic_percentage",type=float,help="This field is required",required=True)
#task_post_args.add_argument("dbl_salary",type=float,help="This field is required",required=True)


task_put_args=reqparse.RequestParser()

task_post_args.add_argument("vchr_employee_code",type=str)
task_post_args.add_argument("vchr_employee_name",type=str)
task_post_args.add_argument("dat_birth_date",type=str)
task_post_args.add_argument("vchr_contact_number",type=str)
task_post_args.add_argument("dbl_basic_pay",type=float)
task_post_args.add_argument("dbl_basic_percentage",type=float)


class ToDoList(Resource):
    
    def get(self):
        table=ToDoModel.query.all()
        todos={}
        for task in table:
            todos[task.pk_bint_employee_master_id]={"vchr_employee_code":task.vchr_employee_code,"vchr_employee_name":task.vchr_employee_name,"dat_birth_date":task.dat_birth_date,"vchr_contact_number":task.vchr_contact_number,"dbl_basic_pay":task.dbl_basic_pay,"dbl_basic_percentage":task.dbl_basic_percentage,"dbl_salary":task.dbl_salary}
        return todos

class ToDo(Resource):
    @marshal_with(resouce_fields)  #To parse the data in a defined order.
    def get(self,employee_id):
        task=ToDoModel.query.filter_by(pk_bint_employee_master_id=employee_id).first()  #checking if the data is present in db
        if not task:
            abort(403,descrption="Bad Request")
        return task

    @marshal_with(resouce_fields)  #Used for parsing.
    def post(self,employee_id):
        args=task_post_args.parse_args()  #These are the values which are passed in body(POSTMAN)
        task=ToDoModel.query.filter_by(pk_bint_employee_master_id=employee_id).first()
        if task:
            abort(409,descrption="This task already exits")
        bp = args["dbl_basic_pay"]
        allw = args["dbl_basic_percentage"]
        salary = bp * (1 + (allw/100))
        todos=ToDoModel(pk_bint_employee_master_id=employee_id,vchr_employee_code=args["vchr_employee_code"],vchr_employee_name=args["vchr_employee_name"],dat_birth_date=args["dat_birth_date"],vchr_contact_number=args["vchr_contact_number"],dbl_basic_pay=args["dbl_basic_pay"],dbl_basic_percentage=args["dbl_basic_percentage"],salary=salary)  
        db.session.add(todos)   #Adding values to table
        db.session.commit()   #Commiting
        return todos   #Displays the recently added values
    @marshal_with(resouce_fields)
    def put(self,employee_id):
        args=task_put_args.parse_args()
        table=ToDoModel.query.filter_by(pk_bint_employee_master_id=employee_id).first()
        if not table:
            abort(403, message="This task doesn't exist")
        if args["vchr_employee_code"]:
            table.vchr_employee_code=args["vchr_employee_code"]
        if args["vchr_employee_name"]:
            table.vchr_employee_name=args["vchr_employee_name"]
        if args["dat_birth_date"]:
            table.dat_birth_date=args["dat_birth_date"]
        if args["vchr_contact_number"]:
            table.vchr_contact_number=args["vchr_contact_number"]
        if args["dbl_basic_pay"]:
            table.dbl_basic_pay=args["dbl_basic_pay"]
        if args["dbl_basic_percentage"]:
            table.dbl_basic_percentage=args["dbl_basic_percentage"]
        bp = args["dbl_basic_pay"]
        allw = args["dbl_basic_percentage"]
        salary = bp * (1 + (allw/100))
        table.salary=salary
        db.session.commit()
        return table

    def delete(self,employee_id):
        table=ToDoModel.query.filter_by(pk_bint_employee_master_id=employee_id).first()
        if not table:
            abort(403,message="Task doesn't exist")
        db.session.delete(table)
        return 'Todo Deleted Successfully'


api.add_resource(ToDoList,'/todo')  #Call goes to ToDo List Class
api.add_resource(ToDo,'/todo/<int:employee_id>')  #Call goes to specific row

if __name__=='__main__':
    app.run(debug=True)
