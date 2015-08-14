$(document).ready(function(){
	//init the data
	InitData();

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

//save the cluster storage info.
function SaveClusterStorage(){
	var cluster_storage_data = {
		storage_class:[],
		storage_group:[]
	};

	$(".lable-storage-class").each(function(){
		cluster_storage_data.storage_class.push(this.innerHTML);
	});

	$("#tStorageGroup>tbody>tr").each(function(){
		var group_name = this.children[0].innerHTML;
		var friendly_name = this.children[1].innerHTML;
		var storage_class = this.children[2].innerHTML;
		var group_data = {
			"group_name":group_name,
			"friendly_name":friendly_name,
			"storage_class":storage_class,
		}
		cluster_storage_data.storage_group.push(group_data);
	});

	var token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
        type: "post",
        url: "/manifest/set_cluster_storage_file/",
        data: JSON.stringify(cluster_storage_data),
        dataType:"json",
        success: function(data){
        	ShowMessage($("#divStorageMessage"),2,"Save the cluster storage info. successfully!");
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
           if(XMLHttpRequest.status == 500){
           		ShowMessage($("#divStorageMessage"),0,"INTERNAL SERVER ERROR!");
           }
        },
        headers: {
            "X-CSRFToken": token
        },
        complete: function(){

        }
    });

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

//remove the storage class
function RemoveStorageClass(obj){
	if(confirm("Remove the storage class?")==true){
		obj.remove();
	}
}

//add the storage group
function AddStorageGroup(){
	var html = "";
	html += "<tr>";
	// html += "<form class='form-inline'>";
	html += "	<td><input class='form-control' type='textbox'/></td>";
	html += "	<td><input class='form-control' type='textbox' /></td>";
	html += "	<td>";
	html += "	 	<select class='form-control' style='width:185px;'>";
		for(var i=0; i<$(".lable-storage-class").length;i++){
			var value = $(".lable-storage-class")[i].innerHTML;
			html += "	 <option value='"+value+"'>"+value+"</option>";
		}
	html += "	 	</select>";
	html += "	</td>";

	html += "	<td>";
	html += "		<a class='btn btn-success'  onclick='SaveStorageGroup(this)'>save</a>";
	html += "	    <a class='btn btn-danger'  onclick='RemoveStorageGroup(this)'>cancel</a>";
	html += "	</td>";
	// html += "</form>";
	html += "</tr>";

	$("#tStorageGroup>tbody").append(html);
}

//save the storage group
function SaveStorageGroup(obj){
	var ctrlGroupName= obj.parentNode.parentNode.children[0].children[0];
	var ctrFriendlyName= obj.parentNode.parentNode.children[1].children[0];
	var ctrlStorageName= obj.parentNode.parentNode.children[2].children[0];

	var is_pass = true;
	if(ctrlGroupName.value == ""){
		ctrlGroupName.style.border = "1px solid red";
		is_pass = false;
	}

	if(ctrFriendlyName.value == ""){
		ctrFriendlyName.style.border = "1px solid red";
		is_pass = false;
	}

	if(ctrlStorageName.value == ""){
		ctrlStorageName.style.border = "1px solid red";
		is_pass = false;
	}

	if(is_pass == false){
		return false;
	}

	//save the items
	var html = "";
	html += "<tr>";
	html += "	<td>"+ctrlGroupName.value+"</td>";
	html += "	<td>"+ctrFriendlyName.value+"</td>";
	html += "	<td>"+ctrlStorageName.value+"</td>";
	html += "	<td><a class='btn btn-danger' onclick='RemoveStorageGroup(this)'>remove</a></td>";
	html += "</tr>";

	//first remove the row
	obj.parentNode.parentNode.remove();
	$("#tStorageGroup>tbody").append(html);	
}

//remove the storage group
function RemoveStorageGroup(obj){
	if(confirm("Remove the storage group?")==true){
		obj.parentNode.parentNode.remove();
	}
}


