import testtools

from column.api import backend


class TestLocalMemoryCache(testtools.TestCase):

    def setUp(self):
        super(TestLocalMemoryCache, self).setUp()
        self.store = backend.get_store()

    def test_add_runs(self):
        self.assertTrue(self.store.create_run('key1', {'id': '1'}))
        self.assertEqual({'id': '1'}, self.store.get_run('key1'))

    def test_update_run(self):
        self.store.create_run('key5', {'id': '5'})
        self.store.update_run('key5', {'id': '55'})
        self.assertEqual({'id': '55'}, self.store.get_run('key5'))
