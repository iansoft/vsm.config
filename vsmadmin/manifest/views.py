from django.http import HttpResponse,JsonResponse, HttpResponseNotFound
from django.template import RequestContext, loader
import datetime
import os
import random
import json
import re
import dashboard.views as dashboard_view

def index(request):
	template = loader.get_template('manifest/index.html')
	#read the config file
	config_data = dashboard_view.read_config_file()
	cluster_basic_data = read_cluster_basic_manifest()
	cluster_storage_data = read_cluster_storage_manifest()

	context_data = {
		"config_data": config_data,
		"cluster_basic_data":cluster_basic_data,
		"cluster_storage_data":cluster_storage_data
	}
	context = RequestContext(request, context_data)
	return HttpResponse(template.render(context))


def read_cluster_basic_manifest():
	base_dir = os.path.dirname(os.path.dirname(__file__))
	manifest_path = base_dir + "/files/cluster.basic.manifest"
	fileHandler = open(manifest_path,"a+")
	file_lines = fileHandler.readlines()
	#remove all the '\n' item
	file_lines = filter(lambda a: a != '\n', file_lines)
	file_lines = [item.replace('\n','') for item in file_lines]

	cluster_basic = {
		"cluster":"",
		"file_system":"",
		"management_addr":"",
		"ceph_public_addr":"",
		"ceph_cluster_addr":"",
	}

	item_flag = ""
	for item in file_lines:
		#get the cluster mark
		if item == "[cluster]":
			item_flag = "cluster"
			continue
		#get the file_system mark
		if item == "[file_system]":
			item_flag = "file_system"
			continue
		#get the management_addr. mark
		if item == "[management_addr]":
			item_flag = "management_addr"
			continue
		#get the ceph public addr. mark
		if item == "[ceph_public_addr]":
			item_flag = "ceph_public_addr"
			continue
		#get the ceph cluster addr. mark
		if item == "[ceph_cluster_addr]":
			item_flag = "ceph_cluster_addr"
			continue

		if item_flag == "cluster":
			cluster_basic["cluster"] = item
		if item_flag == "file_system":
			cluster_basic["file_system"] = item
		if item_flag == "management_addr":
			cluster_basic["management_addr"] = item
		if item_flag == "ceph_public_addr":
			cluster_basic["ceph_public_addr"] = item
		if item_flag == "ceph_cluster_addr":
			cluster_basic["ceph_cluster_addr"] = item

	return cluster_basic 


def read_cluster_storage_manifest():
	base_dir = os.path.dirname(os.path.dirname(__file__))
	manifest_path = base_dir + "/files/cluster.storage.manifest"
	fileHandler = open(manifest_path,"a+")
	file_lines = fileHandler.readlines()
	#remove all the '\n' item
	file_lines = filter(lambda a: a != '\n', file_lines)
	file_lines = [item.replace('\n','') for item in file_lines]

	#format: [storage group name]  [user friendly storage group name] [storage class]

	cluster_storage = {
		"storage_class":[],
		"storage_group":[],
	}

	item_flag = ""
	for item in file_lines:
		#get the cluster mark
		if item == "[storage_class]":
			item_flag = "storage_class"
			continue
		#get the file_system mark
		if item == "[storage_group]":
			item_flag = "storage_group"
			continue

		if item_flag == "storage_class":
			cluster_storage["storage_class"].append(item) 
		if item_flag == "storage_group":
			item = re.sub("(\s+)",",",item)
			group_items = re.split("(\,)",item)
			group_items_data = {
				"group_name":group_items[0],
				"friendly_name":group_items[2],
				"storage_class":group_items[4],
			}
			cluster_storage["storage_group"].append(group_items_data) 

	return cluster_storage 


def set_cluster_basic_file(request):
	#get the data
	data = json.loads(request.body)
	file_lines = [];
	file_lines.append("[cluster]\n")
	file_lines.append(data["cluster"]+"\n\n")
	file_lines.append("[file_system]\n")
	file_lines.append(data["file_system"]+"\n\n")
	file_lines.append("[management_addr]\n")
	file_lines.append(data["management_addr"]+"\n\n")
	file_lines.append("[ceph_public_addr]\n")
	file_lines.append(data["ceph_public_addr"]+"\n\n")
	file_lines.append("[ceph_cluster_addr]\n")
	file_lines.append(data["ceph_cluster_addr"]+"\n\n")

	#write the files
	write_file("cluster_basic",file_lines)
	#response the data
	rs = json.dumps({"status":0})
	return HttpResponse(rs);

def write_file(file_type,file_content):
	base_dir = os.path.dirname(os.path.dirname(__file__))
	file_path = "";
	if(file_type == "cluster_basic"):
		file_path = base_dir + "/files/cluster.basic.manifest"

	fileHandler = open(file_path,"w")
	fileHandler.writelines(file_content)
	fileHandler.close()





