from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from app.main import db
from ..util.dto import Task_DTO
from ..service.task_service import *
from typing import Dict, Tuple

from ..util.file import upload_file
from ..util.response_tip import *
from ..util.write_json_to_obj import wj2o

ns = Task_DTO.ns
_taskIn = Task_DTO.taskIn
_taskOut = Task_DTO.taskOut
_searchWordsIn = Task_DTO.searchWordsIn
_taskIDsIn = Task_DTO.taskIDsIn

@ns.route('/')
class Tasks(Resource):

    @ns.doc('list_of_tasks')
    # @admin_token_required
    @ns.marshal_list_with(_taskOut, envelope='children')
    # @jwt_required
    def get(self):
        """List all tasks"""
        return get_all_tasks()

    @ns.expect(_taskIn, validate=True)
    @ns.response(201, 'Task successfully created.')
    @ns.doc('create a new task')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new Task """
        data = request.json
        return save_new_task(data=data)

    @ns.doc('delete tasks')
    @ns.expect(_taskIDsIn, validate=True)
    def delete(self):
        """Delete Tasks"""
        taskIDs = request.json
        for id in taskIDs['id']:
            operate_a_task(id, "delete")
        return response_with(SUCCESS_201)

@ns.route('/<id>')
@ns.param('id', 'The Task identifier')
@ns.response(404, 'Task not found.')
class Task(Resource):
    @ns.doc('delete a task')
    def delete(self, id):
        """fxxking delete a task"""
        task, resp_status_code = get_a_task(id)
        if not task:
            ns.abort(404)
        else:
            return operate_a_task(id, "delete")

    @ns.expect(_taskIn, validate=True)
    @ns.response(201, 'Task successfully modified.')
    @ns.doc("update a task's info")
    def put(self, id):
        """update a task's info, status not included"""
        return update_a_task(id)

    @ns.doc('get a task')
    @ns.marshal_with(_taskOut)
    def get(self, id):
        """get a task by its id"""
        task, http_code = get_a_task(id)
        if not task:
            ns.abort(404)
        else:
            return task

@ns.route('/search')
class SearchForTasks(Resource):
    """task view"""

    @ns.doc('search for orgs')
    @ns.marshal_list_with(_taskOut, envelope='children')
    @ns.expect(_searchWordsIn, validate=True)
    def post(self):
        """search for tasks by id, partial_name, create_time, modify_time, status, mail_server_name, catcher_name"""
        data = request.json
        return search_for_tasks(data)

@ns.route('/action/<operator>')
@ns.param('operator', 'such as freeze|unfreeze, lock|unlock, pause|restart|stop|finish, delete etc')
@ns.response(404, 'Task not found.')
class PatchTasks(Resource):
    """task view"""

    @ns.doc('operate tasks')
    @ns.expect(_taskIDsIn, validate=True)
    def patch(self, operator):
        """modify the status of a task"""
        taskIDs = request.json
        for id in taskIDs['data']:
            operate_a_task(id, operator)
        return response_with(SUCCESS_201)

@ns.route('/<id>/action/<operator>')
@ns.param('operator', 'such as freeze|unfreeze, lock|unlock, pause|restart|stop|finish, delete etc')
@ns.param('id', 'The Task identifier')
@ns.response(404, 'Task not found.')
class PatchATask(Resource):
    """task view"""

    @ns.doc('modify a task status')
    def patch(self, id, operator):
        """modify the status of organizations, status enum: lock|unlock"""
        task, http_code = get_a_task(id)
        if not task:
            ns.abort(404)
        else:
            return operate_a_task(id, operator)








