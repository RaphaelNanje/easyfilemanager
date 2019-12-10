import os
import unittest

import yaml

from easyfilemanager import FileManager

file_manager = FileManager()


class MyTestCase(unittest.TestCase):
    folder = './testfiles/'

    @classmethod
    def setUpClass(cls) -> None:
        os.mkdir('testfiles')
        for i, folder in enumerate('testfolder' + str(i) for i in range(5)):
            if not os.path.exists(folder):
                os.mkdir(os.path.join('testfiles', folder))
            for file in [f'testfile{i}{j}.json' for j in range(2)]:
                with open(os.path.join('testfiles', folder, file), 'w') as f:
                    f.write('')

    def test_directory_load(self):
        file_manager.directory_load('./testfiles/', True)
        for i in range(5):
            for file in [f'testfile{i}{j}.json' for j in range(2)]:
                self.assertIn(file, file_manager)

    def test_register(self):
        file_manager.register_file('test.json', './testfiles', 'testj')
        file_manager.register_file('test.yaml', './testfiles', 'testy')
        file_manager.register_file('test.txt', './testfiles', 'testt')

        self.assertTrue('testj' in file_manager)
        self.assertTrue('testy' in file_manager)
        self.assertTrue('testt' in file_manager)

    def test_save(self):
        file_manager.register_file('test.json', './testfiles', 'testj')
        file_manager.register_file('test.yaml', './testfiles', 'testy')
        file_manager.register_file('test.txt', './testfiles', 'testt')
        data = dict(
                a=1,
                b=2,
                c=3
        )

        file_manager.smart_save('testj', data)
        self.assertIsNotNone(file_manager.smart_load('testj'))
        file_manager.smart_save('testy', data)
        self.assertIsNotNone(file_manager.smart_load('testy'))
        file_manager.smart_save('testt', data)
        self.assertIsNotNone(file_manager.smart_load('testt'))

    def test_yaml(self):
        data = [list(range(100))]
        file_manager.register_file('yaml1.yaml', 'testfiles/',
                                   short_name='yaml1')

        file_manager.yaml_save('yaml1', data, default_flow_style=False,
                               Dumper=yaml.Dumper)
        data = file_manager.smart_load('yaml1')

        self.assertTrue(data)

    def test_csv(self):
        file_manager.register_file('test_numbers.csv', './testfiles/', 'csv')
        data = [[f'test{i}', f'data{i}', f'row{i}'] for i in range(100)]
        file_manager.csv_save('csv', data, 'test,data,row'.split(','))

        load = file_manager.csv_load('csv')
        self.assertTrue(data, load)

    def test_csv_failed(self):
        file_manager.register_file('test2.csv', self.folder, 'csv')
        data = ' '
        with open(file_manager.get_path('csv'), 'w') as f:
            f.write(data)
        load = file_manager.load('csv')
        self.assertEqual(load, [''])

    def tearDown(self) -> None:
        file_manager.clear()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        import shutil
        shutil.rmtree('./testfiles/')


if __name__ == '__main__':
    unittest.main()
