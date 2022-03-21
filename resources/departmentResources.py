import json
from pprint import pprint

from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_current_user, get_jwt_identity
from flask_restful import Resource

from passlib.hash import pbkdf2_sha256 as sha256

from models.departments import Departments
from models.members import Members
from models.revokedTokens import RevokedTokens
from utils.decorator import departmentHead_required, director_required


class DepartmentRegistration(Resource):
    @jwt_required()
    @director_required
    def post(self):
        data = request.get_json(force=True)
        current_id = get_jwt_identity()

        ##Check if all the fields exists in the json data
        ##Check if the email already exists or not before creating the new organisation

        password = sha256.hash(data['password'])

        try:
            new_department = Departments(
                organisation_id=str(current_id),
                name=data['name'],
                tagline=data['tagline'],
                head_name=data['head_name'],
                email=data['email'],
                password=password
            )

            new_department.save()

            access_token = create_access_token(identity=str(new_department['id']), additional_claims={"roles": "departmentHead"})
            refresh_token = create_refresh_token(identity=str(new_department['id']), additional_claims={"roles": "departmentHead"})

            return {
                'message': 'Departments {} was created'.format(data['name']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        except Exception as e:
            print(f"Got error while registering department -: {e}")
            return {'message': 'Something went wrong'}, 500


class DepartmentLogin(Resource):
    def post(self):
        data = request.get_json(force=True)

        ##Check if email and password exists in the json data

        email = data["email"]
        password = data["password"]

        current_department = Departments.objects(email=email).first()

        if not current_department:
            return {'message': 'Email {} doesn\'t exist'.format(email)}, 401

        if sha256.verify(password, current_department.password):
            access_token = create_access_token(identity=str(current_department['id']), additional_claims={"roles": "departmentHead"})
            refresh_token = create_refresh_token(identity=str(current_department['id']), additional_claims={"roles": "departmentHead"})

            return {
                       'message': 'Logged in as {}'.format(current_department.head_name),
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        else:
            return {'message': 'Wrong credentials'}, 401


class DepartmentLogoutAccess(Resource):
    @jwt_required()
    @departmentHead_required
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokens(jti=jti)
            revoked_token.save()
            return {'message': 'Logout Successfully - Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class DepartmentInfo(Resource):
    @jwt_required()
    @departmentHead_required
    def get(self):
        current_id = get_jwt_identity()
        current_department = Departments.objects(id=str(current_id)).first()

        return {
            "organisation_id": current_department["organisation_id"],
            "name": current_department["name"],
            "tagline": current_department["tagline"],
            "director_name": current_department["head_name"],
            "email": current_department["email"],
        }


class AllDepartment(Resource):
    def get(self):
        all_department = Departments.objects(organisation_id="6236fd2b7d5d64f7fe581a75")
        all_department = json.loads(all_department.to_json())

        data = []

        for deparment in all_department:
            data.append({
                "name": deparment["name"],
                "id": deparment["_id"]["$oid"],
                "tagline": deparment["tagline"],
                "head_name": deparment["head_name"],
                "email": deparment["email"]
            })

        return {"data": data}, 200


class DepartmentMembers(Resource):
    @jwt_required()
    @departmentHead_required
    def get(self):
        current_id = get_jwt_identity()
        all_members = Members.objects(department_id=str(current_id))
        all_members = json.loads(all_members.to_json())

        data = []

        for member in all_members:
            data.append({
                "name": member["name"],
                "email": member["email"]
            })

        return {"data": data}
