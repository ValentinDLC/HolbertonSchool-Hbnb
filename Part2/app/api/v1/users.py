# api/v1/users.py
from flask import request, jsonify
from flask_restx import Namespace, Resource, abort
from app.services import facade

api = Namespace('users', description='User operations')

@api.route('/')
class UserList(Resource):
    def post(self):
        """Create a new user"""
        data = request.get_json()
        try:
            user = facade.create_user(data)
            return user.to_dict(), 201
        except ValueError as e:
            abort(400, message=str(e))

    def get(self):
        """Get a list of all users"""
        users = facade.user_repo.get_all()
        return [user.to_dict() for user in users], 200

@api.route('/<string:user_id>')
class UserDetail(Resource):
    def get(self, user_id):
        """Get a user by ID"""
        user = facade.user_repo.get(user_id)
        if not user:
            abort(404, message="User not found")
        return user.to_dict(), 200

    def put(self, user_id):
        """Update a user by ID"""
        user = facade.user_repo.get(user_id)
        if not user:
            abort(404, message="User not found")
        data = request.get_json()
        try:
            facade.user_repo.update(user_id, data)
            return facade.user_repo.get(user_id).to_dict(), 200
        except ValueError as e:
            abort(400, message=str(e))
