from django.http import HttpResponse
from django.shortcuts import render,render_to_response
from django import forms
import time
import os
import tarfile
from django.conf import settings
import api.handlerfile as HandlerFile
import subprocess

class UploadFileForm(forms.Form):
	file = forms.FileField()

def index(request):
	if request.method == "POST":
		form = UploadFileForm(request.POST,request.FILES)
		if form.is_valid():
			file_name = handle_uploaded_file(request.FILES['file'])
			return render(request,"installer/index.html",{'form':form,"file_name":file_name})
	else:
		form = UploadFileForm()

	return render(request,"installer/index.html",{'form':form})


def handle_uploaded_file(f):
	file_name = ""
	package_name = f.name.replace(".tar.gz","")
	try:
		file_path = settings.PACKAGE_DIR + f.name
		#if the package folder is not is exsit
		#then create one
		if not os.path.exists(settings.PACKAGE_DIR):
			os.makedirs(settings.PACKAGE_DIR)
		if not os.path.exists(settings.INSTALLER_DIR):
			os.makedirs(settings.INSTALLER_DIR)
		#write the file bytes
		destination = open(file_path,"wb+")
		for chunk in f.chunks():
			destination.write(chunk)
		destination.close()
		#extract the tar.gz
		HandlerFile.extract_tarfile(file_path,settings.INSTALLER_DIR)
		#copy the manifest file into the install folder
		HandlerFile.copy_manifest(package_name)
		#edit the installer resource file
		HandlerFile.edit_installrc(package_name)
		#excute the install.sh
		install_vsm(package_name)

	except Exception,e:
		print e

	return f.name


def install_vsm(package_name):
	install_sh_path = settings.INSTALLER_DIR + package_name +"/install.sh"
	cmd = subprocess.Popen(install_sh_path, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	print "=====================excute the install.sh====================="
	print output