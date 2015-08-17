$(document).ready(function(){
	//init the data
	InitData();

	//Init Profile Detail
	//InitProfileDetail();
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

//save the cluster profile info.
function SaveClusterProfile(){
	var cluster_profile_data = {
		profiles:[]
	};

	$("#tProfiles>tbody>tr").each(function(){
		var profile_name = this.children[0].innerHTML;
		var pg_number = this.children[1].innerHTML;
		var plugin_name = this.children[2].innerHTML;
		var plugin_path = this.children[3].innerHTML;
		var profile_data = this.children[4].innerHTML;
		var profile_item = {
			"profile_name":profile_name,
			"pg_number":pg_number,
			"plugin_name":plugin_name,
			"plugin_path":plugin_path,
			"profile_data":profile_data,
		}
		cluster_profile_data.profiles.push(profile_item);
	});

	var token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
        type: "post",
        url: "/manifest/set_cluster_profile_file/",
        data: JSON.stringify(cluster_profile_data),
        dataType:"json",
        success: function(data){
        	ShowMessage($("#divProfileMessage"),2,"Save the cluster profile info. successfully!");
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
           if(XMLHttpRequest.status == 500){
           		ShowMessage($("#divProfileMessage"),0,"INTERNAL SERVER ERROR!");
           }
        },
        headers: {
            "X-CSRFToken": token
        },
        complete: function(){

        }
    });
}

function SaveClusterCache(){
	var is_pass = true;
	var txt_cache_list = $(".txt-cache");
	for(var i=0;i<txt_cache_list.length;i++){
		var ctrl = txt_cache_list[i];
		if(ctrl.value == ""){
			ctrl.style.border = "1px solid red";
			is_pass = false
		}
		else{
			ctrl.style.border = "1px solid #ccc";
		}
	}

	$("#divCacheMessage").empty();
	if(is_pass == false){
		ShowMessage($("#divCacheMessage"),1,"the cache item should not be empty!");
		return false;
	}

	var cluster_cache_data = {
		"ct_hit_set_count":$("#txt_ct_hit_set_count").val(),
		"ct_hit_set_period_s":$("#txt_ct_hit_set_period_s").val(),
		"ct_target_max_objects":$("#txt_ct_target_max_objects").val(),
		"ct_target_max_mem_mb":$("#txt_ct_target_max_mem_mb").val(),
		"ct_target_dirty_ratio":$("#txt_ct_target_dirty_ratio").val(),
		"ct_target_full_ratio":$("#txt_ct_target_full_ratio").val(),
		"ct_target_min_flush_age_m":$("#txt_ct_target_min_flush_age_m").val(),
		"ct_target_min_evict_age_m":$("#txt_ct_target_min_evict_age_m").val(),
	}

	var token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
        type: "post",
        url: "/manifest/set_cluster_cache_file/",
        data: JSON.stringify(cluster_cache_data),
        dataType:"json",
        success: function(data){
        	ShowMessage($("#divCacheMessage"),2,"Save the cluster cache info. successfully!");
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
           if(XMLHttpRequest.status == 500){
           		ShowMessage($("#divCacheMessage"),0,"INTERNAL SERVER ERROR!");
           }
        },
        headers: {
            "X-CSRFToken": token
        },
        complete: function(){

        }
    });
}

function SaveClusterSettings(){
	var is_pass = true;
	var txt_settings_list = $(".txt-settings");
	for(var i=0;i<txt_settings_list.length;i++){
		var ctrl = txt_settings_list[i];
		if(ctrl.value == ""){
			ctrl.style.border = "1px solid red";
			is_pass = false
		}
		else{
			ctrl.style.border = "1px solid #ccc";
		}
	}

	$("#divSettingMessage").empty();
	if(is_pass == false){
		ShowMessage($("#divSettingMessage"),1,"the settings item should not be empty!");
		return false;
	}

	var cluster_settings_data = {
		"storage_group_near_full_threshold":$("#txt_storage_group_near_full_threshold").val(),
		"storage_group_full_threshold":$("#txt_storage_group_full_threshold").val(),
		"ceph_near_full_threshold":$("#txt_ceph_near_full_threshold").val(),
		"ceph_full_threshold":$("#txt_ceph_full_threshold").val(),
		"pg_count_factor":$("#txt_pg_count_factor").val(),
		"heartbeat_interval":$("#txt_heartbeat_interval").val(),
		"osd_heartbeat_interval":$("#txt_osd_heartbeat_interval").val(),
		"osd_heartbeat_grace":$("#txt_osd_heartbeat_grace").val(),
		"disk_near_full_threshold":$("#txt_disk_near_full_threshold").val(),
		"disk_full_threshold":$("#txt_disk_full_threshold").val(),
	}

	var token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
        type: "post",
        url: "/manifest/set_cluster_settings_file/",
        data: JSON.stringify(cluster_settings_data),
        dataType:"json",
        success: function(data){
        	ShowMessage($("#divSettingMessage"),2,"Save the cluster settings info. successfully!");
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
           if(XMLHttpRequest.status == 500){
           		ShowMessage($("#divSettingMessage"),0,"INTERNAL SERVER ERROR!");
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

//add the storage group
function AddProfileGroup(){
	var html = "";
	html += "<tr class='profile-row'>";
	// html += "<form class='form-inline'>";
	html += "	<td><input class='form-control' type='textbox'/></td>";
	html += "	<td><input class='form-control' type='textbox' /></td>";
	html += "	<td><input class='form-control' type='textbox' /></td>";
	html += "	<td><input class='form-control' type='textbox' /></td>";
	html += "	<td><input class='form-control' type='textbox' /></td>";
	html += "	<td>";
	html += "		<a class='btn btn-success'  onclick='SaveProfileGroup(this)'>save</a>";
	html += "	    <a class='btn btn-danger'  onclick='RemoveProfile(this)'>cancel</a>";
	html += "	</td>";
	// html += "</form>";
	html += "</tr>";

	$("#tProfiles>tbody").append(html);
}

//save the profile group
function SaveProfileGroup(obj){
	var ctrlProfileName= obj.parentNode.parentNode.children[0].children[0];
	var ctrPGNumber= obj.parentNode.parentNode.children[1].children[0];
	var ctrPluginName= obj.parentNode.parentNode.children[2].children[0];
	var ctrlPluginPath= obj.parentNode.parentNode.children[3].children[0];
	var ctrlPluginData= obj.parentNode.parentNode.children[4].children[0];

	var is_pass = true;
	if(ctrlProfileName.value == ""){
		ctrlProfileName.style.border = "1px solid red";
		is_pass = false;
	}

	if(ctrPGNumber.value == ""){
		ctrPGNumber.style.border = "1px solid red";
		is_pass = false;
	}

	if(ctrPluginName.value == ""){
		ctrPluginName.style.border = "1px solid red";
		is_pass = false;
	}

	if(ctrlPluginPath.value == ""){
		ctrlPluginPath.style.border = "1px solid red";
		is_pass = false;
	}

	if(ctrlPluginData.value == ""){
		ctrlPluginData.style.border = "1px solid red";
		is_pass = false;
	}

	if(is_pass == false){
		return false;
	}

	//save the items
	var html = "";
	html += "<tr class='profile-row'>";
	html += "	<td>"+ctrlProfileName.value+"</td>";
	html += "	<td>"+ctrPGNumber.value+"</td>";
	html += "	<td>"+ctrPluginName.value+"</td>";
	html += "	<td>"+ctrlPluginPath.value+"</td>";
	html += "	<td>"+ctrlPluginData.value+"</td>";
	html += "	<td><a class='btn btn-danger' onclick='RemoveProfile(this)'>remove</a></td>";
	html += "</tr>";

	//first remove the row
	obj.parentNode.parentNode.remove();
	$("#tProfiles>tbody").append(html);	
}

//remove the ec_profile
function RemoveProfile(obj){
	if(confirm("Remove the profile?")==true){
		obj.parentNode.parentNode.remove();
	}
}

//see the ec_profile detail
// function InitProfileDetail(){
// 	//prepend
// 	var profile_rows = $(".profile-row");
// 	for(var i=0;i<profile_rows.length;i++){
// 		var detail_html = "";
// 		detail_html += "<div class='profile-detail'>";
// 		detail_html += "	<label>profile name:</label>";
// 		detail_html += "	<span>"+profile_rows[i].children[0].innerHTML+"</span>";
// 		detail_html += "	<br>";
// 		detail_html += "	<label>pg number:</label>";
// 		detail_html += "	<span>"+profile_rows[i].children[2].innerHTML+"</span>";
// 		detail_html += "	<br>";
// 		detail_html += "	<label>plugin name:</label>";
// 		detail_html += "	<span>"+profile_rows[i].children[1].innerHTML+"</span>";
// 		detail_html += "	<br>";
// 		detail_html += "	<label>profile path:</label>";
// 		detail_html += "	<span>"+profile_rows[i].children[3].innerHTML+"</span>";
// 		detail_html += "	<br>";
// 		// detail_html += "	<label>data:</label>";
// 		// detail_html += "	<span><em>"+profile_rows[i].children[4].innerHTML+"</em></span>";
// 		// detail_html += "	<br>";
// 		detail_html += "</div>";



// 		var html_btnProfileDetail = GenerateProfileDetailButton("Profile Detail",detail_html);
// 		profile_rows[i].children[5].innerHTML = "";
// 		profile_rows[i].children[5].innerHTML += html_btnProfileDetail;
// 		profile_rows[i].children[5].innerHTML += "<a class='btn btn-danger' onclick='RemoveProfile(this)'>remove</a>";
// 		var data_html = "<em>"+profile_rows[i].children[4].innerHTML+"</em>"
// 		console.log(data_html);
// 	}

// 	//register the popover
//     $("a[data-toggle=popover]").popover();
// }




// function GenerateProfileDetailButton(popover_title,popover_content){
// 	var html = "";
// 		html += "<a class='btn btn-success' tabindex='0' ";
// 		html += " role='button' ";
// 		html += " data-toggle='popover' ";
// 		html += " data-container='body' ";
// 		html += " data-placement='left' ";
// 		html += " data-trigger='click' ";
// 		html += " data-html='true' ";
// 		html += " onblur='HidePopover()' ";
// 		html += " title='"+popover_title+"' ";
// 		html += " data-content=\""+popover_content+"\">";
// 		html += "detail";
// 		html += "</a>";
// 	return html;
// }


// function HidePopover(){
// 	$(".popover").popover("hide");
// }

