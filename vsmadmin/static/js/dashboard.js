/**
 * Created by shouanxx on 3/26/2015.
 */

require.config({
    paths:{
        echarts:"static/js/echarts",
    }
});

var cThroughput;
var cLatency;
var cClusterGague;
require(
    [
        'echarts',
        'echarts/chart/line',
        'echarts/chart/bar',
        'echarts/chart/pie',
        'echarts/chart/gauge'
    ],
    function(ec){
        cIOPs = ec.init(document.getElementById('divIOPsContent'));
        cLatency = ec.init(document.getElementById('divLatencyContent'));
        cClusterGague = ec.init(document.getElementById('divClusterGauge'));
        cIOPs.setOption(GenerateLineOption());
        cLatency.setOption(GetAreaLineOption());
        cClusterGague.setOption(GenerateGaugeOption());

        var CapcityInterval = setInterval(function(){
            $.ajax({
            type: "get",
            url: "/dashboard/ajax_capcity/",
            data: null,
            dataType:"json",
            success: function(data){
                    option.series[0].data[0].value = data.value;
                    cClusterGague.setOption(option, true);
                }
            });
        },2000);


        var IOPsInterval = setInterval(function (){
            $.ajax({
                type: "get",
                url: "/dashboard/ajax_IOPs/",
                data: null,
                dataType: "json",
                success: function (data) {
                    var axisData = (new Date()).toLocaleTimeString().replace(/^\D*/, '');
                    var line1Data =  [0,data.line1, false, false, axisData];
                    var line2Data =  [1,data.line2, false, false, axisData];

                    // 动态数据接口 addData
                    cIOPs.addData([line1Data,line2Data]);
                }
            });
        }, 2000);
    }

);


$(document).ready(function(){
    //loadVSMStatus();
    //loadOSD();
    //loadMonitor();
    //loadMDS();
    //loadStorage();

    $("#btnAlert").click(function(){
        $("#divAlert").alert("close");
    });

})


function loadVSMStatus(){
    setInterval(function() {
        $.ajax({
            type: "get",
            url: "/dashboard/ajax_vsm_status/",
            data: null,
            dataType: "json",
            success: function (data) {
                var statusTip = "";
                var statusClass = "";
                var noteClass = "";

                switch (data.status) {
                    case 0: //health
                        statusTip = "health";
                        statusClass = "btn btn-success";
                        noteClass = "alert alert-success";
                        break;
                    case 1: //warning
                        statusTip = "warning";
                        statusClass = "btn btn-warning";
                        noteClass = "alert alert-warning";
                        break;
                    case 2: //error
                        statusTip = "error";
                        statusClass = "btn btn-danger";
                        noteClass = "alert alert-danger";
                        break;
                }

                $("#btnClusterTip")[0].innerText = statusTip;
                $("#btnClusterTip")[0].className = statusClass;
                $("#divClusterContent")[0].innerHTML = data.note;
                $("#divClusterContent")[0].className = noteClass;
            }
        });
    },2000);
}

function loadOSD(){
    setInterval(function(){
        $.ajax({
        type: "get",
        url: "/dashboard/ajax_OSD/",
        data: null,
        dataType:"json",
        success: function(data){
            $("#lblOSDEpoch")[0].innerText ="Epoch:"+ data.epoch;
            $("#lblOSDUpdate")[0].innerText ="Update:"+ data.update;
            $("#divOSD_INUP")[0].innerText = data.in_up;
            $("#divOSD_INDOWN")[0].innerText = data.in_down;
            $("#divOSD_OUTUP")[0].innerText = data.out_up;
            $("#divOSD_OUTDOWN")[0].innerText = data.out_down;
        }
        });
    },2000);
}

function loadMonitor(){
    setInterval(function(){
        $.ajax({
            type: "get",
            url: "/dashboard/ajax_Monitor/",
            data: null,
            dataType:"json",
            success: function(data){
                $("#lblMonitorEpoch")[0].innerText ="Epoch:"+ data.epoch;
                $("#lblMonitorUpdate")[0].innerText ="Update:"+ data.update;

                var rect =null;
                $("#divMonitorRect").empty();
                for(var i=0;i<data.monitors.length;i++) {
                    if (i == data.selMonitor)
                        rect = "<div class='vsm-rect vsm-rect-1 vsm-rect-green'>"+data.monitors[i]+"</div>";
                    else
                        rect = "<div class='vsm-rect vsm-rect-1'>"+data.monitors[i]+"</div>";
                    $("#divMonitorRect").append(rect);
                }
            }
     });
    },2000);
}

function loadMDS(){
    setInterval(function(){
        $.ajax({
            type: "get",
            url: "/dashboard/ajax_MDS/",
            data: null,
            dataType:"json",
            success: function(data){
                $("#lblMDSEpoch")[0].innerText ="Epoch:"+ data.epoch;
                $("#lblMDSUpdate")[0].innerText ="Update:"+ data.update;

                var rect =null;
                $("#divMDSRect").empty();
                for(var i=0;i<data.MDS.length;i++) {
                    if (i == data.selMDS)
                        rect = "<div class='vsm-rect vsm-rect-1 vsm-rect-green'>"+data.MDS[i]+"</div>";
                    else
                        rect = "<div class='vsm-rect vsm-rect-1'>"+data.MDS[i]+"</div>";
                    $("#divMDSRect").append(rect);
                }
            }
     });
    },2000);
}

function loadStorage(){
    setInterval(function(){
        $.ajax({
            type: "get",
            url: "/dashboard/ajax_Storage/",
            data: null,
            dataType:"json",
            success: function(data){
                $("#lblStorageNearFull")[0].innerHTML = data.nearfull;
                $("#lblStorageFull")[0].innerHTML = data.full;
            }
     });
    },2000);
}

function GenerateLineOption(){
   var option = {
        tooltip : {
            trigger: 'axis'
        },
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data :(function () {
                    var now = new Date();
                    var res = [];
                    var len = 10;
                    while (len--) {
                        res.unshift(now.toLocaleTimeString().replace(/^\D*/, ''));
                        now = new Date(now - 2000);
                    }
                    return res;
                })()
            }
        ],
        yAxis : [
            {
                type : 'value',
                min:0,
                max:15,
                axisLabel : {
                    formatter: '{value}'
                }
            }
        ],
        grid: {
            x:30,
            y:20,
            x2:30,
            y2:40,

        },
        series : [
            {
                name:'',
                type:'line',
                data:(function () {
                    var res = [];
                    var len = 10;
                    while (len--) {
                        res.push(0);
                    }
                    return res;
                })()
            },
            {
                name:'',
                type:'line',
                data:(function () {
                    var res = [];
                    var len = 10;
                    while (len--) {
                        res.push(0);
                    }
                    return res;
                })()
            },
        ]
    };
    return option;
}

function GenerateGaugeOption() {
    option = {
        tooltip: {
            formatter: "{a} <br/>{b} : {c}%"
        },
        series: [
            {
                name: '',
                type: 'gauge',
                detail: {formatter: '{value}%'},
                data: [{value: 0, name: 'Capcity'}],
                splitLine:{
                    show: true,
                    length :5,
                    lineStyle: {
                        color: '#0062a8',
                        width: 1,
                        type: 'solid'
                    }
                },
                axisLine:{
                    show: true,
                    lineStyle: {
                        color: [
                            [0.2, '#228b22'],
                            [0.8, '#48b'],
                            [1, '#ff4500']
                        ],
                        width: 10,
                    }
                },
                axisTick:{
                    show: true,
                    splitNumber: 5,
                    length :5,
                    lineStyle: {
                        color: '#eee',
                        width: 1,
                        type: 'solid'
                    }
                },
                radius:['30%', '95%'],
                center:['55%','50%']
            }
        ],
    };

    return option;
}

function GetAreaLineOption(){
    option = {
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : ['周一','周二','周三','周四','周五','周六','周日']
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
         grid: {
            x:30,
            y:20,
            x2:30,
            y2:40,
        },
        series : [
            {
                name:'邮件营销',
                type:'line',
                stack: '总量',
                itemStyle: {normal: {areaStyle: {type: 'default'}}},
                data:[120, 132, 101, 134, 90, 230, 210]
            },
            {
                name:'联盟广告',
                type:'line',
                stack: '总量',
                itemStyle: {normal: {areaStyle: {type: 'default'}}},
                data:[220, 182, 191, 234, 290, 330, 310]
            },
            {
                name:'视频广告',
                type:'line',
                stack: '总量',
                itemStyle: {normal: {areaStyle: {type: 'default'}}},
                data:[150, 232, 201, 154, 190, 330, 410]
            },
            {
                name:'直接访问',
                type:'line',
                stack: '总量',
                itemStyle: {normal: {areaStyle: {type: 'default'}}},
                data:[320, 332, 301, 334, 390, 330, 320]
            },
            {
                name:'搜索引擎',
                type:'line',
                stack: '总量',
                itemStyle: {normal: {areaStyle: {type: 'default'}}},
                data:[820, 932, 901, 934, 1290, 1330, 1320]
            }
        ]
    };
    return option;
}


//clearInterval(timeTicket);
//    timeTicket = setInterval(function () {
//        option.series[0].data[0].value = (Math.random() * 100).toFixed(2) - 0;
//        myChart.setOption(option, true);
//    }, 2000);










