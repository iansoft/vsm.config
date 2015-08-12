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


def set_config(request):
	data = json.loads(request.body)
	#generate the config.manifest
	file_lines = set_config_file(data)
	#write the file
	base_dir = os.path.dirname(os.path.dirname(__file__))
	config_manifest_path = base_dir + "/files/config.manifest";
	fileHandler = open(config_manifest_path,"w")
	fileHandler.writelines(file_lines)
	fileHandler.close()

	rs = json.dumps({"status":0})
	return HttpResponse(rs);


def set_config_file(data):
	file_lines = [];
	file_lines.append("[controller_address]\n")
	file_lines.append(data["controller"]+"\n\n")
	file_lines.append("[nodes]\n")
	file_lines.extend([node+"\n" for node in data["nodes"] ])

	return file_lines;

def read_config_file():
	base_dir = os.path.dirname(os.path.dirname(__file__))
	config_manifest_path = base_dir + "/files/config.manifest";
	fileHandler = open(config_manifest_path,"r")
	file_lines = fileHandler.readlines()
	#remove all the '\n' item
	file_lines = filter(lambda a: a != '\n', file_lines)
	file_lines = [item[0:-1] for item in file_lines]

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

	print config_data
	return config_data


