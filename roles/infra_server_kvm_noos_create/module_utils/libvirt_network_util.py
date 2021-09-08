# libvirt_storage - Utility Class for the LibVirt Network API Python Bindings

#  Copyright (C) 2021 Petros Petrou
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import libvirt
import sys
import os
import ipaddress

from jinja2 import Template, Environment, PackageLoader
from libvirt import virNetwork, libvirtError

# Network Classes
class Network:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        str_repr = "NAME: " + self.name

        return str_repr

class NatBasedIPv4Network(Network):
    def __init__(self, name, cidr):
        super().__init__(name)
        self.cidr = cidr
        self.network = ipaddress.ip_network(cidr)
        self.netmask = self.network.netmask
        usuable_hosts = list(self.network.hosts())
        self.ip = usuable_hosts[0]          # First element is the first address in the network. Libvirt uses this as the bridge ip address. It is NOT the network ip address.
        self.dhcp_start = usuable_hosts[1]  # Second element is the dhcp start address.
        self.dhcp_end = usuable_hosts[-1]   # Last element is the dhcp end address. It is not the network broadcast address

    def __str__(self):
        str_repr = "NAME: " + self.name + "\t" + \
                   "CIDR: " + self.cidr + "\t" + \
                   "IP: " + self.ip + "\t" + \
                   "NETMASK: " + self.netmask + "\t" + \
                   "DHCP_START: " + self.dhcp_start + "\t" + \
                   "DHCP_END: " + self.dhcp_end

        return str_repr

class IsolatedNetwork(Network):
    def __init__(self, name):
        super().__init__(name)

# Exceptions
class ExNetworkNotFound(Exception):
    ERR_NETWORK_NOT_FOUND = "Network {0} not found."

    def __init__(self, network_name):
        message = self.ERR_NETWORK_NOT_FOUND.format(network_name)
        super().__init__(message)

class ExNetworkExists(Exception):
    ERR_NETWORK_EXISTS = "Network {0} exists."
    
    def __init__(self, network_name):
        message = self.ERR_NETWORK_EXISTS.format(network_name)
        super().__init__(message)

class ExUnsupportedNetwork(Exception):
    ERR_UNSUPPORTED_NETWORK = "Network of class {0} is not supported."
    
    def __init__(self, network_class_name):
        message = self.ERR_UNSUPPORTED_NETWORK.format(network_class_name)
        super().__init__(message)

class ExNotANetwork(Exception):
    ERR_NOT_A_NETWORK = "Network {0} is not a subclass of Network."
    
    def __init__(self, class_name):
        message = self.ERR_NOT_A_NETWORK.format(class_name)
        super().__init__(message)

# Libvirt Network Utility Class
class LibVirtNetworkUtil:
    
    TEMPLATES_DIR = 'templates'
    NETWORK_TEMPLATES_DIR = 'network'
    NAT_BASED_NETWORK_J2 = os.path.join(NETWORK_TEMPLATES_DIR, 'nat_based_network.xml.j2')
    ISOLATED_NETWORK_J2 = os.path.join(NETWORK_TEMPLATES_DIR, 'isolated_network.xml.j2')
    
    ALREADY_EXISTS = 'already exists'
    NETWORK_NOT_FOUND = 'Network not found'
    
    # Initialize LibVirtNetworkUtil
    def __init__(self, uri):
        # Create Jinja2 Environment. Set the templates directory relative to this class module path.
        self.env = Environment(loader=PackageLoader(__name__, self.TEMPLATES_DIR))
        self.conn = libvirt.open(uri)

    # Release resources on object deletion
    def __del__(self):
        self.conn.close()

    # Create Pool
    def create_network(self, network):
        try:
            network_xml = None
            
            if (not isinstance(network, Network)):
                raise ExNotANetwork(type(network).__name__)
            elif (isinstance(network, NatBasedIPv4Network)):
                template = self.env.get_template(self.NAT_BASED_NETWORK_J2)
                network_xml = template.render(net_name=network.name, net_ip=network.ip, net_netmask=network.netmask, net_dhcp_start=network.dhcp_start, net_dhcp_end=network.dhcp_end)
            elif (isinstance(network, IsolatedNetwork)):
                template = self.env.get_template(self.ISOLATED_NETWORK_J2)
                network_xml = template.render(name=network.name)
            else:
                raise ExUnsupportedNetwork(type(network).__name__)
            
            self.conn.networkCreateXML(network_xml)
        except libvirtError as e:
            if (self.ALREADY_EXISTS in e.get_error_message()):
                raise ExNetworkExists(network.name)
            else:
                raise e
    
    # Delete Pool
    def delete_network(self, network_name):
        # Check if Pool exists
        try:
            network = self.conn.networkLookupByName(network_name)
            network.destroy()
        except libvirtError as e:
            if (self.NETWORK_NOT_FOUND in e.get_error_message()):
                raise ExNetworkNotFound(network_name)
            else:
                raise e
