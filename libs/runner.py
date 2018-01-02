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

    # def v2_runner_on_ok(self, result, **kwargs):
    #     """Print a json representation of the result

    #     This method could store the result in an instance attribute for retrieval later
    #     """
    #     host = result._host
    #     print(json.dumps({host.name: result._result}, indent=4))

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


def runner(hosts):
    Options = namedtuple('Options', [
        'connection', 'module_path', 'forks', 'become', 'become_method',
        'become_user', 'check', 'diff', 'ansible_user', 'remote_user'
    ])
    # initialize needed objects
    loader = DataLoader()
    options = Options(
        # connection='local',
        connection='smart',
        module_path='',
        forks=100,
        become=None,
        become_method=None,
        become_user=None,
        check=False,
        diff=False,
        ansible_user='app',
        remote_user='app')
    passwords = dict(vault_pass='secret')

    # Instantiate our ResultCallback for handling results as they come in
    results_callback = ResultCallback()

    # create inventory and pass to var manager
    inventory = InventoryManager(loader=loader, sources=','.join(hosts))
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # create play with tasks
    play_source = dict(
        name="Ansible Play",
        hosts=hosts,
        gather_facts='no',
        tasks=[dict(action=dict(module='command', args='hostname'))])
    play = Play().load(
        play_source, variable_manager=variable_manager, loader=loader)

    # actually run it
    tqm = None
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords,
            # stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
        )
        tqm._stdout_callback = results_callback
        result = tqm.run(play)
    finally:
        if tqm is not None:
            tqm.cleanup()

    print("UP ***********")
    for host, result in results_callback.host_ok.items():
        print('{} >>> {}'.format(host, result._result['stdout']))

    print("FAILED *******")
    for host, result in results_callback.host_failed.items():
        print('{} >>> {}'.format(host, result._result['msg']))

    print("DOWN *********")
    for host, result in results_callback.host_unreachable.items():
        print('{} >>> {}'.format(host, result._result['msg']))
