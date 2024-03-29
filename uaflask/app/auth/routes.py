from app.auth import bp
from flask import jsonify, redirect, url_for, request, render_template
from datetime import datetime, timezone, timedelta
import sqlalchemy as sa
import hashlib
from app import db, functions as f
from app.models import Users, Profiles
from sqlalchemy.exc import SQLAlchemyError, DataError
from config import r


@bp.post('/login')
def login():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        if req.get('email'):
            user = db.session.scalar(sa.select(Users).where(Users.email == req["email"]))
        else:
            user = db.session.scalar(sa.select(Users).where(Users.name == req["name"]))
        # 유저 없음
        if not user:
            raise Exception('user not exists')
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')
        # 로그인 확인
        if f.login_required(req['name']):
            raise Exception('already login')
        # 패스워드 확인
        check = user.check_password(req["password"])
        if not check:
            if r.get(user.name) == 'stop': # 로그인 멈춤
                raise Exception('stop login')
            raise Exception('password error')
        # 세션 및 로그인
        session_key = hashlib.sha256(f'{user.name}{datetime.now(timezone(timedelta(hours=9)))}'.encode()).hexdigest()
        r.set(user.name, session_key, ex=3600*24)
        res['status'] = 'success'
        res['data'] = 'login'
    except Exception as err:
        print(err)
        if err.__str__() == 'password error':
            val = r.get(user.name)
            if val:
                if int(val)>=5: # 5회 실패시 5분 멈춤
                    r.set(user.name, 'stop', ex=300)
                else:
                    r.incr(user.name)
            else:
                r.set(user.name, 1, ex=600) # 로그인 실패 횟수 설정
        res['status'] = 'error'
        res['data'] = str(err).strip("'")
    return jsonify(res)


@bp.route('/create_user', methods=['POST'])
def create_user():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        # 아이디 검증
        check, reason = Users.validate_id(req["name"], req["email"])
        if not check:
            raise Exception(reason)
        user = db.session.scalar(sa.select(Users).where(Users.email == req["email"] or Users.name == req["name"]))
        # 유저 이미 있음
        if user:
            raise Exception('user already exists')
        # 유저 생성
        new_user = Users(id=Users.create_uuid(), email=req["email"], name=req["name"])
        # 패스워드 검증
        check, reason = new_user.validate_password(req["password"])
        if not check:
            raise Exception(reason)
        hash_pw = new_user.digest_password(req["password"])
        new_user.password=hash_pw
        new_user.password_last = {datetime.today().strftime('%Y-%m-%d'):hash_pw}
        # 프로필 생성
        profile = Profiles(nationality=req["nationality"])
        new_user.r_profile.append(profile)
        db.session.add(new_user)
        db.session.commit()
        res['status'] = 'success'
        res['data'] = 'create user'
    except Exception as err:
        print('Error<create_user>:', err)
        res['status'] = 'error'
        res['data'] = str(err).strip("'")
    print('#1###-> ', res)
    return jsonify(res)


@bp.route('/update_user', methods=['POST'])
def update_user():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        # 로그인 확인
        if not f.login_required(req['name']):
            raise Exception('required login')
        user = db.session.scalar(sa.select(Users).where(Users.email == req["email"] or Users.name == req["name"]))
        # 유저가 없으면
        if not user:
            raise Exception('no exists user')
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')
        # 아이디, 패스워드 검증
        check, reason = Users.validate_id(req["newname"], req["newemail"])
        if not check:
            raise Exception(reason)
        check, reason = user.validate_password(req["newpassword"])
        if not check:
            raise Exception(reason)
        # 당일 업데이트 가능 시간 검증
        now = datetime.now() - timedelta(hours=9) #kr한정
        if (now - user.updated_at) <= timedelta(minutes=1):
            raise Exception('can not update today')
        # 유저 수정
        user.email = req["newemail"]
        user.name = req["newname"]
        hash_pw = user.digest_password(req["newpassword"])
        user.password = hash_pw
        user.password_last[f"{datetime.today().strftime('%Y-%m-%d')}"] = hash_pw
        user.business = req["business"]
        user.updated_at = now
        db.session.commit()
        # 세션 업데이트
        r.delete(req["name"])
        session = hashlib.sha256(f'{user.name}{datetime.now(timezone(timedelta(hours=9)))}'.encode()).hexdigest()
        r.set(user.name, session, ex=3600*24)
        res['status'] = 'success'
        res['data'] = 'update user'
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = str(err).strip("'")
    return jsonify(res)


@bp.route('/delete_user', methods=['POST'])
def delete_user():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        # 로그인 확인
        if not f.login_required(req['name']):
            raise Exception('required login')
        user = db.session.scalar(sa.select(Users).where(Users.email == req["email"] or Users.name == req["name"]))
        # 유저가 없으면
        if not user:
            raise Exception('no exists user')
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')
        # 유저 삭제
        last_user = user.name
        db.session.delete(user)
        db.session.commit()
        # 세션 삭제
        r.delete(last_user)
        res['status'] = 'success'
        res['data'] = 'delete user'
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = str(err).strip("'")
    return jsonify(res)


@bp.get('/logout')
def logout():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        # 로그인 되어있는지 확인 후 세션 제거
        if f.login_required(req['name']):
            r.delete(req['name'])
        else:
            raise Exception('logout failure')
        res['status'] = 'success'
        res['data'] = 'logout'
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = str(err).strip("'")
    return jsonify(res)


@bp.route('/update_profile', methods=['POST'])
def update_profile():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        # 로그인 확인
        if not f.login_required(req['name']):
            raise Exception('required login')
        user = db.session.scalar(sa.select(Users).where(Users.email == req["email"] or Users.name == req["name"]))
        # 유저가 없으면
        if not user:
            raise Exception('no exists user')
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')
        # 프로필 수정
        for x, y in req['newprofile'].items():
            match x:
                case 'image':
                    user.r_profile[0].image = y
                case 'nationality':
                    user.r_profile[0].nationality = y
                case 'like':
                    user.r_profile[0].like = {**user.r_profile[0].like, **y}
                case 'accommodation':
                    user.r_profile[0].accommodation = user.r_profile[0].accommodation + [y]
                case 'clip':
                    user.r_profile[0].clip = user.r_profile[0].clip + [y]
                case 'follow':
                    user.r_profile[0].follow = user.r_profile[0].follow + [y]
                case 'comment':
                    user.r_profile[0].comment = user.r_profile[0].comment + [y]
        for x, y in req['delprofile'].items():
            match x:
                case 'image':
                    user.r_profile[0].image = y
                case 'like':
                    user.r_profile[0].like = {z1:z2 for z1, z2 in user.r_profile[0].like.items() if z1!=y}
                case 'accommodation':
                    user.r_profile[0].accommodation = [z for z in user.r_profile[0].accommodation if z!=y]
                case 'clip':
                    user.r_profile[0].clip = [z for z in user.r_profile[0].clip if z!=y]
                case 'follow':
                    user.r_profile[0].follow = [z for z in user.r_profile[0].follow if z!=y]
                case 'comment':
                    user.r_profile[0].comment = [z for z in user.r_profile[0].comment if z!=y]
        db.session.commit()
        res['status'] = 'success'
        res['data'] = 'update profile'
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = str(err).strip("'")
    return jsonify(res)


@bp.route('/get_user_info', methods=['GET'])
def get_user_info():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        # 로그인 확인
        if not f.login_required(req['name']):
            raise Exception('required login')
        user = db.session.scalar(sa.select(Users).where(Users.email == req["email"] or Users.name == req["name"]))
        # 유저가 없으면
        if not user:
            raise Exception('no exists user')
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')
        # 유저 정보
        info = {}
        for x in req['user']:
            match x:
                case 'email':
                    info["email"] = user.email
                case 'name':
                    info["name"] = user.name
                case 'business':
                    info["business"] = user.business
                case 'updated_at':
                    info["updated_at"] = user.updated_at
                case 'created_at':
                    info["created_at"] = user.created_at
                case 'deleted_at':
                    info["deleted_at"] = user.deleted_at
                case 'status':
                    info["status"] = user.status
        for x in req['profile']:
            match x:
                case 'image':
                    info["image"] = user.r_profile[0].image
                case 'nationality':
                    info["nationality"] = user.r_profile[0].nationality
                case 'like':
                    info["like"] = user.r_profile[0].like
                case 'accommodation':
                    info["accommodation"] = user.r_profile[0].accommodation
                case 'clip':
                    info["clip"] = user.r_profile[0].clip
                case 'follow':
                    info["follow"] = user.r_profile[0].follow
                case 'comment':
                    info["comment"] = user.r_profile[0].comment
        res['status'] = 'success'
        res['data'] = 'get user info'
        print(info)
        res['info'] = info
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = str(err).strip("'")
    return jsonify(res)
