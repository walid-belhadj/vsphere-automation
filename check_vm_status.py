import getpass
import requests
import urllib3
from vmware.vapi.vsphere.client import create_vsphere_client
from vcenter.helper.vm_helper import get_vm
from common.sample_util import pp
from com.vmware.vcenter.vm_client import Power

session = requests.session()
session.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
pwd = getpass.getpass("Enter Password: ")
client = create_vsphere_client(server='ip-server',
                               username='username',
                               password=pwd,
                               session=session)
vm = client.vcenter.VM.list(client.vcenter.VM.FilterSpec(names={'VGR-VM-micro-cloned'}))[0]
print(vm)
#check general state
name_vm = input('Enter the VM you want to check status: ')
vm = get_vm(client, name_vm)
if not vm:
    raise Exception('Sample requires an existing vm with name ({}). '
                        'Please create the vm first. ')
# Get the vm power state
status = client.vcenter.vm.Power.get(vm)
print("\n")
print('(vm.Power.get({}) -> {}'.format(vm, pp(status)))

#Poweron a machine
name_vm = input('Enter the VM you want to power on: ')
print("\n")
vm = get_vm(client, name_vm)
status = client.vcenter.vm.Power.get(vm)

if status == Power.Info(state=Power.State.POWERED_ON):
    print("The VM is already powered on...")
else:
    client.vcenter.vm.Power.start(vm)
    print("The VM started succefully ! ")

#Poweroff a machine
name_vm = input('Enter the VM you want to power off: ')
print("\n")
vm = get_vm(client, name_vm)
status = client.vcenter.vm.Power.get(vm)

if status==Power.Info(state=Power.State.POWERED_OFF):
    print("The VM is already powered off...")
else:
    client.vcenter.vm.Power.stop(vm)
    print("The VM stoped succefully ! ")

#Reset a machine
print("Reminder : You could only reset a VM which is powered on ")
name_vm = input('Enter the VM you want to reset: ')

vm = get_vm(client, name_vm)
status = client.vcenter.vm.Power.get(vm)

if status == (Power.Info(state=Power.State.POWERED_OFF) or Power.Info(state=Power.State.SUSPENDED) ):
    print("Virtual machine that is powered off or suspended cannot be reset.")
else:
     client.vcenter.vm.Power.reset(vm)
     print("VM reset succefully ! ")

#suspend a machine
print("Reminder: you can suspend a VM only if it is powered on  ")
name_vm = input('Enter the VM you want to suspend: ')

vm = get_vm(client, name_vm)
status = client.vcenter.vm.Power.get(vm)

if status == Power.Info(state=Power.State.POWERED_ON):
    client.vcenter.vm.Power.suspend(vm)
    print("VM suspended succefully ! ")
"""
# delete a vm

name_vm = input('Enter the VM you want to delete: ')

vm = get_vm(client, name_vm)
if not vm:
    raise Exception('Sample requires an existing vm with name ({}). '
                        'Please create the vm first. ')
else:
    client.vcenter.VM.delete(vm)
    print("VM deleted succefully ! ")
"""








"""
# Power on the vm
print('# Example: Power on the vm')
client.vcenter.vm.Power.start(vm)
print('vm.Power.start({})'.format(vm))

# Power off the vm if it is on
if status == Power.Info(state=Power.State.POWERED_ON):
    print('\n# Example: VM is powered on, power it off')
    client.vcenter.vm.Power.stop(vm)
    print('vm.Power.stop({})'.format(vm))




vm = client.vcenter.VM.list(client.vcenter.VM.FilterSpec(
        names={'10.20.6.77-xyz.tomcat.xyz-common-main.01.sit'}))[0]
client.vcenter.vm.Power.get(vm.vm)
client.vcenter.vm.Power.stop(vm.vm)

get_vm = input("Enter the name if your VM: ")

vm = client.vcenter.VM.list(client.vcenter.VM.FilterSpec(
        names={get_vm}))[0]
if vm.vm.status == Power.Info(state=Power.State.POWERED_OFF, clean_power_off=True):
    print('VM is powered off')
"""
