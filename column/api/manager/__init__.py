from column.api.manager import run_manager

_managers = {
    'run': run_manager.RunManager()
}


def get_manager(manager_type):
    if manager_type in _managers:
        return _managers[manager_type]
    raise NotImplemented
