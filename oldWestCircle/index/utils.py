import json
import random

from index.models import Student, Teacher, Mysession
from utils import get_current_time, hash_password


def check_login(phone_number, password, login_type):
    if not all([phone_number, password, login_type]):
        return None, None

    # # 对于 student 与 teacher ，可使用 register_time 作为 salt
    # password = hash_password(password, register_time)

    elif login_type == 'student':
        try:
            student = Student.objects.get(phonenumber=phone_number, userpd=password)
        except Student.DoesNotExist:
            student = None

        if student is not None:
            student_id = student.studentid
            return 'student', student_id

    elif login_type == 'teacher':
        try:
            teacher = Teacher.objects.get(phonenumber=phone_number, userpd=password)
        except Teacher.DoesNotExist:
            teacher = None

        if teacher is not None:
            teacher_id = teacher.teacherid
            return 'teacher', teacher_id
    return None, None


def check_register(uuid, real_name, phone_number, password):
    # 注册加判断已经存在用户已存在
    users = Student.objects.all()
    for i in users:
        if phone_number == i.phonenumber:
            return "用户已存在"

    # 对于 student ，可使用 register_time 作为 salt
    register_time = get_current_time()
    # password = hash_password(password, register_time)

    try:
        Student.objects.create(studentid=uuid,
                               realname=real_name,
                               phonenumber=phone_number,
                               userpd=password,
                               registertime=register_time)
        return "注册成功"
    except Exception as e:
        print(e)
        return "注册失败"


def get_session_id():
    res = ''
    for i in range(4):
        num = str(random.randint(1, 9))
        letter = chr(random.randint(65, 90))
        group = random.choice([num, letter])
        res += group
    return res


def set_login_session(phone, power):
    """
    登录验证与权限管理。返回 Session ID。
    @param phone:
    @param power:
    @return:
    """
    session_id = get_session_id()

    # 生成自定义session的value
    if power == 'student':
        value = {'phone': phone, 'power': 'student'}
    elif power == 'teacher':
        value = {'phone': phone, 'power': 'teacher'}

    # 将自定义session信息存入数据库
    value = json.dumps(value)
    Mysession.objects.create(session_id=session_id, session_value=value)

    # 将自定义session_id返回
    return session_id
