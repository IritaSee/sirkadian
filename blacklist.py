from db import db
from datetime import datetime, timezone

from models.user_history import UserLoginHistoryModel

def _epoch_utc_to_datetime(epoch_utc):
    return datetime.fromtimestamp(epoch_utc, tz=timezone.utc)

def is_token_revoked(decoded_token):
    jti = decoded_token['jti']
    try:
        token = UserLoginHistoryModel.query.filter_by(jti_access=jti).order_by(UserLoginHistoryModel.id.desc()).first() or UserLoginHistoryModel.query.filter_by(jti_refresh=jti).order_by(UserLoginHistoryModel.id.desc()).first()
        return token.revoked
    except:
        return True

def revoke_token(user):
    try:
        token = UserLoginHistoryModel.query.filter_by(user_id=user).order_by(UserLoginHistoryModel.id.desc()).first()
        token.revoked = True
        db.session.commit()
    except:
        return 'tokennotfound'

def prune_database():
    now = datetime.now()
    expired = UserLoginHistoryModel.query.filter(UserLoginHistoryModel.expires < now).all()
    for token in expired:
        db.session.delete(token)
    db.session.commit()