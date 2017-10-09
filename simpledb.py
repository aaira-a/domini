import boto3
import os


DOMAIN = "domini-items"


class SimpleDB(object):

    def __init__(self, region='us-west-2',
                 access_key=os.environ["MY_ACCESS_KEY_ID"],
                 secret_key=os.environ["MY_SECRET_ACCESS_KEY"]):
        self.client = boto3.client(
            'sdb',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

    def get_or_create_domain(self, domain_name=DOMAIN):
        domains = self.client.list_domains()
        if domain_name not in domains['DomainNames']:
            self.create_domain(domain_name)
        return domains

    def create_domain(self, domain_name=DOMAIN):
        return self.client.create_domain(
            DomainName=domain_name
        )

    def delete_domain(self, domain_name=DOMAIN):
        return self.client.delete_domain(
            DomainName=domain_name
        )

    def list_domains(self):
        return self.client.list_domains()

    def put_attributes(self, item_name, attributes, domain_name=DOMAIN):
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

    def get_item(self, item_name, domain_name=DOMAIN):
        return self.client.get_attributes(
            DomainName=domain_name,
            ItemName=item_name,
            ConsistentRead=True
        )

    def delete_item(self, item_name, domain_name=DOMAIN):
        return self.client.delete_attributes(
            DomainName=domain_name,
            ItemName=item_name
        )

    def query(self, attribute_name, attribute_value, domain_name=DOMAIN):
        expression = (f'select * from `{domain_name}` \
                        where `{attribute_name}`="{attribute_value}"')
        return self.client.select(
            SelectExpression=expression,
            ConsistentRead=True)
