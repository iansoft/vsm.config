$(document).ready(function(){
	$("#btnSaveCluster").show();
	$("#btnSaveServer").hide();
	$("#btnGenerateManifest").show();
	$("#btnInstaller").show();
});

var _INDEX_TAB = "";
var _GROUP_NAME_LIST = new Array();

//save server
function SaveServer(){
	var server_data = {
		server_ip:"",
		role:"",
		auth_key:"",
		path_data:[]
	};

	server_data.server_ip = $("#node_"+_INDEX_TAB).find("#txtServerIP").val();
	server_data.role = $("#node_"+_INDEX_TAB).find("#selRole").val();
	server_data.auth_key = $("#node_"+_INDEX_TAB).find("#txtAuthKey").val();

	for(var i=0;i<_GROUP_NAME_LIST.length;i++){
		var group_name = _GROUP_NAME_LIST[i];
		var table_name = "t_"+_GROUP_NAME_LIST[i]+"_"+_INDEX_TAB;

		var str_json_sg_path = "{\""+group_name+"\":[";
		
		if($("#"+table_name+">tbody>tr").length != 0){
			$("#"+table_name+">tbody>tr").each(function(index){
				var device_path = this.children[0].innerHTML;
				var journal_path = this.children[1].innerHTML;

				str_json_sg_path += "{\"device_path\":\""+device_path+"\",\"journal_path\":\""+journal_path+"\"},";
			});
			str_json_sg_path = str_json_sg_path.substring(0,str_json_sg_path.length-1);
		}

		str_json_sg_path +="]}";
		
		var json_sg_path = JSON.parse(str_json_sg_path);
		server_data.path_data.push(json_sg_path);
	}

	console.log(server_data)


	var token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
        type: "post",
        url: "/manifest/set_cluster_server_file/",
        data: JSON.stringify(server_data),
        dataType:"json",
        success: function(data){
        	ShowMessage($("#node_"+_INDEX_TAB).find("#divServerMessage"),2,"Save the server【"+server_data.server_ip+"】 successfully!");
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
           if(XMLHttpRequest.status == 500){
           		ShowMessage($("#node_"+_INDEX_TAB).find("#divServerMessage"),0,"Save the server【"+server_data.server_ip+"】 failed!");
           }
        },
        headers: {
            "X-CSRFToken": token
        },
        complete: function(){

        }
    });
}


function SelecteClusterTab(){
	$("#btnSaveCluster").show();
	$("#btnSaveServer").hide();
}

function SelecteTab(tabIndex){
	$("#btnSaveCluster").hide();
	$("#btnSaveServer").show();

	_INDEX_TAB = tabIndex;
	$("#node_"+_INDEX_TAB).find("#divServerMessage").empty();
	var server_ip = $("#link_node_"+tabIndex)[0].innerHTML;

	InitStorageGroup(tabIndex,server_ip);
}

function InitStorageGroup(tabIndex,server_ip){
	var token = $("input[name=csrfmiddlewaretoken]").val();
	$.ajax({
        type: "post",
        url: "/manifest/read_server_manifest/",
        data: JSON.stringify({"server_ip":server_ip}),
        dataType:"json",
        success: function(data){
        	_GROUP_NAME_LIST.length = 0;
        	for(var key in data){
        		if(key == "role" || key == "server_ip" || key == "auth_key"){
        			continue;
        		}
        		_GROUP_NAME_LIST.push(key);
			}

			//get the basic info.
			$("#node_"+tabIndex).find("#txtServerIP").val(data.server_ip);
			$("#node_"+tabIndex).find("#txtAuthKey").val(data.auth_key);
			$("#node_"+tabIndex).find("#selRole").val(data.role);

        	var servers_path_container = $(".server-path-container");
        	servers_path_container[tabIndex].innerHTML = GenerateStorageGroupHTML(tabIndex,_GROUP_NAME_LIST,data);
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

function GenerateStorageGroupHTML (tabIndex,groupNameList,dataSource) {
	var htmlStorageGroup = "";
	for(var i=0;i<groupNameList.length;i++){
		htmlStorageGroup += "<div>";
		htmlStorageGroup += "	<span class='module-title'>"+groupNameList[i]+"</span>";
		htmlStorageGroup += "<hr>";

		htmlStorageGroup += "<div class='option-bar'>";
		htmlStorageGroup += "	<a id='btn_"+groupNameList[i]+"_"+tabIndex+"' onclick='AddServerPath("+tabIndex+",\""+groupNameList[i]+"\")' class='btn btn-primary btn-right'>Add Path</a>";
		htmlStorageGroup += "</div>";

		htmlStorageGroup += "	<table id='t_"+groupNameList[i]+"_"+tabIndex+"' class='table table-bordered table-server-path'>";
		htmlStorageGroup += "		<thead>";
		htmlStorageGroup += "			<tr >";
		htmlStorageGroup += "				<th >device path</th>";
		htmlStorageGroup += "				<th >journal path</th>";
		htmlStorageGroup += "				<th style='width:150px;'></th>";
		htmlStorageGroup += "			</tr>";
		htmlStorageGroup += "		</thead>";
		htmlStorageGroup += "		<tbody>";

		for(var j=0;j<dataSource[groupNameList[i]].length;j++){
				htmlStorageGroup += "			<tr>";
				htmlStorageGroup += "				<td>"+dataSource[groupNameList[i]][j].device_path+"</td>";
				htmlStorageGroup += "				<td>"+dataSource[groupNameList[i]][j].journal_path+"</td>";
				htmlStorageGroup += "				<td style='text-align:center'><a class='btn btn-danger' onclick='RemoveServerPath(this)'>remove</a></td>";
				htmlStorageGroup += "			</tr>";
		}

		htmlStorageGroup += "		</tbody>";
		htmlStorageGroup += "	</table>";
		htmlStorageGroup += "</div>";
	}

	return htmlStorageGroup;
}

function AddServerPath(tabIndex,groupName){
	var html = "";
	html += "<tr>";
	html += "	<td><input class='form-control' type='textbox'/></td>";
	html += "	<td><input class='form-control' type='textbox'/></td>";
	html += "	<td>";
	html += "		<a class='btn btn-success'  onclick=\"SaveServerPath(this,'"+tabIndex+"','"+groupName+"')\">save</a>";
	html += "	    <a class='btn btn-danger'  onclick='RemoveServerPath(this)'>cancel</a>";
	html += "	</td>";
	html += "</tr>";

	var table_name = "t_"+groupName+"_"+tabIndex;
	$("#"+table_name+">tbody").append(html);
}


//save the profile group
function SaveServerPath(obj,tabIndex,groupName){
	var ctrlDevicePath= obj.parentNode.parentNode.children[0].children[0];
	var ctrlJournalPath= obj.parentNode.parentNode.children[1].children[0];

	var is_pass = true;
	if(ctrlDevicePath.value == ""){
		ctrlDevicePath.style.border = "1px solid red";
		is_pass = false;
	}

	if(ctrlJournalPath.value == ""){
		ctrlJournalPath.style.border = "1px solid red";
		is_pass = false;
	}

	if(is_pass == false){
		return false;
	}

	//save the items
	var html = "";
	html += "<tr class='profile-row'>";
	html += "	<td>"+ctrlDevicePath.value+"</td>";
	html += "	<td>"+ctrlJournalPath.value+"</td>";
	html += "	<td style='text-align:center'><a class='btn btn-danger' onclick='RemoveProfile(this)'>remove</a></td>";
	html += "</tr>";

	//first remove the row
	obj.parentNode.parentNode.remove();
	var table_name = "t_"+groupName+"_"+tabIndex;
	$("#"+table_name+">tbody").append(html);
}


//remove the storage class
function RemoveServerPath(obj){
	if(confirm("Remove the server path?")==true){
		obj.parentNode.parentNode.remove();
	}
}
