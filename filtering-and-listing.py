import json

import requests
import urllib3
from vmware.vapi.vsphere.client import create_vsphere_client
from com.vmware.vcenter_client import Cluster, Folder, VM, Datastore, Network, Host, ResourcePool

session = requests.session()

# Disable cert verification for demo purpose.
# This is not recommended in a production environment.
session.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


vsphere_client = create_vsphere_client(
		server='ip-server',
		username='username',
		password="password",
		session=session)

#vms=None, names=None, folders=None, datacenters=None, hosts=None, clusters=None, resource_pools=None, power_states=None
network_name = input("Enter a Network name: ")
network_id = vsphere_client.vcenter.Network.list(
        Network.FilterSpec(names={network_name},
                           types={Network.Type.DISTRIBUTED_PORTGROUP}))[0].network

filter = vsphere_client.vcenter.VM.list(vsphere_client.vcenter.VM.FilterSpec(networks={network_id}))
with open('vm_list_by_network.json', 'w') as outfile:
	for vm in filter:
		outfile.write("\n")
		outfile.write(str(json.dumps(vars(vm), indent=4)))


get_cluster = input("Enter a Cluster name: ")
cluster_id = vsphere_client.vcenter.Cluster.list(Cluster.FilterSpec(names={get_cluster}))[0].cluster
filter = vsphere_client.vcenter.VM.list(vsphere_client.vcenter.VM.FilterSpec(clusters={cluster_id}))

with open('vm_list_by_cluster.json', 'w') as outfile:
	for vm in filter:
		outfile.write("\n")
		outfile.write(str(json.dumps(vars(vm), indent=4)))

get_folder = input("Enter a Folder name: ")
folder_id = vsphere_client.vcenter.Folder.list(Folder.FilterSpec(names={get_folder}))[0].folder
vsphere_client.vcenter.VM.list(vsphere_client.vcenter.VM.FilterSpec(folders={folder_id}))

with open('vm_list_by_folder.json', 'w') as outfile:
	for vm in vsphere_client.vcenter.VM.list(vsphere_client.vcenter.VM.FilterSpec(folders={folder_id})):
		outfile.write("\n")
		outfile.write(str(json.dumps(vars(vm), indent=4)))

########################
"""
get_network = input("Enter network name: ")
network_id = vsphere_client.vcenter.Network.list(
            Network.FilterSpec(names={get_network},
                               types={Network.Type.STANDARD_PORTGROUP}))[0].network
#type or standard or distributed
vsphere_client.vcenter.VM.list(vsphere_client.vcenter.VM.FilterSpec(networks={network_id}))
"""
##################
"""
get_network = input("Enter a Network name: ")
network_id = vsphere_client.vcenter.Network.list(Network.FilterSpec(names={get_network}))[0].network
vsphere_client.vcenter.VM.list(vsphere_client.vcenter.VM.FilterSpec(networks={network_id}))


with open('vm_list_by_network.json', 'w') as outfile:
	for vm in vsphere_client.vcenter.VM.list(vsphere_client.vcenter.VM.FilterSpec(networks={network_id})):
		outfile.write("\n")
		outfile.write(str(json.dumps(vars(vm), indent=4)))


"""
resource_pool_id = vsphere_client.vcenter.ResourcePool.list(ResourcePool.FilterSpec(clusters={cluster_id}))[
                0].resource_pool
                
datastore_id = vsphere_client.vcenter.Datastore.list(Datastore.FilterSpec(names={datastore_name}))[0].datastore
"""


