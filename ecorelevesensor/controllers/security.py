"""
Created on Mon Aug 25 13:00:16 2014

@author: Natural Solutions (Thomas)
"""

from ecorelevesensor.models import DBSession, User

from pyramid.security import (
    ALL_PERMISSIONS,
    DENY_ALL,
    Allow,
    Authenticated,
)

# Root class security #
class SecurityRoot(object):
    __acl__ = [
        (Allow, Authenticated, 'read'),
        (Allow, 'user', 'edit'),
        (Allow, 'admin', ALL_PERMISSIONS),
        DENY_ALL
    ]
    
    def __init__(self, request):
        self.request = request

# Useful fucntions #
def role_loader(user_id, request):
    return DBSession.query(User.role).filter(User.id==user_id).one()
    