import re,os
import shutil
import tempfile,zipfile
from django.conf import settings


def write_file(file_path,file_content):
	fileHandler = open(file_path,"w")
	fileHandler.writelines(file_content)
	fileHandler.close()

#=====================GET SOME INFORMATION====================
def get_storage_class_name_list():
	manifest_path = settings.RESOURCE_DIR + "/cluster.manifest.files/storage.manifest"
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

def get_server_ip_list():
	config_path = settings.RESOURCE_DIR + "/config.manifest"
	fileHandler = open(config_path,"a+")
	file_lines = fileHandler.readlines()
	#remove all the '\n' item
	file_lines = filter(lambda a: a != '\n', file_lines)
	file_lines = [item.replace('\n','') for item in file_lines]

	server_ip_list = []
	item_flag = ""
	group_counter = 0
	for item in file_lines:
		#get the file_system mark
		if item == "[nodes]":
			item_flag = "nodes"
			continue
		if item == "[controller_address]":
			continue

		if item_flag == "nodes":
			server_ip_list.append(item)
	return server_ip_list

#=====================READ THE MANIFEST=======================
def read_conf_manifest():
	config_manifest_path = settings.RESOURCE_DIR + "config.manifest"
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

def read_cluster_manifest():
	manifest_path = settings.RESOURCE_DIR + "cluster.manifest"
	fileHandler = open(manifest_path,"a+")
	file_lines = fileHandler.readlines()
	#remove all the '\n' item
	file_lines = filter(lambda a: a != '\n', file_lines)
	file_lines = [item.replace('\n','') for item in file_lines]

	cluster_manifest = {
		"basic":"",
		"storage":"",
		"profile":"",
		"cache":"",
		"settings":"",
	}
	cluster_manifest["basic"] = read_cluster_basic(file_lines)
	cluster_manifest["storage"] = read_cluster_storage(file_lines)
	cluster_manifest["profile"] = read_cluster_profile(file_lines)
	cluster_manifest["cache"] = read_cluster_cache(file_lines)
	cluster_manifest["settings"] = read_cluster_settings(file_lines)

	return cluster_manifest

def read_server_manifest(server_ip):
	#read info. from file
	manifest_path = settings.RESOURCE_DIR + server_ip +"/server.manifest"
	
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

	return server_data

def read_cluster_basic(file_lines):
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
		#get out the loop of basic
		if item == "[storage_class]":
			break

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

def read_cluster_storage(file_lines):
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
		#get out the loop of cluster storage
		if item == "[ec_profiles]":
			break

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

def read_cluster_profile(file_lines):
	cluster_profiles = []
	item_flag = ""
	group_counter = 0
	for item in file_lines:
		#get the cluster mark
		if item == "[ec_profiles]":
			item_flag = "ec_profiles"
			continue
		#get out the loop of cluster profile
		if item == "[Cache]":
			break

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

def read_cluster_cache(file_lines):
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

	item_flag = ""
	for item in file_lines:
		#get the cluster mark
		if item == "[Cache]":
			item_flag = "Cache"
			continue
		#get out the loop of cluster cache
		if item == "[Settings]":
			break

		if item_flag == "Cache":
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

def read_cluster_settings(file_lines):
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

	item_flag = ""
	for item in file_lines:
		#get the cluster mark
		if item == "[Settings]":
			item_flag = "Settings"
			continue

		#get out the loop of cluster cache
		if item_flag == "Settings":
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


#=====================SET THE MANIFEST======================== 
def generate_server_manifest(datasource):
	file_lines = [];
	file_lines.append("[vsm_controller_ip]\n")
	file_lines.append(datasource["server_ip"]+"\n\n")
	file_lines.append("[role]\n")
	file_lines.append(datasource["role"]+"\n\n")
	file_lines.append("[auth_key]\n")
	file_lines.append(datasource["auth_key"]+"\n\n")
	for sg_item in datasource["path_data"]:
		sg_name =  sg_item.keys()[0]
		file_lines.append("["+sg_name+"]\n")
		for path_item in sg_item[sg_name]:
			file_lines.append(path_item["device_path"])
			file_lines.append("   ")
			file_lines.append(path_item["journal_path"]+"\n")
		file_lines.append("\n\n")
	return file_lines

def generate_cluster_manifest(datasource):
	#the document lines of manifest
	file_lines = []

	#get the basic datasource
	basic = datasource["basic"]
	file_lines.append("[cluster]\n")
	file_lines.append(basic["cluster"]+"\n\n")
	file_lines.append("[file_system]\n")
	file_lines.append(basic["file_system"]+"\n\n")
	file_lines.append("[management_addr]\n")
	file_lines.append(basic["management_addr"]+"\n\n")
	file_lines.append("[ceph_public_addr]\n")
	file_lines.append(basic["ceph_public_addr"]+"\n\n")
	file_lines.append("[ceph_cluster_addr]\n")
	file_lines.append(basic["ceph_cluster_addr"]+"\n\n")

	#get the group datasource
	storage = datasource["group"]
	file_lines.append("[storage_class]\n")
	for storage_class in storage["storage_class"]:
		file_lines.append(storage_class+"\n")
	file_lines.append("\n");
	file_lines.append("[storage_group]\n")
	file_lines.append("#[group_name]   [friendly_name]   [storage_class]\n")
	for storage_group  in storage["storage_group"]:
		file_lines.append(storage_group["group_name"]+"   ")
		file_lines.append(storage_group["friendly_name"]+"   ")
		file_lines.append(storage_group["storage_class"]+"   ")
		file_lines.append("\n")

	#get the profile datasource
	profile = datasource["profile"]
	file_lines.append("\n\n[ec_profiles]\n")
	file_lines.append("#[profile-name] [path-to-plugin] [plugin-name] [pg_num value] [json format key/value]\n")
	for item in profile["profiles"]:
		file_lines.append(item["profile_name"]+"   ")
		file_lines.append(item["pg_number"]+"   ")
		file_lines.append(item["plugin_name"]+"   ")
		file_lines.append(item["plugin_path"]+"   ")
		file_lines.append(item["profile_data"]+"   ")
		file_lines.append("\n")

	#get the cache datasource
	cache = datasource["cache"]
	file_lines.append("\n\n[Cache]\n")
	file_lines.append("ct_hit_set_count   ")
	file_lines.append(cache["ct_hit_set_count"]+"\n")
	file_lines.append("ct_hit_set_period_s   ")
	file_lines.append(cache["ct_hit_set_period_s"]+"\n")
	file_lines.append("ct_target_max_objects   ")
	file_lines.append(cache["ct_target_max_objects"]+"\n")
	file_lines.append("ct_target_max_mem_mb   ")
	file_lines.append(cache["ct_target_max_mem_mb"]+"\n")
	file_lines.append("ct_target_dirty_ratio   ")
	file_lines.append(cache["ct_target_dirty_ratio"]+"\n")
	file_lines.append("ct_target_full_ratio   ")
	file_lines.append(cache["ct_target_full_ratio"]+"\n")
	file_lines.append("ct_target_min_flush_age_m   ")
	file_lines.append(cache["ct_target_min_flush_age_m"]+"\n")
	file_lines.append("ct_target_min_evict_age_m   ")
	file_lines.append(cache["ct_target_min_evict_age_m"]+"\n")


	#get the settings datasource
	settings = datasource["settings"]
	file_lines.append("\n\n[Settings]\n")
	file_lines.append("storage_group_near_full_threshold   ")
	file_lines.append(settings["storage_group_near_full_threshold"]+"\n")
	file_lines.append("storage_group_full_threshold   ")
	file_lines.append(settings["storage_group_full_threshold"]+"\n")
	file_lines.append("ceph_near_full_threshold   ")
	file_lines.append(settings["ceph_near_full_threshold"]+"\n")
	file_lines.append("ceph_full_threshold   ")
	file_lines.append(settings["ceph_full_threshold"]+"\n")
	file_lines.append("pg_count_factor   ")
	file_lines.append(settings["pg_count_factor"]+"\n")
	file_lines.append("heartbeat_interval   ")
	file_lines.append(settings["heartbeat_interval"]+"\n")
	file_lines.append("osd_heartbeat_interval   ")
	file_lines.append(settings["osd_heartbeat_interval"]+"\n")
	file_lines.append("osd_heartbeat_grace   ")
	file_lines.append(settings["osd_heartbeat_grace"]+"\n")
	file_lines.append("disk_near_full_threshold   ")
	file_lines.append(settings["disk_near_full_threshold"]+"\n")
	file_lines.append("disk_full_threshold   ")
	file_lines.append(settings["disk_full_threshold"]+"\n")

	return file_lines

#====================INSTALL STUFF============================
def extract_tarfile(file_path,extract_path):
	tar = tarfile.open(file_path)
	names = tar.getnames()
	for name in names:
		tar.extract(name,path=extract_path)
	tar.close()

def copy_manifest(package_name):
	#get the file list
	file_list = []
	#get the cluster manifest
	controller_ip = read_conf_manifest()["controller_address"]

	f_path = settings.RESOURCE_DIR +"/cluster.manifest"
	t_path = settings.INSTALLER_DIR + package_name +"/manifest/" + controller_ip + "/cluster.manifest"
	t_folder = settings.INSTALLER_DIR + package_name +"/manifest/" + controller_ip
	cluster_manifest_item = {
		"f":f_path,
		"t":t_path,
		"folder":t_folder,
	}
	file_list.append(cluster_manifest_item);
	#get the server manifest
	server_ip_list = get_server_ip_list()
	for server_ip in server_ip_list:
	 	f_path = settings.RESOURCE_DIR + server_ip + "/server.manifest"
	 	t_path = settings.INSTALLER_DIR + package_name +"/manifest/" + server_ip + "/server.manifest"
	 	t_folder = settings.INSTALLER_DIR + package_name +"/manifest/" + server_ip
		server_manifest_item = {
			"f":f_path,
			"t":t_path,
			"folder":t_folder,
		}
		file_list.append(server_manifest_item)

	#clear the exist file
	target_package = settings.INSTALLER_DIR + package_name+"/manifest/"
	for file_item in os.listdir(target_package):
		target_dir = os.path.join(target_package,file_item)
		if os.path.isdir(target_dir):
			shutil.rmtree(target_dir)

	#excute copy
	for item in file_list:
		if not os.path.exists(item["t"]):
			os.mkdir(item["folder"])
		shutil.copyfile(item["f"],item["t"])

def edit_installrc(package_name):
	#get the server ip list
	server_ip_list = get_server_ip_list()
	server_ip_list_str = ""
	for server_ip in server_ip_list:
		server_ip_list_str = server_ip_list_str + server_ip + " "
	#get the controller_ip
	controller_ip = read_conf_manifest()["controller_address"]

	rc_path = settings.INSTALLER_DIR + package_name +"/installrc"
	fileHandler = open(rc_path,"a+")
	file_lines = fileHandler.readlines()
	#remove all the '\n' item
	# file_lines = filter(lambda a: a != '\n', file_lines)
	# file_lines = [item.replace('\n','') for item in file_lines]

	#generate the content of file
	file_content = [] #for rewrite the installrc file
	for line in file_lines:
		line_item = line.split("=")
		if line_item[0] == "#AGENT_ADDRESS_LIST":
			line = "#AGENT_ADDRESS_LIST=\"" + server_ip_list_str + "\"\n"
		if line_item[0] == "#CONTROLLER_ADDRESS":
			line = "#CONTROLLER_ADDRESS=\"" + controller_ip + "\""
		file_content.append(line)

	#write the file 
	write_file(rc_path,file_content)
