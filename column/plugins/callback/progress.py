import logging

import column

LOG = logging.getLogger(__name__)


class AnsibleTrackProgress(column.AnsibleCallback):
    """Ansible progress callback class """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.total_plays = 0
        self.finished_plays = 0
        self.playbook = None
        self.progress = 0

    def run_on_playbook_start(self, playbook):
        self.playbook = playbook._file_name
        LOG.debug("Start progress for Playbook [%s]", self.playbook)
        self.total_plays = len(playbook.get_plays())
        LOG.debug("Total plays to run: %d", self.total_plays)

    def run_on_playbook_play_start(self, play):
        LOG.debug("Started PLAY [%s]", play.get_name())
        self.progress = float(self.finished_plays) / float(self.total_plays)
        LOG.debug("Playbook progress %d%%", self.progress * 100.0)
        self.finished_plays += 1

    def run_on_playbook_stats(self, stats):
        self.progress = 1

    def run_on_playbook_task_start(self, task, is_conditional):
        LOG.debug("Started TASK [%s]", task.get_name())
