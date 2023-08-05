from neo.libs import login as login_lib
from novaclient import client as nova_client


def get_nova_client(session=None):
    if not session:
        session = login_lib.load_dumped_session()

    compute = nova_client.Client(2, session=session)
    return compute


def get_list(session=None):
    compute = get_nova_client(session)
    instances = [instance for instance in compute.servers.list()]
    return instances


def detail(vm_id, session=None):
    compute = get_nova_client(session)
    return compute.servers.get(vm_id)


def do_delete(instance_id, session=None):
    compute = get_nova_client(session)
    compute.servers.delete(instance_id)


def get_flavor(session=None):
    compute = get_nova_client(session)
    return compute.flavors.list()


def detail_flavor(flavor_id, session=None):
    compute = get_nova_client(session)
    return compute.flavors.get(flavor_id)


def get_keypairs(session=None):
    compute = get_nova_client(session)
    return compute.keypairs.list()


def get_console_logs(instance_id, length=None, session=None):
    compute = get_nova_client(session)
    logs = None
    if length:
        logs = compute.servers.get_console_output(instance_id, length=length)
    else:
        logs = compute.servers.get_console_output(instance_id)
    return logs


def suspend(vm_id, session=None):
    compute = get_nova_client(session)
    return compute.servers.suspend(vm_id)


def resume(vm_id, session=None):
    compute = get_nova_client(session)
    return compute.servers.resume(vm_id)


def lock(vm_id, session=None):
    compute = get_nova_client(session)
    return compute.servers.lock(vm_id)


def unlock(vm_id, session=None):
    compute = get_nova_client(session)
    return compute.servers.unlock(vm_id)

