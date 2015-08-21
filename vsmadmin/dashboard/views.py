from django.http import HttpResponse,JsonResponse, HttpResponseNotFound
from django.template import RequestContext, loader
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
	base_dir = os.path.dirname(os.path.dirname(__file__))
	config_manifest_path = base_dir + "/files/config.manifest";
	fileHandler = open(config_manifest_path,"w")

	file_lines = [];
	file_lines.append("[controller_address]\n")
	file_lines.append(data["controller"]+"\n\n")
	file_lines.append("[nodes]\n")
	file_lines.extend([node+"\n" for node in data["nodes"] ])
	
	fileHandler.writelines(file_lines)
	fileHandler.close()


def set_server_file(data):
	base_dir = os.path.dirname(os.path.dirname(__file__))
	server_list = data["nodes"]
	for server in server_list:
		config_manifest_path = base_dir + "/files/server."+server+".manifest";
		if os.path.exists(config_manifest_path) == False:
			fileHandler = open(config_manifest_path,"w+")
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
	base_dir = os.path.dirname(os.path.dirname(__file__))
	config_manifest_path = base_dir + "/files/config.manifest"
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


