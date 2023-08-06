# -*- coding: utf-8 -*-

"""
cloudcix.auth
~~~~~~~~~~~~~

This module implements the CloudCIX API Client Authentications
"""

import json
from keystoneauth1.session import Session
from keystoneclient import access, exceptions
from keystoneclient.auth.identity.v3 import AuthMethod, Auth
from keystoneclient.i18n import _
import logging
from oslo_config import cfg
import requests

from cloudcix.api import Membership
from cloudcix.conf import settings

_logger = logging.getLogger(__name__)


def get_admin_token():
    """
    Generates an `admin` token using the credentials specified in the settings module
    """
    data = {
        'email': settings.CLOUDCIX_API_USERNAME,
        'password': settings.CLOUDCIX_API_PASSWORD,
        'api_key': settings.CLOUDCIX_API_KEY,
    }
    response = Membership.login.post(data=data)
    if response.status_code == 201:
        return response.json()['token']
    raise Exception(response.json()['error_code'])


class TokenAuth(requests.auth.AuthBase):
    """
    CloudCIX Token-based authentication
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers['X-Auth-Token'] = self.token
        return request

    def __eq__(self, other):
        return self.token == other.token


class AdminSession(Session):
    """
    Requests wrapper for Keystone authentication using cloudcix credentials
    """

    def __init__(self):
        self.headers = {'content-type': 'application/json'}
        self.auth_url = settings.CLOUDCIX_AUTH_URL
        self.username = settings.CLOUDCIX_API_USERNAME
        self.password = settings.CLOUDCIX_API_PASSWORD
        self.domain = settings.CLOUDCIX_API_KEY
        # Create a CloudCIXAuth instance and use to to create the super
        auth = CloudCIXAuth(
            auth_url=self.auth_url,
            username=self.username,
            password=self.password,
            member_id=self.domain,
        )
        super(AdminSession, self).__init__(auth)

    def get_token(self, **kwargs):
        kwargs['headers'] = self.headers
        response = requests.post(self.token_url, data=json.dumps(self.data), **kwargs)
        if response.status_code < 400:
            return response.headers['X-Subject-Token']
        # TODO: not sure if should return entire response, False, or status?
        return response

    @property
    def token_url(self):
        return '{}/auth/tokens'.format(self.auth_url)

    @property
    def data(self):
        return {
            'auth': {
                'identity': {
                    'methods': ['password'],
                    'password': {
                        'user': {
                            'name': self.username,
                            'password': self.password,
                            'domain': {
                                'id': self.domain,
                            },
                        },
                    },
                },
            },
        }


class ActiveDirectoryAuth:
    """
    Provides authentication for active directory backends into CloudCIX

    TODO: Deprecate or migrate to v0.3+ of python-cloudcix
    """

    def __init__(self):
        raise NotImplemented


class CloudCIXAuthMethod(AuthMethod):

    _method_parameters = ['username', 'password', 'member_id', 'token_id']

    def get_auth_data(self, session, auth, headers, **kwargs):
        if self.token_id:
            auth_data = {'token': {'id': self.token_id}}
        else:
            auth_data = {'name': self.username, 'password': self.password}
        if self.member_id:
            auth_data['domain'] = {'id': self.member_id}
        return 'password', {'user': auth_data}


class CloudCIXAuth(Auth):

    _auth_method_class = CloudCIXAuthMethod

    def __init__(
            self,
            auth_url,
            username=None,
            password=None,
            member_id=None,
            scope=None,
            token_id=None,
            reauthenticate=True,
    ):
        super(Auth, self).__init__(auth_url=auth_url, reauthenticate=reauthenticate)
        self._auth_method = self._auth_method_class(
            username=username,
            password=password,
            member_id=member_id,
            token_id=token_id,
        )
        self.member_id = member_id
        self.scope = scope
        self.members = []
        self.token_id = None

    def get_auth_ref(self, session, **kwargs):
        headers = {'Accept': 'application/json'}
        body = {'auth': {'identity': {}}}
        ident = body['auth']['identity']
        rkwargs = {}

        for method in self.auth_methods:
            name, auth_data = method.get_auth_data(session, self, headers, request_kwargs=rkwargs)
            ident.setdefault('methods', []).append(name)
            ident[name] = auth_data

        if not ident:
            raise exceptions.AuthenticationRequired(_('Authentication method required (i.e. password)'))

        if self.scope:
            body['auth']['scope'] = self.scope

        _logger.info('Making authentication request to {}'.format(self.token_url))
        try:
            resp = session.post(self.token_url, json=body, headers=headers, authenticated=False, log=False, **rkwargs)
        except exceptions.HTTPError as e:
            try:
                resp = e.response.json()['error']['identity']['password']
            except (KeyError, ValueError):
                pass
            else:
                self.members = resp['members']
                self.token_id = resp['token']['id']
            finally:
                raise e

        try:
            resp_data = resp.json()['token']
        except (KeyError, ValueError):
            raise exceptions.InvalidResponse(response=resp)
        else:
            self.members = []
            self.token_id = None
            return access.AccessInfoV3(resp.headers['X-Subject-Token'], **resp_data)

    @property
    def additional_auth_required(self):
        return self.token_id and self.members

    @property
    def auth_methods(self):
        return [self._auth_method]

    def select_account(self, member_id):
        member_id = str(member_id)
        assert member_id in [m['member_id'] for m in self.members]
        self.member_id = str(member_id)
        self._auth_method.token_id = self.token_id
        self._auth_method.member_id = member_id

    @classmethod
    def get_options(cls):
        options = super(Auth, cls).get_options()
        options.extend([
            cfg.StrOpt('username', help='Username'),
            cfg.StrOpt('password', secret=True, help='User\'s Password'),
            cfg.StrOpt('member_id', help='ID of the User\'s Member'),
            cfg.StrOpt('scope', help='Dict containing a scope for this auth request'),
        ])
        return options
