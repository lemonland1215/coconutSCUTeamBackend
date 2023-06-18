from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from app.main import db
from ..util.dto import OrganizationDTO
from ..service.organization_service import save_new_organization, get_all_organizations, get_an_organization, \
    get_sub_organizations, update_an_organization, operate_an_organization, search_for_organizations, \
    get_parent_organization, get_org_by_user_id
from typing import Dict, Tuple

from ..util.file import upload_file
from ..util.response_tip import *
from ..util.write_json_to_obj import wj2o

ns = OrganizationDTO.ns
_organizationIn = OrganizationDTO.organizationIn
_organizationOut = OrganizationDTO.organizationOut
_searchWordsIn = OrganizationDTO.searchWordsIn
_organizationIDsIn = OrganizationDTO.organizationIDsIn


@ns.route('/')
class Organizations(Resource):

    @ns.doc('list_of_registered_organizations')
    # @admin_token_required
    @ns.marshal_list_with(_organizationOut, envelope='children')
    # @jwt_required
    def get(self):
        """List all registered organizations"""
        return get_all_organizations()

    @ns.expect(_organizationIn, validate=True)
    @ns.response(201, 'Organization successfully created.')
    @ns.doc('create a new organization')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new Organization """
        data = request.json
        return save_new_organization(data=data)

    @ns.doc('delete organizations')
    @ns.expect(_organizationIDsIn, validate=True)
    def delete(self):
        """WARNING! Deleting an organization will leading to the children tests stopped and relative data deleted!"""
        organizationIDs = request.json
        for id in organizationIDs['id']:
            operate_an_organization(id, "delete")
        return response_with(SUCCESS_201)

    @ns.route('/logo')
    class UploadLogo(Resource):
        upload_parser = ns.parser()
        upload_parser.add_argument('file', location='files',
                                   type=FileStorage, required=True)
        upload_parser.add_argument("name", type=str, required=True, location="form")

        @ns.expect(upload_parser)
        def post(self):
            """
            上传一个组织的图标
            Returns:
                json
            """

            return upload_file(subdir='logo')


@ns.route('/<id>/sub_organization')
class Get_Sub_Organizations(Resource):
    @ns.doc('list_sub_organizations of their parent that have the offered id')
    @ns.marshal_list_with(_organizationOut, envelope='children')
    def get(self, id):
        """List all registered organizations"""
        return get_sub_organizations(id)


@ns.route('/<id>/parent_organization')
class Get_Parent_Organizations(Resource):
    @ns.doc('list the parent organization of an organization that have the offered id')
    @ns.marshal_with(_organizationOut)
    def get(self, id):
        """get the parent of an organizations"""
        return get_parent_organization(id)


@ns.route('/<id>')
@ns.param('id', 'The Organization identifier')
@ns.response(404, 'Organization not found.')
class Organization(Resource):
    @ns.doc('delete an organization')
    def delete(self, id):
        """WARNING! Deleting an organization will leading to the children tests stopped and relative data deleted!"""
        organization, resp_status_code = get_an_organization(id)
        if not organization:
            ns.abort(404)
        else:
            return operate_an_organization(id, "delete")

    @ns.expect(_organizationIn, validate=True)
    @ns.response(201, 'Organization successfully modified.')
    @ns.doc("update an org's info")
    def put(self, id):
        """update an org's info, status not included"""
        return update_an_organization(id)

    @ns.doc('get an organization')
    @ns.marshal_with(_organizationOut)
    def get(self, id):
        """get an organization by its id"""
        organization, http_code = get_an_organization(id)
        if not organization:
            ns.abort(404)
        else:
            return organization


@ns.route('/search')
class SearchForOrganizations(Resource):
    """organization view"""

    @ns.doc('search for orgs')
    @ns.marshal_list_with(_organizationOut, envelope='children')
    @ns.expect(_searchWordsIn, validate=True)
    def post(self):
        """search for organizations by id, partial_name, create_time, modify_time"""
        data = request.json
        return search_for_organizations(data)


@ns.route('/action/<operator>')
@ns.param('operator', 'such as freeze|unfreeze, lock|unlock, delete etc')
@ns.response(404, 'Organization not found.')
class PatchOrganizations(Resource):
    """organization view"""

    @ns.doc('operate organizations')
    @ns.expect(_organizationIDsIn, validate=True)
    def patch(self, operator):
        """modify the status of an org"""
        organizationIDs = request.json
        for id in organizationIDs['data']:
            operate_an_organization(id, operator)
        return response_with(SUCCESS_201)


@ns.route('/<id>/action/<operator>')
@ns.param('operator', 'such as freeze|unfreeze, lock|unlock, delete etc')
@ns.param('id', 'The Organization identifier')
@ns.response(404, 'Organization not found.')
class PatchAnOrganization(Resource):
    """organization view"""

    @ns.doc('modify an organization status')
    def patch(self, id, operator):
        """modify the status of organizations, status enum: lock|unlock"""
        organization, http_code = get_an_organization(id)
        if not organization:
            ns.abort(404)
        else:
            return operate_an_organization(id, operator)


@ns.route('/user/<uid>')
@ns.param('uid', 'The user identifier')
@ns.response(404, 'Organization not found.')
class User(Resource):
    @ns.marshal_with(_organizationOut)
    def get(self, uid):
        """get a user's org by uid"""
        org, http_code = get_org_by_user_id(uid)
        if not org:
            return response_with(INVALID_INPUT_422)
        else:
            return org, 201


