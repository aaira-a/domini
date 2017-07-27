from deepdiff import DeepDiff
import os
import unittest
import uuid

from simpledb import SimpleDB


class SimpleDBIntegrationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sdb = SimpleDB(
            access_key=os.environ["TEST_AWS_KEY"],
            secret_key=os.environ["TEST_AWS_SECRET"]
        )

    def setUp(self):
        self.domain = str(uuid.uuid4())
        self.sdb.create_domain(self.domain)
        domains = self.sdb.list_domains()
        self.assertIn(self.domain, str(domains))

    def tearDown(self):
        self.sdb.delete_domain(self.domain)
        domains = self.sdb.list_domains()
        self.assertNotIn(self.domain, str(domains))

    def test_put_get_delete_generic_item(self):
        item_name = str(uuid.uuid4())

        attributes = [
            {"Name": "attribute1name", "Value": "attribute1value"},
            {"Name": "attribute2name", "Value": "attribute2value"}
        ]
        self.sdb.put_attributes(item_name, attributes, self.domain)

        item = self.sdb.get_item(item_name, self.domain)
        difference = DeepDiff(attributes, item["Attributes"],
                              ignore_order=True)
        self.assertEqual({}, difference)

        self.sdb.delete_item(item_name, self.domain)
        item_recheck = self.sdb.get_item(item_name, self.domain)
        if "Attributes" in item_recheck:
            self.fail("item should not contain any attribute")

    def test_put_attribute_should_replace_previous_same_key(self):
        item_name = str(uuid.uuid4())

        attributes1 = [{"Name": "attribute1name", "Value": "attribute1value1"}]
        attributes2 = [{"Name": "attribute1name", "Value": "attribute1value2"}]
        self.sdb.put_attributes(item_name, attributes1, self.domain)
        self.sdb.put_attributes(item_name, attributes2, self.domain)

        item_recheck = self.sdb.get_item(item_name, self.domain)
        self.assertEqual(attributes2, item_recheck["Attributes"])

    def test_query_more_than_one_items_by_attribute_value(self):
        item_1_name = str(uuid.uuid4())
        item_2_name = str(uuid.uuid4())
        item_3_name = str(uuid.uuid4())

        value1 = {"Name": "attribute1name", "Value": "attribute1value1"}
        value2 = {"Name": "attribute1name", "Value": "attribute1value2"}

        self.sdb.put_attributes(item_1_name, [value1], self.domain)
        self.sdb.put_attributes(item_2_name, [value1], self.domain)
        self.sdb.put_attributes(item_3_name, [value2], self.domain)

        response = self.sdb.query("attribute1name", "attribute1value1", self.domain)
        self.assertEqual(2, len(response["Items"]))
