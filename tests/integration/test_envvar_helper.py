import unittest

import json
import os
from pathlib import Path
import shutil

from envvar_helper import add_aws_envvar


class EnvVarHelperTests(unittest.TestCase):

    def setUp(self):
        base_path = Path(Path.cwd(), "tests", "integration", "fixtures")
        self.template = Path(base_path, "template.json")
        self.temporary = Path(base_path, "undertest.json")
        self.expected = Path(base_path, "expected.json")
        shutil.copy2(self.template, self.temporary)

    def tearDown(self):
        os.remove(self.temporary)

    def test_add_envvars(self):
        add_aws_envvar("stage1", "key4", "value4", self.temporary)
        add_aws_envvar("stage1", "key5", "value5", self.temporary)

        with open(self.temporary, "r") as f1:
            actual = json.load(f1)

        with open(self.expected, "r") as f2:
            expected = json.load(f2)

        self.assertDictEqual(expected, actual)
