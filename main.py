from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import os

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inshorts.db'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret')
db = SQLAlchemy(app)
# db.create_all()
migrate = Migrate(app, db)
jwt = JWTManager(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, is_admin={self.is_admin})"


class ShortModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publish_date = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)
    actual_content_link = db.Column(db.String(200))
    image = db.Column(db.String(200))
    upvote = db.Column(db.Integer, default=0)
    downvote = db.Column(db.Integer, default=0)


signup_args = reqparse.RequestParser()
signup_args.add_argument("username", type=str, help="Username is required", required=True)
signup_args.add_argument("password", type=str, help="Password is required", required=True)
signup_args.add_argument("email", type=str, help="Email is required", required=True)

login_args = reqparse.RequestParser()
login_args.add_argument("username", type=str, help="Username is required", required=True)
login_args.add_argument("password", type=str, help="Password is required", required=True)

short_create_args = reqparse.RequestParser()
short_create_args.add_argument("category", type=str, help="Category is required", required=True)
short_create_args.add_argument("title", type=str, help="Title is required", required=True)
short_create_args.add_argument("author", type=str, help="Author is required", required=True)
short_create_args.add_argument("publish_date", type=str, help="Publish date is required", required=True)
short_create_args.add_argument("content", type=str, help="Content is required", required=True)
short_create_args.add_argument("actual_content_link", type=str)
short_create_args.add_argument("image", type=str)
short_create_args.add_argument("upvote", type=int, default=0)
short_create_args.add_argument("downvote", type=int, default=0)

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'is_admin': fields.Boolean
}

short_fields = {
    'id': fields.Integer,
    'category': fields.String,
    'title': fields.String,
    'author': fields.String,
    'publish_date': fields.DateTime,
    'content': fields.String,
    'actual_content_link': fields.String,
    'image': fields.String,
    'upvote': fields.Integer,
    'downvote': fields.Integer
}


class UserRegister(Resource):
    def post(self):
        args = signup_args.parse_args()
        if UserModel.query.filter_by(username=args['username']).first():
            abort(409, message="Username already taken")
        if UserModel.query.filter_by(email=args['email']).first():
            abort(409, message="Email already taken")
        
        hashed_password = generate_password_hash(args['password'], method='pbkdf2:sha256')
        user = UserModel(username=args['username'], password=hashed_password, email=args['email'])
        db.session.add(user)
        db.session.commit()
        return {"status": "Account successfully created", "status_code": 200, "user_id": user.id}, 201

class UserLogin(Resource):
    def post(self):
        args = login_args.parse_args()
        user = UserModel.query.filter_by(username=args['username']).first()
        if not user or not check_password_hash(user.password, args['password']):
            return {"status": "Incorrect username/password provided. Please retry", "status_code": 401}, 401

        access_token = create_access_token(identity={'username': user.username, 'is_admin': user.is_admin})
        return {"status": "Login successful", "status_code": 200, "user_id": user.id, "access_token": access_token}, 200

class Short(Resource):
    @marshal_with(short_fields)
    def get(self, short_id):
        short = ShortModel.query.filter_by(id=short_id).first()
        if not short:
            abort(404, message="Short not found")
        return short

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user['is_admin']:
            abort(403, message="Admin privileges required")

        args = short_create_args.parse_args()
        try:
            publish_date = datetime.fromisoformat(args['publish_date'])
        except ValueError:
            abort(400, message="Invalid publish date format")
        
        short = ShortModel(category=args['category'], title=args['title'], author=args['author'], 
                           publish_date=publish_date, content=args['content'], 
                           actual_content_link=args.get('actual_content_link'), image=args.get('image'),
                           upvote=args.get('upvote', 0), downvote=args.get('downvote', 0))
        db.session.add(short)
        db.session.commit()
        return {"message": "Short added successfully", "short_id": short.id, "status_code": 200}, 200

class ShortsFeed(Resource):
    @marshal_with(short_fields)
    def get(self):
        shorts = ShortModel.query.order_by(ShortModel.publish_date.desc(), ShortModel.upvote.desc()).all()
        return shorts

class FilterShorts(Resource):
    @jwt_required()
    @marshal_with(short_fields)
    def get(self):
        filters = request.args.get('filter')
        search = request.args.get('search')

        query = ShortModel.query
        
        if filters:
            try:
                filters = json.loads(filters)
            except json.JSONDecodeError:
                abort(400, message="Invalid filter format")
            
            if 'category' in filters:
                query = query.filter_by(category=filters['category'])
            if 'publish_date' in filters:
                try:
                    publish_date = datetime.fromisoformat(filters['publish_date'])
                    query = query.filter(ShortModel.publish_date >= publish_date)
                except ValueError:
                    abort(400, message="Invalid publish date format")
            if 'upvote' in filters:
                query = query.filter(ShortModel.upvote >= filters['upvote'])

        if search:
            try:
                search = json.loads(search)
            except json.JSONDecodeError:
                abort(400, message="Invalid search format")
                
            if 'title' in search:
                query = query.filter(ShortModel.title.contains(search['title']))
            if 'keyword' in search:
                query = query.filter(ShortModel.title.contains(search['keyword']) | ShortModel.content.contains(search['keyword']))
            if 'author' in search:
                query = query.filter_by(author=search['author'])
        
        results = query.all()
        if not results:
            return {"status": "No short matches your search criteria", "status_code": 400}, 400
        return results

api.add_resource(UserRegister, "/api/signup")
api.add_resource(UserLogin, "/api/login")
api.add_resource(Short, "/api/shorts/<int:short_id>", "/api/shorts/create")
api.add_resource(ShortsFeed, "/api/shorts/feed")
api.add_resource(FilterShorts, "/api/shorts/filter")

if __name__ == "__main__":
    app.run(debug=True)
