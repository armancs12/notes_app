from flask_jwt_extended import JWTManager

from app.models import User


auth = JWTManager()


@auth.user_identity_loader
def user_identity_lookup(user):
    return user.id


@auth.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
