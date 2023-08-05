# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class Policy(pulumi.CustomResource):
    """
    Allows management of Organization policies for a Google Organization. For more information see
    [the official
    documentation](https://cloud.google.com/resource-manager/docs/organization-policy/overview) and
    [API](https://cloud.google.com/resource-manager/reference/rest/v1/organizations/setOrgPolicy).
    """
    def __init__(__self__, __name__, __opts__=None, boolean_policy=None, constraint=None, list_policy=None, org_id=None, restore_policy=None, version=None):
        """Create a Policy resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if boolean_policy and not isinstance(boolean_policy, dict):
            raise TypeError('Expected property boolean_policy to be a dict')
        __self__.boolean_policy = boolean_policy
        """
        A boolean policy is a constraint that is either enforced or not. Structure is documented below. 
        """
        __props__['booleanPolicy'] = boolean_policy

        if not constraint:
            raise TypeError('Missing required property constraint')
        elif not isinstance(constraint, basestring):
            raise TypeError('Expected property constraint to be a basestring')
        __self__.constraint = constraint
        """
        The name of the Constraint the Policy is configuring, for example, `serviceuser.services`. Check out the [complete list of available constraints](https://cloud.google.com/resource-manager/docs/organization-policy/understanding-constraints#available_constraints).
        """
        __props__['constraint'] = constraint

        if list_policy and not isinstance(list_policy, dict):
            raise TypeError('Expected property list_policy to be a dict')
        __self__.list_policy = list_policy
        """
        A policy that can define specific values that are allowed or denied for the given constraint. It can also be used to allow or deny all values. Structure is documented below.
        """
        __props__['listPolicy'] = list_policy

        if not org_id:
            raise TypeError('Missing required property org_id')
        elif not isinstance(org_id, basestring):
            raise TypeError('Expected property org_id to be a basestring')
        __self__.org_id = org_id
        """
        The numeric ID of the organization to set the policy for.
        """
        __props__['orgId'] = org_id

        if restore_policy and not isinstance(restore_policy, dict):
            raise TypeError('Expected property restore_policy to be a dict')
        __self__.restore_policy = restore_policy
        """
        A restore policy is a constraint to restore the default policy. Structure is documented below. 
        """
        __props__['restorePolicy'] = restore_policy

        if version and not isinstance(version, int):
            raise TypeError('Expected property version to be a int')
        __self__.version = version
        """
        Version of the Policy. Default version is 0.
        """
        __props__['version'] = version

        __self__.etag = pulumi.runtime.UNKNOWN
        """
        (Computed) The etag of the organization policy. `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a policy from overwriting each other. 
        """
        __self__.update_time = pulumi.runtime.UNKNOWN
        """
        (Computed) The timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds, representing when the variable was last updated. Example: "2016-10-09T12:33:37.578138407Z".
        """

        super(Policy, __self__).__init__(
            'gcp:organizations/policy:Policy',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'booleanPolicy' in outs:
            self.boolean_policy = outs['booleanPolicy']
        if 'constraint' in outs:
            self.constraint = outs['constraint']
        if 'etag' in outs:
            self.etag = outs['etag']
        if 'listPolicy' in outs:
            self.list_policy = outs['listPolicy']
        if 'orgId' in outs:
            self.org_id = outs['orgId']
        if 'restorePolicy' in outs:
            self.restore_policy = outs['restorePolicy']
        if 'updateTime' in outs:
            self.update_time = outs['updateTime']
        if 'version' in outs:
            self.version = outs['version']
