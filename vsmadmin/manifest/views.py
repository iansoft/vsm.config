from django.http import HttpResponse,JsonResponse, HttpResponseNotFound
from django.template import RequestContext, loader
from django.conf import settings 
import datetime
import os
import random
import json

import dashboard.views as dashboard_view
import tempfile,zipfile
from django.core.servers.basehttp import FileWrapper
import api.handlerfile as HandlerFile

def index(request):
	template = loader.get_template('manifest/index.html')
	context_data = HandlerFile.read_cluster_manifest()
	context = RequestContext(request, context_data)
	return HttpResponse(template.render(context))

def read_server_manifest(request):
	data = json.loads(request.body)
	server_ip = data["server_ip"]
	server_manifest_data =  HandlerFile.read_server_manifest(server_ip)
	rs = json.dumps(server_manifest_data)
	return HttpResponse(rs);

def set_cluster_manifest(request):
	#get the data
	datasource = json.loads(request.body)
	cluster_basic_content = HandlerFile.generate_cluster_basic_content(datasource);
	print cluster_basic_content
	#write the files
	HandlerFile.write_file("cluster_basic",cluster_basic_content)
	#response the data
	rs = json.dumps({"status":0})
	return HttpResponse(rs);

def set_cluster_storage_file(request):
	#get the data
	data = json.loads(request.body)
	
	
	#write the files
	handlerfile.write_file("cluster_storage",file_lines)
	#response the data
	rs = json.dumps({"status":0})
	return HttpResponse(rs);

def set_cluster_profile_file(request):
	#get the data 
	data = json.loads(request.body)
	

	#write the files
	handlefile.write_file("cluster_profile",file_lines)
	#response the data
	rs = json.dumps({"status":0})
	return HttpResponse(rs);

def set_cluster_cache_file(request):
	#get the data 
	data = json.loads(request.body)
	

	# #write the files
	handlefile.write_file("cluster_cache",file_lines)
	#response the data
	rs = json.dumps({"status":0})
	return HttpResponse(rs);

def set_cluster_settings_file(request):
	#get the data 
	data = json.loads(request.body)
	

	# #write the files
	handlefile.write_file("cluster_settings",file_lines)
	#response the data
	rs = json.dumps({"status":0})
	return HttpResponse(rs);

def set_cluster_server_file(request):
	#get the data
	data = json.loads(request.body)
	server_ip = data["server_ip"]
	

	#write the files
	write_server_file(server_ip,file_lines)
	#response the data
	rs = json.dumps({"status":0})
	return HttpResponse(rs);







def write_server_file(server_ip,file_content):
	file_path = settings.RESOURCE_DIR + server_ip +"/server.manifest"
	fileHandler = open(file_path,"w")
	fileHandler.writelines(file_content)
	fileHandler.close()


#generate the manifest
def download_manifest_zip(request):
    #generate the cluster manifest file
    manifest_file_content = generate_cluster_manifest_content()
    write_file("cluster",manifest_file_content)

    #get the zip package files
    cluster_manifest_path = settings.RESOURCE_DIR +"/cluster.manifest"
    server_ip_list = get_server_ip_list();

    zip_file_list = [{"type":"cluster","ip":"","path":cluster_manifest_path}]
    for server_ip  in server_ip_list:
        server_manifeset_path = settings.RESOURCE_DIR + server_ip+"/server.manifest"
        zip_file_list.append({"type":"server","ip":server_ip,"path":server_manifeset_path})

    #package as a zip
    if not os.path.exists(settings.MANIFEST_DIR):
    	os.mkdir(settings.MANIFEST_DIR)
    download_file_path = settings.MANIFEST_DIR + "manifest.zip"
    archive = zipfile.ZipFile(download_file_path, 'w', zipfile.ZIP_DEFLATED)
    for zip_file in zip_file_list:
    	if zip_file["type"] == "cluster":
        	archive.write(zip_file["path"],"cluster.manifest")
        else:
        	archive.write(zip_file["path"],zip_file["ip"]+"/server.manifest")

    archive.close()

    def read_file_for_downlod(file_path,buf_size=262144):
        f = open(file_path,"rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    response = HttpResponse(read_file_for_downlod(download_file_path),content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=manifest.zip'
    return response



