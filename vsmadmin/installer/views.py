from django.http import HttpResponse
from django.shortcuts import render,render_to_response
from django import forms
import time
import os
import tarfile

class UploadFileForm(forms.Form):
	title = forms.CharField(max_length=50)
	file = forms.FileField()

def index(request):
	if request.method == "POST":
		form = UploadFileForm(request.POST,request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			return HttpResponse('upload ok!')
	else:
		form = UploadFileForm()

	return render(request,"installer/index.html",{'form':form})


def handle_uploaded_file(f):
	file_name = ""

	try:
		base_dir = os.path.dirname(os.path.dirname(__file__))
		upload_path = base_dir +"/files/package/"
		extract_path = base_dir +"/files/installer/"
		file_path = upload_path + f.name

		#if the package folder is not is exsit
		#then create one
		if not os.path.exists(upload_path):
			os.makedirs(upload_path)
		if not os.path.exists(extract_path):
			os.makedirs(extract_path)
		#write the file bytes
		destination = open(file_path,"wb+")
		for chunk in f.chunks():
			destination.write(chunk)
		destination.close()
		#extract the tar.gz
		extract_tarfile(file_path,extract_path)
	except Exception,e:
		print e

	return file_name


def extract_tarfile(file_path,extract_path):
	tar = tarfile.open(file_path)
	names = tar.getnames()
	for name in names:
		tar.extract(name,path=extract_path)
	tar.close()
