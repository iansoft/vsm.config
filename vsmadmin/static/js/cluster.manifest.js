$(document).ready(function(){
	//init the data
	InitData();

	//add the storage class
	$("#btnAddStorageClass").click(function(){
		AddStorageClass();
	});

	$("#btnSaveClusterBasic").click(function(){
		SaveClusterBasic();
	});
});


function InitData(){
	var _Selected_File_System = $("#hfFileSystem").val();
	var _Sel_File_System = $("#selFileSystem")[0];
	for(var i=0;i<_Sel_File_System.options.length;i++){
		if(_Sel_File_System.options[i].text == _Selected_File_System){
			_Sel_File_System.options[i].selected = true;
		}
	}
}

//add the storage class
function AddStorageClass(){
	var class_name = $("#txtStorageClass").val();
	if(class_name == ""){
		return false;
	}
	var html = "";
	html += "<span class='label label-info lable-storage-class' onclick='RemoveStorageClass(this)'>"+ class_name +"</span>";
	$("#divStorageClass1").append(html);
}

function RemoveStorageClass(obj){
	if(confirm("Remove the storage group?")==true){
		obj.remove();
	}
}

//save the cluster basic info.
function SaveClusterBasic(){
	//check the management address
	var _Management_Address = $("#lblManagementAddress").val();
	if(checkIPWithPort(_Management_Address)==false){
		ShowMessage($("#divBasicMessage"),1,"The management address format is wrong!");
		return false;
	}

	//check the ceph public address
	var _Ceph_Public_Address = $("#lblCephPublicAddress").val();
	if(checkIPWithPort(_Ceph_Public_Address)==false){
		ShowMessage($("#divBasicMessage"),1,"The ceph public address format is wrong!");
		return false;
	}

	//check the ceph cluster address
	var _Ceph_Cluster_Address = $("#lblCephClusterAddress").val();
	if(checkIPWithPort(_Ceph_Cluster_Address)==false){
		ShowMessage($("#divBasicMessage"),1,"The ceph cluster address format is wrong!");
		return false;
	}

	var cluster_basic_data = {
		"cluster":$("#txtCluster").val(),
		"file_system":$("#selFileSystem").val(),
		"management_addr":_Management_Address,
		"ceph_public_addr":_Ceph_Public_Address,
		"ceph_cluster_addr":_Ceph_Cluster_Address,
	};


	var token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
        type: "post",
        url: "/manifest/set_cluster_basic_file/",
        data: JSON.stringify(cluster_basic_data),
        dataType:"json",
        success: function(data){
        	ShowMessage($("#divBasicMessage"),2,"Save the cluster basic info. successfully!");
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
           if(XMLHttpRequest.status == 500){
           		ShowMessage($("#divBasicMessage"),0,"INTERNAL SERVER ERROR!");
           }
        },
        headers: {
            "X-CSRFToken": token
        },
        complete: function(){

        }
    });
}

