from flask import abort
from flask_jwt_extended import create_access_token, get_jwt
from api.models import db, User

class AuthService:
    
    @staticmethod
    def signup(data):
        required_fields = ["email", "username", "password"]
        for field in required_fields:
            if field not in data or not data[field]:
                abort(400, description=f"El campo {field} es obligatorio")
        
        if User.query.filter_by(email=data["email"]).first():
            abort(409, description="Ya existe un usuario con ese email")
        
        if User.query.filter_by(username=data["username"]).first():
            abort(409, description="Ya existe un usuario con ese username")
        
        try:
            new_user = User(
                email=data["email"],
                username=data["username"],
                is_active=True
            )
            new_user.set_password(data["password"])
            
            db.session.add(new_user)
            db.session.commit()
            
            access_token = create_access_token(identity=str(new_user.id))
        
        except Exception as error:
            db.session.rollback()
            abort(500, description=f"Error al crear usuario: {str(error)}")
        
        return {
            "token": access_token,
            "user": new_user.serialize()
        }
    
    @staticmethod
    def login(data):
        if "email" not in data or "password" not in data:
            abort(400, description="Email y password son obligatorios")
        
        user = User.query.filter_by(email=data["email"]).first()
        
        if user is None:
            abort(401, description="Email o password incorrectos")
        
        if not user.is_active:
            abort(401, description="La cuenta está desactivada")
        
        if not user.check_password(data["password"]):
            abort(401, description="Email o password incorrectos")
        
        access_token = create_access_token(identity=str(user.id))
        
        return {
            "token": access_token,
            "user": user.serialize()
        }
    
    @staticmethod
    def get_me(user_id):
        user = User.query.get(user_id)
        
        if user is None:
            abort(404, description="Usuario no encontrado")
        
        if not user.is_active:
            abort(401, description="La cuenta está desactivada")
        
        return user.serialize()