# libvirt_snapshot - Utility Class for the LibVirt Snapshot API Python Bindings

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

from jinja2 import Template
from libvirt import virDomainSnapshot

class Snapshot:
    def __init__(self, name, description, domain):
        self.name = name
        self.description = description
        self.domain = domain

    def __str__(self):
        str_repr = "NAME: " + str(self.name) + "\t" + \
                   "DESCRIPTION: " + self.description + "\t" + \
                   "DOMAIN: " + str(self.domain)

        return str_repr

class LibVirtSnapshotUtil:
    
    SNAPSHOT_XML = Template("<domainsnapshot><name>{{ snapshot_name }}</name><description>{{ snapshot_description }}</description></domainsnapshot>")

    # Initialize LibVirtSnapshotUtil
    def __init__(self, uri):
        self.conn = libvirt.open(uri)

    # Release resources on object deletion
    def __del__(self):
        self.conn.close()

    # Create Snapshot
    def create_snapshot(self, snapshot):
        snapshotXml = self.SNAPSHOT_XML.render(snapshot_name=snapshot.name, snapshot_description=snapshot.description)
        dom0 = self.conn.lookupByName(snapshot.domain)
        dom0.snapshotCreateXML(snapshotXml, 0);
    
    # Delete Snapshot
    def delete_snapshot(self, snapshot):
        dom0 = self.conn.lookupByName(snapshot.domain)
        lookupSnapshot = dom0.snapshotLookupByName(snapshot.name, 0)
        lookupSnapshot.delete(0)       

def main():
    tryme()

def tryme():
    libvirtUtil = LibVirtSnapshotUtil("qemu:///system")
    snapshot = Snapshot("test00", "Test Description", "coredns")
    #libvirtUtil.create_snapshot(snapshot)
    libvirtUtil.delete_snapshot(snapshot)

if __name__ == '__main__':
    main()


# 
# try:
#     t = Template("Hello {{ something }}!")
#     x = t.render(something="World")
#     print(x)
# 
#     conn = libvirt.open("qemu:///system")
# except libvirt.libvirtError:
#     print('Failed to open connection to the hypervisor')
#     sys.exit(1)
# 
# try:
#     dom0 = conn.lookupByName("coredns")
#     
#     snapXML = "<domainsnapshot><name>test1</name><description>Libvirt Python API Test</description><disks><disk name='vda'></disk></disks></domainsnapshot>"
#     snapXML2 = "<domainsnapshot><name>test1</name><description>Libvirt Python API Test</description></domainsnapshot>"
#     dom0.snapshotCreateXML(snapXML2, 0)
#     
# except libvirt.libvirtError:
#     print('Failed to find the main domain')
#     sys.exit(1)
# 
# print("Domain 0: id %d running %s" % (dom0.ID(), dom0.OSType()))
# print(dom0.isActive())

