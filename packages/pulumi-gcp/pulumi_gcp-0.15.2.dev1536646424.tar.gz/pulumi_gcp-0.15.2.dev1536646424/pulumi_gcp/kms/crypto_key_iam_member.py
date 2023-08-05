# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class CryptoKeyIAMMember(pulumi.CustomResource):
    """
    Allows creation and management of a single member for a single binding within
    the IAM policy for an existing Google Cloud KMS crypto key.
    
    ~> **Note:** This resource _must not_ be used in conjunction with
       `google_kms_crypto_key_iam_policy` or they will fight over what your policy
       should be. Similarly, roles controlled by `google_kms_crypto_key_iam_binding`
       should not be assigned to using `google_kms_crypto_key_iam_member`.
    """
    def __init__(__self__, __name__, __opts__=None, crypto_key_id=None, member=None, role=None):
        """Create a CryptoKeyIAMMember resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not crypto_key_id:
            raise TypeError('Missing required property crypto_key_id')
        elif not isinstance(crypto_key_id, basestring):
            raise TypeError('Expected property crypto_key_id to be a basestring')
        __self__.crypto_key_id = crypto_key_id
        """
        The key ring ID, in the form
        `{project_id}/{location_name}/{key_ring_name}/{crypto_key_name}` or
        `{location_name}/{key_ring_name}/{crypto_key_name}`. In the second form,
        the provider's project setting will be used as a fallback.
        """
        __props__['cryptoKeyId'] = crypto_key_id

        if not member:
            raise TypeError('Missing required property member')
        elif not isinstance(member, basestring):
            raise TypeError('Expected property member to be a basestring')
        __self__.member = member
        """
        The user that the role should apply to.
        """
        __props__['member'] = member

        if not role:
            raise TypeError('Missing required property role')
        elif not isinstance(role, basestring):
            raise TypeError('Expected property role to be a basestring')
        __self__.role = role
        """
        The role that should be applied. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        __props__['role'] = role

        __self__.etag = pulumi.runtime.UNKNOWN
        """
        (Computed) The etag of the project's IAM policy.
        """

        super(CryptoKeyIAMMember, __self__).__init__(
            'gcp:kms/cryptoKeyIAMMember:CryptoKeyIAMMember',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'cryptoKeyId' in outs:
            self.crypto_key_id = outs['cryptoKeyId']
        if 'etag' in outs:
            self.etag = outs['etag']
        if 'member' in outs:
            self.member = outs['member']
        if 'role' in outs:
            self.role = outs['role']
