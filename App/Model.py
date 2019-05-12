from flask_login import UserMixin, AnonymousUserMixin, LoginManager
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask import g, current_app

db = SQLAlchemy()
login_manager = LoginManager()

# 继承UserMixin 和 AnonymousUserMixin 来实现flask_login
class User(UserMixin, AnonymousUserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(300), unique=False)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(30), unique=False)


class Student(db.Model, User):
    __tablename__ = "students"
    address = db.Column(db.String(120))
    school = db.Column(db.String(120))


class Teacher(db.Model, User):

    __tablename__ = "teachers"
    address = db.Column(db.String(120))
    company_id = db.Column(db.Integer, nullable=True)

    def dict(self):
        return {
            'id': self.id,
            'account': self.account,
            'email': self.email,
            'name': self.name,
            'address': self.address
        }


class Admin(db.Model, User):
    __tablename__ = "admin"


class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    account = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    name = db.Column(db.String(32))


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(32), unique=True)
    course_status = db.Column(db.Integer, default=0)  # 0 表示带审核 1 表示审核通过可选 2 表示不可选
    course_begin_date = db.Column(db.DATETIME)  # 课程开始的日期
    course_time = db.Column(db.String(32))  # 课程上课的时间, 格式为h:min 24小时制
    course_last_time = db.Column(db.Integer)  # 一节课持续时间
    course_interval = db.Column(db.Integer)  # 两节课之间的间隔时间
    course_total_times = db.Column(db.Integer)  # 总课时
    number_had_finish = db.Column(db.Integer, default=0)  # 已经完成的课时数，默认是0，上完一次课老师和学生都确认后加一
    price = db.Column(db.Float, nullable=False, default=0.0)  # 课程的价格
    teacher_id = db.Column(db.Integer, unique=False, nullable=False)
    course_type_id = db.Column(db.Integer, unique=False, nullable=False)  # 课程所属类型的id

    # 如果课时已经上完则返回None,否则返回下一次上课的日期
    def next_course(self):
        if self.number_had_finish < self.course_total_times:
            need_day = self.number_had_finish * self.course_interval
            next_day = self.course_begin_date + timedelta(days = need_day)
            return next_day
        return None

    def dict(self):
        course = {
            'course_id': self.id,
            'course_name': self.course_name,
            'course_status': self.course_status,
            'course_begin_date': self.course_begin_date,
            'course_time': self.course_time,
            'course_last_time': self.course_last_time,
            'course_interval': self.course_interval,
            'course_total_times': self.course_total_times,
            'course_had_finish': self.number_had_finish,
            'course_price': self.price,
        }
        next_course = self.next_course()
        if next_course is not None:
            course['next_course'] = next_course
        teacher = Teacher.query.filter_by(id=self.teacher_id)
        if teacher.count() == 1:
            course['teacher'] = teacher.dict()
        course_type = CourseType.query.filter_by(id=self.course_type_id)
        if course_type.count() == 1:
            course['type'] = course_type.dict()
        return course




class CourseType(db.Model):
    __tablename__ = "coursetypies"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(32), unique=True)
    parent_type_id = db.Column(db.Integer, nullable=True)  # 父类型

    def dict(self):
        re = {
            'id': self.id,
            'type_name': self.type_name,
        }
        parent_type = CourseType.query.filter_by(id=self.parent_type_id)
        if parent_type.count() == 1:
            parent_type = parent_type.first().dict()
            re['parent_type'] = parent_type
        else:
            return re



class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commenter_id = db.Column(db.Integer, nullable=False)  # 评论者的id
    commented_id = db.Column(db.Integer, nullable=False)  # 被评论者的id
    content = db.Column(db.Text, nullable=False)  # 评论的内容
    # 评论的类型
    # 1 student to teacher. 2 student to course. 3 teacher to company
    comment_type = db.Column(db.Integer, nullable=False)


class Report(db.Model):
    __tablename__ = "reports"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reporter = db.Column(db.Integer, nullable=False)  # 举报者
    reported = db.Column(db.Integer, nullable=False)  # 被举报者
    # 举报类型
    report_type = db.Column(db.Integer, nullable=False)
    report_result = db.Column(db.TEXT, nullable=False, default="已接受举报，等待管理员处理")
    admin = db.Column(db.Integer, nullable=False)  # 处理的管理员


class ChooseCourse(db.Model):
    __tablename__ = "choosecourses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False, default=0.0)


@login_manager.user_loader
def user_load(user_id):
    # user is student
    user = Student.query.filter_by(id=user_id).first()
    if user is not None:
        return user
    # user is teacher
    user = Teacher.query.filter_by(id=user_id).first()
    if user is not None:
        return user
    # user is admin
    user = Admin.query.filter_by(id=user_id).first()
    if user is not None:
        return user
    # user is company
    user = Company.query.filter_by(id=user_id).first()
    if user is not None:
        return user


class AnonymousUser(AnonymousUserMixin):
    def can(self):
        return False

    def is_admin(self):
        return False