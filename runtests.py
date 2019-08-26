import unittest

import src.testModel as testModel

runner = unittest.TextTestRunner()
runner.run(testModel.suite())
