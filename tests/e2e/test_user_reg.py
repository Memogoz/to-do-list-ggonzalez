import pytest
from app.models.models import User

def test_register_user(db_session, new_user):
    db_session.add(new_user)
    db_session.commit()
    user = User.query.first()
    assert user is not None
    assert user.username == 'test_user'