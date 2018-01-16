import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class MyRunner:
    def __init__(self, hosts):
        self.hosts = hosts
        self.sources = ','.join(hosts)
        self.loader = None
        self.options = None
        self.passwords = None
        self.results_callback = None
        self.inventory = None
        self.variable_manager = None
        self.results_raw = {}
        self._initialize_data()

    def _initialize_data(self):
        Options = namedtuple('Options', [
            'connection', 'module_path', 'forks', 'become', 'become_method',
            'become_user', 'check', 'diff'
        ])
        # initialize needed objects
        self.loader = DataLoader()
        self.options = Options(
            # connection='local',
            connection='smart',
            module_path='',
            forks=100,
            become=True,
            become_method='sudo',
            become_user='root',
            check=False,
            diff=False)
        self.passwords = dict(vault_pass='secret')

        # create inventory and pass to var manager
        self.inventory = InventoryManager(self.loader, sources=self.sources)
        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory)

    def run_module(self, module, module_args):
        # create play with tasks
        play_source = dict(
            name="Ansible Module Play",
            hosts=self.hosts,
            gather_facts='no',
            tasks=[dict(action=dict(module=module, args=module_args))])
        play = Play().load(
            play_source,
            variable_manager=self.variable_manager,
            loader=self.loader)

        # Instantiate our ResultCallback for handling results as they come in
        self.results_callback = ResultCallback()

        # actually run it
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                # stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
            )
            tqm._stdout_callback = self.results_callback
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

    def get_module_results(self):
        self.results_raw = {'ok': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.results_callback.host_ok.items():
            # self.results_raw['ok'][host] = result._result['stdout']
            self.results_raw['ok'][host] = result._result

        for host, result in self.results_callback.host_failed.items():
            self.results_raw['failed'][host] = result._result['msg']

        for host, result in self.results_callback.host_unreachable.items():
            self.results_raw['unreachable'][host] = result._result['msg']
        return self.results_raw
