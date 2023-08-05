# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class GetDefaultServiceAccountResult(object):
    """
    A collection of values returned by getDefaultServiceAccount.
    """
    def __init__(__self__, email=None, project=None, id=None):
        if email and not isinstance(email, basestring):
            raise TypeError('Expected argument email to be a basestring')
        __self__.email = email
        """
        Email address of the default service account used by VMs running in this project
        """
        if project and not isinstance(project, basestring):
            raise TypeError('Expected argument project to be a basestring')
        __self__.project = project
        if id and not isinstance(id, basestring):
            raise TypeError('Expected argument id to be a basestring')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

def get_default_service_account(project=None):
    """
    Use this data source to retrieve default service account for this project
    """
    __args__ = dict()

    __args__['project'] = project
    __ret__ = pulumi.runtime.invoke('gcp:compute/getDefaultServiceAccount:getDefaultServiceAccount', __args__)

    return GetDefaultServiceAccountResult(
        email=__ret__.get('email'),
        project=__ret__.get('project'),
        id=__ret__.get('id'))
