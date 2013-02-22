import os
import unittest
from StringIO import StringIO
import sef

class LinesTest(unittest.TestCase):
    def test_ignores_unreadable_file(self):
        improbable_filename = '/no/such/file/ever'
        assert sef.read_lines(improbable_filename) == []

    def test_reads_from_existing_file(self):
        filename = os.path.join(os.path.dirname(__file__), 'test_env.txt')
        assert sef.read_lines(filename) == ['hello\n', 'world\n']

    def test_reads_from_opened_file(self):
        file = StringIO('hello')
        assert sef.read_lines(file) == ['hello']


class EnvReaderTest(unittest.TestCase):
    def setUp(self):
        os.environ.clear()
        self.reader = sef.EnvReader()

    def test_handles_quotes(self):
        key, value = self.reader.key_value_from_line('hello = "a \\" b"')
        assert value == 'a " b'

    def test_ignores_comments_at_end(self):
        key, value = self.reader.key_value_from_line('hello = world # not')
        assert (key, value) == ('hello', 'world')

    def test_ignores_empty_lines(self):
        for line in [' ', '#', '', ' # ']:
            assert self.reader.is_empty(line)

    def test_reads_multiple_lines(self):
        d = self.reader.dict(['hello = world', 'a=b'])
        assert d == {'hello': 'world', 'a': 'b'}

    def test_sets_environment(self):
        self.reader.set_environ(['hello = world'])
        assert os.environ['hello'] == 'world'

    def test_does_not_override_environ(self):
        os.environ['hello'] = 'me'
        self.reader.set_environ(['hello = world'])
        assert os.environ['hello'] == 'me'


if __name__ == '__main__':
    unittest.main()
