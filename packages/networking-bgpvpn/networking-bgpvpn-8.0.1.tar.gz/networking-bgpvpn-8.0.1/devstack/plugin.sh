#!/bin/bash

# Save trace setting
_XTRACE_NETWORKING_BGPVPN=$(set +o | grep xtrace)
set -o xtrace

if is_service_enabled q-agt; then
   source $NEUTRON_DIR/devstack/lib/l2_agent
fi

if [[ "$1" == "source" ]]; then
    # no-op
    :
elif [[ "$1" == "stack" && "$2" == "install" ]]; then
    echo_summary "Installing networking-bgpvpn"
    setup_develop $NETWORKING_BGPVPN_DIR
elif [[ "$1" == "stack" && "$2" == "pre-install" ]]; then
    echo_summary "Enabling networking-bgpvpn service plugin"
    _neutron_service_plugin_class_add bgpvpn
    if [[ "$Q_AGENT" == "bagpipe-openvswitch" ]]; then
        echo "networking-bagpipe: you don't need to set Q_AGENT=bagpipe-openvswitch anymore"
        Q_AGENT=openvswitch``
    fi
elif [[ "$1" == "stack" && "$2" == "test-config" ]]; then
    if is_service_enabled tempest; then
        echo_summary "Enabling bgpvpn in $TEMPEST_CONFIG"
    fi
elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
    if is_service_enabled q-svc; then
        echo_summary "Configuring networking-bgpvpn"
        mkdir -v -p $NEUTRON_CONF_DIR/policy.d && cp -v $NETWORKING_BGPVPN_DIR/etc/neutron/policy.d/bgpvpn.conf $NEUTRON_CONF_DIR/policy.d
        mkdir -v -p $(dirname $NETWORKING_BGPVPN_CONF) && cp -v $NETWORKING_BGPVPN_DIR/etc/neutron/networking_bgpvpn.conf $NETWORKING_BGPVPN_CONF
        inicomment $NETWORKING_BGPVPN_CONF service_providers service_provider
        iniadd $NETWORKING_BGPVPN_CONF service_providers service_provider $NETWORKING_BGPVPN_DRIVER
        neutron_server_config_add $NETWORKING_BGPVPN_CONF
    fi
    if is_service_enabled q-agt && is_service_enabled b-bgp ; then
        echo_summary "Configuring agent for bagpipe bgpvpn"

        plugin_agent_add_l2_agent_extension bagpipe_bgpvpn
        configure_l2_agent
        if [[ "$Q_AGENT" == "openvswitch" ]]; then
            # l2pop and arp_responder are required for bagpipe driver
            iniset /$Q_PLUGIN_CONF_FILE agent l2_population True
            iniset /$Q_PLUGIN_CONF_FILE agent arp_responder True
        elif [[ "$Q_AGENT" == "linuxbridge" ]]; then
            # l2pop is required for EVPN/VXLAN bagpipe driver
            iniset /$Q_PLUGIN_CONF_FILE vxlan l2_population True
        else
            die $LINENO "unsupported agent for networking-bagpipe: $Q_AGENT"
	fi
    fi
    if is_service_enabled h-eng; then
        echo_summary "Enabling bgpvpn in $HEAT_CONF"
        iniset $HEAT_CONF DEFAULT plugin_dirs $NETWORKING_BGPVPN_DIR/networking_bgpvpn_heat
    fi
    if is_service_enabled horizon; then
        cp $BGPVPN_DASHBOARD_ENABLE $HORIZON_DIR/openstack_dashboard/local/enabled/
        # Add policy file for BGPVPN_DASHBOARD
        _set_policy_file $DEST/horizon/openstack_dashboard/local/local_settings.py \
            networking-bgpvpn $NETWORKING_BGPVPN_DIR/bgpvpn_dashboard/etc/bgpvpn-horizon.conf
    fi
fi

function _ensure_policy_file {
    local file=$1

    # Look for POLICY_FILES dict.
    start=$(grep -nE '^\s*POLICY_FILES\s*=\s*' $file | cut -d : -f 1)
    if [ ! -n "$start" ]; then
        # If POLICY_FILES is not found, define it.
        cat <<EOF >> $file
POLICY_FILES = {
    'identity': 'keystone_policy.json',
    'compute': 'nova_policy.json',
    'volume': 'cinder_policy.json',
    'image': 'glance_policy.json',
    'orchestration': 'heat_policy.json',
    'network': 'neutron_policy.json',
}
EOF
    fi
}

function _set_policy_file {
    local file=$1
    local policy_name=$2
    local policy_file=$3

    _ensure_policy_file $file
    echo "POLICY_FILES['$policy_name'] = '$policy_file'" >> $file
}

if [[ "$1" == "unstack" ]]; then
    #no-op
    :
fi
if [[ "$1" == "clean" ]]; then
    # Remove bgpvpn-dashboard enabled files and pyc
    rm -f $HORIZON_DIR/openstack_dashboard/local/enabled/*_bgpvpn_panel*
fi

# Restore XTRACE
${_XTRACE_NETWORKING_BGPVPN}

