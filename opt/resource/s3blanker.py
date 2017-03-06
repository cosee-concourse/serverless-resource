import boto3
import yaml

S3_RESOURCE_TYPE_NAME = 'AWS::S3::Bucket'


class S3Blanker:
    def __init__(self, access_key, secret_key, region_name):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region_name = region_name

    def client_init(self, service_name):
        client = boto3.client(
            service_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name
        )
        return client

    def get_buckets_from_stack(self, client, stack_name):
        bucket_list = []
        resources = client.describe_stack_resources(
            StackName=stack_name
        )
        resources = resources['StackResources']
        for resource in resources:
            if self.is_bucket(resource):
                bucket_list.append(resource['PhysicalResourceId'])
        return bucket_list

    def empty_buckets_for_serverless_config(self, file_path, stage):
        stack_name = self.get_service_name(file_path) + stage
        client = self.client_init('cloudformation')

        buckets = self.get_buckets_from_stack(client, stack_name)

        client = self.client_init('s3')
        for bucket in buckets:
            self.empty_bucket(client, bucket)

    @staticmethod
    def empty_bucket(client, bucket_name):
        objects = client.list_objects_v2(Bucket=bucket_name)
        keys = []
        for content in objects['Contents']:
            keys.append({
                'Key': content['Key']
            })
        client.delete_objects(Bucket=bucket_name, Delete={'Objects': keys})

    @staticmethod
    def is_bucket(resource):
        # ignore serverless deployment bucket
        return resource['ResourceType'] == S3_RESOURCE_TYPE_NAME and \
               'serverless' not in resource['PhysicalResourceId']

    @staticmethod
    def get_service_name(file_path):
        with open(file_path, 'r') as stream:
            yaml_dict = yaml.load(stream)
            service_name = yaml_dict['service']

        return service_name
