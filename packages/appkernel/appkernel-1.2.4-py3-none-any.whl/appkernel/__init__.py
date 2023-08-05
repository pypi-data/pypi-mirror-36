import sys
try:
    from gevent import monkey
    gettrace = getattr(sys, 'gettrace', None)
    if gettrace and gettrace():
        # we are in debug mode
        pass
    else:
        # need to patch sockets to make requests async
        monkey.patch_all()
except ImportError:
    # skipping patching
    pass
from .core import AppKernelException
from .util import extract_model_messages, create_custom_error
from .model import Model, Property, Index, TextIndex, UniqueIndex, PropertyRequiredException, Marshaller, action, resource
from .validators import NotEmpty, Regexp, Past, Future, ValidationException, Email, Min, Max, Validator, Unique
from .generators import create_uuid_generator, date_now_generator, content_hasher
from .repository import Repository, AuditableRepository, MongoQuery, MongoRepository, Query
from .service import ServiceException
from .iam import IdentityMixin, Role, Anonymous, Denied, CurrentSubject, Authority, Permission, RbacMixin
from .engine import AppKernelEngine, ResourceController
from .configuration import config
from .infrastructure import CfgEngine
