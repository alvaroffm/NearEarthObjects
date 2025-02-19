import unittest
import collections
import collections.abc
import contextlib
import csv
import datetime
import io
import json
import pathlib
import unittest.mock
from colorama import init, Fore

from extract import load_neos, load_approaches
from database import NEODatabase
from write import write_to_csv, write_to_json

# Inicializar colorama
init(autoreset=True)

TESTS_ROOT = (pathlib.Path(__file__).parent).resolve()
TEST_NEO_FILE = TESTS_ROOT / 'test-neos-2020.csv'
TEST_CAD_FILE = TESTS_ROOT / 'test-cad-2020.json'

def build_results(n):
    neos = tuple(load_neos(TEST_NEO_FILE))
    approaches = tuple(load_approaches(TEST_CAD_FILE))
    NEODatabase(neos, approaches)
    return approaches[:n]

@contextlib.contextmanager
def UncloseableStringIO(value=''):
    buf = io.StringIO(value)
    buf._close = buf.close
    buf.close = lambda: False
    yield buf
    buf.close = buf._close
    delattr(buf, '_close')
    buf.close()

class ColorTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        print(Fore.LIGHTGREEN_EX + f"OK: {test}")

class CustomTextTestRunner(unittest.TextTestRunner):
    resultclass = ColorTestResult

class TestWriteToCSV(unittest.TestCase):
    @classmethod
    @unittest.mock.patch('write.open')
    def setUpClass(cls, mock_file):
        results = build_results(5)
        with UncloseableStringIO() as buf:
            mock_file.return_value = buf
            try:
                write_to_csv(results, None)
            except csv.Error as err:
                raise cls.failureException("Unable to write results to CSV.") from err
            else:
                buf.seek(0)
                cls.value = buf.getvalue()

    def test_csv_data_is_well_formed(self):
        buf = io.StringIO(self.value)
        try:
            collections.deque(csv.DictReader(buf), maxlen=0)
        except csv.Error as err:
            raise self.failureException("write_to_csv produced an invalid CSV format.") from err

    def test_csv_data_has_five_rows(self):
        buf = io.StringIO(self.value)
        try:
            reader = csv.DictReader(buf)
            rows = tuple(reader)
        except csv.Error as err:
            raise self.failureException("write_to_csv produced an invalid CSV format.") from err
        self.assertEqual(len(rows), 5)

class TestWriteToJSON(unittest.TestCase):
    @classmethod
    @unittest.mock.patch('write.open')
    def setUpClass(cls, mock_file):
        results = build_results(5)
        with UncloseableStringIO() as buf:
            mock_file.return_value = buf
            try:
                write_to_json(results, None)
            except csv.Error as err:
                raise cls.failureException("Unable to write results to CSV.") from err
            else:
                buf.seek(0)
                cls.value = buf.getvalue()

    def test_json_data_is_well_formed(self):
        buf = io.StringIO(self.value)
        try:
            json.load(buf)
        except json.JSONDecodeError as err:
            raise self.failureException("write_to_json produced an invalid JSON document") from err

if __name__ == '__main__':
    unittest.main(testRunner=CustomTextTestRunner())
