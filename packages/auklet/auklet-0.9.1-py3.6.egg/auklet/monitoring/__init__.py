# Portions of this file are taken from
# https://github.com/what-studio/profiling/tree/0.1.1,
# the license for which can be found in the "licenses/profiling.txt" file
# in this repository/package.
from __future__ import absolute_import

import sys
import time
import signal
from six import iteritems
from six.moves import _thread

from auklet.broker import MQTTClient
from auklet.utils import get_mac, setup_thread_excepthook, create_dir
from auklet.monitoring.logging import AukletLogging
from auklet.monitoring.processing import Client
from auklet.stats import MonitoringTree
from auklet.errors import AukletConfigurationError

__all__ = ['Monitoring']

except_hook_set = False


class Monitoring(AukletLogging):
    #: The frames sampler.  Usually it is an instance of :class:`profiling.
    #: sampling.samplers.Sampler`
    sampler = None
    tree = None
    client = None
    broker = None
    monitor = True
    samples_taken = 0
    timer = signal.ITIMER_REAL
    sig = signal.SIGALRM
    stopping = False
    stopped = False

    interval = 1e-3  # 1ms

    total_samples = 0

    emission_rate = 60000  # 60 seconds
    network_rate = 10000  # 10 seconds
    hour = 3600000  # 1 hour

    def __init__(self, api_key=None, app_id=None, release=None,
                 base_url="https://api.auklet.io/", monitoring=True):
        if release is None:
            raise AukletConfigurationError(
                "Must include release in Monitoring Creation")
        global except_hook_set
        sys.excepthook = self.handle_exc
        if not except_hook_set:
            # ensure not attempting to set threading excepthook more than once
            setup_thread_excepthook()
            except_hook_set = True
        create_dir()
        self.app_id = app_id
        self.mac_hash = get_mac()
        self.client = Client(api_key, app_id, release, base_url, self.mac_hash)
        self.emission_rate = self.client.update_limits()
        self.tree = MonitoringTree(self.mac_hash)
        self.broker = MQTTClient(self.client)
        self.monitor = monitoring
        signal.signal(self.sig, self.sample)
        signal.siginterrupt(self.sig, False)
        super(Monitoring, self).__init__()

    def start(self):
        # Set a timer which fires a SIGALRM every interval seconds
        signal.setitimer(self.timer, self.interval, self.interval)

    def stop(self):
        self.stopping = True
        self.wait_for_stop()

    def wait_for_stop(self):
        while not self.stopped:
            time.sleep(.1)

    def sample(self, sig, current_frame):
        """Samples the given frame."""
        if self.stopping:
            signal.setitimer(self.timer, 0, 0)
            self.stopped = True
            return
        current_thread = _thread.get_ident()
        for thread_id, frame in iteritems(sys._current_frames()):
            if thread_id == current_thread:
                frame = current_frame
            frames = []
            while frame is not None:
                frames.append(frame)
                frame = frame.f_back
            self.tree.update_hash(frames)
        self.total_samples += 1
        self.samples_taken += 1
        self.process_periodic()

    def process_periodic(self):
        if self.total_samples % self.emission_rate == 0:
            self.broker.produce(
                self.tree.build_msgpack_tree(self.client))
            self.tree.clear_root()
            self.samples_taken = 0
        if self.total_samples % self.network_rate == 0:
            self.client.update_network_metrics(self.network_rate)
        if self.total_samples % self.hour == 0:
            self.emission_rate = self.client.update_limits()
            self.client.check_date()

    def handle_exc(self, type, value, traceback):
        self.broker.produce(
            self.client.build_msgpack_event_data(
                type, traceback, self.tree), "event")
        sys.__excepthook__(type, value, traceback)

    def log(self, msg, data_type, level="INFO"):
        self.broker.produce(
            self.client.build_msgpack_log_data(msg, data_type, level), "event")
