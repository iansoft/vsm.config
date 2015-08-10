var datasource = {
    basic:{
        cluster:"cluster name",
        file_system:"file system",
        management_addr:"management address",
        ceph_public_addr:"ceph public address",
        ceph_cluster_addr:"ceph cluster address"
    },
    storage:{
        classes:["ssd","10krpm_sas","7200_rpm_sata"],
        groups:[
            {name:"Group Name A",nickname:"Nick A",class:"ssd"},
            {name:"Group Name B",nickname:"Nick B",class:"ssd"},
        ],
    },
    Profiles:[
        {name:"Profile Name A",plugin:"plugin A",path:"path A",pg_num:"3",data:"data..."},
        {name:"Profile Name B",plugin:"plugin B",path:"path B",pg_num:"3",data:"data..."},
        {name:"Profile Name C",plugin:"plugin C",path:"path C",pg_num:"3",data:"data..."},
    ],
    Settings:{
        storage_group_near_full_threshold:"123",
        storage_group_full_threshold:"123",
        ceph_near_full_threshold:"123",
        ceph_full_threshold:"123",
        pg_count_factor:"123",
        hearbeat_interval:"123",
        osd_hearbeat_interval:"123",
        osd_hearbeat_grace:"123",
        disk_near_full_threshold:"123",
        disk_full_threshold:"123",
    },
    Cache:{
        ct_hit_set_count:"1",
        ct_hit_set_period:"2",
        ct_target_max_objects:"3",
        ct_target_max_mem_mb:"4",
        ct_target_dirty_ratio:"5",
        ct_target_full_ratio:"6",
        ct_target_min_flush_age_m:"7",
        ct_target_min_evict_age_m:"8",
    }
}

$(document).ready(function(){
    var strJSON = JSON.stringify(datasource);
    var data = JSON.parse(strJSON);

    console.log(strJSON);
    console.log(data);
})