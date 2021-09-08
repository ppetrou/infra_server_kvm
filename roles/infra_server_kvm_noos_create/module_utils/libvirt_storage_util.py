# libvirt_storage - Utility Class for the LibVirt Pool/Volume API Python Bindings

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

from jinja2 import Template, Environment, PackageLoader
from libvirt import virStorageVol, virStoragePool, libvirtError

# Storage Classes
class Pool:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __str__(self):
        str_repr = "NAME: " + self.name + "\t" + \
                   "PATH: " + self.path

        return str_repr

class Volume:
    def __init__(self, name, extension, unit, size):
        self.name = name
        self.extension = extension
        self.unit = unit
        self.size = size

    def __str__(self):
        str_repr = "NAME: " + self.name + "\t" + \
                   "EXTENSION: " + self.extension + "\t" + \
                   "UNIT: " + self.unit + "\t" + \
                   "SIZE: " + str(self.size)

        return str_repr

# Exceptions
class ExStoragePoolNotFound(Exception):
    ERR_STORAGE_POOL_NOT_FOUND = "Storage Pool {0} not found."

    def __init__(self, pool_name):
        message = self.ERR_STORAGE_POOL_NOT_FOUND.format(pool_name)
        super().__init__(message)

class ExStorageVolumeNotFound(Exception):
    ERR_STORAGE_POOL_NOT_FOUND = "Storage Volume {0} not found."

    def __init__(self, volume_name):
        message = self.ERR_STORAGE_POOL_NOT_FOUND.format(volume_name)
        super().__init__(message)
        
class ExStoragePoolExists(Exception):
    ERR_STORAGE_POOL_EXISTS = "Storage Pool {0} exists."
    
    def __init__(self, pool_name):
        message = self.ERR_STORAGE_POOL_EXISTS.format(pool_name)
        super().__init__(message)

class ExStorageVolumeExists(Exception):
    ERR_STORAGE_VOLUME_EXISTS = "Storage Volume {0} exists."
    
    def __init__(self, volume_name):
        message = self.ERR_STORAGE_VOLUME_EXISTS.format(volume_name)
        super().__init__(message)

# Libvirt Storage Utility Class
class LibVirtStorageUtil:
    
    FILETYPE_POOL_J2 = """
         <pool type="dir">
           <name>{{ pool_name }}</name>
             <target>
               <path>{{ pool_path }}</path>
             </target>
         </pool>
    """
    
    VOLUME_J2 = """
         <volume>
           <name>{{ volume_name }}.{{ volume_extension }}</name>
           <allocation>0</allocation>
           <capacity unit="{{volume_unit}}">{{ volume_size }}</capacity>
         </volume>
    """
    
    ALREADY_EXISTS = 'already exists'
    POOL_NOT_FOUND = 'pool not found'
    VOLUME_NOT_FOUND = 'volume not found'
    
    # Initialize LibVirtStorageUtil
    def __init__(self, uri):
        self.conn = libvirt.open(uri)

    # Release resources on object deletion
    def __del__(self):
        self.conn.close()

    # Create Pool
    def create_pool(self, pool):
        try:
            template = Template(self.FILETYPE_POOL_J2)
            pool_xml = template.render(pool_name=pool.name, pool_path=pool.path)
            self.conn.storagePoolCreateXML(pool_xml)
        except libvirtError as e:
            if (self.ALREADY_EXISTS in e.get_error_message()):
                raise ExStoragePoolExists(pool.name)
            else:
                raise e
    
    # Delete Pool
    def delete_pool(self, pool_name):
        # Check if Pool exists
        try:
            pool = self.conn.storagePoolLookupByName(pool_name)
            pool.destroy()
        except libvirtError as e:
            if (self.POOL_NOT_FOUND in e.get_error_message()):
                raise ExStoragePoolNotFound(pool_name)
            else:
                raise e

    # Create Volume
    def create_volume(self, pool_name, volume):
        # Create Volume XML
        template = Template(self.VOLUME_J2)
        volume_xml = template.render(volume_name=volume.name, volume_extension=volume.extension, volume_unit=volume.unit, volume_size=volume.size)
        
        try:
            # Check if Pool exists
            pool = self.conn.storagePoolLookupByName(pool_name)
            if (pool == None):
                raise ExStoragePoolNotFound(pool_name)
            else:
                # Pool exists, create the volume
                pool.createXML(volume_xml)
        except libvirtError as e:
            if (self.ALREADY_EXISTS in e.get_error_message()):
                raise ExStorageVolumeExists(volume.name)
            else:
                raise e
    
    # Delete Volume
    def delete_volume(self, pool_name, volume_name):
        # Check if Pool exists
        try:
            pool = self.conn.storagePoolLookupByName(pool_name)
            volume = pool.storageVolLookupByName(volume_name)
            volume.delete()
        except libvirtError as e:
            if (self.POOl_NOT_FOUND in e.get_error_message()):
                raise ExStoragePoolNotFound(pool_name)
            elif (self.VOLUME_NOT_FOUND in e.get_error_message()):
                raise ExStorageVolumeNotFound(volume_name)
            else:
                raise e 

