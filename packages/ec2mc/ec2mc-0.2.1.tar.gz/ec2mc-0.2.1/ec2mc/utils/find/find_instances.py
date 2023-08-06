from ec2mc import consts
from ec2mc.utils import aws
from ec2mc.utils import halt
from ec2mc.utils.threader import Threader

def main(cmd_args, *, single_instance=False):
    """wrapper for probe_regions which prints found instances to the CLI

    Requires ec2:DescribeInstances permission.

    Halts if no instances found. This functionality is relied upon.

    Args:
        cmd_args (dict): See argparse_args function.
        single_instance (bool): Halt if multiple instances are found.

    Returns: See what probe_regions returns.
    """
    regions, tag_filter = parse_filters(cmd_args)

    print("")
    print(f"Probing {len(regions)} AWS region(s) for instances...")

    all_instances = probe_regions(regions, tag_filter)

    if not all_instances:
        if (cmd_args['region_filter'] or cmd_args['tag_filters'] or
                cmd_args['name_filter'] or cmd_args['id_filter']):
            halt.err("No namespace instances found.",
                "  Remove specified filter(s) and try again.")
        halt.err("No namespace instances found.")

    for region in regions:
        instances = [instance for instance in all_instances
            if instance['region'] == region]
        if not instances:
            continue

        print(f"{region}: {len(instances)} instance(s) found:")
        for instance in instances:
            print(f"  {instance['name']} ({instance['id']})")
            for tag_key, tag_value in instance['tags'].items():
                print(f"    {tag_key}: {tag_value}")

    if single_instance is True:
        if len(all_instances) > 1:
            halt.err("Instance query returned multiple results.",
                "  Narrow filter(s) so that only one instance is found.")
        return all_instances[0]
    return all_instances


def probe_regions(regions=None, tag_filter=None):
    """probe AWS region(s) for instances, and return dict(s) of instance(s)

    Requires ec2:DescribeInstances permission.

    Uses multithreading to probe all whitelisted regions simultaneously.

    Args:
        regions (list[str]): AWS region(s) to probe.
        tag_filter (list[dict]): Tag filter to filter instances with.

    Returns:
        list[dict]: Found instance(s).
            'region' (str): AWS region that an instance is in.
            For other key-value pairs, see what probe_region returns.
    """
    if regions is None:
        regions = consts.REGIONS

    if tag_filter is None:
        tag_filter = []
    tag_filter.append({'Name': "tag:Namespace", 'Values': [consts.NAMESPACE]})

    threader = Threader()
    for region in regions:
        threader.add_thread(probe_region, (region, tag_filter))
    regions_instances = threader.get_results(return_dict=True)

    return [{'region': region, **instance}
        for region, instances in regions_instances.items()
        for instance in instances]


def probe_region(region, tag_filter):
    """probe single AWS region for non-terminated named instances

    Requires ec2:DescribeInstances permission.

    Args:
        region (str): AWS region to probe.
        tag_filter (list[dict]): Filter out instances that don't have tags
            matching the filter. If None/empty, filter not used.

    Returns:
        list[dict]: Instance(s) found in region.
            'id' (str): ID of instance.
            'name' (str): Tag value for instance tag key "Name".
            'tags' (dict): Instance tag key-value pair(s).
    """
    reservations = aws.ec2_client(region).describe_instances(
        Filters=tag_filter)['Reservations']

    region_instances = []
    for reservation in reservations:
        for instance in reservation['Instances']:
            if instance['State']['Name'] in ("shutting-down", "terminated"):
                continue
            if not any(tag['Key'] == "Name" for tag in instance['Tags']):
                continue

            region_instances.append({
                'id': instance['InstanceId'],
                'tags': dict(sorted({tag['Key']: tag['Value']
                    for tag in instance['Tags']}.items()))
            })
            region_instances[-1].update({
                'name': region_instances[-1]['tags'].pop('Name')
            })

    return sorted(region_instances, key=lambda k: k['name'])


def parse_filters(cmd_args):
    """parses region and tag filters

    Args:
        cmd_args (dict): See main's arguments.

    Returns:
        tuple:
            list[str]: Region(s) to probe.
            list[dict]: Filter to pass to EC2 client's describe_instances.
    """
    regions = consts.REGIONS
    if cmd_args['region_filter'] is not None:
        region_filter = set(cmd_args['region_filter'])
        # Validate region filter
        if not region_filter.issubset(set(regions)):
            halt.err("Following region(s) not in region whitelist:",
                *(region_filter - set(regions)))
        regions = tuple(region_filter)

    tag_filter = []
    if cmd_args['tag_filters']:
        # Convert dict(s) list to what describe_instances' Filters expects.
        for filter_elements in cmd_args['tag_filters']:
            # Filter instances based on tag key-value(s).
            if len(filter_elements) > 1:
                tag_filter.append({
                    'Name': f"tag:{filter_elements[0]}",
                    'Values': filter_elements[1:]
                })
            # If no filter tag values given, filter by just the tag key.
            elif filter_elements:
                tag_filter.append({
                    'Name': "tag-key",
                    'Values': [filter_elements[0]]
                })
    if cmd_args['name_filter']:
        tag_filter.append({
            'Name': "tag:Name",
            'Values': cmd_args['name_filter']
        })
    if cmd_args['id_filter']:
        tag_filter.append({
            'Name': "instance-id",
            'Values': cmd_args['id_filter']
        })

    return (regions, tag_filter)


def get_state_and_ip(region, instance_ip):
    """return state and (elastic) IP of instance

    Requires ec2:DescribeInstances permission.
    """
    response = aws.ec2_client(region).describe_instances(
        InstanceIds=[instance_ip]
    )['Reservations'][0]['Instances'][0]

    instance_state = response['State']['Name']
    instance_ip = None
    for network_interface in response['NetworkInterfaces']:
        if 'Association' in network_interface:
            # IP is elastic unless association's 'IpOwnerId' is "amazon"
            instance_ip = network_interface['Association']['PublicIp']
            break
    else:
        # Script expects running instances to always have a public IP
        if instance_state == "running":
            instance_state = "???"

    return (instance_state, instance_ip)


def argparse_args(cmd_parser):
    """initialize argparse arguments that the main() function expects"""
    cmd_parser.add_argument(
        "-n", dest="name_filter", nargs="+", metavar="",
        help="Instance tag value filter for the tag key \"Name\".")
    cmd_parser.add_argument(
        "-r", dest="region_filter", nargs="+", metavar="",
        help=("AWS region(s) to probe for instances. If not set, all "
            "whitelisted regions will be probed."))
    cmd_parser.add_argument(
        "-t", dest="tag_filters", nargs="+", action="append", metavar="",
        help=("Instance tag value filter. First value is the tag key, with "
            "proceeding value(s) as the tag value(s). If only 1 value given, "
            "the tag key itself will be filtered for instead."))
    cmd_parser.add_argument(
        "-i", dest="id_filter", nargs="+", metavar="",
        help="Instance ID filter.")
