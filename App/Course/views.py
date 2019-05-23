from flask_login import current_user, login_required
from flask import request, jsonify, make_response
from . import course_blueprint as course
from App.Model import *
from datetime import datetime
import json


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


def check_user_role(role_name):
    return current_user.role == role_name


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
        return make_response(json.dumps({'msg':msg},cls=CJsonEncoder),statue)
    if request.method == "POST":
        post_data = request.json
        keywords = post_data.get('keywords', [])
        query_word = post_data.get("query_word")
        res = CourseType.query
        for keyword in keywords:
            if keyword == "course_id":
                res = res.filter_by(id=query_word['course_id'])
                if res.count() == 1:
                    return make_response(json.dumps({'msg': res.dict()}, cls=CJsonEncoder), statue)
            if keyword == "course_name":
                res = res.filter_by(course_name=query_word['course_name'])
            if keyword == "course_type_id":
                res = res.filter_by(course_type_id=query_word['course_type_id'])
        if res.count() >0 :
            return make_response(json.dumps({'msg':[re.dict() for re in res.all()]},cls = CJsonEncoder),statue)
        else:
            return jsonify({'data': "没有数据"}), statue


# 改变course 的status, 审核通过课程0->1 or 课程审核不通过或者不可选0->2 or 1->2
@course.route("/change_course_status", methods=['POST'])
@login_required
def change_course_status():
    request_data = request.json
    if check_user_role("Admin"):
        try:
            course = Course.query.filter_by(id=request_data['course_id']).first()
            orign_status = request_data['orign_status']  # 做同步验证用
            aim_status = request_data['aim_status']  # 目标状态
            if orign_status == course.course_status and (orign_status, aim_status) in [(0,1),(0,2),(1,2)]:
                course.course_status = aim_status
                db.session.add(course)
                db.session.commit()
                return jsonify({'msg':'修改成功'}), 200
            else:
                return jsonify({'msg': '参数错误'}), 400
        except Exception as e:
            print(e)
            return jsonify({'msg': '参数错误'}), 400
    else:
        return jsonify({'msg':'没有权限'}), 401


# 增加course_type, /course/add_course_type, user_role is teacher and admin
@course.route("/add_course_type", methods=['POST'])
@login_required
def add_course_type():
    request_data = request.json
    print(current_user.account)
    if check_user_role("Teacher") or check_user_role("Admin"):
        type_name = request_data.get("type_name")
        parent_type_id = request_data.get("parent_type_id", None)
        new_course_type = CourseType(type_name=type_name,parent_type_id=parent_type_id)
        try:
            db.session.add(new_course_type)
            db.session.commit()
            return jsonify({'msg':"插入新的课程类型成功"})
        except Exception as e:
            return jsonify({'msg':"插入课程类型失败"}), 400
    else:
        return jsonify({'msg': '用户权限不对'}), 401

# 获取course_type信息,/course/get_course_type?parent_type_id=?
# 0 所有的父课程类型
# 某个父类型的id ，该类型下的所有子类型
@course.route("/get_course_type", methods=['GET'])
@login_required
def get_course_type():
    parent_id = request.args.get("parent_type_id", 0)
    all_type = CourseType.query.filter_by(parent_type_id=parent_id)
    if all_type.count() >0:
        types_result = [course_type.dict() for course_type in all_type]
        return make_response(json.dumps({"msg": types_result},cls=CJsonEncoder))
    else:
        return jsonify({'msg': "no course type"}), 404
