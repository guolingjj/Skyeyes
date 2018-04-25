

class UserProtal():
    '''用户命令行端交互入口'''

    def __init__(self):
        self.user = None

    def user_auth(self):
        '''完成用户交互'''
        retry_count = 0
        while retry_count < 3:
            email = input('Email:').strip()
            if len(email) == 0: continue
            password = getpass.getpass("Password").strip()


            if not password:
                print("Password cannot be null")
                print("--------------please retry-----------")
                continue
            user = authenticate(username=email, password=password)
            if user:
                self.user = user
                return
            else:
                print('Invalid password or email')
                print("--------------please retry-----------")
            retry_count += 1
        else:
            exit('Too many attemps...')

    def user_choice_func(self, user_choice):
        if len(user_choice) == 0: return 'false'
        if user_choice.isdigit(): return int(user_choice)

    def interactive(self):
        '''交互函数'''
        self.user_auth()
        if self.user:
            # print(self.user.bind_hosts.all())
            exit_flag = False
            while not exit_flag:
                group = self.user.host_group.all()
                for index, i in enumerate(group):
                    print('%s %s[%s]' % (index, i, i.bind_hosts.all().count()))
                print('%s. Ungrouphost[%s]' % (index + 1, self.user.bind_hosts.all().count()))

                user_choice = input('Choice anyGroup you want').strip()
                user_choice = self.user_choice_func(user_choice)
                if user_choice == 'false':
                    print('Invalid input')
                    print("--------------please retry-----------")
                    continue
                if user_choice >= 0 and user_choice <= group.count():

                    if user_choice == group.count():
                        selected_hostgroup = self.user
                    else:
                        selected_hostgroup = group[user_choice]
                    while True:
                        for index, host in enumerate(selected_hostgroup.bind_hosts.all()):
                            print("%s.%s " % (index, host))
                        user_choice = input('Choice anyhost you want').strip()
                        user_choice = self.user_choice_func(user_choice)
                        if user_choice == 'false':
                            print('Invalid input')
                            print("--------------please retry-----------")
                            continue
                        else:
                            if user_choice >= 0 and user_choice < selected_hostgroup.bind_hosts.all().count():
                                t = time.time()
                                m = hashlib.md5()
                                m.update(str(t).encode('utf-8'))
                                md5_str = m.hexdigest()
                                selected_host = selected_hostgroup.bind_hosts.all()[user_choice]
                                login_cmd = 'sshpass -p {password} ssh {user}@{ip_addr} -o StrictHostKeyChecking=no -Z {md5_str}'.format(
                                    password=selected_host.host_user.password,
                                    user=selected_host.host_user.username,
                                    ip_addr=selected_host.host.ip_addr,
                                    md5_str=md5_str
                                )
                                print(login_cmd)
                                session_tracker=settings.SESSION_TRACKER
                                tracker_obj=subprocess.Popen('%s %s'%(session_tracker,md5_str),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=settings.BASE_DIR)


                                ssh_conect = subprocess.run(login_cmd, shell=True)
                                print('exit')

                                print(tracker_obj.stdout.read().decode(),tracker_obj.stderr.read().decode())
                                print('curret user:',self.user)
                                print('bind_host:',selected_host)
                                models.SeesionLog.objects.create(
                                    user=self.user,
                                    bind_host=selected_host,
                                    session_tag=md5_str,
                                )

                            else:
                                print('Invalid input')
                                print("--------------please retry-----------")
                                continue
                                # 判断user_choice的值然后退出..

                else:
                    print('Invalid input')
                    print("--------------please retry-----------")
                    continue


if __name__ == '__main__':

    import django
    import getpass, os, subprocess, hashlib, time

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Skyeyes.settings")
    django.setup()
    from django.contrib.auth import authenticate
    from audit import models
    from Skyeyes import settings
    portal = UserProtal()
    portal.interactive()
