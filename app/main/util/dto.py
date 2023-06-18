from flask_restx import Namespace, fields

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
        'logopath': fields.String(required=True, default="N/A",description='organization logo\'s file path'),
        'istoporg': fields.Boolean(required=True, default=False, description='is it a top organization'),
        'higherorgid': fields.Integer(required=True, description='higher organization id'),
        'islocked': fields.Boolean(required=True, default=False,description='can organization be modified'),
        'isfrozen': fields.Boolean(required=True, default=False,description='can organization be operated'),
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
        'is_locked': fields.String(),
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
        'project_manager_id': fields.Integer(required=False, description='project_manager_id'),
        'orgid': fields.Integer(required=False, description='orgid'),
        'customer_contact': fields.String(required=False, description='客户对接人'),
        'contact_email': fields.String(required=False, description='客户联系邮箱'),
        'liaison_id': fields.Integer(required=False, description='联系人id'),
        'comment': fields.String(required=False, description='comment'),
        # 'status': fields.String(required=True, description='status')
    }, strict=True)

    project_Out = ns.model('project_Out', {
        'id': fields.Integer(),
        'projectname': fields.String(),
        'project_manager': fields.String(),
        'customer_contact': fields.String(),
        'contact_email': fields.String(),
        'liaison_name': fields.String(),
        'liaison_email': fields.String(),
        'test_number': fields.Integer(),
        'is_frozen': fields.String(),
        'comment': fields.String(),
        'status': fields.String()
    })

    updateIn = ns.model('project_Update', {
        'projectname': fields.String(required=False, description='name'),
        'project_manager_id': fields.String(required=False, description='project_manager_id'),
        'customer_contact': fields.String(required=False, description='客户对接人'),
        'contact_email': fields.String(required=False, description='客户联系邮箱'),
        'liaison_id': fields.String(required=False, description='liaison_id'),
        'comment': fields.String(required=False, description='sysrole')
    })

    searchIn = ns.model('project_Search', {
        'id': fields.Integer(required=False, description='id'),
        'projectname': fields.String(required=False, description='name'),
        'create_time': fields.DateTime(required=False, description='create_time'),
        'modified_time': fields.DateTime(required=False, description='modified_time'),
        'orgname': fields.String(required=False, description='orgname'),
        'orgid': fields.Integer(required=False, description='orgid'),
        'project_manager': fields.String(required=False, description='project_manager'),
        'is_frozen': fields.String(required=False, description='is_frozen')
    })

class Task_DTO:
    ns = Namespace('task', description='task related operations')

    taskIDsIn = ns.model('taskIDsIn', IDs_In)

    taskIn = ns.model('taskIn', {
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

    taskOut = ns.model('taskOut', {
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


class Mail_DTO:
    ns = Namespace('template_html', description='html template related operations')

    html_templateIDsIn = ns.model('html_templateIDsIn', IDs_In)

    html_template_in = ns.model('html_template_in', {
        'type': fields.Integer(reqired=True, default=1, description='模板类型：如文本/html、二进制、office等'),
        'name': fields.String(reqired=True, default="1", description='模板名称;例：中石油-上级发文，xx局-入学通知，xx部门-人事任免公告等'),
        'subject': fields.String(reqired=True, default="1", description='邮件主题'),
        'content': fields.String(reqired=True, default="内容", description='邮件内容'),
        'attachid': fields.Integer(description='附件模板编号'),
        'islocked': fields.Boolean(description='是否锁定;锁定：不允许修改、删除。'),
        'ishidden': fields.Boolean(description='是否隐藏;隐藏：不可被选择使用'),
        'comments': fields.String(description='备注'),
    })

    html_template_out = ns.model('html_template_out', {
        'id': fields.Integer(description='html template id'),
        'type': fields.Integer(description='模板类型：如文本/html、二进制、office等'),
        'name': fields.String(description='模板名称;例：中石油-上级发文，xx局-入学通知，xx部门-人事任免公告等'),
        'subject': fields.String(description='邮件主题'),
        'content': fields.String(description='邮件内容'),
        'attachid': fields.Integer(description='附件模板编号'),
        'islocked': fields.Boolean(description='是否锁定;锁定：不允许修改、删除。'),
        'createtime': fields.DateTime(description='创建时间'),
        'createdbyuid': fields.Integer(description='创建人编号'),
        'lastmodifiedtime': fields.DateTime(description='修改时间'),
        'lastmodifiedbyuid': fields.Integer(description='修改人编号'),
        'ishidden': fields.Boolean(description='是否隐藏;不可被选择使用'),
        'comments': fields.String(description='备注'),
    })

    searchWordsIn = ns.model('searchIn', searchWordsIn)