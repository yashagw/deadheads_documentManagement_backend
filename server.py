from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager

from models.revokedTokens import RevokedTokens

default_config = {
    'MONGODB_SETTINGS': {
        'db': 'deadheads',
        'host': '165.232.183.136',
        'port': 2727,
        'username': 'yashMongo',
        'password': 'MongoChacha$123'
    },
    'JWT_SECRET_KEY': "dfasjfrijsa845238rfdugidgfj230498",
    'JWT_ACCESS_TOKEN_EXPIRES': 365 * 24 * 60 * 60,
    'JWT_BLACKLIST_ENABLED': True,
    'JWT_BLACKLIST_TOKEN_CHECKS': ['access'],
    'PROPAGATE_EXCEPTIONS': True
}

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config.update(default_config)

db = MongoEngine(app=app)
jwt = JWTManager(app=app)


@app.route('/')
def index():
    return jsonify({'message': 'Deadheads Backend Working'})


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    current_token = RevokedTokens.objects(jti=jti).first()
    if current_token:
        return True
    else:
        return False


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    return jsonify({
        'message': 'Token has expired'
    }), 401


@jwt.invalid_token_loader
def my_invalid_token_loader(invalid_token):
    return jsonify({
        'message': 'Token is not valid'
    }), 401


@jwt.revoked_token_loader
def my_revoked_token_loader(jwt_header, jwt_payload):
    return jsonify({
        'message': 'Token has been revoked'
    }), 401


from resources import organisationResources, departmentResources, memberResources, citizenResources

api.add_resource(organisationResources.OrganisationRegistration, '/organisation/register')
api.add_resource(organisationResources.OrganisationLogin, '/organisation/login')
api.add_resource(organisationResources.OrganisationLogoutAccess, '/organisation/logout/access')
api.add_resource(organisationResources.OrganisationInfo, '/organisation')
api.add_resource(organisationResources.OrganisationStats, '/organisation/stats')

api.add_resource(departmentResources.DepartmentRegistration, '/organisation/department/register')
api.add_resource(departmentResources.DepartmentLogin, '/department/login')
api.add_resource(departmentResources.DepartmentLogoutAccess, '/department/logout/access')
api.add_resource(departmentResources.DepartmentInfo, '/department')
api.add_resource(departmentResources.DepartmentMembers, '/department/members')
api.add_resource(departmentResources.AllDepartment, '/departments/')

api.add_resource(memberResources.MemberRegistration, '/department/member/register')
api.add_resource(memberResources.MemberLogin, '/member/login')
api.add_resource(memberResources.MemberLogoutAccess, '/member/logout/access')
api.add_resource(memberResources.MemberInfo, '/member')
api.add_resource(memberResources.ApprovalSubmit, '/member/approval')

api.add_resource(citizenResources.CitizenRegistration, '/citizen/register')
api.add_resource(citizenResources.CitizenLogin, '/citizen/login')
api.add_resource(citizenResources.CitizenLogoutAccess, '/citizen/logout/access')
api.add_resource(citizenResources.CitizenInfo, '/citizen')
api.add_resource(citizenResources.QuerySubmit, '/citizen/submitQuery')

app.run(host='0.0.0.0')
# app.run()
