from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, get_jwt


def director_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['roles'] != 'director':
            return {'message': 'Director Only'}, 401
        else:
            return fn(*args, **kwargs)

    return wrapper


def departmentHead_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['roles'] != 'departmentHead':
            return {'message': 'Department Head Only'}, 401
        else:
            return fn(*args, **kwargs)

    return wrapper


def members_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['roles'] != 'member':
            return {'message': 'Members Only'}, 401
        else:
            return fn(*args, **kwargs)

    return wrapper


def citizen_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['roles'] != 'citizen':
            return {'message': 'Citizen Only'}, 401
        else:
            return fn(*args, **kwargs)

    return wrapper
