import boto3
import os


class SimpleDB(object):

    def __init__(self, region='us-west-2',
                 access_key=os.environ["AWS_ACCESS_KEY_ID"],
                 secret_key=os.environ["AWS_SECRET_ACCESS_KEY"]):
        self.client = boto3.client(
            'sdb',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

    def create_domain(self, domain_name):
        return self.client.create_domain(
            DomainName=domain_name
        )

    def delete_domain(self, domain_name):
        return self.client.delete_domain(
            DomainName=domain_name
        )

    def list_domains(self):
        return self.client.list_domains()

    def put_attributes(self, domain_name, item_name, attributes):
        return self.client.put_attributes(
            DomainName=domain_name,
            ItemName=item_name,
            Attributes=[
                {
                    "Name": x["Name"],
                    "Value": x["Value"],
                    "Replace": True
                } for x in attributes
            ]
        )

    def get_item(self, domain_name, item_name):
        return self.client.get_attributes(
            DomainName=domain_name,
            ItemName=item_name,
            ConsistentRead=True
        )

    def delete_item(self, domain_name, item_name):
        return self.client.delete_attributes(
            DomainName=domain_name,
            ItemName=item_name
        )

    def query(self, domain_name, attribute_name, attribute_value):
        expression = (f'select * from `{domain_name}` \
                        where `{attribute_name}`="{attribute_value}"')
        return self.client.select(
            SelectExpression=expression,
            ConsistentRead=True)
