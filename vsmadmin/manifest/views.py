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
	cluster_profile_data = read_cluster_profile_manifest()
	cluster_cache_data = read_cluster_cache_manifest()
	cluster_settings_data = read_cluster_settings_manifest();

	context_data = {
		"config_data": config_data,
		"cluster_basic_data":cluster_basic_data,
		"cluster_storage_data":cluster_storage_data,
		"cluster_profile_data":cluster_profile_data,
		"cluster_cache_data":cluster_cache_data,
		"cluster_settings_data":cluster_settings_data,
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
	group_counter = 0
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
			group_counter = group_counter + 1
			#ignore the comment line
			if(group_counter == 1):
				continue
			
			group_items_data = {
				"group_name":group_items[0],
				"friendly_name":group_items[2],
				"storage_class":group_items[4],
			}
			cluster_storage["storage_group"].append(group_items_data) 
	return cluster_storage 

def read_cluster_profile_manifest():
	base_dir = os.path.dirname(os.path.dirname(__file__))
	manifest_path = base_dir + "/files/cluster.profile.manifest"
	fileHandler = open(manifest_path,"a+")
	file_lines = fileHandler.readlines()
	#remove all the '\n' item
	file_lines = filter(lambda a: a != '\n', file_lines)
	file_lines = [item.replace('\n','') for item in file_lines]

	#format: [profile-name] [path-to-plugin] [plugin-name] [pg_num value] [json format key/value]
	cluster_profiles = []
	item_flag = ""
	group_counter = 0
	for item in file_lines:
		#get the cluster mark
		if item == "[ec_profiles]":
			item_flag = "ec_profiles"
			continue
		if item_flag == "ec_profiles":
			group_counter = group_counter + 1
			#ignore the comment line
			if(group_counter == 1):
				continue
			item = re.sub("(\s+)","|",item)
			profile_items = re.split("(\|)",item)
			profile_items_data = {
				"name":profile_items[0],
				"plugin_name":profile_items[4],
				"plugin_path":profile_items[2],
				"pg_num":profile_items[6],
				"data":profile_items[8],
			}
			cluster_profiles.append(profile_items_data)

	return cluster_profiles

def read_cluster_cache_manifest():
	base_dir = os.path.dirname(os.path.dirname(__file__))
	manifest_path = base_dir + "/files/cluster.cache.manifest"
	fileHandler = open(manifest_path,"a+")
	file_lines = fileHandler.readlines()
	#remove all the '\n' item
	file_lines = filter(lambda a: a != '\n', file_lines)
	file_lines = [item.replace('\n','') for item in file_lines]

	cluster_cache = {
		"ct_hit_set_count":0,
		"ct_hit_set_period_s":0,
		"ct_target_max_objects":0,
		"ct_target_max_mem_mb":0,
		"ct_target_dirty_ratio":0,
		"ct_target_full_ratio":0,
		"ct_target_min_flush_age_m":0,
		"ct_target_min_evict_age_m":0
	}

	for item in file_lines:
		item = re.sub("(\s+)","|",item)
		cache_items = re.split("(\|)",item)
		if cache_items[0] == "ct_hit_set_count":
			cluster_cache["ct_hit_set_count"] = cache_items[2]
		if cache_items[0] == "ct_hit_set_period_s":
			cluster_cache["ct_hit_set_period_s"] = cache_items[2]
		if cache_items[0] == "ct_target_max_objects":
			cluster_cache["ct_target_max_objects"] = cache_items[2]
		if cache_items[0] == "ct_target_max_mem_mb":
			cluster_cache["ct_target_max_mem_mb"] = cache_items[2]
		if cache_items[0] == "ct_target_dirty_ratio":
			cluster_cache["ct_target_dirty_ratio"] = cache_items[2]
		if cache_items[0] == "ct_target_full_ratio":
			cluster_cache["ct_target_full_ratio"] = cache_items[2]
		if cache_items[0] == "ct_target_min_flush_age_m":
			cluster_cache["ct_target_min_flush_age_m"] = cache_items[2]
		if cache_items[0] == "ct_target_min_evict_age_m":
			cluster_cache["ct_target_min_evict_age_m"] = cache_items[2]

	return cluster_cache

def read_cluster_settings_manifest():
	base_dir = os.path.dirname(os.path.dirname(__file__))
	manifest_path = base_dir + "/files/cluster.settings.manifest"
	fileHandler = open(manifest_path,"a+")
	file_lines = fileHandler.readlines()
	#remove all the '\n' item
	file_lines = filter(lambda a: a != '\n', file_lines)
	file_lines = [item.replace('\n','') for item in file_lines]

	cluster_cache = {
		"storage_group_near_full_threshold":0,
		"storage_group_full_threshold":0,
		"ceph_near_full_threshold":0,
		"ceph_full_threshold":0,
		"osd_heartbeat_interval":0,
		"osd_heartbeat_grace":0,
		"disk_near_full_threshold":0,
		"disk_full_threshold":0,
		"pg_count_factor":0,
		"heartbeat_interval":0,
	}

	for item in file_lines:
		item = re.sub("(\s+)","|",item)
		cache_items = re.split("(\|)",item)
		if cache_items[0] == "storage_group_near_full_threshold":
			cluster_cache["storage_group_near_full_threshold"] = cache_items[2]
		if cache_items[0] == "storage_group_full_threshold":
			cluster_cache["storage_group_full_threshold"] = cache_items[2]
		if cache_items[0] == "ceph_near_full_threshold":
			cluster_cache["ceph_near_full_threshold"] = cache_items[2]
		if cache_items[0] == "ceph_full_threshold":
			cluster_cache["ceph_full_threshold"] = cache_items[2]
		if cache_items[0] == "osd_heartbeat_interval":
			cluster_cache["osd_heartbeat_interval"] = cache_items[2]
		if cache_items[0] == "osd_heartbeat_grace":
			cluster_cache["osd_heartbeat_grace"] = cache_items[2]
		if cache_items[0] == "disk_near_full_threshold":
			cluster_cache["disk_near_full_threshold"] = cache_items[2]
		if cache_items[0] == "disk_full_threshold":
			cluster_cache["disk_full_threshold"] = cache_items[2]
		if cache_items[0] == "pg_count_factor":
			cluster_cache["pg_count_factor"] = cache_items[2]
		if cache_items[0] == "heartbeat_interval":
			cluster_cache["heartbeat_interval"] = cache_items[2]

	return cluster_cache

def read_cluster_server_manifest(request):
	#get the request data
	print request.body
	data = json.loads(request.body)
	server_ip = data["server_ip"]

	#read info. from file
	base_dir = os.path.dirname(os.path.dirname(__file__))
	manifest_path = base_dir + "/files/server."+server_ip+".manifest"
	fileHandler = open(manifest_path,"a+")
	file_lines = fileHandler.readlines()
	#remove all the '\n' item
	file_lines = filter(lambda a: a != '\n', file_lines)
	file_lines = [item.replace('\n','') for item in file_lines]

	storage_class_name_list = get_storage_class_name_list()
	server_data_str = ""
	server_data_str += "{'server_ip':'','role':'','auth_key':'',"
	for storage_class_name in storage_class_name_list:
	 	server_data_str += "'"+storage_class_name +"':[],"
	server_data_str += "}"
	server_data = eval(server_data_str)
	
	item_flag = ""
	is_item_path = False
	for item in file_lines:
		if item == "[vsm_controller_ip]":
			item_flag = "vsm_controller_ip"
			continue
		if item == "[role]":
			item_flag = "role"
			continue
		if item == "[auth_key]":
			item_flag = "auth_key"
			continue

		is_flag = False
		for _sg_name in storage_class_name_list:
			_sg_name_mark  = "["+_sg_name+"]"
			if item == _sg_name_mark:
				item_flag = _sg_name
				is_flag = True
				is_item_path = True
		if is_flag == True:
			continue

		#get the info.
		if item_flag == "vsm_controller_ip":
			server_data["server_ip"] = item
		if item_flag == "role":
			server_data["role"] = item
		if item_flag == "auth_key":
			server_data["auth_key"] = item
		if is_item_path == True:
			for sg_key in server_data.keys():
				if  item_flag == sg_key:
					item = re.sub("(\s+)","|",item)
					path_items = re.split("(\|)",item)
					path_data_dict = {"device_path":path_items[0],"journal_path":path_items[2]}
					server_data[sg_key].append(path_data_dict)

	rs = json.dumps(server_data)
	return HttpResponse(rs);






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

def set_cluster_storage_file(request):
	#get the data
	data = json.loads(request.body)
	file_lines = [];
	file_lines.append("[storage_class]\n")
	for storage_class in data["storage_class"]:
		file_lines.append(storage_class+"\n")
	file_lines.append("\n");
	
	file_lines.append("[storage_group]\n")
	file_lines.append("#[group_name]   [friendly_name]   [storage_class]\n")
	for storage_group  in data["storage_group"]:
		file_lines.append(storage_group["group_name"]+"   ")
		file_lines.append(storage_group["friendly_name"]+"   ")
		file_lines.append(storage_group["storage_class"]+"   ")
		file_lines.append("\n")
	
	#write the files
	write_file("cluster_storage",file_lines)
	#response the data
	rs = json.dumps({"status":0})
	return HttpResponse(rs);

def set_cluster_profile_file(request):
	#get the data 
	data = json.loads(request.body)
	file_lines = [];
	file_lines.append("[ec_profiles]\n")
	file_lines.append("#[profile-name] [path-to-plugin] [plugin-name] [pg_num value] [json format key/value]\n")
	for profile in data["profiles"]:
		file_lines.append(profile["profile_name"]+"   ")
		file_lines.append(profile["pg_number"]+"   ")
		file_lines.append(profile["plugin_name"]+"   ")
		file_lines.append(profile["plugin_path"]+"   ")
		file_lines.append(profile["profile_data"]+"   ")
		file_lines.append("\n")

	#write the files
	write_file("cluster_profile",file_lines)
	#response the data
	rs = json.dumps({"status":0})
	return HttpResponse(rs);

def set_cluster_cache_file(request):
	#get the data 
	data = json.loads(request.body)
	file_lines = []
	file_lines.append("ct_hit_set_count   ")
	file_lines.append(data["ct_hit_set_count"]+"\n")
	file_lines.append("ct_hit_set_period_s   ")
	file_lines.append(data["ct_hit_set_period_s"]+"\n")
	file_lines.append("ct_target_max_objects   ")
	file_lines.append(data["ct_target_max_objects"]+"\n")
	file_lines.append("ct_target_max_mem_mb   ")
	file_lines.append(data["ct_target_max_mem_mb"]+"\n")
	file_lines.append("ct_target_dirty_ratio   ")
	file_lines.append(data["ct_target_dirty_ratio"]+"\n")
	file_lines.append("ct_target_full_ratio   ")
	file_lines.append(data["ct_target_full_ratio"]+"\n")
	file_lines.append("ct_target_min_flush_age_m   ")
	file_lines.append(data["ct_target_min_flush_age_m"]+"\n")
	file_lines.append("ct_target_min_evict_age_m   ")
	file_lines.append(data["ct_target_min_evict_age_m"]+"\n")

	# #write the files
	write_file("cluster_cache",file_lines)
	#response the data
	rs = json.dumps({"status":0})
	return HttpResponse(rs);

def set_cluster_settings_file(request):
	#get the data 
	data = json.loads(request.body)
	file_lines = []
	file_lines.append("storage_group_near_full_threshold   ")
	file_lines.append(data["storage_group_near_full_threshold"]+"\n")
	file_lines.append("storage_group_full_threshold   ")
	file_lines.append(data["storage_group_full_threshold"]+"\n")
	file_lines.append("ceph_near_full_threshold   ")
	file_lines.append(data["ceph_near_full_threshold"]+"\n")
	file_lines.append("ceph_full_threshold   ")
	file_lines.append(data["ceph_full_threshold"]+"\n")
	file_lines.append("pg_count_factor   ")
	file_lines.append(data["pg_count_factor"]+"\n")
	file_lines.append("heartbeat_interval   ")
	file_lines.append(data["heartbeat_interval"]+"\n")
	file_lines.append("osd_heartbeat_interval   ")
	file_lines.append(data["osd_heartbeat_interval"]+"\n")
	file_lines.append("osd_heartbeat_grace   ")
	file_lines.append(data["osd_heartbeat_grace"]+"\n")
	file_lines.append("disk_near_full_threshold   ")
	file_lines.append(data["disk_near_full_threshold"]+"\n")
	file_lines.append("disk_full_threshold   ")
	file_lines.append(data["disk_full_threshold"]+"\n")

	# #write the files
	write_file("cluster_settings",file_lines)
	#response the data
	rs = json.dumps({"status":0})
	return HttpResponse(rs);

def set_cluster_server_file(request):
	#get the data
	data = json.loads(request.body)
	server_ip = data["server_ip"]
	file_lines = [];
	file_lines.append("[vsm_controller_ip]\n")
	file_lines.append(data["server_ip"]+"\n\n")
	file_lines.append("[role]\n")
	file_lines.append(data["role"]+"\n\n")
	file_lines.append("[auth_key]\n")
	file_lines.append(data["auth_key"]+"\n\n")

	for sg_item in data["path_data"]:
		sg_name =  sg_item.keys()[0]
		file_lines.append("["+sg_name+"]\n")
		for path_item in sg_item[sg_name]:
			file_lines.append(path_item["device_path"])
			file_lines.append("   ")
			file_lines.append(path_item["journal_path"]+"\n")
		file_lines.append("\n\n")

	#write the files
	write_server_file(server_ip,file_lines)
	#response the data
	rs = json.dumps({"status":0})
	return HttpResponse(rs);


def get_storage_class_name_list():
	base_dir = os.path.dirname(os.path.dirname(__file__))
	manifest_path = base_dir + "/files/cluster.storage.manifest"
	fileHandler = open(manifest_path,"a+")
	file_lines = fileHandler.readlines()
	#remove all the '\n' item
	file_lines = filter(lambda a: a != '\n', file_lines)
	file_lines = [item.replace('\n','') for item in file_lines]

	storage_class = []
	item_flag = ""
	group_counter = 0
	for item in file_lines:
		#get the file_system mark
		if item == "[storage_class]":
			item_flag = "storage_class"
			continue
		if item == "[storage_group]":
			break

		if item_flag == "storage_class":
			storage_class.append(item)
	return storage_class

def write_file(file_type,file_content):
	base_dir = os.path.dirname(os.path.dirname(__file__))
	file_path = "";
	if(file_type == "cluster_basic"):
		file_path = base_dir + "/files/cluster.basic.manifest"
	if(file_type == "cluster_storage"):
		file_path = base_dir + "/files/cluster.storage.manifest"
	if(file_type == "cluster_profile"):
		file_path = base_dir + "/files/cluster.profile.manifest"
	if(file_type == "cluster_cache"):
		file_path = base_dir + "/files/cluster.cache.manifest"
	if(file_type == "cluster_settings"):
		file_path = base_dir + "/files/cluster.settings.manifest"

	fileHandler = open(file_path,"w")
	fileHandler.writelines(file_content)
	fileHandler.close()


def write_server_file(server_ip,file_content):
	base_dir = os.path.dirname(os.path.dirname(__file__))
	file_path = "";
	file_path = base_dir + "/files/server."+server_ip+".manifest"

	fileHandler = open(file_path,"w")
	fileHandler.writelines(file_content)
	fileHandler.close()




