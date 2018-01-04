import os
import subprocess
import tarfile

from app import redis

from models.deploys import Deploy as DeployModel
from models.projects import Project as ProjectModel
from app import socketio


class DeployService:
    def __init__(self, deploy, config, project_args):
        self.deploy = deploy
        self.config = config
        self.checkout_path = config.get('CHECKOUT_PATH')
        self.deploy_path = config.get('DEPLOY_PATH')
        self.repo_name = project_args.get('name')
        self.repo_ssh_url = project_args.get('repo_ssh_url')
        self.service = project_args.get('service')
        self.full_checkout_path = os.path.join(self.checkout_path,
                                               self.repo_name)
        self.full_deploy_path = os.path.join(self.deploy_path, self.repo_name)
        self.runner = None

    def run(self):
        return self.step_1()

    def step_1(self):
        "clone or fetch repo"
        # prepare code
        DeployModel.update(self.deploy, status=1)
        if os.path.exists(self.full_checkout_path) and os.path.isdir(
                self.full_checkout_path):
            cmd = 'git reset -q --hard origin/master && git fetch --all -q'
            rs = subprocess.run(cmd, shell=True, cwd=self.full_checkout_path)
            if rs.returncode:
                return {'status': 1, 'msg': 'git fetch failed'}
        else:
            cmd = 'git clone -q %s %s' % (self.repo_ssh_url, self.repo_name)
            rs = subprocess.run(cmd.split(), cwd=self.checkout_path)
            if rs.returncode:
                return {'status': 1, 'msg': 'git clone failed'}
        cmd = 'git reset -q --hard %s' % self.deploy.commit_id
        rs = subprocess.run(cmd.split(), cwd=self.full_checkout_path)
        if rs.returncode:
            return {'status': 1, 'msg': 'git reset failed'}
        return self.step_2()

    def step_2(self):
        # exec before commands
        DeployModel.update(self.deploy, status=2)
        excludes = ' '.join('--exclude ' + ex for ex in ['.git', '.gitignore'])
        cmd = 'sudo rsync -qa --delete {exclude} {src}/ {dst}/'.format(
            exclude=excludes,
            src=self.full_checkout_path,
            dst=self.full_deploy_path)
        rs = subprocess.run(cmd.split())
        if rs.returncode:
            return {'status': 2, 'msg': 'rsync shell failed'}
        cmd = ' && '.join(self.deploy.project.before_cmd.split('\n')).strip()
        rs = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
        if rs.returncode:
            return {'status': 2, 'msg': 'exec user custom shell failed'}
        # exec default commands
        cmd = 'sudo chown -R %s:%s %s' % (self.config.get('CODE_USER'),
                                          self.config.get('CODE_GROUP'),
                                          self.full_deploy_path)
        rs = subprocess.run(cmd.split())
        if rs.returncode:
            return {'status': 2, 'msg': 'shell chown failed'}
        cmd = 'tar -zcf %s.tgz --exclude-vcs -C %s .' % (self.repo_name,
                                                         self.full_deploy_path)
        rs = subprocess.run(cmd.split(), cwd=self.deploy_path)
        if rs.returncode:
            return {'status': 2, 'msg': 'shell tar failed'}
        return self.step_3()

    def step_3(self):
        # deploy
        DeployModel.update(self.deploy, status=3)
        _p = ProjectModel.get(self.deploy.project_id)
        hosts = [h.ip_addr for h in _p.hosts if h.env == self.deploy.env]
        from libs.runner import MyRunner
        self.runner = MyRunner(hosts)
        opj = os.path.join
        self.runner.run_module(
            'file', 'path=%s state=directory mode=0755 owner=%s group=%s' %
            (opj('/tmp', self.repo_name), self.config.get('CODE_USER'),
             self.config.get('CODE_GROUP')))
        print('---mkdir--->', self.runner.get_module_results())
        self.runner.run_module('unarchive', 'src=%s dest=%s copy=yes' %
                               (opj(self.deploy_path, self.repo_name + '.tgz'),
                                opj('/tmp', self.repo_name)))
        res = self.runner.get_module_results()
        if res.get('failed'):
            return res.get('failed')
        elif res.get('unreachable'):
            return res.get('unreachable')
        return self.step_4()

    def step_4(self):
        # exec after commands
        DeployModel.update(self.deploy, status=4)
        if self.service:
            print('----service---->', self.service)
            self.runner.run_module('service', 'name=php-fpm state=restarted')
            res = self.runner.get_module_results()
            if res.get('failed'):
                return res.get('failed')
            elif res.get('unreachable'):
                return res.get('unreachable')
        redis.publish('deploy', self.deploy.project.name + '部署成功')
        DeployModel.update(self.deploy, status=5)
        return self.deploy.project.name + '部署成功'

    def rsync_local(self, src, dest, excludes=[]):
        excludes.append('.git')
        exclude_args = ''
        for e in excludes:
            exclude_args = exclude_args + ' --exclude %s' % e
        cmd = 'rsync -qa --delete %s %s%s %s%s' % (exclude_args, src, os.sep,
                                                   dest, os.sep)
        rc = subprocess.check_call(cmd.split())


# 发邮件任务
# @celery.task
def send_async_email(sender, to, cc, subject, template, **kwargs):
    msg = Message(subject, sender=sender, recipients=to, cc=cc)
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
