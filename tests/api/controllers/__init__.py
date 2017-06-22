import testtools

from column.api.run import app


class APITest(testtools.TestCase):

    def setUp(self):
        super(APITest, self).setUp()
        app.config['SERVER_NAME'] = '127.0.0.1:48620'
        self.pb_running_time = 60
        self.wait_interval = 5
        self.counter = self.pb_running_time / self.wait_interval
        self.app = app.test_client()
