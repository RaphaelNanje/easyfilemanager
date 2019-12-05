import unittest

from easyfilemanager import FileManager

file_manager = FileManager()


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        import os
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

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        import shutil
        shutil.rmtree('./testfiles/')


if __name__ == '__main__':
    unittest.main()
