# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class SharedVPCHostProject(pulumi.CustomResource):
    """
    Enables the Google Compute Engine
    [Shared VPC](https://cloud.google.com/compute/docs/shared-vpc)
    feature for a project, assigning it as a Shared VPC host project.
    
    For more information, see,
    [the Project API documentation](https://cloud.google.com/compute/docs/reference/latest/projects),
    where the Shared VPC feature is referred to by its former name "XPN".
    """
    def __init__(__self__, __name__, __opts__=None, project=None):
        """Create a SharedVPCHostProject resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not project:
            raise TypeError('Missing required property project')
        elif not isinstance(project, basestring):
            raise TypeError('Expected property project to be a basestring')
        __self__.project = project
        """
        The ID of the project that will serve as a Shared VPC host project
        """
        __props__['project'] = project

        super(SharedVPCHostProject, __self__).__init__(
            'gcp:compute/sharedVPCHostProject:SharedVPCHostProject',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'project' in outs:
            self.project = outs['project']
