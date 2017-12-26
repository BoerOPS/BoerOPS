import os
import subprocess
import tarfile

from models.deploys import Deploy as DeployModel


class DeployService:
    def __init__(self, deploy, config):
        self.deploy = deploy
        self.checkout_path = config.get('CHECKOUT_PATH')
        self.deploy_path = config.get('DEPLOY_PATH')

    def test(self):
        return '部署成功'

    def step_1(self, repo_ssh_url, repo_name):
        "clone or fetch repo"
        commit_id = self.deploy.commit_id
        # prepare code
        full_checkout_path = os.path.join(self.checkout_path, repo_name)
        full_deploy_path = os.path.join(self.deploy_path, repo_name)
        if os.path.exists(full_checkout_path) and os.path.isdir(
                full_checkout_path):
            cmd = 'git reset -q --hard origin/master && git fetch --all -q'
            rs = subprocess.run(cmd, shell=True, cwd=full_checkout_path)
            if rs.returncode:
                return {'status': 1, 'msg': 'git fetch failed'}
        else:
            cmd = 'git clone -q %s %s' % (repo_ssh_url, repo_name)
            rs = subprocess.run(cmd.split(), cwd=self.checkout_path)
            if rs.returncode:
                return {'status': 1, 'msg': 'git clone failed'}
        cmd = 'git reset -q --hard %s' % commit_id
        rs = subprocess.run(cmd.split(), cwd=full_checkout_path)
        if rs.returncode:
            return {'status': 1, 'msg': 'git reset failed'}
        # EXCLUDE_DIRS = ['.git']
        # EXCLUDE_FILES = ['.gitignore']
        # os.chdir(self.checkout_path)
        # with tarfile.open(full_deploy_path + '.tgz', 'w:gz') as tar:
        #     for root, dirs, files in os.walk(repo_name):
        #         dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        #         for file in files:
        #             if file in EXCLUDE_FILES:
        #                 continue
        #             fullpath = os.path.join(root, file)
        #             tar.add(fullpath)
        DeployModel.update(self.deploy, status=1)
        return {'status': 1, 'msg': 'prepare code success'}

    def step_2(self):
        # exec before commands
        cmd = self.deploy.project.before_cmd
        # TODO
        # exec default commands
        cmd = 'tar -zcf %s.tgz --exclude-vcs --exclude-vcs-ignores -C %s .' % (
            repo_name, full_checkout_path)
        rs = subprocess.run(cmd.split(), cwd=self.deploy_path)
        if rs.returncode:
            return {'status': 2, 'msg': 'shell tar failed'}
        DeployModel.update(self.deploy, status=2)
        return {'status': 2, 'msg': 'exec before commands success'}

    def step_3(self):
        # deploy
        pass

    def step_4(self):
        # exec after commands
        pass

    def deploy_task(self, project_id, environ):
        c_d = self.first(
            project_id=project_id,
            status=0) if int(environ) != 2 else self.first(
                project_id=project_id, status=3)
        if not c_d:
            return
        # 检出代码库
        cmd = 'git clone -q %s %s' % (c_d.project.repo_url,
                                      c_d.project.checkout_dir)
        git_path = os.path.join(c_d.project.checkout_dir, '.git')
        if os.path.exists(git_path) and os.path.isdir(git_path):
            cmd = 'cd %s && git fetch --all -fq' % c_d.project.checkout_dir
        rc = subprocess.call(cmd, shell=True)
        # 指定版本
        cmd = 'cd %s && git reset -q --hard %s' % (c_d.project.checkout_dir,
                                                   c_d.version.strip())
        rc = subprocess.call(cmd, shell=True)
        # 同步到编译/打包目录
        cmd = 'rsync -qa --delete --exclude .git %s%s %s%s' % (
            c_d.project.checkout_dir, os.sep, c_d.project.compile_dir, os.sep)
        rc = subprocess.call(cmd, shell=True)
        # 执行用户自定义命令（权限，fis编译，打包）
        cmds = c_d.project.compile_cmd.split('\n')
        cmds = ' && '.join(cmds)
        rc = subprocess.call(cmds, shell=True)
        # 获取ansible动态Inventory
        resource = get_dynamic_inventory(c_d.project, environ)
        host_lists = [
            h.ip_address for h in c_d.project.hosts
            if h.environ == int(environ)
        ]
        # 执行ansible playbook
        runner = MyRunner(resource)
        runner.run_playbook(host_lists, c_d.project.playbook_path)
        if int(environ) == 2:
            self.update(c_d, status=4)
        else:
            self.update(c_d, status=1)
        # return runner.get_playbook_result()
        return self.get(id=c_d.id).status

    def update_repo(self, repo_path, repo_url, commit_id):
        git_path = os.path.join(repo_path, '.git')
        if os.path.exists(git_path) and os.path.isdir(git_path):
            # command 有&&就要shell=True
            cmd = 'cd %s && git reset -q --hard origin/master && git fetch -q' % repo_path
            rc = subprocess.check_call(cmd, shell=True, cwd=repo_path)
            os.chdir(repo_path)
        else:
            if os.path.exists(os.path.dirname(repo_path)) and os.path.isdir(
                    os.path.dirname(repo_path)):
                shutil.rmtree(os.path.dirname(repo_path))
            else:
                os.makedirs(os.path.dirname(repo_path))
            cmd = 'git clone -q %s %s' % (repo_url,
                                          os.path.basename(repo_path))
            rc = subprocess.check_call(
                cmd.split(), cwd=os.path.dirname(repo_path))
            os.chdir(repo_path)
        # 指定commit_id
        cmd = 'git reset -q --hard %s' % commit_id
        rc = subprocess.check_call(cmd.split(), cwd=repo_path)

    def rsync_local(self, src, dest, excludes=[]):
        excludes.append('.git')
        exclude_args = ''
        for e in excludes:
            exclude_args = exclude_args + ' --exclude %s' % e
        cmd = 'rsync -qa --delete %s %s%s %s%s' % (exclude_args, src, os.sep,
                                                   dest, os.sep)
        rc = subprocess.check_call(cmd.split())

    def chk_and_set_exe(self, src_path):
        if not os.access(src_path, os.X_OK):
            os.chmod(src_path, 755)


# @celery.task
def exec_custom_cmd(script_file):
    if os.path.exists(script_file) and os.path.isfile(script_file):
        chk_and_set_exe(script_file)
        # output = subprocess.check_output(script_file, shell=False)
        # return output
        p = Popen(script_file, stdout=PIPE)
        c_pid = p.pid
        output = p.communicate()[0]
        rc = p.wait()
        if rc == 0:
            result = output
            deploy_type = json.loads(redis.rpop('deploy_type'))
            recipients = json.loads(redis.rpop('recipients'))
            carbon_copy = json.loads(redis.rpop('carbon_copy'))
            functions = json.loads(redis.rpop('functions'))
            restart_service = json.loads(redis.rpop('restart_service'))
            subject = json.loads(redis.rpop('subject'))
            name = json.loads(redis.rpop('name'))
            repo_name = json.loads(redis.rpop('repo_name'))
            commit_id = json.loads(redis.rpop('commit_id'))
            commit_msg = json.loads(redis.rpop('commit_msg'))
            if restart_service:
                restarted_phpfpm_service.delay()
            send_async_email.delay(
                'boer@heclouds.com',
                recipients,
                carbon_copy,
                subject,
                'deploy',
                name=name,
                repo_name=repo_name,
                commit_id=commit_id,
                introduce=commit_msg,
                functions=functions,
                result=result)
        else:
            raise subprocess.CalledProcessError()


# 发邮件任务
# @celery.task
def send_async_email(sender, to, cc, subject, template, **kwargs):
    msg = Message(subject, sender=sender, recipients=to, cc=cc)
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
