from . import main_blueprint
from flask import request, make_response, current_app, jsonify
import json
from App.Model import db, Student, Teacher, Admin, Company, Course, ChooseCourse
from flask_login import current_user, login_user, logout_user, login_required
from App.Course.views import CJsonEncoder

def check_user_role(role_name):
    return current_user.role == role_name


@main_blueprint.route("/index")
def index():
    print(current_user)
    return "ok"


@main_blueprint.route("/register", methods=['POST'])
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
                school=data.get("school"),
                role="Student"
            )
            db.session.add(new_student)
            db.session.commit()
            return make_response(json.dumps({'msg': '注册成功'}))
        if data.get('type') == "teacher":
            new_teacher = Teacher(
                account=data.get("account"),
                password=data.get("password"),
                name=data.get("name"),
                email=data.get("email"),
                address=data.get("address"),
                role="Teacher"
            )
            db.session.add(new_teacher)
            db.session.commit()
            return make_response(json.dumps({'msg': '注册成功'}))
        if data.get("type") == "admin":
            new_admin = Admin(
                account=data.get("account"),
                password=data.get("password"),
                name=data.get("name"),
                email=data.get("email"),
                role="Admin"
            )
            db.session.add(new_admin)
            db.session.commit()
            return make_response(json.dumps({'msg': '注册成功'}))
        if data.get("type") == "company":
            new_company = Company(
                account=data.get("account"),
                password=data.get("password"),
                name=data.get('name')
            )
            db.session.add(new_company)
            db.session.commit()
            return make_response(json.dumps({'msg': '注册成功'}))
        return make_response(json.dumps({"msg":"参数错误"}))
    except Exception as e:
        print(e)
        db.session.rollback()
        print("register failure")
        return make_response(json.dumps({"msg":'注册参数存在错误'}), 400)



def login_contral(user, password):
    if user is None:
        # log no user
        return make_response(json.dumps({'msg': 'no account'}), 401)
    if user.password == password:
        login_user(user, remember=True)
        print(current_user)
        return json.dumps({'msg':"successful"})


@main_blueprint.route("/login", methods=['POST'])
def login():
    data = request.json
    if data is None:
        return jsonify({"msg":"没有收到任何数据"}), 400
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


# /main/choose_course?course_id=xxx&cost=xxx
@main_blueprint.route("/choose_course", methods=['GET'])
@login_required
def choose_course():
    if check_user_role("Student"):
        course_id = request.args.get("course_id")
        cost = request.args.get("cost")
        # check course 
        aim_course = Course.query.filter_by(id=course_id).first()
        if aim_course is None:
            return jsonify({'msg': '课程当前不存在'}), 404
        if aim_course.course_status != 1:
            return jsonify({'msg': '课程目前不可选'}), 400
        new_choose_course = ChooseCourse(student_id=current_user.id, course_id=course_id,cost=cost)
        try:
            db.session.add(new_choose_course)
            db.session.commit()
            return jsonify({'msg': '选课成功'}), 200
        except Exception as e:
            print(e)
            return jsonify({'msg': '选课失败'}),500
    else:
        return jsonify({'msg': '身份不对，不能选课'}),401


@main_blueprint.route("/my_schedule", methods=['GET'])
@login_required
def my_schedule():
    if check_user_role("Student"):
        all_schedule = ChooseCourse.query.filter_by(student_id=current_user.id)
        effective_course_ids = [schedule.course_id for schedule in all_schedule.all() if schedule.course_status == 1]
        effective_courses = [effective_course.dict() for effective_course in
                             Course.query.filter(Course.id.in_(effective_course_ids)).all()]
        return make_response(json.dumps({'msg': effective_courses},cls = CJsonEncoder))
    
