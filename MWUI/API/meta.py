# -*- coding: utf-8 -*-
#
#  Copyright 2016-2018 Ramil Nugmanov <stsouko@live.ru>
#  This file is part of MWUI.
#
#  MWUI is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
from flask_login import login_user, current_user
from flask_restful import Resource, marshal_with, marshal, reqparse
from .common import AuthResource, DBAuthResource, swagger, dynamic_docstring, authenticate, request_arguments_parser
from .marshal import AdditiveMagicResponseFields, LogInFields, LogInResponseFields
from ..constants import (AdditiveType, ModelType, TaskType, TaskStatus, StructureType, StructureStatus,
                         ResultType, UserRole)
from ..logins import UserLogin
from ..models import Additive


auth_post = reqparse.RequestParser(bundle_errors=True)
auth_post.add_argument('user', type=str, location='json', required=True, dest='username', case_sensitive=False,
                       store_missing=False, nullable=False, trim=True)
auth_post.add_argument('password', type=str, location='json', required=True)

additives_types_desc = ', '.join('{0.value} - {0.name}'.format(x) for x in AdditiveType)
models_types_desc = ', '.join('{0.value} - {0.name}'.format(x) for x in ModelType)


class AvailableAdditives(DBAuthResource):
    @swagger.operation(
        notes='Get available additives',
        nickname='additives',
        responseClass=AdditiveMagicResponseFields.__name__,
        responseMessages=[dict(code=200, message="additives list"), dict(code=401, message="user not authenticated")])
    @marshal_with(AdditiveMagicResponseFields.resource_fields)
    @dynamic_docstring(additives_types_desc)
    def get(self):
        """
        Get available additives list

        response format:
        additive - id
        name - name of additive
        structure - chemical structure in smiles or marvin or cml format
        type - additive type: {0}
        """
        return list(Additive.get_additives_dict().values()), 200


class MagicNumbers(AuthResource):
    @swagger.operation(
        notes='Magic Numbers',
        nickname='magic',
        responseMessages=[dict(code=200, message="magic numbers"),
                          dict(code=401, message="user not authenticated")])
    def get(self):
        """
        Get Magic numbers

        Dict of all magic numbers with values.
        """
        data = {x.__name__: self.__to_dict(x) for x in [TaskType, TaskStatus, StructureType, StructureStatus,
                                                        AdditiveType, ResultType, ModelType, UserRole]}

        return data, 200

    @staticmethod
    def __to_dict(enum):
        return {x.name: x.value for x in enum}


class LogIn(Resource):
    @swagger.operation(
        notes='user login',
        nickname='whoami',
        responseClass=LogInResponseFields.__name__,
        responseMessages=[dict(code=200, message="user data"),
                          dict(code=401, message="user not authenticated")])
    @authenticate
    @marshal_with(LogInResponseFields.resource_fields)
    def get(self):
        """
        Get user data
        """
        return current_user

    @swagger.operation(
        notes='App login',
        nickname='login',
        parameters=[dict(name='credentials', description='User credentials', required=True,
                         allowMultiple=False, dataType=LogInFields.__name__, paramType='body')],
        responseClass=LogInResponseFields.__name__,
        responseMessages=[dict(code=200, message="logged in"),
                          dict(code=400, message="invalid data"),
                          dict(code=403, message="bad credentials")])
    @request_arguments_parser(auth_post)
    def post(self, username, password):
        """
        Get auth token

        Token returned in headers as remember_token.
        for use task api send in requests headers Cookie: 'remember_token=_token_' or 'session=_session_'
        """
        if username:
            user = UserLogin.get(username, password)
            if user:
                login_user(user, remember=True)
                return marshal(user, LogInResponseFields.resource_fields)
        return dict(message='bad credentials'), 403
