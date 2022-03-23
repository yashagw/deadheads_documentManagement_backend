from pprint import pprint

from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_current_user, get_jwt_identity
from flask_restful import Resource

from passlib.hash import pbkdf2_sha256 as sha256

from models.citizens import Citizens
from models.departmentCirculars import DepartmentCirculars
from models.organisations import Organisations
from models.queries import Queries
from models.revokedTokens import RevokedTokens
from utils.decorator import director_required


class OrganisationRegistration(Resource):
    def post(self):
        data = request.get_json(force=True)

        ##Check if all the fields exists in the json data
        ##Check if the email already exists or not before creating the new organisation

        password = sha256.hash(data['password'])

        try:
            new_organisation = Organisations(
                name=data['name'],
                tagline=data['tagline'],
                director_name=data['director_name'],
                city=data['city'],
                state=data['state'],
                pincode=data['pincode'],
                logo=data['logo'],
                banner=data['banner'],
                email=data['email'],
                password=password
            )

            new_organisation.save()

            access_token = create_access_token(identity=str(new_organisation['id']), additional_claims={"roles": "director"})
            refresh_token = create_refresh_token(identity=str(new_organisation['id']), additional_claims={"roles": "director"})

            return {
                'message': 'Organisation {} was created'.format(data['name']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        except Exception as e:
            print(f"Got error while registering organisation -: {e}")
            return {'message': 'Something went wrong'}, 500


class OrganisationLogin(Resource):
    def post(self):
        data = request.get_json(force=True)

        ##Check if email and password exists in the json data

        email = data["email"]
        password = data["password"]

        current_organisation = Organisations.objects(email=email).first()

        if not current_organisation:
            return {'message': 'Email {} doesn\'t exist'.format(email)}, 401

        if sha256.verify(password, current_organisation.password):
            access_token = create_access_token(identity=str(current_organisation['id']), additional_claims={"roles": "director"})
            refresh_token = create_refresh_token(identity=str(current_organisation['id']), additional_claims={"roles": "director"})

            return {
                       'message': 'Logged in as {}'.format(current_organisation.director_name),
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        else:
            return {'message': 'Wrong credentials'}, 401


class OrganisationLogoutAccess(Resource):
    @jwt_required()
    @director_required
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokens(jti=jti)
            revoked_token.save()
            return {'message': 'Logout Successfully - Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class OrganisationInfo(Resource):
    @jwt_required()
    @director_required
    def get(self):
        current_id = get_jwt_identity()
        current_organisation = Organisations.objects(id=str(current_id)).first()

        return {
            "name": current_organisation["name"],
            "tagline": current_organisation["tagline"],
            "director_name": current_organisation["director_name"],
            "city": current_organisation["city"],
            "state": current_organisation["state"],
            "pincode": current_organisation["pincode"],
            "logo": current_organisation["logo"],
            "banner": current_organisation["banner"],
        }


class OrganisationStats(Resource):
    @jwt_required()
    @director_required
    def get(self):
        current_id = get_jwt_identity()
        current_organisation = Organisations.objects(id=str(current_id)).first()

        total_queries = Queries.objects()
        unsolved_queries = Queries.objects(replied=False)
        solved_queries = Queries.objects(replied=True)
        registered_citizen = Citizens.objects()

        return {
            "total_queries": len(total_queries),
            "unsolved_queries": len(unsolved_queries),
            "solved_queries": len(solved_queries),
            "no_of_citizen": len(registered_citizen),
            "director_name": current_organisation["director_name"],
        }


class DepartmentCircularSubmit(Resource):
    @jwt_required()
    @director_required
    def post(self):
        data = request.get_json(force=True)

        try:
            new_circular = DepartmentCirculars(
                title=data['title'],
                description=data['description']
            )

            new_circular.save()

            return {
                'message': 'Departmental Circular created successfully'
            }

        except Exception as e:
            print(f"Got error while creating departmental circulars -: {e}")
            return {'message': 'Something went wrong'}, 500
