# rbac.py
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import jsonify

def role_required(required_role): #This makes a special tool (called a decorator) that checks if someone has the right role (like "admin" or "user") before letting them use a feature.
    def decorator(fn): #This is a helper that will wrap around the feature (function) you want to protect.
        @wraps(fn) #This keeps the original name and info of the feature you’re protecting.
        def wrapper(*args, **kwargs): #This is the actual gatekeeper that checks if the person is allowed in.
            verify_jwt_in_request() #This checks if the person has shown their ID card (a special token called JWT) when asking to use the feature.
            claims = get_jwt() #This reads the information (like their role) from the ID card.
            if claims['role'] != required_role:
                return jsonify(msg="Access denied"), 403
            return fn(*args, **kwargs) #If the user’s role matches the required role, this line calls the original function (the route you’re protecting) and lets the request go through.
        return wrapper #This gives back the wrapper function, which now acts as a security guard for your route. It replaces the original function with the version that checks the user’s role.
    return decorator #This gives back the decorator function itself, so you can use @role_required('admin') or @role_required('user') on any route you want to protect.

