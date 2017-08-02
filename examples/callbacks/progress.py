# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

import logging

import column


LOG = logging.getLogger(__name__)


# Simple callback to track progress of playbook execution
class TrackProgress(column.AnsibleCallback):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.progress = 0
        self.started_plays = 0
        self.total_plays = 0
        self.playbook = None

    def run_on_playbook_start(self, playbook):
        LOG.debug("Start progress for Playbook [%s]", self.playbook.filename)
        self.playbook = playbook
        self.total_plays = len(playbook.playbook)

    def run_on_playbook_play_start(self, play):
        LOG.debug("Started PLAY [%s]", play.name)
        self.started_plays += 1
        self.progress = float(self.started_plays) / float(self.total_plays)

    def run_on_playbook_stats(self, stats):
        LOG.debug("Finished Playbook [%s]", self.playbook.filename)


def main():
    api_runner = column.APIRunner()
    api_runner.add_callback(TrackProgress())
    api_runner.run_playbook("playbook.yml")
