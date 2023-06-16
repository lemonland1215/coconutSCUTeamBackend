from datetime import datetime

def wj2o(obj_db, data={}):
    for key in obj_db.__class__.__dict__.keys():
        if key in data:
            setattr(obj_db, key, data[key])
        # if hasattr(obj_db, 'createtime'):
        #     setattr(obj_db, 'createtime', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# new_obj SOME_CLASS() # new_obj为操作数据库表的orm class对象
# wj2o(new_obj, a_dict) # a_dict为json数据源，前提是json数据和类对象的属性字段相对应，即json的key和数据库表字段相同