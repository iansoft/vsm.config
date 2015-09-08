from django.http import HttpResponse,JsonResponse, HttpResponseNotFound
from django.template import RequestContext, loader
from django.conf import settings
import datetime
import os
import random
import json

def index(request):
    template = loader.get_template('dashboard/index.html')
    #read the config file
    config_data = read_config_file()
    context = RequestContext(request, {"config_data": config_data})
    return HttpResponse(template.render(context))


def init_files(request):
	data = json.loads(request.body)
	#write the config file
	set_config_file(data)
	#write the server file
	set_server_file(data)
	
	rs = json.dumps({"status":0})
	return HttpResponse(rs);


def set_config_file(data):
	config_manifest_path = settings.RESOURCE_DIR + "config.manifest";
	fileHandler = open(config_manifest_path,"w")

	file_lines = [];
	file_lines.append("[controller_address]\n")
	file_lines.append(data["controller"]+"\n\n")
	file_lines.append("[nodes]\n")
	file_lines.extend([node+"\n" for node in data["nodes"] ])
	
	fileHandler.writelines(file_lines)
	fileHandler.close()


def set_server_file(data):
	server_list = data["nodes"]
	for server in server_list:
		server_manifest_folder_path = settings.RESOURCE_DIR + server
		server_manifest_file_path = settings.RESOURCE_DIR + server + "/server.manifest"

		if not os.path.exists(server_manifest_folder_path):
			os.makedirs(server_manifest_folder_path)

		if not os.path.exists(server_manifest_file_path):
			fileHandler = open(server_manifest_file_path,"w+")
			file_lines = [];
			file_lines.append("[vsm_controller_ip]\n")
			file_lines.append(server+"\n\n")
			file_lines.append("[role]\n")
			file_lines.extend("storage\n\n")
			file_lines.append("[auth_key]\n")
			file_lines.append("auth_key\n\n")

			fileHandler.writelines(file_lines)
			fileHandler.close()


def read_config_file():
	config_manifest_path = settings.RESOURCE_DIR + "config.manifest"
	print config_manifest_path
	fileHandler = open(config_manifest_path,"a+")
	file_lines = fileHandler.readlines()
	#remove all the '\n' item
	file_lines = filter(lambda a: a != '\n', file_lines)
	file_lines = [item.replace('\n','') for item in file_lines]

	item_flag = ""
	controller = ""
	nodes = []
	for item in file_lines:
		#get the controller mark
		if item == "[controller_address]":
			item_flag = "controller"
			continue
		#get the node mark
		if item == "[nodes]":
			item_flag = "nodes"
			continue
		#get the controller IP
		if item_flag == "controller":
			controller = item
		#get the node IP
		if item_flag == "nodes":
			nodes.append(item)

	config_data = {"controller_address":controller,"nodes":nodes}
	return config_data


