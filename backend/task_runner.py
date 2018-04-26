import sys,os




if __name__=='__main__':
    #设置当前的运行路径
    current_base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    sys.path.append(current_base_dir)
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Skyeyes.settings")
    django.setup()
    from audit import models
    import time
    if len(sys.argv) == 1:#执行pyton 脚本的时候可以动态传入参数
        exit('task id not provided')
    task_id=sys.argv[1]
    task_obj=models.Task.objects.get(id=task_id)
    print('task runner...',task_obj)
    time.sleep(10)
    task_obj.content='test'
    task_obj.save()