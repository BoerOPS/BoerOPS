"""ansible api"""

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import Inventory, Host, Group
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor


class MyInventory(Inventory):
    """inventory"""

    def __init__(self, resource, loader, variable_manager):
        self.resource = resource
        self.inventory = Inventory(
            loader=loader, variable_manager=variable_manager, host_list=[])
        self.dynamic_inventory()

    def add_dynamic_group(self, hosts, groupname, groupvars=None):
        """dynamic inventory group"""
        my_group = Group(name=groupname)
        if groupvars:
            for key, value in groupvars.items():
                my_group.set_variable(key, value)
        for host in hosts:
            # set connection variables
            hostname = host.get("hostname")
            hostip = host.get('ip', hostname)
            hostport = host.get("port")
            username = host.get("username")
            password = host.get("password")
            ssh_key = host.get("ssh_key")
            my_host = Host(name=hostname, port=hostport)
            my_host.set_variable('ansible_ssh_host', hostip)
            my_host.set_variable('ansible_ssh_port', hostport)
            my_host.set_variable('ansible_ssh_user', username)
            my_host.set_variable('ansible_ssh_pass', password)
            my_host.set_variable('ansible_ssh_private_key_file', ssh_key)
            for key, value in host.items():
                if key not in ["hostname", "port", "username", "password"]:
                    my_host.set_variable(key, value)
            my_group.add_host(my_host)

        self.inventory.add_group(my_group)

    def dynamic_inventory(self):
        if isinstance(self.resource, list):
            self.add_dynamic_group(self.resource, 'default_group')
        elif isinstance(self.resource, dict):
            for groupname, hosts_and_vars in self.resource.items():
                self.add_dynamic_group(
                    hosts_and_vars.get("hosts"), groupname,
                    hosts_and_vars.get("vars"))


class ModuleResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ModuleResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class PlayBookResultCallback(CallbackBase):
    def __init__(self, tasklist, *args, **kwargs):
        super(PlayBookResultCallback, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        if result._host.get_name() in tasklist:
            data = {}
            data['task'] = str(result._task).replace("TASK: ", "")
            tasklist[result._host.get_name()].get('ok').append(data)
        self.task_ok[result._host.get_name()] = tasklist[
            result._host.get_name()]['ok']

    def v2_runner_on_failed(self, result, *args, **kwargs):
        if result._host.get_name() in tasklist:
            data = {}
            data['task'] = str(result._task).replace("TASK: ", "")
            msg = result._result.get('stderr')
            if msg is None:
                results = result._result.get('results')
                if result:
                    task_item = {}
                    for rs in results:
                        msg = rs.get('msg')
                        if msg:
                            task_item[rs.get('item')] = msg
                            data['msg'] = task_item
                    tasklist[result._host.get_name()]['failed'].append(data)
                else:
                    msg = result._result.get('msg')
                    data['msg'] = msg
                    tasklist[result._host.get_name()].get('failed').append(
                        data)
        else:
            data['msg'] = msg
            tasklist[result._host.get_name()].get('failed').append(data)
        self.task_failed[result._host.get_name()] = tasklist[
            result._host.get_name()]['failed']

    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        if result._host.get_name() in tasklist:
            data = {}
            data['task'] = str(result._task).replace("TASK: ", "")
            tasklist[result._host.get_name()].get('skipped').append(data)
        self.task_ok[result._host.get_name()] = tasklist[
            result._host.get_name()]['skipped']

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                "ok": t['ok'],
                "changed": t['changed'],
                "unreachable": t['unreachable'],
                "skipped": t['skipped'],
                "failed": t['failures']
            }


class MyRunner:
    def __init__(self, resource, *args, **kwargs):
        self.resource = resource
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.results_callback = None
        self.inventory = None
        self._initialize_data()
        self.results_raw = {}

    def _initialize_data(self):
        Options = namedtuple('Options', [
            'connection', 'module_path', 'forks', 'timeout', 'remote_user',
            'ask_pass', 'private_key_file', 'ssh_common_args',
            'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become',
            'become_method', 'become_user', 'ask_value_pass', 'verbosity',
            'check', 'listhosts', 'listtasks', 'listtags', 'syntax'
        ])

        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.options = Options(
            connection='smart',
            module_path=None,
            forks=100,
            timeout=10,
            remote_user='root',
            ask_pass=False,
            private_key_file=None,
            ssh_common_args=None,
            ssh_extra_args=None,
            sftp_extra_args=None,
            scp_extra_args=None,
            become=None,
            become_method=None,
            become_user='root',
            ask_value_pass=False,
            verbosity=None,
            check=False,
            listhosts=False,
            listtasks=False,
            listtags=False,
            syntax=False)

        self.passwords = dict(sshpass=None, becomepass=None)
        self.inventory = MyInventory(self.resource, self.loader,
                                     self.variable_manager).inventory
        self.variable_manager.set_inventory(self.inventory)

    def run_module(self, hosts, module_name, module_args):
        # create play with tasks
        play_source = dict(
            name="Ansible Play",
            hosts=hosts,
            gather_facts='no',
            tasks=[dict(action=dict(module=module_name, args=module_args))])
        play = Play().load(
            play_source,
            variable_manager=self.variable_manager,
            loader=self.loader)

        self.results_callback = ModuleResultCallback()
        # actually run it
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=self.
                results_callback,  # Use our custom callback instead of the ``default`` callback plugin
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

    def run_playbook(self, hosts, playbook_path):
        """
        run ansible palybook
        """
        global tasklist
        tasklist = {}
        for host in hosts:
            tasklist[host] = {}
            tasklist[host]['ok'] = []
            tasklist[host]['failed'] = []
            tasklist[host]['skppied'] = []

        self.results_callback = PlayBookResultCallback(tasklist)
        try:
            executor = PlaybookExecutor(
                playbooks=[playbook_path],
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords)
            executor._tqm._stdout_callback = self.results_callback
            executor.run()
        except Exception as e:
            print(e)
            return False

    def get_module_result(self):
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.results_callback.host_ok.items():
            self.results_raw['success'][host] = result._result

        for host, result in self.results_callback.host_failed.items():
            self.results_raw['failed'][host] = result._result

        for host, result in self.results_callback.host_unreachable.items():
            self.results_raw['unreachable'][host] = result._result
        return json.dumps(self.results_raw)

    def get_playbook_result(self):
        self.results_raw = {
            'skipped': {},
            'failed': {},
            'ok': {},
            "status": {},
            'unreachable': {}
        }

        for host, result in self.results_callback.task_ok.items():
            self.results_raw['ok'][host] = result

        for host, result in self.results_callback.task_failed.items():
            self.results_raw['failed'][host] = result

        for host, result in self.results_callback.task_status.items():
            self.results_raw['status'][host] = result

        for host, result in self.results_callback.task_skipped.items():
            self.results_raw['skipped'][host] = result

        for host, result in self.results_callback.task_unreachable.items():
            self.results_raw['unreachable'][host] = result._result
        return json.dumps(self.results_raw)


def get_dynamic_inventory(proj, environ):
    return {
        proj.name: {
            'hosts': [{
                'hostname': h.ip_address,
                'port': h.ssh_port,
                'username': h.username,
                'password': h.password
            } for h in proj.hosts if h.environ == int(environ)],
            'vars': {
                'ansible_user': 'boer',
                'ansible_become': True,
                'ansible_become_method': 'sudo',
                'ansible_become_user': 'root',
                'ansible_become_pass': 'Admin@123'
            }
        }
    }
