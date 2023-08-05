# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class URLMap(pulumi.CustomResource):
    """
    Manages a URL Map resource within GCE. For more information see
    [the official documentation](https://cloud.google.com/compute/docs/load-balancing/http/url-map)
    and
    [API](https://cloud.google.com/compute/docs/reference/latest/urlMaps).
    
    """
    def __init__(__self__, __name__, __opts__=None, default_service=None, description=None, host_rules=None, name=None, path_matchers=None, project=None, tests=None):
        """Create a URLMap resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not default_service:
            raise TypeError('Missing required property default_service')
        elif not isinstance(default_service, basestring):
            raise TypeError('Expected property default_service to be a basestring')
        __self__.default_service = default_service
        """
        The backend service or backend bucket to use when none of the given rules match.
        """
        __props__['defaultService'] = default_service

        if description and not isinstance(description, basestring):
            raise TypeError('Expected property description to be a basestring')
        __self__.description = description
        """
        A brief description of this resource.
        """
        __props__['description'] = description

        if host_rules and not isinstance(host_rules, list):
            raise TypeError('Expected property host_rules to be a list')
        __self__.host_rules = host_rules
        """
        A list of host rules. Multiple blocks of this type are permitted. Structure is documented below.
        """
        __props__['hostRules'] = host_rules

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        """
        A unique name for the resource, required by GCE.
        Changing this forces a new resource to be created.
        """
        __props__['name'] = name

        if path_matchers and not isinstance(path_matchers, list):
            raise TypeError('Expected property path_matchers to be a list')
        __self__.path_matchers = path_matchers
        """
        A list of paths to match. Structure is documented below.
        """
        __props__['pathMatchers'] = path_matchers

        if project and not isinstance(project, basestring):
            raise TypeError('Expected property project to be a basestring')
        __self__.project = project
        """
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        __props__['project'] = project

        if tests and not isinstance(tests, list):
            raise TypeError('Expected property tests to be a list')
        __self__.tests = tests
        """
        The test to perform.  Multiple blocks of this type are permitted. Structure is documented below.
        """
        __props__['tests'] = tests

        __self__.fingerprint = pulumi.runtime.UNKNOWN
        """
        The unique fingerprint for this resource.
        """
        __self__.map_id = pulumi.runtime.UNKNOWN
        """
        The GCE assigned ID of the resource.
        """
        __self__.self_link = pulumi.runtime.UNKNOWN
        """
        The URI of the created resource.
        """

        super(URLMap, __self__).__init__(
            'gcp:compute/uRLMap:URLMap',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'defaultService' in outs:
            self.default_service = outs['defaultService']
        if 'description' in outs:
            self.description = outs['description']
        if 'fingerprint' in outs:
            self.fingerprint = outs['fingerprint']
        if 'hostRules' in outs:
            self.host_rules = outs['hostRules']
        if 'mapId' in outs:
            self.map_id = outs['mapId']
        if 'name' in outs:
            self.name = outs['name']
        if 'pathMatchers' in outs:
            self.path_matchers = outs['pathMatchers']
        if 'project' in outs:
            self.project = outs['project']
        if 'selfLink' in outs:
            self.self_link = outs['selfLink']
        if 'tests' in outs:
            self.tests = outs['tests']
