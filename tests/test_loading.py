import unittest

from easyfilemanager import FileManager

file_manager = FileManager()


class TestLoading(unittest.TestCase):
    folder = './testfiles/'

    def test_json_empty(self):
        file_manager.register_file('test2.json', self.folder, 'json')
        data = ''
        with open(file_manager.get_path('json'), 'w') as f:
            f.write(data)
        load = file_manager.smart_load('json')
        self.assertEqual(load, {})

    def test_load_empty_csv(self):
        file_manager.register_file('test2.csv', self.folder, 'csv')
        data = ''
        file_manager.save('csv', data)
        load = file_manager.smart_load('csv')
        self.assertEqual(load, [])

    def test_csv2(self):
        file_manager.register_file('test2.csv', self.folder, 'csv')
        data = ',,,,,,,,,,,,,,,,'
        with open(file_manager.get_path('csv'), 'w') as f:
            f.write(data)
        load = file_manager.smart_load('csv')
        self.assertEqual(load, [])

    def test_csv3(self):
        file_manager.register_file('pairs.csv', self.folder, 'csv')
        # file_manager.register_file('pairs.csv', './props/', 'csv')
        data = [list(range(3)) for _ in range(5)]
        file_manager.csv_save('csv', data, headers='a,b,c'.split(','))
        load = file_manager.csv_load('csv')
        self.assertIsInstance(load, list)

    def tearDown(self) -> None:
        file_manager.clear()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        import shutil
        shutil.rmtree('./testfiles/')


if __name__ == '__main__':
    unittest.main()
