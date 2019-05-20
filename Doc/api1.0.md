# API 1.0

host = 39.105.64.7

## index

描述：测试用API, 测试链接状态

url = /main/index

return: "hello"

## register

描述： 用户注册，接收一个json, 用来注册student,teacher, admin, company

url = /main/register

method = POST

传入参数：{

    type:  // 注册账户的类型, string, 备选项[student, teacher, admin, company]
    account:
    password:
    name:
    email:
    // 以上所有类型都需要提供， password为长度不低于12位的字符串， 类型都是string
    address: // student 和teacher 需要提供
    school:  // student 需要提供
}

return :

    {"msg":'注册参数存在错误'}, 400
    {'msg':'注册成功'}, 200

## login

描述：用户登陆，所有的类型共用这一个api

url = /main/login?account={account}&password={password}&role={role}

method = GET

参数：

    account: 用户的account
    password: 用户的password
    role: 登陆账户的角色，备选项：["student","teacher", "admin", "company"]

return:

    {'msg': 'no account'}, 401
    {'msg':"successful"}, 200

## logout

描述：用户退出登陆

url = /main/logout

method = GET

无传入参数， 但需要带上cookies

return:

    {'msg':'successful'}, 200
    {'msg':'退出登陆失败'}, 400

## add_course

描述：教师添加自己教学的科目到数据库中，添加完成后等待管理员审核, 传递一个json

url: /course/add_course

method:POST

参数：

{

    course_begin_date: 课程开始日期，string 类型，格式为 yyyy/mm/dd
    course_name:
    course_time: 上课的时间， string 类型，格式为h:min 24小时制
    course_last_time: 一节课持续时间，int 类型
    course_interval： 两节课之间的间隔时间， 类型int ,单位天
    course_total_times: 课程总课时， int类型
    price: 课程价格，int 类型
    course_type_id: 课程分类的对应分类id
}

return:

    {'msg':"添加失败，请检查上传数据"}, 400
    {'msg':"添加成功，等待审核"},200
    {'msg':"用户身份错误"}, 401

## get_course

描述：通关传递参数得到course

    GET course/get_courses?status=1
    POST a json about query_key world
    {keywords:[], query_word: {keyword1 = xxx,keyword2 = xxx, keyword3 = xxx }}
    select * from courses where keyword1=xx and keyword2 = xxx;

method: GET

得到不同状态的course

传入参数：
    status: 0 表示带审核 1 表示审核通过可选 2 表示不可选

返回结果：
    
    {'msg': "没有数据"}, 404
    
    {"data": [{
        'course_id': self.id,               // 课程id
        'course_name': self.course_name,    // 课程名
        'course_status': self.course_status,    // 课程的状态码
        'course_begin_date': self.course_begin_date,    // 开始上课的日期
        'course_time': self.course_time,    // 上课时间
        'course_last_time': self.course_last_time,  // 一节课持续时间
        'course_interval': self.course_interval,    // 课程间隔时间
        'course_total_times': self.course_total_times, // 总课程数
        'course_had_finish': self.number_had_finish, // 已经完成的课程数
        'course_price': self.price,
        'next_course':  // 下一节课开始的日期
        'teacher': {
                'id': self.id,
                'account': self.account,
                'email': self.email,
                'name': self.name,
                'address': self.address
                }     // 教师的信息
        'type': // 课程类型
        }]
    }

method: POST

得到满足传入条件的course

参数可选：course_id, course_name, course_type_id

返回和GET相同


## change_course_status

描述：改变课程的状态，待审核到审核（0->1), 审核不通过(0->2), 课程不可选(1->2)

url = /course/change_course_status

method = POST

传入参数:

    {
        course_id:
        orign_status:  // 源状态码，用来做同步验证
        aim_status:    // 目标状态码
    }

return:

    {'msg':'修改成功'}, 200
    {'msg': '参数错误'}, 400
    {'msg':'没有权限'}, 401

## choose course

描述：学生选择课程，在付费完成之后（可以不做）使用该API，在数据库中添加选择课程的信息

url = /main/choose_course?course_id=xxx&cost=xxx (xxx 是需要传入的参数，如果最后确实没有付费功能，cost=xxx就随便写个数字)

method = GET

传入参数:

    course_id: 学生选择的课程的id
    cost: 购买该课程的花费

return:

    {'msg':'选课成功'}, 200
    {'msg':'课程当前不存在'}, 404
    {'msg':'课程目前不可选'}, 400
    {'msg':'选课失败'},500
    {'msg':'身份不对，不能选课'},401  


## add_course_type

描述: teacher 或者 admin 向数据库中添加课程分类，可以添加一级分类和二级分类（需要提供parent_type_id）

url: /course/add_course/type

method = POST

传入参数：

    {
        type_name:
        parent_type_id:     如果添加的是一级分类，则没有这一项，如果是某个分类下面的子分类，这一项是该分类的id
    }

return:

    {'msg':"插入新的课程类型成功"}, 200
    {'msg':"插入课程类型失败"}, 400
    {'msg': '用户权限不对'}, 401

## my_schedule

描述: 获得学生已经选择的课程信息，课程信息同course, 只能在登陆状态下查看

url: /main/my_schedule

method = GET

return:

    {msg:  [
        {
            'course_id': self.id,               // 课程id
            'course_name': self.course_name,    // 课程名
            'course_status': self.course_status,    // 课程的状态码
            'course_begin_date': self.course_begin_date,    // 开始上课的日期
            'course_time': self.course_time,    // 上课时间
            'course_last_time': self.course_last_time,  // 一节课持续时间
            'course_interval': self.course_interval,    // 课程间隔时间
            'course_total_times': self.course_total_times, // 总课程数
            'course_had_finish': self.number_had_finish, // 已经完成的课程数
            'course_price': self.price,
            'next_course':  // 下一节课开始的日期
            'teacher': {
                    'id': self.id,
                    'account': self.account,
                    'email': self.email,
                    'name': self.name,
                    'address': self.address
                    }     // 教师的信息
            'type': // 课程类型
        }
        ]
    }, 200

## get_course_type

描述：获得课程类型的信息

url: /course/get_course_type?parent_type_id=

method = GET

参数说明：

    0： 获得所有父类型的课程类型
    某个具体的课程类型id，获取该课程类型的所有子类型

return：

    {
        "msg":[
            {
                "id":  该课程类型的id,
                "type_name": 该课程类型的名称,
                "parent_type" : {
                    "id":
                    "parent_type"
                    # 递归，直到最顶上的父类型，如果没有父类型，则没有这一项
                }
            }
        ]
    }