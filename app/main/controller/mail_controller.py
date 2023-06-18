from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource

from app.main import db
from ..util.dto import Mail_DTO
from ..service.mail_service import *
from typing import Dict, Tuple

from ..util.file import upload_file
from ..util.response_tip import *
from ..util.write_json_to_obj import wj2o

ns = Mail_DTO.ns
_htmlTemplateIn = Mail_DTO.html_template_in
_htmlTemplateOut = Mail_DTO.html_template_out
_searchWordsIn = Mail_DTO.searchWordsIn
_htmlTemplateIDsIn = Mail_DTO.html_templateIDsIn

@ns.route('/template')
class MailTemplates(Resource):

    @ns.doc('list_of_templates')
    # @admin_token_required
    @ns.marshal_list_with(_htmlTemplateOut, envelope='children')
    # @jwt_required
    def get(self):
        """List all mail templates"""
        return get_all_mail_templates()

    @ns.expect(_htmlTemplateIn, validate=True)
    @ns.response(201, 'Template successfully created.')
    @ns.doc('create a new mail template')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new mail template """
        data = request.json
        return save_new_mail_template(data=data)

    @ns.doc('delete templates')
    @ns.expect(_htmlTemplateIDsIn, validate=True)
    def delete(self):
        """Delete mail templates"""
        htmlTemplateIDs = request.json
        for id in htmlTemplateIDs['id']:
            operate_a_mail_template(id, "delete")
        return response_with(SUCCESS_201)

@ns.route('/template/<id>')
@ns.param('id', 'The Mail Template identifier')
@ns.response(404, 'Template not found.')
class MailTemplate(Resource):
    @ns.doc('delete a mail template')
    def delete(self, id):
        """delete a template"""
        mailtemplate, resp_status_code = get_a_mail_template(id)
        if not mailtemplate:
            ns.abort(404)
        else:
            return operate_a_mail_template(id, "delete")

    @ns.expect(_htmlTemplateIn, validate=True)
    @ns.response(201, 'Template successfully modified.')
    @ns.doc("update a template's info")
    def put(self, id):
        """update a template's info, status not included"""
        return update_a_mail_template(id)

    @ns.doc('get a mail template')
    @ns.marshal_with(_htmlTemplateOut)
    def get(self, id):
        """get a mail template by its id"""
        mailtemplate, http_code = get_a_mail_template(id)
        if not mailtemplate:
            ns.abort(404)
        else:
            return mailtemplate

@ns.route('/template/search')
class SearchForMailTemplates(Resource):
    """mail template view"""

    @ns.doc('search for mail templates')
    @ns.marshal_list_with(_htmlTemplateOut, envelope='children')
    @ns.expect(_searchWordsIn, validate=True)
    def post(self):
        """search for tasks by id, partial_name, create_time, modify_time, status, mail_server_name, catcher_name"""
        data = request.json
        return search_for_mail_templates(data)

@ns.route('/template/action/<operator>')
@ns.param('operator', 'such as freeze|unfreeze, lock|unlock, pause|restart|stop|finish, delete etc')
@ns.response(404, 'Task not found.')
class PatchMailTemplates(Resource):
    """task view"""

    @ns.doc('operate MailTemplates')
    @ns.expect(_htmlTemplateIn, validate=True)
    def patch(self, operator):
        """modify the status of a task"""
        MailTemplatesIDs = request.json
        for id in MailTemplatesIDs['data']:
            operate_a_mail_template(id, operator)
        return response_with(SUCCESS_201)

@ns.route('/template/<id>/action/<operator>')
@ns.param('operator', 'such as freeze|unfreeze, lock|unlock, pause|restart|stop|finish, delete etc')
@ns.param('id', 'The MailTemplate identifier')
@ns.response(404, 'Task not found.')
class PatchAMailTemplate(Resource):
    """task view"""

    @ns.doc('modify a MailTemplate status')
    def patch(self, id, operator):
        """modify the status of organizations, status enum: lock|unlock"""
        task, http_code = get_a_mail_template(id)
        if not task:
            ns.abort(404)
        else:
            return operate_a_mail_template(id, operator)

@ns.route('/sendmail/<id>')
@ns.param('id', 'The Task identifier')
@ns.response(404, 'Task not found.')
class SendMailofTask(Resource):
    """task view"""
    @ns.doc('send mails of a task')
    def get(self):
        """send mails of a task"""
        send_mails_of_task(id)
        return response_with(SUCCESS_201)








