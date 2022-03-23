import json
from pprint import pprint

from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_current_user, get_jwt_identity
from flask_restful import Resource

from passlib.hash import pbkdf2_sha256 as sha256

from models.citizens import Citizens
from models.queries import Queries
from models.revokedTokens import RevokedTokens
from utils.decorator import citizen_required


class CitizenRegistration(Resource):
    def post(self):
        data = request.get_json(force=True)

        ##Check if all the fields exists in the json data
        ##Check if the email already exists or not before creating the new organisation

        password = sha256.hash(data['password'])

        try:
            new_citizen = Citizens(
                name=data['name'],
                email=data['email'],
                password=password
            )

            new_citizen.save()

            access_token = create_access_token(identity=str(new_citizen['id']), additional_claims={"roles": "citizen"})
            refresh_token = create_refresh_token(identity=str(new_citizen['id']), additional_claims={"roles": "citizen"})

            return {
                'message': 'Citizen {} was created'.format(data['name']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        except Exception as e:
            print(f"Got error while registering citizen -: {e}")
            return {'message': 'Something went wrong'}, 500


class CitizenLogin(Resource):
    def post(self):
        data = request.get_json(force=True)

        ##Check if email and password exists in the json data

        email = data["email"]
        password = data["password"]

        current_citizen = Citizens.objects(email=email).first()

        if not current_citizen:
            return {'message': 'Email {} doesn\'t exist'.format(email)}, 401

        if sha256.verify(password, current_citizen.password):
            access_token = create_access_token(identity=str(current_citizen['id']), additional_claims={"roles": "citizen"})
            refresh_token = create_refresh_token(identity=str(current_citizen['id']), additional_claims={"roles": "citizen"})

            return {
                       'message': 'Logged in as {}'.format(current_citizen.name),
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        else:
            return {'message': 'Wrong credentials'}, 401


class CitizenLogoutAccess(Resource):
    @jwt_required()
    @citizen_required
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokens(jti=jti)
            revoked_token.save()
            return {'message': 'Logout Successfully - Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class CitizenInfo(Resource):
    @jwt_required()
    @citizen_required
    def get(self):
        current_id = get_jwt_identity()
        current_citizen = Citizens.objects(id=str(current_id)).first()

        return {
            "name": current_citizen["name"],
            "email": current_citizen["email"]
        }


class AllQueries(Resource):
    @jwt_required()
    @citizen_required
    def get(self):
        current_id = get_jwt_identity()
        all_queries = Queries.objects(citizen_id=str(current_id))
        all_queries = json.loads(all_queries.to_json())

        data = []

        for query in all_queries:
            data.append({
                "department_id": query["department_id"],
                "title": query['title'],
                "description": query['description']
            })

        return {"data": data}, 200


class QuerySubmit(Resource):
    @jwt_required()
    @citizen_required
    def post(self):
        data = request.get_json(force=True)
        print(data)

        current_id = get_jwt_identity()

        try:
            new_query = Queries(
                citizen_id=current_id,
                department_id=data["department_id"],
                title=data['title'],
                description=data['description'],
                replied=False
            )

            new_query.save()

            return {
                     'message': 'Queries submitted successfully'
                   }, 200

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500
