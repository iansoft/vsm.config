from django.http import HttpResponse,JsonResponse, HttpResponseNotFound
from django.template import RequestContext, loader
import datetime
import os
import random
import json
import dashboard.views as dashboard_view

def index(request):
	template = loader.get_template('manifest/index.html')
	#read the config file
	config_data = dashboard_view.read_config_file()
	cluster_basic_data = read_cluster_basic_manifest()

	context_data = {
		"config_data": config_data,
		"cluster_basic_data":cluster_basic_data,
	}
	context = RequestContext(request, context_data)
	return HttpResponse(template.render(context))


def read_cluster_basic_manifest():
	base_dir = os.path.dirname(os.path.dirname(__file__))
	config_manifest_path = base_dir + "/files/cluster.basic.manifest"
	fileHandler = open(config_manifest_path,"a+")
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





