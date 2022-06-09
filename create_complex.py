#!/usr/bin/env python

__author__ = 'VMware, Inc.'
__vcenter_version__ = '6.5+'

import getpass

from com.vmware.vcenter.vm.hardware.boot_client import Device as BootDevice
from com.vmware.vcenter.vm.hardware_client import (
    Cpu, Memory, Disk, Ethernet, Cdrom, Serial, Parallel, Floppy, Boot)
from com.vmware.vcenter.vm.hardware_client import ScsiAddressSpec
from com.vmware.vcenter.vm_client import (Hardware, Power, GuestOS)
from com.vmware.vcenter_client import VM, Network
from vmware.vapi.vsphere.client import create_vsphere_client

from samples.vsphere.common.ssl_helper import get_unverified_session
from samples.vsphere.common import sample_cli
from samples.vsphere.common import sample_util
from samples.vsphere.common.sample_util import pp
from samples.vsphere.vcenter.helper import network_helper
from samples.vsphere.vcenter.helper import vm_placement_helper
from samples.vsphere.vcenter.helper.vm_helper import get_vm



class CreateExhaustiveVM(object):
    """
    Demonstrates how to create a exhaustive VM with the below configuration:
    3 disks, 2 nics, 2 vcpu, 2 GB, memory, boot=BIOS, 1 cdrom, 1 serial port,
    1 parallel port, 1 floppy, boot_device=[CDROM, DISK, ETHERNET])
    Sample Prerequisites:
        - datacenter
        - vm folder
        - resource pool
        - datastore
        - standard switch network
        - distributed switch network
        - An iso file on the datastore mentioned above
    """

    def __init__(self, client=None, placement_spec=None,
                 standard_network=None, distributed_network=None):
        self.client = client
        self.placement_spec = placement_spec
        self.standard_network = standard_network
        self.distributed_network = distributed_network
        self.vm_name = 'VM_NAME_EXHAUSTIVE'
        self.cleardata = None

        # Execute the sample in standalone mode.
        if not self.client:

            parser = sample_cli.build_arg_parser()
            parser.add_argument('-n', '--vm_name',
                                action='store',
                                help='Name of the testing vm')
            args = sample_util.process_cli_args(parser.parse_args())
            if args.vm_name:
                self.vm_name = args.vm_name
            self.cleardata = args.cleardata
            session = get_unverified_session() if args.skipverification else None
            self.client = create_vsphere_client(server=args.server,
                                                username=args.username,
                                                password=args.password,
                                                session=session)

    def run(self):
        # Get a placement spec

        datacenter_name = 'LAB-TOULOUSE'
        vm_folder_name = 'VGR-LAB-CISCO-ACI'
        datastore_name = 'FRTLS-LAB-P-ESX2 Datastore'
        std_portgroup_name = 'CNS.Paris.172.20.2'
        dv_portgroup_name = '25-LAB-TRAINING-SANDBOX'

        get_dc = input("Enter the datacenter name: ")
        get_folder = input("Enter the folder name: ")
        get_datastore = input("Enter the datastore name: ")
        get_sdr_prtgrp = input("Enter the portgroupname name (standard: CNS.Paris.172.20.2) : ")
        get_dst_prtgrp = input("Enter the distributedportgroup name: ")

        if not self.placement_spec:
            self.placement_spec = vm_placement_helper.get_placement_spec_for_resource_pool(
                self.client,
                get_dc, # datacenter_name
                get_folder, # vm_folder_name
                get_datastore) # datastore_name

        # Get a standard network backing
        if not self.standard_network:
            self.standard_network = network_helper.get_network_backing(
                self.client,
                get_sdr_prtgrp,
                get_dc,
                Network.Type.STANDARD_PORTGROUP)

        # Get a distributed network backing
        if not self.distributed_network:
            self.distributed_network = network_helper.get_network_backing(
                self.client,
                get_dst_prtgrp,
                get_dc,
                Network.Type.DISTRIBUTED_PORTGROUP)

        """
        Create an exhaustive VM.
        Using the provided PlacementSpec, create a VM with a selected Guest OS
        and provided name.
        Create a VM with the following configuration:
        * Hardware Version = VMX_11 (for 6.0)
        * CPU (count = 2, coresPerSocket = 2, hotAddEnabled = false,
        hotRemoveEnabled = false)
        * Memory (size_mib = 2 GB, hotAddEnabled = false)
        * 3 Disks and specify each of the HBAs and the unit numbers
          * (capacity=40 GB, name=<some value>, spaceEfficient=true)
        * Specify 2 ethernet adapters, one using a Standard Portgroup backing and
        the
          other using a DISTRIBUTED_PORTGROUP networking backing.
          * nic1: Specify Ethernet (macType=MANUAL, macAddress=<some value>)
          * nic2: Specify Ethernet (macType=GENERATED)
        * 1 CDROM (type=ISO_FILE, file="os.iso", startConnected=true)
        * 1 Serial Port (type=NETWORK_SERVER, file="tcp://localhost/16000",
        startConnected=true)
        * 1 Parallel Port (type=HOST_DEVICE, startConnected=false)
        * 1 Floppy Drive (type=CLIENT_DEVICE)
        * Boot, type=BIOS
        * BootDevice order: CDROM, DISK, ETHERNET
        Use guest and system provided defaults for remaining configuration settings.
        """

        iso_datastore_path = '[FRTLS-LAB-P-ESX2 Datastore]EVE.iso'
        serial_port_network_location ='SERIAL_PORT_NETWORK_SERVER_LOCATION'
        iso_path= input('Enter the path to the image (go to the right datastore and copy paste the full path to the image): ')
        nbr_cpu = input("Enter number of cpu: ")
        nbr_cores_per_socket =input("Enter number of cores per socket: ")
        print("Hot add/remove enabled by default...")

        GiB = 1024 * 1024 * 1024
        GiBMemory = 1024
        mem = input("Enter memory value (GigaBytes): ")
        print("Hot add/remove enabled by default...")
        disk_boot = input("Enter boot disk capacity (GigaBytes): ")
        disk_1 = input("Enter disk1 disk capacity (GigaBytes): ")
        disk_2 = input("Enter disk2 disk capacity (GigaBytes): ")
        print("Guestos deal by dfault (OTHER_3X_LINUX_64)")
        vm_create_spec = VM.CreateSpec(
            guest_os=GuestOS.OTHER_3X_LINUX_64,
            name=self.vm_name,
            placement=self.placement_spec,
            hardware_version=Hardware.Version.VMX_11,
            cpu=Cpu.UpdateSpec(count=int(nbr_cpu), #2
                               cores_per_socket=int(nbr_cores_per_socket), # 1
                               hot_add_enabled=True,
                               hot_remove_enabled=True),
            memory=Memory.UpdateSpec(size_mib=int(mem) * GiBMemory,
                                     hot_add_enabled=True),
            disks=[
                Disk.CreateSpec(type=Disk.HostBusAdapterType.SCSI,
                                scsi=ScsiAddressSpec(bus=0, unit=0),
                                new_vmdk=Disk.VmdkCreateSpec(name='boot',
                                                             capacity=int(disk_boot) * GiB)),
                Disk.CreateSpec(new_vmdk=Disk.VmdkCreateSpec(name='data1',
                                                             capacity=int(disk_1) * GiB)),
                Disk.CreateSpec(new_vmdk=Disk.VmdkCreateSpec(name='data2',
                                                             capacity=int(disk_2) * GiB))
            ],
            nics=[
                Ethernet.CreateSpec(
                    start_connected=True,
                    mac_type=Ethernet.MacAddressType.MANUAL,
                    mac_address='11:23:58:13:21:34',
                    backing=Ethernet.BackingSpec(
                        type=Ethernet.BackingType.STANDARD_PORTGROUP,
                        network=self.standard_network)),
                Ethernet.CreateSpec(
                    start_connected=True,
                    mac_type=Ethernet.MacAddressType.GENERATED,
                    backing=Ethernet.BackingSpec(
                        type=Ethernet.BackingType.DISTRIBUTED_PORTGROUP,
                        network=self.distributed_network)),
            ],
            cdroms=[
                Cdrom.CreateSpec(
                    start_connected=True,
                    backing=Cdrom.BackingSpec(type=Cdrom.BackingType.ISO_FILE,
                                              iso_file=iso_path) #  iso_datastore_path
                )
            ],
            serial_ports=[
                Serial.CreateSpec(
                    start_connected=False,
                    backing=Serial.BackingSpec(
                        type=Serial.BackingType.NETWORK_SERVER,
                        network_location=serial_port_network_location)
                )
            ],
            parallel_ports=[
                Parallel.CreateSpec(
                    start_connected=False,
                    backing=Parallel.BackingSpec(
                        type=Parallel.BackingType.HOST_DEVICE)
                )
            ],
            floppies=[
                Floppy.CreateSpec(
                    backing=Floppy.BackingSpec(
                        type=Floppy.BackingType.CLIENT_DEVICE)
                )
            ],
            boot=Boot.CreateSpec(type=Boot.Type.BIOS,
                                 delay=0,
                                 enter_setup_mode=False
                                 ),
            # TODO Should DISK be put before CDROM and ETHERNET?  Does the BIOS
            # automatically try the next device if the DISK is empty?
            boot_devices=[
                BootDevice.EntryCreateSpec(BootDevice.Type.CDROM),
                BootDevice.EntryCreateSpec(BootDevice.Type.DISK),
                BootDevice.EntryCreateSpec(BootDevice.Type.ETHERNET)
            ]
        )
        print(
            '# Example: create_exhaustive_vm: Creating a VM using specifications\n-----')
        print(pp(vm_create_spec))
        print('-----')

        vm = self.client.vcenter.VM.create(vm_create_spec)

        print("create_exhaustive_vm: Created VM '{}' ({})".format(self.vm_name,
                                                                  vm))

        vm_info = self.client.vcenter.VM.get(vm)
        print('vm.get({}) -> {}'.format(vm, pp(vm_info)))

        return vm

    def cleanup(self):
        vm = get_vm(self.client, self.vm_name)
        if vm:
            state = self.client.vcenter.vm.Power.get(vm)
            if state == Power.Info(state=Power.State.POWERED_ON):
                self.client.vcenter.vm.Power.stop(vm)
            elif state == Power.Info(state=Power.State.SUSPENDED):
                self.client.vcenter.vm.Power.start(vm)
                self.client.vcenter.vm.Power.stop(vm)
            print("Deleting VM '{}' ({})".format(self.vm_name, vm))
            self.client.vcenter.VM.delete(vm)


def main():
    create_exhaustive_vm = CreateExhaustiveVM()
    create_exhaustive_vm.cleanup()
    create_exhaustive_vm.run()
    if create_exhaustive_vm.cleardata:
        create_exhaustive_vm.cleanup()


if __name__ == '__main__':
    main()
