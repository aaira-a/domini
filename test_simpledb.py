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

    def test_put_get_delete_generic_item(self):
        domain = str(uuid.uuid4())
        item_name = str(uuid.uuid4())
        self.sdb.create_domain(domain)

        attribute = {"Name": "attribute1name", "Value": "attribute1value"}
        self.sdb.put_attribute(domain, item_name, attribute)

        item = self.sdb.get_item(domain, item_name)
        self.assertDictEqual(attribute, item["Attributes"][0])

        self.sdb.delete_item(domain, item_name)
        item2 = self.sdb.get_item(domain, item_name)
        item2_attribute = item2.get("Attributes", "empty")
        self.assertEqual(item2_attribute, "empty")

        self.sdb.delete_domain(domain)

    def test_query_more_than_one_items_by_attribute_value(self):
        domain = str(uuid.uuid4())
        self.sdb.create_domain(domain)

        item_1_name = str(uuid.uuid4())
        item_2_name = str(uuid.uuid4())
        item_3_name = str(uuid.uuid4())

        value1 = {"Name": "attribute1name", "Value": "attribute1value1"}
        value2 = {"Name": "attribute1name", "Value": "attribute1value2"}

        self.sdb.put_attribute(domain, item_1_name, value1)
        self.sdb.put_attribute(domain, item_2_name, value1)
        self.sdb.put_attribute(domain, item_3_name, value2)

        response = self.sdb.query(domain, "attribute1name", "attribute1value1")
        self.assertEqual(2, len(response["Items"]))

        self.sdb.delete_domain(domain)
