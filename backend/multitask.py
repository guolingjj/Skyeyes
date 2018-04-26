import json,subprocess
from audit import models
from django import conf
class MultiTaskManage():
    def __init__(self,req):
        self.req=req
        self.run_task()
        pass
    def parse_task(self):
        '''解析任务'''
        self.task_arguments = json.loads(self.req.POST.get('task_args'))
        self.task_type=self.task_arguments['task_type']



        pass
    def run_task(self):
        self.parse_task()
        if hasattr(self,self.task_type):
            task_type_run=getattr(self,self.task_type)
            task_type_run()
        else:
            print('can not find task_type:',self.task_type)

    def cmd(self):
        '''批量cmd类型任务
        1.生成任务在数据库中的记录,达到任务id
        2.触发任务,不阻赛
        3.返回任务id给前段

        '''
        task_obj=models.Task.objects.create(
            task_type='cmd',
            content=self.task_arguments['cmd'],
            user=self.req.user
        )
        self.host_id_list=set(self.task_arguments['host_array'])
        sub_task_objs=[]
        for i in self.host_id_list:
            sub_task_objs.append(models.TaskLogDetail(
                task=task_obj,
                bind_host_id=int(i),
                run_result='',
            ))
        models.TaskLogDetail.objects.bulk_create(sub_task_objs)

        print ('start running-------------------')
        run_py_dir=conf.settings.MUTIL_RUN
        run_py_dir=run_py_dir+' '+str(task_obj.id)
        print('-----',run_py_dir)
        sub_run=subprocess.Popen(run_py_dir,shell=True)
        self.task_id=task_obj.id