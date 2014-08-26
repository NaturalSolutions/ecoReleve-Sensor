"""
Created on Mon Aug 25 12:12:47 2014

@author: Natural Solutions (Thomas)
"""

from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.security import remember, forget, NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from ecorelevesensor.models import DBSession
from ecorelevesensor.models.security import User


route_prefix = 'security/'

@view_config(
    route_name=route_prefix+'login',
    permission=NO_PERMISSION_REQUIRED,
    request_method='POST')
def login(request):
    user_id = request.POST.get('user_id', '')
    pwd = request.POST.get('password', '')
    user = DBSession.query(User).filter(User.pk_id==user_id).one()
    if user is not None and user.check_password(pwd):
        headers = remember(request, user_id)
        response = request.response
        response.headerlist.extend(headers)
        return response
    else:
        return HTTPUnauthorized()
        
@view_config(route_name=route_prefix+'logout')
def logout(request):
    headers = forget(request)
    request.response.headerlist.extend(headers)
    return request.response
    
@view_config(route_name=route_prefix+'has_access')
def has_access(request):
    return request.response