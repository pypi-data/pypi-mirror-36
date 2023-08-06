"""miscellaneous functions that directly/indirectly interact with AWS"""

import re
from time import sleep
import boto3
from botocore.exceptions import ClientError

from ec2mc import consts
from ec2mc.utils import halt

def ec2_client(region):
    """wrapper for ec2_client_no_validate which validates specified region"""
    if region is None:  # True for when command has unused region argument
        if len(consts.REGIONS) > 1:
            halt.err("AWS region whitelist has more than one entry.",
                "  A region must be specified using the -r argument.")
        region = consts.REGIONS[0]
    elif region not in consts.REGIONS:
        halt.err(f"\"{region}\" not in region whitelist.")

    return ec2_client_no_validate(region)


def ec2_client_no_validate(region):
    """create and return EC2 client using IAM user access key and a region"""
    return boto3.client("ec2",
        aws_access_key_id=consts.KEY_ID,
        aws_secret_access_key=consts.KEY_SECRET,
        region_name=region
    )


def iam_client():
    """create and return IAM client using IAM user access key"""
    return boto3.client("iam",
        aws_access_key_id=consts.KEY_ID,
        aws_secret_access_key=consts.KEY_SECRET
    )


def get_region_vpc(region):
    """get VPC from region with name of aws_setup's namespace

    Requires ec2:DescribeVpcs permission.
    """
    vpcs = ec2_client(region).describe_vpcs(Filters=[
        {'Name': "tag:Name", 'Values': [consts.NAMESPACE]}
    ])['Vpcs']

    if len(vpcs) > 1:
        halt.err(f"Multiple VPCs named {consts.NAMESPACE} in {region} region.")
    elif vpcs:
        return vpcs[0]
    return None


def get_vpc_security_groups(region, vpc_id):
    """get non-default security groups in specified VPC

    Requires ec2:DescribeSecurityGroups permission.
    """
    aws_sgs = ec2_client(region).describe_security_groups(Filters=[
        {'Name': "vpc-id", 'Values': [vpc_id]}
    ])['SecurityGroups']
    return [sg for sg in aws_sgs if sg['GroupName'] != "default"]


# TODO: Attach tag(s) on resource (e.g. VPC) creation when it becomes supported
def attach_tags(region, resource_id, name_tag=None):
    """attempt to attach tag(s) to resource (including Namespace tag) for 60s

    Requires ec2:CreateTags permission.

    The functionality of blocking until the resource exists is relied upon.

    To account for newly created resources, NotFound exceptions are checked
    for and passed in a loop attempting to create tag(s). Why not use waiters?
    Because waiters don't work reliably (in my experience), that's why.

    Args:
        region (str): AWS region the resource resides in.
        resource_id (str): The ID of the resource.
        name_tag (str): A tag value to assign to the tag key "Name".
    """
    new_tags = [{'Key': "Namespace", 'Value': consts.NAMESPACE}]
    if name_tag is not None:
        new_tags.append({'Key': "Name", 'Value': name_tag})

    _ec2_client = ec2_client(region)
    not_found_regex = re.compile("Invalid[a-zA-Z]*\\.NotFound")
    for _ in range(60):
        try:
            _ec2_client.create_tags(Resources=[resource_id], Tags=new_tags)
            break
        except ClientError as e:
            if not_found_regex.search(e.response['Error']['Code']) is None:
                halt.err(f"Exception when tagging {resource_id}:", str(e))
            sleep(1)
    else:
        halt.err(f"Can't find {resource_id} a minute after its creation.")


def validate_user_exists(path_prefix, user_name):
    """validate IAM user exists (case insensitive), and return exact name

    Requires iam:ListUsers permission.
    """
    iam_users = iam_client().list_users(PathPrefix=path_prefix)['Users']
    for iam_user in iam_users:
        if iam_user['UserName'].lower() == user_name.lower():
            return iam_user['UserName']
    halt.err(f"IAM user \"{user_name}\" not found from AWS.")


def validate_group_exists(path_prefix, group_name):
    """validate IAM group exists (case sensitive), and return name

    Requires iam:ListGroups permission.
    """
    iam_groups = iam_client().list_groups(PathPrefix=path_prefix)['Groups']
    for iam_group in iam_groups:
        if iam_group['GroupName'] == group_name:
            return iam_group['GroupName']
    halt.err(f"IAM group \"{group_name}\" not found from AWS.")


def access_key_owner(access_key_id):
    """get name of IAM user who owns access key (or None if key invalid)

    Requires iam:GetAccessKeyLastUsed permission.
    """
    with ClientErrorHalt(allow=["AccessDenied"]):
        return iam_client().get_access_key_last_used(
            AccessKeyId=access_key_id)['UserName']
    return None


class ClientErrorHalt:
    """context manager to catch ClientErrors"""

    def __init__(self, *, allow=None):
        self.pass_exceptions = allow
        if allow is None:
            self.pass_exceptions = []

    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None and issubclass(exc_type, ClientError):
            if exc_value.response['Error']['Code'] not in self.pass_exceptions:
                halt.err(str(exc_value))
            return True  # Ignore ClientError
        return False  # ClientError wasn't raised
