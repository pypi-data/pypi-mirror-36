# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class Router(pulumi.CustomResource):
    """
    Manages a V2 router resource within OpenStack.
    """
    def __init__(__self__, __name__, __opts__=None, admin_state_up=None, availability_zone_hints=None, distributed=None, enable_snat=None, external_fixed_ips=None, external_gateway=None, external_network_id=None, name=None, region=None, tenant_id=None, value_specs=None, vendor_options=None):
        """Create a Router resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if admin_state_up and not isinstance(admin_state_up, bool):
            raise TypeError('Expected property admin_state_up to be a bool')
        __self__.admin_state_up = admin_state_up
        """
        Administrative up/down status for the router
        (must be "true" or "false" if provided). Changing this updates the
        `admin_state_up` of an existing router.
        """
        __props__['adminStateUp'] = admin_state_up

        if availability_zone_hints and not isinstance(availability_zone_hints, list):
            raise TypeError('Expected property availability_zone_hints to be a list')
        __self__.availability_zone_hints = availability_zone_hints
        """
        An availability zone is used to make 
        network resources highly available. Used for resources with high availability so that they are scheduled on different availability zones. Changing
        this creates a new router.
        """
        __props__['availabilityZoneHints'] = availability_zone_hints

        if distributed and not isinstance(distributed, bool):
            raise TypeError('Expected property distributed to be a bool')
        __self__.distributed = distributed
        """
        Indicates whether or not to create a
        distributed router. The default policy setting in Neutron restricts
        usage of this property to administrative users only.
        """
        __props__['distributed'] = distributed

        if enable_snat and not isinstance(enable_snat, bool):
            raise TypeError('Expected property enable_snat to be a bool')
        __self__.enable_snat = enable_snat
        """
        Enable Source NAT for the router. Valid values are
        "true" or "false". An `external_network_id` has to be set in order to
        set this property. Changing this updates the `enable_snat` of the router.
        """
        __props__['enableSnat'] = enable_snat

        if external_fixed_ips and not isinstance(external_fixed_ips, list):
            raise TypeError('Expected property external_fixed_ips to be a list')
        __self__.external_fixed_ips = external_fixed_ips
        """
        An external fixed IP for the router. This
        can be repeated. The structure is described below. An `external_network_id`
        has to be set in order to set this property. Changing this updates the
        external fixed IPs of the router.
        """
        __props__['externalFixedIps'] = external_fixed_ips

        if external_gateway and not isinstance(external_gateway, basestring):
            raise TypeError('Expected property external_gateway to be a basestring')
        __self__.external_gateway = external_gateway
        """
        The
        network UUID of an external gateway for the router. A router with an
        external gateway is required if any compute instances or load balancers
        will be using floating IPs. Changing this updates the external gateway
        of an existing router.
        """
        __props__['externalGateway'] = external_gateway

        if external_network_id and not isinstance(external_network_id, basestring):
            raise TypeError('Expected property external_network_id to be a basestring')
        __self__.external_network_id = external_network_id
        """
        The network UUID of an external gateway
        for the router. A router with an external gateway is required if any
        compute instances or load balancers will be using floating IPs. Changing
        this updates the external gateway of the router.
        """
        __props__['externalNetworkId'] = external_network_id

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        """
        A unique name for the router. Changing this
        updates the `name` of an existing router.
        """
        __props__['name'] = name

        if region and not isinstance(region, basestring):
            raise TypeError('Expected property region to be a basestring')
        __self__.region = region
        """
        The region in which to obtain the V2 networking client.
        A networking client is needed to create a router. If omitted, the
        `region` argument of the provider is used. Changing this creates a new
        router.
        """
        __props__['region'] = region

        if tenant_id and not isinstance(tenant_id, basestring):
            raise TypeError('Expected property tenant_id to be a basestring')
        __self__.tenant_id = tenant_id
        """
        The owner of the floating IP. Required if admin wants
        to create a router for another tenant. Changing this creates a new router.
        """
        __props__['tenantId'] = tenant_id

        if value_specs and not isinstance(value_specs, dict):
            raise TypeError('Expected property value_specs to be a dict')
        __self__.value_specs = value_specs
        """
        Map of additional driver-specific options.
        """
        __props__['valueSpecs'] = value_specs

        if vendor_options and not isinstance(vendor_options, dict):
            raise TypeError('Expected property vendor_options to be a dict')
        __self__.vendor_options = vendor_options
        """
        Map of additional vendor-specific options.
        Supported options are described below.
        """
        __props__['vendorOptions'] = vendor_options

        super(Router, __self__).__init__(
            'openstack:networking/router:Router',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'adminStateUp' in outs:
            self.admin_state_up = outs['adminStateUp']
        if 'availabilityZoneHints' in outs:
            self.availability_zone_hints = outs['availabilityZoneHints']
        if 'distributed' in outs:
            self.distributed = outs['distributed']
        if 'enableSnat' in outs:
            self.enable_snat = outs['enableSnat']
        if 'externalFixedIps' in outs:
            self.external_fixed_ips = outs['externalFixedIps']
        if 'externalGateway' in outs:
            self.external_gateway = outs['externalGateway']
        if 'externalNetworkId' in outs:
            self.external_network_id = outs['externalNetworkId']
        if 'name' in outs:
            self.name = outs['name']
        if 'region' in outs:
            self.region = outs['region']
        if 'tenantId' in outs:
            self.tenant_id = outs['tenantId']
        if 'valueSpecs' in outs:
            self.value_specs = outs['valueSpecs']
        if 'vendorOptions' in outs:
            self.vendor_options = outs['vendorOptions']
