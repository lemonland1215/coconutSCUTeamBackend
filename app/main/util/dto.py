from flask_restx import Namespace, fields
from datetime import datetime

CustomDate = fields.DateTime


class CustomDate(fields.DateTime):
    '''
    自定义CustomDate,原有的fileds.DateTime序列化后
    只支持 rfc822,ios8601 格式，新增 strftime 格式
    strftime格式下支持 format 参数，默认为 '%Y-%m-%d %H:%M:%S'
    '''

    def __init__(self, dt_format='rfc822', format=None, **kwargs):
        super().__init__(**kwargs)
        self.dt_format = dt_format

    def format(self, value):
        if self.dt_format in ('rfc822', 'iso8601'):
            return super().format(value)
        elif self.dt_format == 'str_time':
            if isinstance(value, str):
                return value
            return value.strftime('%Y-%m-%d %H:%M:%S')

        else:
            raise Exception('Unsupported date format %s' % self.dt_format)


searchWordsIn = {
    'id': fields.Integer(required=False, description='id'),
    'username': fields.String(required=False, description='name'),
    'sysrole': fields.String(required=False, description='sysrole'),
    'is_frozen': fields.String(required=False, description='is_frozen'),
    'orgid': fields.Integer(required=False, description='orgid')
}

IDs_In = {
    'id': fields.List(fields.Integer, required=True, description='提供多个编号，列表类型'),
}


class OrganizationDTO:
    ns = Namespace('organization', description='organization related operations')

    organizationIDsIn = ns.model('organizationIDsIn', IDs_In)

    organizationIn = ns.model('organizationIn', {
        'name': fields.String(required=True, description='organization name'),
        'logopath': fields.String(required=True, default="N/A", description='organization logo\'s file path'),
        'istoporg': fields.Boolean(required=True, default=False, description='is it a top organization'),
        'higherorgid': fields.Integer(required=True, description='higher organization id'),
        'islocked': fields.Boolean(required=True, default=False, description='can organization be modified'),
        'isfrozen': fields.Boolean(required=True, default=False, description='can organization be operated'),
        'frozenbyuid': fields.Integer(description='frozen id'),
        'clientcontact': fields.String(required=True, description='client contact name'),
        'comments': fields.String(required=True, description='organization comments'),
    }, strict=True)

    organizationOut = ns.model('organizationOut', {
        'id': fields.Integer(description='organization id'),
        'name': fields.String(description='organization name'),
        'logopath': fields.String(description='organization logo\'s file path'),
        'istoporg': fields.Boolean(description='is it a top organization'),
        'higherorgid': fields.Integer(description='organization id'),
        'islocked': fields.Boolean(description='can organization be modified'),
        'isfrozen': fields.Boolean(required=True, default=False, description='can organization be operated'),
        'createtime': CustomDate(required=True, description='the time when the organization created'),
        'modifytime': CustomDate(required=False, dt_format='str_time', description='like topic mentioned'),
        'freezetime': CustomDate(required=False, dt_format='str_time', description='like topic mentioned'),
        'clientcontact': fields.String(required=True, description='client contact name'),
        'comments': fields.String(description='organization comments'),
    })

    searchWordsIn = ns.model('searchIn', searchWordsIn)


class User_DTO:
    # 创建命名空间。生成一个api文档
    ns = Namespace('user', description='user related operations')

    user_IDs_In = ns.model('user_IDs_In', IDs_In)

    # 创建输入的DTO，对可输入字段进行过滤
    user_In = ns.model('user_In', {
        'username': fields.String(required=True, default="username", description='user_name'),
        'orgid': fields.Integer(required=True, default=1, description='orgid'),
        'email': fields.String(required=True, default="email", description='email'),
        'comment': fields.String(required=False, default="comment", description='comment'),
        'sysrole': fields.String(required=True, default="sysrole", description='system_role'),
        'password': fields.String(required=True, default="password", description='password')
    }, strict=True)

    user_Out = ns.model('user_Out', {
        'id': fields.String(),
        'username': fields.String(),
        'sysrole': fields.String(),
        'is_frozen': fields.String(),
        'is_locked': fields.Boolean(),
        'email': fields.String(),
        'orgid': fields.Integer()
    })

    updateIn = ns.model('user_Update', {
        'username': fields.String(required=False, description='name'),
        'password': fields.String(required=False, description='name'),
        'orgid': fields.Integer(required=False, description='orgid'),
        'sysrole': fields.String(required=False, description='sysrole'),
        'comment': fields.String(required=False, description='sysrole'),
    })

    searchWordsIn = ns.model('user_Search', searchWordsIn)


class AuthDTO:
    ns = Namespace('auth', description='authentication related operations')
    auth_dto = ns.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password'),
        'verify_code': fields.String(required=True, description='verify code string'),
    })


class Project_DTO:
    # 创建命名空间。生成一个api文档
    ns = Namespace('project', description='project related operations')

    project_IDs_In = ns.model('project_IDs_In', IDs_In)

    # 创建输入的DTO，对可输入字段进行过滤
    project_In = ns.model('project_In', {
        'projectname': fields.String(required=True, description='name'),
        'project_manager_id': fields.Integer(required=True, default=1, description='project_manager_id'),
        'orgid': fields.Integer(required=True, default=1, description='orgid'),
        'customer_contact': fields.String(required=False, description='客户对接人'),
        'contact_email': fields.String(required=False, description='客户联系邮箱'),
        'liaison_id': fields.Integer(required=True, default=1, description='联系人id'),
        'comment': fields.String(required=False, description='comment')
    }, strict=True)

    project_Out = ns.model('project_Out', {
        'id': fields.Integer(),
        'projectname': fields.String(),
        'project_manager': fields.String(),
        'orgid': fields.Integer(),
        'organization_name': fields.String(),
        'customer_contact': fields.String(),
        'contact_email': fields.String(),
        'liaison_id': fields.Integer(),
        'liaison_name': fields.String(),
        'liaison_email': fields.String(),
        'test_number': fields.Integer(),
        'is_frozen': fields.String(),
        'frozen_by': fields.Integer,
        'is_locked': fields.String(),
        'locked_by': fields.Integer,
        'comment': fields.String(),
        'status': fields.String(),
        'create_time': fields.String(),
        'modified_time': fields.String(),
    })

    updateIn = ns.model('project_Update', {
        'projectname': fields.String(required=False, description='name'),
        'project_manager_id': fields.Integer(required=False, description='project_manager_id'),
        'customer_contact': fields.String(required=False, description='客户对接人'),
        'contact_email': fields.String(required=False, description='客户联系邮箱'),
        'liaison_id': fields.Integer(required=False, description='liaison_id'),
        'comment': fields.String(required=False, description='sysrole')
    })

    searchIn = ns.model('project_Search', {
        'id': fields.Integer(required=False, description='id'),
        'projectname': fields.String(required=False, description='name'),
        'create_time': fields.String(required=False, description='create_time'),
        'modified_time': fields.String(required=False, description='modified_time'),
        'orgname': fields.String(required=False, description='orgname'),
        'orgid': fields.Integer(required=False, description='orgid'),
        'project_manager': fields.String(required=False, description='project_manager'),
        'is_frozen': fields.Boolean(required=False, description='is_frozen')
    })


class Task_DTO:
    ns = Namespace('task', description='task related operations')

    taskIDsIn = ns.model('taskIDsIn', IDs_In)

    taskIn = ns.model('taskIn', {
        'name': fields.String(required=True, description='task name'),
        'project_id': fields.Integer(required=True, description='project id'),
        'type': fields.String(required=True, description='task type'),
        'mail_id': fields.Integer(required=True, description='mail template id'),
        'status': fields.String(required=True, default='waiting', descripition='task status'),
        'catcher_id': fields.Integer(required=True, descripition='cather server id'),
        # 'catcher_name': fields.String(rrequired=True, descripition='cather server name'),
        'report_status': fields.Boolean(required=False, default=False, description='dose report be generated'),
        # 'project_manager': fields.String(required=True, description='task manager name(yifang)'),
        'target_num': fields.Integer(required=False, descripition='target num'),
        'target_id_list': fields.String(required=True, description='target list'),
        'delivery_name': fields.String(required=True, description='the name of the person that deliver the mail'),
        'delivery_time': fields.DateTime(required=False, description='发件时间'),
        'delivery_address': fields.String(required=True, description='the address of the delivery, like:deliver@mail'),
        'delivery_freq': fields.Integer(required=True, description='the frequency of the sending mails'),
        'mail_server_id': fields.Integer(required=True, description='server id'),
        # 'mail_server_name': fields.String(required='True', description='server name'),
        'islocked': fields.Boolean(required=True, default=False, description='can task be modified'),
        'isfrozen': fields.Boolean(required=True, default=False, description='can task be operated'),
        'ispaused': fields.Boolean(required=False, default=False, description='is this task still running'),
        'frozenbyuid': fields.Integer(description='frozen id'),
        'comments': fields.String(required=False, description='organization comments'),
    }, strict=True)

    taskOut = ns.model('taskOut', {
        'id': fields.Integer(description='task id'),
        'name': fields.String(description='task name'),
        'project_id': fields.String(description='top project id'),
        'type': fields.String(description='mail type'),
        # 'catcher_name': fields.String(description='catcher server name'),
        'report_status': fields.Boolean(required=True, default=False, description='dose report be generated'),
        'delivery_address': fields.String(description='delivery address'),
        'delivery_freq': fields.Integer(required=True, description='the frequency mail send'),
        'islocked': fields.Boolean(description='can task be modified'),
        'isfrozen': fields.Boolean(required=True, default=False, description='can task be operated'),
        # 'ispaused': fields.Boolean(default=False, description='just be paused, can be modified'),
        'createtime': CustomDate(required=True, description='the time when the task created'),
        'modifytime': CustomDate(required=False, dt_format='str_time', description='the time that be modified'),
        'freezetime': CustomDate(required=False, dt_format='str_time', description='the time that be frozen'),
        'puasetime': CustomDate(required=False, dt_format='str_time', description='the time that be puased'),
        'clientcontact': fields.String(required=True, description='client contact name'),
        'comments': fields.String(description='organization comments'),
    })

    searchIn = ns.model('task_Search', {
        'id': fields.Integer(required=False, description='id'),
        'name': fields.String(required=False, description='name'),
        'createtime': fields.DateTime(required=False, description='create_time'),
        'modifytime': fields.DateTime(required=False, description='modified_time'),
        'project_name': fields.String(required=False, description='project_name'),
        'project_id': fields.Integer(required=False, description='project_id'),
        'project_manager_id': fields.Integer(required=False, description='project_manager_id'),
        'is_frozen': fields.String(required=False, description='is_frozen')
    })

    updateIn = ns.model('task_Update',{
        'name': fields.String(description='name'),
        'type': fields.String(description='mail type'),
        'project_id': fields.Integer(description='父项目id'),
        'catcher_id': fields.Integer(description='捕获服务器id'),
        'mail_server_id': fields.Integer(description='邮件服务器id'),
        'delivery_freq': fields.Integer(description='发件频率'),
        'target_id_list': fields.String(description='目标人员list')
    })

    searchWordsIn = ns.model('searchIn', searchWordsIn)


class Mail_DTO:
    ns = Namespace('template_html', description='html template related operations')

    html_templateIDsIn = ns.model('html_templateIDsIn', IDs_In)

    html_template_in = ns.model('html_template_in', {
        'type': fields.String(required=True, default="text", description='模板类型：如文本/html、二进制、office等'),
        'subject': fields.String(required=True, default="1", description='邮件主题'),
        'content': fields.String(required=True, default="内容", description='邮件内容'),
        'attachid': fields.Integer(description='附件模板编号'),
        'islocked': fields.Boolean(description='是否锁定;锁定：不允许修改、删除。'),
        'comments': fields.String(description='备注'),
    })

    html_template_out = ns.model('html_template_out', {
        'id': fields.Integer(description='html template id'),
        'type': fields.String(required=True, default="text", description='模板类型：如文本/html、二进制、office等'),
        'subject': fields.String(required=True, default="1", description='邮件主题'),
        'content': fields.String(required=True, default="内容", description='邮件内容'),
        'attachid': fields.Integer(description='附件模板编号'),
        'islocked': fields.Boolean(description='是否锁定;锁定：不允许修改、删除。'),
        'comments': fields.String(description='备注'),
        'createtime': fields.DateTime(description='创建时间'),
        'createdbyuid': fields.Integer(description='创建人编号'),
        'modifytime': fields.DateTime(description='修改时间'),
        'modifybyuid': fields.Integer(description='修改人编号'),
    })

    searchWordsIn = ns.model('searchIn', searchWordsIn)


class Event_DTO:
    ns = Namespace('phishing_event', description='phishing event related operations')

    phishing_eventIDsIn = ns.model('phishing_eventIDsIn', IDs_In)

    phishing_event_in = ns.model('phishing_event_in', {
        'type': fields.String(required=True, description='中招事件类型'),
        # 'time': fields.DateTime(required=True, description='中招时间'),
        'user_input': fields.String(required=True, description='用户输入内容'),
        'uid': fields.Integer(required=True, description='中招人员id'),
        'task_id': fields.Integer(required=True, description='中招任务id'),
        'catcher_id': fields.Integer(description='捕获用服务器id'),
        'server_id': fields.Integer(description='发送方服务器id'),
    })

    phishing_event_out = ns.model('phishing_event_out', {
        'id': fields.Integer(description='中招事件编号'),
        'type': fields.String(required=True, description='中招事件类型'),
        'user_input': fields.String(required=True, description='用户输入内容'),
        'uid': fields.Integer(required=True, description='中招人员id'),
        'task_id': fields.Integer(description='中招任务id'),
        'catcher_id': fields.Integer(description='捕获用服务器id'),
        'server_id': fields.Integer(description='发送方服务器id'),
    })

    searchIn = ns.model('searchIn', {
        'uid': fields.Integer(required=True, description='中招人员id'),
        'task_id': fields.Integer(description='中招任务id'),
        'catcher_id': fields.Integer(description='捕获用服务器id'),
        'server_id': fields.Integer(description='发送方服务器id'),
    })

class Sender_DTO:
    ns = Namespace('server_sender', description='server sender event related operations')

    senderIDsIn = ns.model('senderIDsIn', IDs_In)

    sender_in = ns.model('sender_in', {
        'name': fields.String(required=True, default='name', description='sender name'),
        'server': fields.String(required=True, description='sender IP'),
        'port': fields.Integer(required=True, description='sender port'),
        'encryptalg': fields.String(required=True, description='加密算法'),
        'password': fields.String(required=True, description='密码'),
        'isfrozen': fields.Boolean(required=False, default=False, description='冻没'),
        'islocked': fields.Boolean(required=False, default=False, description='锁没'),
        'comments': fields.String(description='备注'),
    })

    sender_out = ns.model('sender_out', {
        'id': fields.Integer(description='id'),
        'name': fields.String(description='sender name'),
        'server': fields.String(description='sender IP'),
        'port': fields.Integer(description='sender port'),
        'encryptalg': fields.String(description='加密算法'),
        'isfrozen': fields.Boolean(description='冻没'),
        'freezetime': fields.DateTime(description='冻结时间'),
        'islocked': fields.Boolean(description='锁没'),
        'locktime': fields.DateTime(description='锁定时间'),
        'createdbyuid': fields.Integer(description='创建者id'),
        'createtime':fields.DateTime(description='创建时间'),
        'modifiedbyuid': fields.Integer(description='修改者id'),
        'modifytime': fields.DateTime(description='修改时间')
    })

    sender_search = ns.model('sender_search', {
        'name': fields.String(description='sender name'),
        'server': fields.String(description='sender IP'),
        'port': fields.Integer(description='sender port'),
        'encryptalg': fields.String(description='加密算法'),
        'isfrozen': fields.Boolean(description='冻没'),
        'islocked': fields.Boolean(description='锁没')
    })

    sender_update = ns.model('sender_update', {
        'name': fields.String(required=True, description='sender name'),
        'server': fields.String(description='sender IP'),
        'port': fields.Integer(description='sender port'),
        'encryptalg': fields.String(description='加密算法'),
        'password': fields.String(description='密码')
    })

class Catcher_DTO:
    ns = Namespace('server_catcher', description='server catcher event related operations')

    catcherIDsIn = ns.model('catcherIDsIn', IDs_In)

    catcher_in = ns.model('catcher_in', {
        'name': fields.String(required=True, default='name', description='sender name'),
        'server': fields.String(required=True, description='sender IP'),
        'port': fields.Integer(required=True, description='sender port'),
        'isfrozen': fields.Boolean(required=False, default=False, description='冻没'),
        'islocked': fields.Boolean(required=False, default=False, description='锁没'),
        'comments': fields.String(description='备注'),
    })

    catcher_out = ns.model('catcher_out', {
        'id': fields.Integer(description='id'),
        'name': fields.String(required=True, description='sender name'),
        'server': fields.String(description='sender IP'),
        'port': fields.Integer(description='sender port'),
        'isfrozen': fields.Boolean(description='冻没'),
        'freezetime': fields.DateTime(description='冻结时间'),
        'islocked': fields.Boolean(description='锁没'),
        'locktime': fields.DateTime(description='锁定时间'),
        'lockbyuid': fields.DateTime(description='锁定人编号'),
        'createdbyuid': fields.Integer(description='创建者id'),
        'createtime':fields.DateTime(description='创建时间'),
        'modifiedbyuid': fields.Integer(description='修改者id'),
        'modifytime': fields.DateTime(description='修改时间'),
        'frozenbyuid': fields.Integer(description='创建者id'),
        'freezetime': fields.DateTime(description='创建时间'),
    })

    catcher_search = ns.model('catcher_search', {
        'name': fields.String(description='sender name'),
        'server': fields.String(description='sender IP'),
        'port': fields.Integer(description='sender port'),
        'isfrozen': fields.Boolean(description='冻没'),
        'islocked': fields.Boolean(description='锁没')
    })

    catcher_update = ns.model('catcher_update', {
        'name': fields.String(required=True, description='sender name'),
        'server': fields.String(description='sender IP'),
        'port': fields.Integer(description='sender port'),
    })


class File_DTO:
    ns = Namespace('upload', description='file and image related operations')


class Log_DTO:
    ns = Namespace('log', description='log related operations')

    log_IDs_In = ns.model('log_IDs_In', IDs_In)

    log_Out = ns.model('log_Out', {
        'id': fields.Integer(),
        'type': fields.String(),
        'operator_id': fields.Integer(),
        'operator': fields.String(),
        'role': fields.String(),
        'details': fields.String(),
        'time': fields.String()
    })

    log_Search = ns.model(('log_search'), {
        'id': fields.Integer(required=False, description='log id'),
        'type': fields.String(required=False, description='log type'),
        'operator_id': fields.Integer(required=False, description='operator id'),
        'operator': fields.String(required=False, description='operator name'),
        'role': fields.String(required=False, description='operator role'),
        'details': fields.String(required=False, description='details'),
        'time': fields.String(required=False, description='time')
    })
