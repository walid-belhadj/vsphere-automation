import requests
import urllib3
import getpass
import json
from vmware.vapi.vsphere.client import create_vsphere_client #, Folder , Datacenter , Datastore ,  Host , Network,VM
from com.vmware.vcenter_client import (Cluster, Datastore, Folder, ResourcePool,
                                       VM)
session = requests.session()

# Disable cert verification for demo purpose.
# This is not recommended in a production environment.
session.verify = False

# Disable the secure connection warning for demo purpose.
# This is not recommended in a production environment.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

pwd = getpass.getpass("Enter your AD password : ")
vsphere_client = create_vsphere_client(
		server='ip-server',
		username='username',
		password=pwd,
		session=session)
print('\n')
print("Connecting to vCenter........ ")
print("-"*70)
print("Printing All VMs.......")

with open(f'vm_list.json', 'w') as outfile:
	for vm in vsphere_client.vcenter.VM.list():
		outfile.write("\n")
		outfile.write(str(json.dumps(vars(vm), indent=4)))
print("-"*70)
print("Printing All Networks........")
#chercher l'ensemble des vms

with open(f'network_list.json', 'w') as outfile:
	for network in vsphere_client.vcenter.Network.list():
		outfile.write("\n")
		outfile.write(str(json.dumps(vars(network), indent=4)))

print("-"*70)
print("Printing All Clusters........")

with open(f'cluster_list.json', 'w') as outfile:
	for cluster in vsphere_client.vcenter.Cluster.list():
		outfile.write("\n")
		outfile.write(str(json.dumps(vars(cluster), indent=4)))

print("-"*70)
print("Printing All Datastores........")

with open(f'datastore_list.json', 'w') as outfile:
	for datastore in vsphere_client.vcenter.Datastore.list():
		outfile.write("\n")
		outfile.write(str(json.dumps(vars(datastore), indent=4)))

print("-"*70)
print("Printing All Folders............")

with open(f'folder_list.json', 'w') as outfile:
	for folder in vsphere_client.vcenter.Folder.list():
		outfile.write("\n")
		outfile.write(str(json.dumps(vars(folder), indent=4)))

print("Printing All Hosts.......")

with open(f'host_list.json', 'w') as outfile:
	for host in vsphere_client.vcenter.Host.list():
		outfile.write("\n")
		outfile.write(str(json.dumps(vars(host), indent=4)))





