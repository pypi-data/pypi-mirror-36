import datetime
import jwt

from appkernel.configuration import config


class Permission(object):

    def __init__(self, name):
        self.name = name


class Role(Permission):
    def __init__(self, role_name='anonymous'):
        super(Role, self).__init__(role_name)

    def __str__(self):
        return 'ROLE_{}'.format(self.name.upper())


class Anonymous(Role):
    def __init__(self):
        super(Anonymous, self).__init__(role_name='anonymous')


class Denied(Role):
    def __init__(self):
        super(Denied, self).__init__(role_name='denied')


class Authority(Permission):
    def __init__(self, identity_name='anonymous', id=None):
        super(Authority, self).__init__(identity_name)
        self.id = id  # pylint: disable=C0103

    def __str__(self):
        return 'AUTHORITY_{}'.format(self.name.upper())


class CurrentSubject(Authority):
    def __init__(self, binding_view_arg='object_id'):
        super(CurrentSubject, self).__init__('current_user')
        self.view_arg = binding_view_arg


class IdentityMixin(object):
    token_validity_in_seconds = 3600

    def __init__(self, id=None, roles=[Anonymous()]):
        self.id = id  # pylint: disable=C0103
        self.roles = roles

    @staticmethod
    def set_validity(seconds):
        IdentityMixin.token_validity_in_seconds = seconds

    @property
    def auth_token(self):
        if not self.id:
            raise AttributeError('The id of the Identity is not defined.')
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=IdentityMixin.token_validity_in_seconds),
            'iat': datetime.datetime.utcnow(),
            'sub': self.id
        }
        # iss: issuer
        # aud: audience
        # jti: jwt id
        if self.roles and isinstance(self.roles, list) and len(self.roles) > 0:
            payload.update(roles=self.roles)
        return jwt.encode(
            payload,
            key=config.private_key,
            algorithm='RS256'
        ).decode('utf-8')


class RbacMixin(object):

    # format of the method registry
    # {
    #   'GET': {
    #              'some_endpoint': [Permission1, Permission2],
    #               '*': [Permission3, Permission4],
    #           }
    # }

    def __init__(self, cls):
        if not hasattr(cls, 'protected_methods'):
            cls.protected_methods = {}

    @staticmethod
    def set_list(cls, methods=[], permissions=Denied(), endpoint=None):
        def add_endpoint_and_permissions(meth):
            if not hasattr(cls, 'protected_methods'):
                cls.protected_methods = {}
            if meth not in cls.protected_methods:
                cls.protected_methods[meth] = {
                    endpoint or '*': permissions if isinstance(permissions, list) else [permissions]}
            else:
                cls.protected_methods[meth][endpoint or '*'] = permissions if isinstance(permissions,
                                                                                               list) else [
                    permissions]

        if (not isinstance(permissions, list) and not isinstance(permissions, Permission)) or (
                isinstance(permissions, list) and len([perm for perm in permissions if isinstance(perm, Permission)]) == 0):
            raise AttributeError('The permission must be a subclass of a Permission or list of Permissions')
        if isinstance(methods, list):
            for method in methods:
                add_endpoint_and_permissions(method)
        elif isinstance(methods, str):
            add_endpoint_and_permissions(methods)
        else:
            raise TypeError('Methods must be of type list or string.')

    def deny_all(self):
        for method in ['GET', 'POST', 'PUT', 'DELETE']:
            if method not in self.cls.protected_methods:
                self.cls.protected_methods[method] = {'*': [Denied()]}
            else:
                self.cls.protected_methods[method]['*'] = [Denied()]
        return self

    def allow_all(self):
        for method in ['GET', 'POST', 'PUT', 'DELETE']:
            if method not in self.cls.protected_methods:
                self.cls.protected_methods[method] = {'*': [Anonymous()]}
            else:
                self.cls.protected_methods[method]['*'] = [Anonymous()]
        return self

    def deny(self, permission, methods, endpoint=None):
        RbacMixin.set_list(methods, permission, endpoint)
        return self

    def require(self, permission, methods, endpoint=None):
        RbacMixin.set_list(self.cls, methods, permission, endpoint)
        return self
