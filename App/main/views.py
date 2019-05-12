from . import main_blueprint
from flask import request, make_response, current_app
import json
from App.Model import db, Student, Teacher, Admin, Company
from flask_login import current_user, login_user, logout_user, login_required


@main_blueprint.route("/index")
@login_required
def index():
    return "hello"


@main_blueprint.route("register", methods=['POST'])
def register():
    # 可以直接得到处理后的json
    data = request.json
    print(data)

    # register student
    try:
        if data.get('type') == "student":
            new_student = Student(
                account=data.get("account"),
                password=data.get("password"),
                name=data.get("name"),
                email=data.get("email"),
                address=data.get("address"),
                school=data.get("school")
            )
            db.session.add(new_student)
            db.session.commit()
        if data.get('type') == "teacher":
            new_teacher = Teacher(
                account=data.get("account"),
                password=data.get("password"),
                name=data.get("name"),
                email=data.get("email"),
                address=data.get("address")
            )
            db.session.add(new_teacher)
            db.session.commit()
        if data.get("type") == "admin":
            new_admin = Admin(
                account=data.get("account"),
                password=data.get("password"),
                name=data.get("name"),
                email=data.get("email"),
            )
            db.session.add(new_admin)
            db.session.commit()
        if data.get("type") == "company":
            new_company = Company(
                account=data.get("account"),
                password=data.get("password"),
                name=data.get('name')
            )
            db.session.add(new_company)
            db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        print("register failure")
        return make_response(json.dumps({"msg":'注册参数存在错误'}), 400)
    return make_response(json.dumps({'msg':'注册成功'}))


def login_contral(user, password):
    if user is None:
        # log no user
        return make_response(json.dumps({'msg': 'no account'}), 401)
    if user.password == password:
        login_user(user, remember=True)
        return json.dumps({'msg':"successful"})


@main_blueprint.route("login", methods=['GET'])
def login():
    data = request.args
    account = data['account']
    password = data['password']
    role = data['role']   # student, teacher, admin or company
    if role == "student":
        user = Student.query.filter_by(account=account).first()
        res = login_contral(user, password)
        print(current_user)
        return res
    if role == "teacher":
        user = Teacher.query.filter_by(account=account).first()
        return login_contral(user,password)
    if role == "admin":
        user = Admin.query.filter_by(account=account).first()
        return login_contral(user,password)
    if role == "company":
        user = Company.query.filter_by(account=account).first()
        return login_contral(user, password)
    return "ok"


@main_blueprint.route("logout", methods=['GET'])
def logout():
    try:
        print(current_user)
        logout_user()
        return make_response(json.dumps({'msg':'successful'}))
    except Exception as e:
        # log
        return make_response(json.dumps({'msg':'退出登陆失败'}), 400)



