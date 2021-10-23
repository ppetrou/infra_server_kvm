from string import *

import guestfs
import math
import sys

class PartitionInfo:
    def __init__(self, num, partition, sector_start, sector_end, size, unit):
        self.num = num
        self.partition = partition
        self.sector_start = sector_start
        self.sector_end = sector_end
        self.size = size
        self.unit = unit

    def __str__(self):
        str_repr = "NUM: " + str(self.num) + "\t" + \
                   "PARTITION: " + self.partition + "\t" + \
                   "SECTOR_START: " + str(self.sector_start) + "\t" + \
                   "SECTOR_END: " + str(self.sector_end) + "\t" + \
                   "SIZE: " + str(self.size) + "\t" + \
                   "UNIT: " + self.unit

        return str_repr

class PartitionInfoList:
    def __init__(self, device, sector_size, gfs_part_list):
        self.num_of_partitions = len(gfs_part_list)
        self.partitions = []

        for p in gfs_part_list:
            part_num = p.get("part_num")
            part_name = device + str(part_num)
            sector_start = math.ceil(p.get("part_start") / sector_size)
            sector_end = math.floor(p.get("part_end") / sector_size)
            size = p.get("part_size")
            unit = "Byte"

            p_info = PartitionInfo(part_num, part_name, sector_start, sector_end, size, unit)
            self.partitions.append(p_info)

    def __str__(self):
        str_rep = "NUM OF PARTITIONS: " + str(self.num_of_partitions) + "\n"
        for p in self.partitions:
            str_rep = str_rep + str(p) + "\n"

        return str_rep

class FileSystemInfo:
    def __init__(self, filesystem, fstype):
        self.filesystem = filesystem
        self.fstype = fstype

    def __str__(self):
        str_repr = "FILESYSTEM: " + str(self.filesystem) + "\t" + \
                   "FSTYPE: " + self.fstype

        return str_repr

class FileSystemInfoList:
    def __init__(self, gfs_filesystem_list):
        self.num_of_filesystens = len(gfs_filesystem_list)
        self.filesystems = []

        for fs in gfs_filesystem_list:
            filesystem = fs.strip()
            fstype = gfs_filesystem_list[fs].strip()

            fs_info = FileSystemInfo(filesystem, fstype)
            self.filesystems.append(fs_info)

    def __str__(self):
        str_rep = "NUM OF FILESYSTEMS: " + str(self.num_of_filesystens) + "\n"
        for fs in self.filesystems:
            str_rep = str_rep + str(fs) + "\n"

        return str_rep

class PartitionListResult:
    def __init__(self, code, description, partition_info_list = None):
        self.code = code
        self.description = description
        self.partition_info_list = partition_info_list

    def __str__(self):
        str_rep = "CODE: " + str(self.code) + "\t" + "DESCRIPTION: " + self.description + "\n" + str(self.partition_info_list)
        return str_rep

class PartitionAddResult:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        str_rep = "CODE: " + str(self.code) + "\t" + "DESCRIPTION: " + self.description
        return str_rep

class PartitionDelResult:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        str_rep = "CODE: " + str(self.code) + "\t" + "DESCRIPTION: " + self.description
        return str_rep

class PartitionResizeResult:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        str_rep = "CODE: " + str(self.code) + "\t" + "DESCRIPTION: " + self.description
        return str_rep

class VGAddResult:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        str_rep = "CODE: " + str(self.code) + "\t" + "DESCRIPTION: " + self.description
        return str_rep

class VGDelResult:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        str_rep = "CODE: " + str(self.code) + "\t" + "DESCRIPTION: " + self.description
        return str_rep

class LVAddResult:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        str_rep = "CODE: " + str(self.code) + "\t" + "DESCRIPTION: " + self.description
        return str_rep

class LVDelResult:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        str_rep = "CODE: " + str(self.code) + "\t" + "DESCRIPTION: " + self.description
        return str_rep

class FSCreateResult:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        str_rep = "CODE: " + str(self.code) + "\t" + "DESCRIPTION: " + self.description
        return str_rep

class FSDelResult:
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        str_rep = "CODE: " + str(self.code) + "\t" + "DESCRIPTION: " + self.description
        return str_rep

class ExInvalidStorageType(Exception):
    ERR_INVALID_STORAGE_TYPE = "{0} is not a supported storage unit type."

    def __init__(self, unit):
        message = self.ERR_INVALID_STORAGE_TYPE.format(unit)
        super(Exception, self).__init__(message)

class ExPartitionListError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class ExPartitionAddError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class ExPartitionDoesNotExistError(Exception):
    ERR_PARTITION_DOES_NOT_EXIST = "Partition {0} does not exist"

    def __init__(self, partition):
        message = self.ERR_PARTITION_DOES_NOT_EXIST.format(partition)
        super(Exception, self).__init__(message)

class ExPartitionExistsError(Exception):
    ERR_PARTITION_EXISTS = "Partition {0} exists"

    def __init__(self, partition):
        message = self.ERR_PARTITION_EXISTS.format(partition)
        super(Exception, self).__init__(message)

class ExPartitionDelError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class ExPartitionResizeError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class ExUnrecognizedDiskLabelError(Exception):
    ERR_UNRECOGNIZED_DISK_LABEL_ERROR = "Device {0} does not have a partition table."

    def __init__(self, device):
        message = self.ERR_UNRECOGNIZED_DISK_LABEL_ERROR.format(device)
        super(Exception, self).__init__(message)

class ExVolumeGroupAddError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class ExVolumeGroupDelError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class ExVolumeGroupDoesNotExistError(Exception):
    ERR_VG_DOES_NOT_EXIST = "VG {0} does not exist"

    def __init__(self, partition):
        message = self.ERR_VG_DOES_NOT_EXIST.format(partition)
        super(Exception, self).__init__(message)

class ExVolumeGroupExistsError(Exception):
    ERR_VG_EXISTS = "VG {0} exists"

    def __init__(self, partition):
        message = self.ERR_VG_EXISTS.format(partition)
        super(Exception, self).__init__(message)

class ExLogicalVolumeAddError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class ExLogicalVolumeDelError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class ExLogicalVolumeDoesNotExistError(Exception):
    ERR_LV_DOES_NOT_EXIST = "LV {0} does not exist"

    def __init__(self, partition):
        message = self.ERR_LV_DOES_NOT_EXIST.format(partition)
        super(Exception, self).__init__(message)

class ExLogicalVolumeExistsError(Exception):
    ERR_LV_EXISTS = "LV {0} exists"

    def __init__(self, partition):
        message = self.ERR_LV_EXISTS.format(partition)
        super(Exception, self).__init__(message)

class ExFilesystemExistsError(Exception):
    ERR_FS_EXISTS = "FS {0} exists"

    def __init__(self, fs):
        message = self.ERR_FS_EXISTS.format(fs)
        super(Exception, self).__init__(message)

class ExFilesystemDoesNotExistError(Exception):
    ERR_FS_DOES_NOT_EXIST = "FS {0} does not exist"

    def __init__(self, fs):
        message = self.ERR_FS_DOES_NOT_EXIST.format(fs)
        super(Exception, self).__init__(message)

class ExDeviceDoesNotExistError(Exception):
    ERR_DEV_DOES_NOT_EXIST = "Device {0} does not exist"

    def __init__(self, dev):
        message = self.ERR_DEV_DOES_NOT_EXIST.format(dev)
        super(Exception, self).__init__(message)

class ExFilesystemCreateError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class ExFilesystemDelError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class ExFilesystemResizeError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class ExCannotListFilesystemsError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)

class ExMountDirExistError(Exception):
    ERR_MOUNTDIR_EXISTS = "Mountpoint {0} exists."

    def __init__(self, mountpoint):
        message = self.ERR_MOUNTDIR_EXISTS.format(mountpoint)
        super(Exception, self).__init__(message)

class GFSLibUtil:

    # Initialize GFSUtil
    def __init__(self, cloud_image_paths):
        self.cloud_image_paths = cloud_image_paths
        self.gfs = guestfs.GuestFS(python_return_dict = True)
        self.num_of_cloud_images = len(cloud_image_paths)
        for cloud_image_path in cloud_image_paths:
            self.gfs.add_drive_opts(cloud_image_path, format = "qcow2", readonly = 0)
        self.gfs.launch()

    # Release resources on object deletion
    def __del__(self):
        self.gfs.close()

    # Get Sector Size
    def get_sector_size(self, device):
        # Set Cloud Image device
        cloud_device_name = self.convert_device_to_cloud_device(device, False)

        # Get the sector size
        sector_size = self.gfs.blockdev_getss(cloud_device_name)
        return sector_size

    # Convert Virtual Disk Device to Cloud Image device
    # The device parameter is in the naming conventions of Virtual Disk e.g. /dev/vda
    # Guestfish mounts the image as a separate partition and the naming changes to /dev/sda so we need to transform the value.
    def convert_device_to_cloud_device(self, device, is_part):
        if self.num_of_cloud_images == 1:
            if is_part:
                cloud_device_name = "/dev/" + device.replace("v", "s", 1)
            else:
                cloud_device_name = "/dev/sda"
        else:
            cloud_device_name = "/dev/" + device.replace("v", "s", 1)

        return cloud_device_name

    # Convert a vol group and logical volume to a device name
    # e.g. lv00 and vg00 = /dev/vg00/lv00
    def convert_lv_vg_to_device(self, lv, vg):
        lv_device = "/dev/" + vg + "/" + lv
        return lv_device

    # Convert Storage Units to Bytes
    # TODO Check for ArithmeticError in the size
    def convert_storage_units_to_bytes(self, size, unit):
        bytes = 0
        if unit == "Byte":
            bytes = size
        elif unit == "KiB":
            bytes = size * 1024
        elif unit == "MiB":
            bytes = size * (1024 *1024)
        elif unit == "GiB":
            bytes = size * (1024 * 1024 * 1024)
        else:
            raise ExInvalidStorageType(unit)

        return bytes

    # Convert Storage Units to MebiBytes
    # TODO Check for ArithmeticError in the size
    def convert_storage_units_to_mebibytes(self, size, unit):
        mibs = 0
        if unit == "Byte":
            mibs = size / 1024 / 1024
        elif unit == "KiB":
            mibs = size / 1024
        elif unit == "MiB":
            mibs = size
        elif unit == "GiB":
            mibs = size * 1024
        else:
            raise ExInvalidStorageType(unit)

        return mibs

    # List Partitions
    def list_partitions(self, device):
        try:
            # Set Cloud Image device
            cloud_device_name = self.convert_device_to_cloud_device(device, False)

            # Get the sector Size
            sector_size = self.get_sector_size(device)

            # List the partitions
            partition_list = self.gfs.part_list(cloud_device_name)

            # Create and return the result object
            partition_info_list = PartitionInfoList(device, sector_size, partition_list)
            return partition_info_list

        except Exception as ex:
            if 'unrecognised disk label' in str(ex):
                raise ExUnrecognizedDiskLabelError(device)
            else:
                raise ExPartitionListError(ex)

    def get_partition_type(self, device):
        try:
            cloud_device_name = self.convert_device_to_cloud_device(device, False)
            part_type = self.gfs.part_get_parttype(cloud_device_name)
            return part_type
        except Exception as ex:
            raise

    def initialize_partition_table(self, device, partition_type):
        cloud_device_name = self.convert_device_to_cloud_device(device, False)
        self.gfs.part_init(cloud_device_name, partition_type)

    def list_filesystems(self):
        try:
            filesystem_list = self.gfs.list_filesystems()

            fs_info_list = FileSystemInfoList(filesystem_list)

            return fs_info_list
        except Exception as ex:
            raise ExCannotListFilesystemsError(ex)

    # Add Partition
    def add_partition(self, device, size, unit):
        try:
            # Set Cloud Image device
            cloud_device_name = self.convert_device_to_cloud_device(device, False)

            # Get the sector Size
            sector_size = self.get_sector_size(device)

            # Get existing partitions
            existing_partitions = self.list_partitions(device)

            # Initialize sector vars
            start_sector_of_new_partition = 0
            last_sector_of_new_partition = 0

            # Check if disk has any partitions to set the correct start sector
            if existing_partitions.num_of_partitions == 0:
                # Set start sector to 1
                start_sector_of_new_partition = 1
                # Calculate last sector
                last_sector_of_new_partition = math.ceil(self.convert_storage_units_to_bytes(size, unit) / sector_size)
            else:
                # Get end sector of last partition
                last_sector_of_last_partition = existing_partitions.partitions[-1].sector_end
                # Add 1 sector to create the new start position
                start_sector_of_new_partition = last_sector_of_last_partition + 1
                # Calculate last sector
                last_sector_of_new_partition = start_sector_of_new_partition + math.ceil(self.convert_storage_units_to_bytes(size, unit) / sector_size)

            # Create new partition
            # TODO parameterize on partition type prlogex
            self.gfs.part_add(cloud_device_name, "p", start_sector_of_new_partition, last_sector_of_new_partition)
            # TODO Add created partition info in the result type
            return PartitionAddResult(0,"OK")
        except ExUnrecognizedDiskLabelError as ex_disk_label_error:
            raise
        except ExPartitionListError as ex_part_list:
            raise
        except Exception as ex:
            raise ExPartitionAddError(ex)

    def delete_partition(self, device, partition_num):
        try:
            # Get existing partitions
            existing_partitions = self.list_partitions(device)

            # Set Cloud Image device
            cloud_device_name = self.convert_device_to_cloud_device(device, False)

            partition_exists = False
            # Check if partition number exists
            for p in existing_partitions.partitions:
                if p.num == partition_num:
                    partition_exists = True
                    break
                else:
                    partition_exists = False

            if partition_exists:
                self.gfs.part_del(cloud_device_name, partition_num)
                # TODO Do we need any more information in the result type of the delete operation
                return PartitionDelResult(0,"OK")
            else:
                raise ExPartitionDoesNotExistError(partitionExMountDirExistError_num)
        # TODO Do we need to raise the ExPartitionListError or wrap it in an ExPartitionDelError
        except ExPartitionListError as ex_part_list:
            raise
        except ExPartitionDoesNotExistError as ex_part_not_exists:
            raise
        except Exception as ex:
            raise ExPartitionDelError(ex)

    # Resize Partition
    def resize_partition(self, device, partition_num, size, unit):
        try:
            # Set Cloud Image device
            cloud_device_name = self.convert_device_to_cloud_device(device, False)

            # Get the sector Size
            sector_size = self.get_sector_size(device)

            # Get existing partitions
            existing_partitions = self.list_partitions(device)
            last_sector_of_partition_to_resized = 0
            partition_size = 0
            partition_unit = None

            # Get end sector of the partition to resize
            for p in existing_partitions.partitions:
                if p.num == partition_num:
                    partition_exists = True
                    last_sector_of_partition_to_resized = p.sector_end
                    partition_size = p.size
                    partition_unit = p.unit
                    break
                else:
                    partition_exists = False

            if partition_exists:
                
                # Convert size in Bytes
                new_size_in_bytes = self.convert_storage_units_to_bytes(size, unit)
                # Calculate the extra space to add to partition
                current_size_in_bytes = self.convert_storage_units_to_bytes(partition_size, partition_unit)
                extra_space_in_bytes_needed = new_size_in_bytes - current_size_in_bytes

                # Calculate Sector for the new size
                new_size_in_sectors = extra_space_in_bytes_needed / sector_size
                # Calculate new end sector
                new_end_sector = math.ceil(last_sector_of_partition_to_resized + new_size_in_sectors)

                # Resize Partition
                self.gfs.part_resize(cloud_device_name, partition_num, new_end_sector)
                return PartitionDelResult(0,"OK")
            else:
                raise ExPartitionDoesNotExistError(partition_num)

            # TODO Add resized partition info in the result type
            return PartitionResizeResult(0,"OK")
        except ExPartitionListError as ex_part_list:
            raise
        except ExPartitionDoesNotExistError as ex_part_not_exists:
            raise
        except Exception as ex:
            raise ExPartitionResizeError(ex)

    # Add Volume Group
    def add_vg(self, vg, pvs):
        try:
            # Convert pvs to cloud notation. Guestfish uses /dev/sd* rather than /dev/vd*
            cloud_pvs = []
            for pv in pvs:
                cloud_pv = self.convert_device_to_cloud_device(pv, True)
                cloud_pvs.append(cloud_pv)

            self.gfs.vgcreate(vg, cloud_pvs)
            # TODO return more info
            return VGAddResult(0, "OK")
        except Exception as ex:
            if 'already exists' in str(ex):
                raise ExVolumeGroupExistsError(vg)
            else:
                raise ExVolumeGroupAddError(ex)

    # Delete Volume Group
    def delete_vg(self, vg):
        try:
            self.gfs.vgremove(vg)
            # TODO return more info
            return VGDelResult(0, "OK")
        except Exception as ex:
            if 'not found' in str(ex):
                raise ExVolumeGroupDoesNotExistError(vg)
            else:
                raise ExVolumeGroupDelError(ex)

    # Add Logical Volume
    def add_lv(self, lv, vg, size, unit):
        try:
            size_in_mibs = self.convert_storage_units_to_mebibytes(size, unit)
            self.gfs.lvcreate(lv, vg, size_in_mibs)
            # TODO return more info
            return LVAddResult(0, "OK")
        except Exception as ex:
            if 'already exists' in str(ex):
                raise ExLogicalVolumeExistsError(vg)
            else:
                raise ExLogicalVolumeAddError(ex)

    # Delete Logical Volume
    def delete_lv(self, lv, vg):
        try:
            lv_device = self.convert_lv_vg_to_device(lv, lg)
            self.gfs.lvremove(lv_device)
            # TODO return more info
            return LVDelResult(0, "OK")
        except Exception as ex:
            if 'not found' in str(ex):
                raise ExLogicalVolumeDoesNotExistError(vg)
            else:
                raise ExLogicalVolumeDelError(ex)

    # Create Filesystem
    def create_fs(self, device, device_type, fstype, force, use_image_mkfs_xfs, mountpoint):
        try:
            cloud_device = ""

            if device_type == 'standard':
                cloud_device = self.convert_device_to_cloud_device(device, True)
            else:
                # LVM Device
                cloud_device = "/dev/" + device

            if force:
                self.gfs.wipefs(cloud_device)

            # Get the filesystems
            fs_info_list = self.list_filesystems()

            # Check if filesystem exists
            for fs_info in fs_info_list.filesystems:
                if fs_info.filesystem == cloud_device and fs_info.fstype != 'unknown':
                    raise ExFilesystemExistsError(cloud_device)

            if fstype == 'swap':
                self.gfs.mkswap(cloud_device)
                self.gfs.swapon_device(cloud_device)
            else:
                # Hack. GuestFS uses the native xfs binary which can be different from the Guest Image one and cause incompatibilities
                # If this is the case use sh and the cloud image binary
                if use_image_mkfs_xfs:
                    self.gfs.mount("/dev/sda1","/")
                    mkfs_xfs_cmd = "mkfs.xfs " + cloud_device
                    self.gfs.sh(mkfs_xfs_cmd)
                    self.gfs.umount("/")
                else:
                    self.gfs.mkfs(fstype, cloud_device)

            # Mount the filesystem
            fs_freq = ""
            fs_passno = ""
            fs_mntops = ""
            fstab_device = "/dev/" + device

            # Mount root filesystem of the cloud image
            self.gfs.mount("/dev/sda1","/")

            if fstype == 'swap':
                fs_freq = "0"
                fs_passno = "0"
                fs_mntops = "defaults"
            else:
                fs_freq = "1"
                fs_passno = "2"
                fs_mntops = "defaults"

                # Create the mountpoint
                self.gfs.mkdir(mountpoint)

            # Add fstab entry
            self.gfs.write_append("/etc/fstab", "{0}\t{1}\t{2}\t{3}\t{4} {5}\n".format(fstab_device, mountpoint, fstype, fs_mntops, fs_freq, fs_passno))
            # Unmount root filesystem
            self.gfs.umount("/")

            result = FSCreateResult(0,"OK")
            return result

        except ExFilesystemExistsError as ex_fs_exists_er:
            raise
        except Exception as ex:
            if 'expecting a device name' in str(ex):
                raise ExDeviceDoesNotExistError(device)
            elif 'File exists' in str(ex):
                raise ExMountDirExistError(mountpoint)
            else:
                raise ExFilesystemCreateError(ex)

    # Delete Filesystem
    def delete_fs(self, device, device_type):
        try:
            cloud_device = ""

            if device_type == 'standard':
                cloud_device = self.convert_device_to_cloud_device(device, True)
            else:
                cloud_device = device

            # Get the filesystems
            fs_info_list = self.list_filesystems()

            # Check if filesystem exists
            for fs_info in fs_info_list.filesystems:
                if fs_info.filesystem == cloud_device and fs_info.fstype == 'unknown':
                    raise ExFilesystemDoesNotExistError(cloud_device)

            self.gfs.wipefs(cloud_device)

            result = FSDelResult(0,"OK")
            return result

        except ExFilesystemDoesNotExistError as ex_fs_does_not_exist_er:
            raise
        except Exception as ex:
            if 'expecting a device name' in str(ex):
                raise ExDeviceDoesNotExistError(device)
            else:
                raise ExFilesystemDelError(ex)
    
     # Resize Filesystem
    def resize_fs(self, device, device_type, fstype, use_image_mkfs_xfs, mountpoint):
        try:
            cloud_device = ""

            if device_type == 'standard':
                cloud_device = self.convert_device_to_cloud_device(device, True)
            else:
                # LVM Device
                cloud_device = "/dev/" + device

            # Get the filesystems
            fs_info_list = self.list_filesystems()

            # Check if filesystem exists
            for fs_info in fs_info_list.filesystems:
                if fs_info.filesystem == cloud_device and fs_info.fstype == 'unknown':
                    raise ExFilesystemDoesNotExistError(cloud_device)

            self.gfs.mount(cloud_device, mountpoint)
            if fstype == "xfs":
                if use_image_mkfs_xfs:
                    mkfs_xfs_cmd = "xfs_growfs " + mountpoint
                    self.gfs.sh(mkfs_xfs_cmd)                   
                else:
                    self.gfs.xfs_growfs(mountpoint)
            else:
                self.gfs.resize2fs(mountpoint)

            self.gfs.umount(mountpoint)

            result = FSCreateResult(0,"OK")
            return result

        except ExFilesystemDoesNotExistError as ex_fs_exists_er:
            raise
        except Exception as ex:
            if 'expecting a device name' in str(ex):
                raise ExDeviceDoesNotExistError(device)
            elif 'File exists' in str(ex):
                raise ExMountDirExistError(mountpoint)
            else:
                raise ExFilesystemResizeError(ex)


def main():
    tryme()

def tryme():
    print("Enter operation: \n 1. List \n 2. Add \n 3. Delete \n 4. Resize \n 5. Init Partition Table \n 6. Create VG One Disk \n 7. Create VG Two Disks \n 8. Delete VG \n 9. Create FS \n 10. Delete FS \n 11. Resize FS \n")
    type = int(input())

    gfs_util = GFSLibUtil(["/kvm/large_vda.qcow2"])
    part = "vdb"
    part_add_num = 2

    if type == 1:
        parts = gfs_util.list_partitions(part)
        print(parts)

    if type == 2:
        result = gfs_util.add_partition(part,part_add_num,"GiB")
        print(result)

    if type == 3:
        result = gfs_util.delete_partition(part, 2)
        print(result)

    if type == 4:
        result = gfs_util.resize_partition(part, 1, 16, "GiB")
        print(result)

    if type == 5:
        result = gfs_util.initialize_partition_table(part, "mbr")
        print(result)

    if type == 6:
        result = gfs_util.add_vg("vg00", ['vda2'])
        print(result)

    if type == 7:
        result = gfs_util.add_vg("vg01", ['vda3','vdb1'])
        print(result)

    if type == 8:
        result = gfs_util.delete_vg("vg00")
        print(result)

    if type == 9:
        result = gfs_util.create_fs("vda3", "standard", "xfs", False, True)
        print(result)

    if type == 10:
        result = gfs_util.delete_fs("vda3", "standard")
        print(result)
    
    if type == 11:
        result = gfs_util.resize_fs("vda1", "standard", "xfs", False, "/")
        print(result)


if __name__ == '__main__':
    main()
