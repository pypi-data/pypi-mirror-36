# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class InstanceTemplate(pulumi.CustomResource):
    """
    Manages a VM instance template resource within GCE. For more information see
    [the official documentation](https://cloud.google.com/compute/docs/instance-templates)
    and
    [API](https://cloud.google.com/compute/docs/reference/latest/instanceTemplates).
    
    """
    def __init__(__self__, __name__, __opts__=None, can_ip_forward=None, description=None, disks=None, guest_accelerators=None, instance_description=None, labels=None, machine_type=None, metadata=None, metadata_startup_script=None, min_cpu_platform=None, name=None, name_prefix=None, network_interfaces=None, project=None, region=None, schedulings=None, service_account=None, tags=None):
        """Create a InstanceTemplate resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if can_ip_forward and not isinstance(can_ip_forward, bool):
            raise TypeError('Expected property can_ip_forward to be a bool')
        __self__.can_ip_forward = can_ip_forward
        """
        Whether to allow sending and receiving of
        packets with non-matching source or destination IPs. This defaults to false.
        """
        __props__['canIpForward'] = can_ip_forward

        if description and not isinstance(description, basestring):
            raise TypeError('Expected property description to be a basestring')
        __self__.description = description
        """
        A brief description of this resource.
        """
        __props__['description'] = description

        if not disks:
            raise TypeError('Missing required property disks')
        elif not isinstance(disks, list):
            raise TypeError('Expected property disks to be a list')
        __self__.disks = disks
        """
        Disks to attach to instances created from this template.
        This can be specified multiple times for multiple disks. Structure is
        documented below.
        """
        __props__['disks'] = disks

        if guest_accelerators and not isinstance(guest_accelerators, list):
            raise TypeError('Expected property guest_accelerators to be a list')
        __self__.guest_accelerators = guest_accelerators
        """
        List of the type and count of accelerator cards attached to the instance. Structure documented below.
        """
        __props__['guestAccelerators'] = guest_accelerators

        if instance_description and not isinstance(instance_description, basestring):
            raise TypeError('Expected property instance_description to be a basestring')
        __self__.instance_description = instance_description
        """
        A brief description to use for instances
        created from this template.
        """
        __props__['instanceDescription'] = instance_description

        if labels and not isinstance(labels, dict):
            raise TypeError('Expected property labels to be a dict')
        __self__.labels = labels
        """
        A set of key/value label pairs to assign to instances
        created from this template,
        """
        __props__['labels'] = labels

        if not machine_type:
            raise TypeError('Missing required property machine_type')
        elif not isinstance(machine_type, basestring):
            raise TypeError('Expected property machine_type to be a basestring')
        __self__.machine_type = machine_type
        """
        The machine type to create.
        """
        __props__['machineType'] = machine_type

        if metadata and not isinstance(metadata, dict):
            raise TypeError('Expected property metadata to be a dict')
        __self__.metadata = metadata
        """
        Metadata key/value pairs to make available from
        within instances created from this template.
        """
        __props__['metadata'] = metadata

        if metadata_startup_script and not isinstance(metadata_startup_script, basestring):
            raise TypeError('Expected property metadata_startup_script to be a basestring')
        __self__.metadata_startup_script = metadata_startup_script
        """
        An alternative to using the
        startup-script metadata key, mostly to match the compute_instance resource.
        This replaces the startup-script metadata key on the created instance and
        thus the two mechanisms are not allowed to be used simultaneously.
        """
        __props__['metadataStartupScript'] = metadata_startup_script

        if min_cpu_platform and not isinstance(min_cpu_platform, basestring):
            raise TypeError('Expected property min_cpu_platform to be a basestring')
        __self__.min_cpu_platform = min_cpu_platform
        """
        Specifies a minimum CPU platform. Applicable values are the friendly names of CPU platforms, such as
        `Intel Haswell` or `Intel Skylake`. See the complete list [here](https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform).
        """
        __props__['minCpuPlatform'] = min_cpu_platform

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        """
        The name of the instance template. If you leave
        this blank, Terraform will auto-generate a unique name.
        """
        __props__['name'] = name

        if name_prefix and not isinstance(name_prefix, basestring):
            raise TypeError('Expected property name_prefix to be a basestring')
        __self__.name_prefix = name_prefix
        """
        Creates a unique name beginning with the specified
        prefix. Conflicts with `name`.
        """
        __props__['namePrefix'] = name_prefix

        if network_interfaces and not isinstance(network_interfaces, list):
            raise TypeError('Expected property network_interfaces to be a list')
        __self__.network_interfaces = network_interfaces
        """
        Networks to attach to instances created from
        this template. This can be specified multiple times for multiple networks.
        Structure is documented below.
        """
        __props__['networkInterfaces'] = network_interfaces

        if project and not isinstance(project, basestring):
            raise TypeError('Expected property project to be a basestring')
        __self__.project = project
        """
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        __props__['project'] = project

        if region and not isinstance(region, basestring):
            raise TypeError('Expected property region to be a basestring')
        __self__.region = region
        """
        An instance template is a global resource that is not
        bound to a zone or a region. However, you can still specify some regional
        resources in an instance template, which restricts the template to the
        region where that resource resides. For example, a custom `subnetwork`
        resource is tied to a specific region. Defaults to the region of the
        Provider if no value is given.
        """
        __props__['region'] = region

        if schedulings and not isinstance(schedulings, list):
            raise TypeError('Expected property schedulings to be a list')
        __self__.schedulings = schedulings
        """
        The scheduling strategy to use. More details about
        this configuration option are detailed below.
        """
        __props__['schedulings'] = schedulings

        if service_account and not isinstance(service_account, dict):
            raise TypeError('Expected property service_account to be a dict')
        __self__.service_account = service_account
        """
        Service account to attach to the instance. Structure is documented below.
        """
        __props__['serviceAccount'] = service_account

        if tags and not isinstance(tags, list):
            raise TypeError('Expected property tags to be a list')
        __self__.tags = tags
        """
        Tags to attach to the instance.
        """
        __props__['tags'] = tags

        __self__.metadata_fingerprint = pulumi.runtime.UNKNOWN
        """
        The unique fingerprint of the metadata.
        """
        __self__.self_link = pulumi.runtime.UNKNOWN
        """
        The URI of the created resource.
        """
        __self__.tags_fingerprint = pulumi.runtime.UNKNOWN
        """
        The unique fingerprint of the tags.
        """

        super(InstanceTemplate, __self__).__init__(
            'gcp:compute/instanceTemplate:InstanceTemplate',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'canIpForward' in outs:
            self.can_ip_forward = outs['canIpForward']
        if 'description' in outs:
            self.description = outs['description']
        if 'disks' in outs:
            self.disks = outs['disks']
        if 'guestAccelerators' in outs:
            self.guest_accelerators = outs['guestAccelerators']
        if 'instanceDescription' in outs:
            self.instance_description = outs['instanceDescription']
        if 'labels' in outs:
            self.labels = outs['labels']
        if 'machineType' in outs:
            self.machine_type = outs['machineType']
        if 'metadata' in outs:
            self.metadata = outs['metadata']
        if 'metadataFingerprint' in outs:
            self.metadata_fingerprint = outs['metadataFingerprint']
        if 'metadataStartupScript' in outs:
            self.metadata_startup_script = outs['metadataStartupScript']
        if 'minCpuPlatform' in outs:
            self.min_cpu_platform = outs['minCpuPlatform']
        if 'name' in outs:
            self.name = outs['name']
        if 'namePrefix' in outs:
            self.name_prefix = outs['namePrefix']
        if 'networkInterfaces' in outs:
            self.network_interfaces = outs['networkInterfaces']
        if 'project' in outs:
            self.project = outs['project']
        if 'region' in outs:
            self.region = outs['region']
        if 'schedulings' in outs:
            self.schedulings = outs['schedulings']
        if 'selfLink' in outs:
            self.self_link = outs['selfLink']
        if 'serviceAccount' in outs:
            self.service_account = outs['serviceAccount']
        if 'tags' in outs:
            self.tags = outs['tags']
        if 'tagsFingerprint' in outs:
            self.tags_fingerprint = outs['tagsFingerprint']
