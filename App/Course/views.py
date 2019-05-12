from flask_login import current_user, login_required
from flask import request, jsonify
from . import course_blueprint as course
from App.Model import *
from datetime import datetime


def check_user_role(role_name):
    return type(current_user).__name__ == role_name


@course.route("/add_course", methods=['POST'])
@login_required
def add_course():
    course_data = request.json
    msg = ""
    statue = 200
    if check_user_role("Teacher"):
        # 教师创建课程
        # 提交给管理员审核
        try:
            # 得到参数的begin_date = yyyy/mm/dd
            begin_date_args = course_data['course_begin_date'].split("/")
            begin_date = datetime(begin_date_args[0],begin_date_args[1],begin_date_args[2])
            new_course = Course(
                course_name=course_data['course_name'],
                course_begin_date=begin_date,
                teacher_id=current_user.id,
                course_time=course_data['course_time'],
                course_last_time=course_data['course_last_time'],
                course_interval=course_data['course_interval'],
                course_total_times=course_data['course_total_times'],
                price=course_data['price'],
                course_type_id=course_data['course_type_id']
            )
            db.session.add(new_course)
            db.session.commit()
            msg = "添加成功，等待审核"
        except Exception as e:
            print(e)
            db.session.rollback()
            statue = 400
            msg = "添加失败，请检查上传数据"
        return jsonify({'msg': msg}), statue
    else:
        msg = "用户身份错误"
        statue = 401
        return jsonify({'msg': msg}), statue


# GET course/get_courses?status=1
# POST a json about query_key world
# {keywords:[], query_word: {keyword1 = xxx,keyword2 = xxx, keyword3 = xxx }}
# select * from courses where keyword1=xx and keyword2 = xxx;
@course.route("/get_courses")
@login_required
def get_course():
    statue = 200
    if request.method == "GET":
        status = request.args.get("status",1)
        result = Course.query.filter_by(course_status=status)
        if result.count() == 0:
            msg = "没有数据"
            statue = 404
        else:
            msg = [res.dict() for res in result.all()]
        return jsonify({'data', msg}), statue
    if request.method == "POST":
        post_data = request.json
        keywords = post_data.get('keywords', [])
        query_word = post_data.get("query_word")
        res = CourseType.query
        for keyword in keywords:
            if keyword == "course_id":
                res = res.filter_by(id=query_word['course_id'])
                if res.count() == 1:
                    return jsonify({'data': res.first().dict()}), statue
            if keyword == "course_name":
                res = res.filter_by(course_name=query_word['course_name'])
            if keyword == "course_type_id":
                res = res.filter_by(course_type_id=query_word['course_type_id'])
        if res.count() >0 :
            return jsonify({'data': [res.first().dict()]}), statue
        else:
            return jsonify({'data': "没有数据"}), statue





