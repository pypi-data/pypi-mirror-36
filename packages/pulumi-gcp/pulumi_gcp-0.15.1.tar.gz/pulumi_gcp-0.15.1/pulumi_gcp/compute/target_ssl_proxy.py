# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class TargetSSLProxy(pulumi.CustomResource):
    def __init__(__self__, __name__, __opts__=None, backend_service=None, description=None, name=None, project=None, proxy_header=None, ssl_certificates=None, ssl_policy=None):
        """Create a TargetSSLProxy resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not backend_service:
            raise TypeError('Missing required property backend_service')
        elif not isinstance(backend_service, basestring):
            raise TypeError('Expected property backend_service to be a basestring')
        __self__.backend_service = backend_service
        __props__['backendService'] = backend_service

        if description and not isinstance(description, basestring):
            raise TypeError('Expected property description to be a basestring')
        __self__.description = description
        __props__['description'] = description

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        __props__['name'] = name

        if project and not isinstance(project, basestring):
            raise TypeError('Expected property project to be a basestring')
        __self__.project = project
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        __props__['project'] = project

        if proxy_header and not isinstance(proxy_header, basestring):
            raise TypeError('Expected property proxy_header to be a basestring')
        __self__.proxy_header = proxy_header
        __props__['proxyHeader'] = proxy_header

        if not ssl_certificates:
            raise TypeError('Missing required property ssl_certificates')
        elif not isinstance(ssl_certificates, basestring):
            raise TypeError('Expected property ssl_certificates to be a basestring')
        __self__.ssl_certificates = ssl_certificates
        __props__['sslCertificates'] = ssl_certificates

        if ssl_policy and not isinstance(ssl_policy, basestring):
            raise TypeError('Expected property ssl_policy to be a basestring')
        __self__.ssl_policy = ssl_policy
        __props__['sslPolicy'] = ssl_policy

        __self__.creation_timestamp = pulumi.runtime.UNKNOWN
        __self__.proxy_id = pulumi.runtime.UNKNOWN
        __self__.self_link = pulumi.runtime.UNKNOWN
        """
        The URI of the created resource.
        """

        super(TargetSSLProxy, __self__).__init__(
            'gcp:compute/targetSSLProxy:TargetSSLProxy',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'backendService' in outs:
            self.backend_service = outs['backendService']
        if 'creationTimestamp' in outs:
            self.creation_timestamp = outs['creationTimestamp']
        if 'description' in outs:
            self.description = outs['description']
        if 'name' in outs:
            self.name = outs['name']
        if 'project' in outs:
            self.project = outs['project']
        if 'proxyHeader' in outs:
            self.proxy_header = outs['proxyHeader']
        if 'proxyId' in outs:
            self.proxy_id = outs['proxyId']
        if 'selfLink' in outs:
            self.self_link = outs['selfLink']
        if 'sslCertificates' in outs:
            self.ssl_certificates = outs['sslCertificates']
        if 'sslPolicy' in outs:
            self.ssl_policy = outs['sslPolicy']
