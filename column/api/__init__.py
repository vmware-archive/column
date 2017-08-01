import copy

from ansible.playbook import play_context


context_attributes = copy.deepcopy(play_context.PlayContext._attributes)
