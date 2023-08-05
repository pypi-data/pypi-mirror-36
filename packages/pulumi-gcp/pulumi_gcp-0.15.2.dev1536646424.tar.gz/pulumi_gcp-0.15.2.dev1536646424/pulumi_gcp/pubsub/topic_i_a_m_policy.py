# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime

class TopicIAMPolicy(pulumi.CustomResource):
    """
    Three different resources help you manage your IAM policy for pubsub topic. Each of these resources serves a different use case:
    
    * `google_pubsub_topic_iam_policy`: Authoritative. Sets the IAM policy for the topic and replaces any existing policy already attached.
    * `google_pubsub_topic_iam_binding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the topic are preserved.
    * `google_pubsub_topic_iam_member`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the topic are preserved.
    
    ~> **Note:** `google_pubsub_topic_iam_policy` **cannot** be used in conjunction with `google_pubsub_topic_iam_binding` and `google_pubsub_topic_iam_member` or they will fight over what your policy should be.
    
    ~> **Note:** `google_pubsub_topic_iam_binding` resources **can be** used in conjunction with `google_pubsub_topic_iam_member` resources **only if** they do not grant privilege to the same role.
    """
    def __init__(__self__, __name__, __opts__=None, policy_data=None, project=None, topic=None):
        """Create a TopicIAMPolicy resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not policy_data:
            raise TypeError('Missing required property policy_data')
        elif not isinstance(policy_data, basestring):
            raise TypeError('Expected property policy_data to be a basestring')
        __self__.policy_data = policy_data
        """
        The policy data generated by
        a `google_iam_policy` data source.
        """
        __props__['policyData'] = policy_data

        if project and not isinstance(project, basestring):
            raise TypeError('Expected property project to be a basestring')
        __self__.project = project
        """
        The project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        __props__['project'] = project

        if not topic:
            raise TypeError('Missing required property topic')
        elif not isinstance(topic, basestring):
            raise TypeError('Expected property topic to be a basestring')
        __self__.topic = topic
        """
        The topic name or id to bind to attach IAM policy to.
        """
        __props__['topic'] = topic

        __self__.etag = pulumi.runtime.UNKNOWN
        """
        (Computed) The etag of the topic's IAM policy.
        """

        super(TopicIAMPolicy, __self__).__init__(
            'gcp:pubsub/topicIAMPolicy:TopicIAMPolicy',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'etag' in outs:
            self.etag = outs['etag']
        if 'policyData' in outs:
            self.policy_data = outs['policyData']
        if 'project' in outs:
            self.project = outs['project']
        if 'topic' in outs:
            self.topic = outs['topic']
