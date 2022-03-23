from datetime import date
from pprint import pprint

from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_current_user, get_jwt_identity
from flask_restful import Resource

from passlib.hash import pbkdf2_sha256 as sha256

from models.approvals import Approvals
from models.members import Members
from models.revokedTokens import RevokedTokens
from utils.decorator import departmentHead_required, members_required


class MemberRegistration(Resource):
    @jwt_required()
    @departmentHead_required
    def post(self):
        data = request.get_json(force=True)
        current_id = get_jwt_identity()

        ##Check if all the fields exists in the json data
        ##Check if the email already exists or not before creating the new organisation

        password = sha256.hash(data['password'])

        try:
            new_member = Members(
                organisation_id=data['organisation_id'],
                department_id=str(current_id),
                name=data['name'],
                email=data['email'],
                password=password
            )

            new_member.save()

            access_token = create_access_token(identity=str(new_member['id']), additional_claims={"roles": "member"})
            refresh_token = create_refresh_token(identity=str(new_member['id']), additional_claims={"roles": "member"})

            return {
                'message': 'Member {} was created'.format(data['name']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        except Exception as e:
            print(f"Got error while registering member -: {e}")
            return {'message': 'Something went wrong'}, 500


class MemberLogin(Resource):
    def post(self):
        data = request.get_json(force=True)

        ##Check if email and password exists in the json data

        email = data["email"]
        password = data["password"]

        current_member = Members.objects(email=email).first()

        if not current_member:
            return {'message': 'Email {} doesn\'t exist'.format(email)}, 401

        if sha256.verify(password, current_member.password):
            access_token = create_access_token(identity=str(current_member['id']), additional_claims={"roles": "member"})
            refresh_token = create_refresh_token(identity=str(current_member['id']), additional_claims={"roles": "member"})

            return {
                       'message': 'Logged in as {}'.format(current_member.name),
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        else:
            return {'message': 'Wrong credentials'}, 401


class MemberLogoutAccess(Resource):
    @jwt_required()
    @members_required
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokens(jti=jti)
            revoked_token.save()
            return {'message': 'Logout Successfully - Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class MemberInfo(Resource):
    @jwt_required()
    @members_required
    def get(self):
        current_id = get_jwt_identity()
        current_member = Members.objects(id=str(current_id)).first()

        return {
            "organisation_id": current_member["organisation_id"],
            "department_id": current_member["department_id"],
            "name": current_member["name"],
            "email": current_member["email"]
        }


class ApprovalSubmit(Resource):
    @jwt_required()
    @members_required
    def post(self):
        data = request.get_json(force=True)
        current_id = get_jwt_identity()

        approval = []

        # print(type(data["departments"]))

        departments = []


        # departments = data["departments"]
        for department in departments:
            approval.append(0)

        # print(departments)
        # print(approval)

        todays_date = date.today()
        todays_date = todays_date.strftime("%b %d, %Y")

        try:
            new_approval = Approvals(
                title=data["title"],
                description=data["description"],
                filepath=data["filepath"],
                member_id=current_id,
                departments=departments,
                approval=approval,
                created_date=todays_date
            )

            new_approval.save()

            return {
                'message': 'Approval created successfully'
            }

        except Exception as e:
            print(f"Got error while creating approval -: {e}")
            return {'message': 'Something went wrong'}, 500
