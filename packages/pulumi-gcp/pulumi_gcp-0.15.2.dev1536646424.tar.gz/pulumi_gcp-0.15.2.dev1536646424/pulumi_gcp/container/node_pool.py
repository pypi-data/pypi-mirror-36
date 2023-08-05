# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class NodePool(pulumi.CustomResource):
    """
    Manages a Node Pool resource within GKE. For more information see
    [the official documentation](https://cloud.google.com/container-engine/docs/node-pools)
    and
    [API](https://cloud.google.com/container-engine/reference/rest/v1/projects.zones.clusters.nodePools).
    """
    def __init__(__self__, __name__, __opts__=None, autoscaling=None, cluster=None, initial_node_count=None, management=None, name=None, name_prefix=None, node_config=None, node_count=None, project=None, region=None, version=None, zone=None):
        """Create a NodePool resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if autoscaling and not isinstance(autoscaling, dict):
            raise TypeError('Expected property autoscaling to be a dict')
        __self__.autoscaling = autoscaling
        """
        Configuration required by cluster autoscaler to adjust
        the size of the node pool to the current cluster usage. Structure is documented below.
        """
        __props__['autoscaling'] = autoscaling

        if not cluster:
            raise TypeError('Missing required property cluster')
        elif not isinstance(cluster, basestring):
            raise TypeError('Expected property cluster to be a basestring')
        __self__.cluster = cluster
        """
        The cluster to create the node pool for.  Cluster must be present in `zone` provided for zonal clusters.
        """
        __props__['cluster'] = cluster

        if initial_node_count and not isinstance(initial_node_count, int):
            raise TypeError('Expected property initial_node_count to be a int')
        __self__.initial_node_count = initial_node_count
        """
        The initial node count for the pool. Changing this will force
        recreation of the resource.
        """
        __props__['initialNodeCount'] = initial_node_count

        if management and not isinstance(management, dict):
            raise TypeError('Expected property management to be a dict')
        __self__.management = management
        """
        Node management configuration, wherein auto-repair and
        auto-upgrade is configured. Structure is documented below.
        """
        __props__['management'] = management

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        """
        The name of the node pool. If left blank, Terraform will
        auto-generate a unique name.
        """
        __props__['name'] = name

        if name_prefix and not isinstance(name_prefix, basestring):
            raise TypeError('Expected property name_prefix to be a basestring')
        __self__.name_prefix = name_prefix
        """
        Creates a unique name for the node pool beginning
        with the specified prefix. Conflicts with `name`.
        """
        __props__['namePrefix'] = name_prefix

        if node_config and not isinstance(node_config, dict):
            raise TypeError('Expected property node_config to be a dict')
        __self__.node_config = node_config
        """
        The node configuration of the pool. See
        google_container_cluster for schema.
        """
        __props__['nodeConfig'] = node_config

        if node_count and not isinstance(node_count, int):
            raise TypeError('Expected property node_count to be a int')
        __self__.node_count = node_count
        """
        The number of nodes per instance group. This field can be used to
        update the number of nodes per instance group but should not be used alongside `autoscaling`.
        """
        __props__['nodeCount'] = node_count

        if project and not isinstance(project, basestring):
            raise TypeError('Expected property project to be a basestring')
        __self__.project = project
        """
        The ID of the project in which to create the node pool. If blank,
        the provider-configured project will be used.
        """
        __props__['project'] = project

        if region and not isinstance(region, basestring):
            raise TypeError('Expected property region to be a basestring')
        __self__.region = region
        """
        The region in which the cluster resides (for regional clusters).
        """
        __props__['region'] = region

        if version and not isinstance(version, basestring):
            raise TypeError('Expected property version to be a basestring')
        __self__.version = version
        """
        The Kubernetes version for the nodes in this pool. Note that if this field
        and `auto_upgrade` are both specified, they will fight each other for what the node version should
        be, so setting both is highly discouraged.
        """
        __props__['version'] = version

        if zone and not isinstance(zone, basestring):
            raise TypeError('Expected property zone to be a basestring')
        __self__.zone = zone
        """
        The zone in which the cluster resides.
        """
        __props__['zone'] = zone

        __self__.instance_group_urls = pulumi.runtime.UNKNOWN

        super(NodePool, __self__).__init__(
            'gcp:container/nodePool:NodePool',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'autoscaling' in outs:
            self.autoscaling = outs['autoscaling']
        if 'cluster' in outs:
            self.cluster = outs['cluster']
        if 'initialNodeCount' in outs:
            self.initial_node_count = outs['initialNodeCount']
        if 'instanceGroupUrls' in outs:
            self.instance_group_urls = outs['instanceGroupUrls']
        if 'management' in outs:
            self.management = outs['management']
        if 'name' in outs:
            self.name = outs['name']
        if 'namePrefix' in outs:
            self.name_prefix = outs['namePrefix']
        if 'nodeConfig' in outs:
            self.node_config = outs['nodeConfig']
        if 'nodeCount' in outs:
            self.node_count = outs['nodeCount']
        if 'project' in outs:
            self.project = outs['project']
        if 'region' in outs:
            self.region = outs['region']
        if 'version' in outs:
            self.version = outs['version']
        if 'zone' in outs:
            self.zone = outs['zone']
