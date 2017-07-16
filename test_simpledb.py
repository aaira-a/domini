import os
import unittest
import uuid

from simpledb import SimpleDB


class SimpleDBIntegrationTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sdb = SimpleDB(
            access_key=os.environ["TEST_AWS_KEY"],
            secret_key=os.environ["TEST_AWS_SECRET"]
        )

    def test_create_list_delete_domain(self):
        domain = str(uuid.uuid4())

        self.sdb.create_domain(domain)
        domains = self.sdb.list_domains()
        self.assertIn(domain, str(domains))

        self.sdb.delete_domain(domain)
        domains = self.sdb.list_domains()
        self.assertNotIn(domain, str(domains))
