import unittest

import src.tests as tests

runner = unittest.TextTestRunner()
runner.run(tests.suite())
