$(document).ready(function () {

    function consumption(value) {
        return (value);
    }

    function renderChart1(yVals, yValsTitle, dates) {
        var highChart = new Highcharts.chart('chart1', {
            chart: {
                type: 'line',
                zoomType: "x"
            },
            title: {
                text: 'Total Power Consumption'
            },
            tooltip: {
                valueSuffix: ' kWh'
            },
            xAxis: {
                categories: dates
            },
            yAxis: {
                title: {
                    text: 'Consumption'
                },
                plotLines: [{
                    value: 0
                }],
                labels: {
                    format: '{value} kWh'
                }
            },
            series: [{
                    name: yValsTitle,
                    data: yVals
                }
            ]

        });
    }
    function renderChart2(feature1, feature2, feature1Vals, feature2Vals, dates) {
        var highChart = new Highcharts.chart('chart2', {
            chart: {
                //renderTo: "myChart",
                type: 'column',
                zoomType: "x"
            },
            title: {
                text: 'HVAC Power Consumption'
            },
            tooltip: {
                valueSuffix: ' kWh'
            },
            xAxis: {
                categories: dates
            },
            yAxis: {
                title: {
                    text: 'Consumption'
                },
                plotLines: [{
                    value: 0
                }],
                labels: {
                    format: '{value} kWh'
                }
            },
            series: [{
                    name: feature1,
                    data: feature1Vals
                },
                {
                    name: feature2,
                    data: feature2Vals
                }
            ]

        });
    }
    function renderChart3(feature1, feature2, feature1Vals, feature2Vals, dates) {
        var highChart = new Highcharts.chart('chart3', {
            chart: {
                //renderTo: "myChart",
                type: 'line',
                zoomType: "x"
            },
            title: {
                text: 'Power Consumption'
            },
            tooltip: {
                valueSuffix: ' kWh'
            },
            xAxis: {
                categories: dates
            },
            yAxis: {
                title: {
                    text: 'Consumption'
                },
                plotLines: [{
                    value: 0
                }]
            },
            series: [{
                    name: feature1,
                    data: feature1Vals
                },
                {
                    name: feature2,
                    data: feature2Vals
                }
            ]

        });
    }
    function renderChart4(yVals, yValsTitle, dates) {
        var highChart = new Highcharts.chart('chart4', {
            chart: {
                type: 'line',
                zoomType: "x"
            },
            title: {
                text: 'Total Power Generated'
            },
            tooltip: {
                valueSuffix: ' kWh'
            },
            xAxis: {
                categories: dates
            },
            yAxis: {
                title: {
                    text: 'Power Generated'
                },
                plotLines: [{
                    value: 0
                }],
                labels: {
                    format: '{value} kWh'
                }

            },
            series: [{
                    name: yValsTitle,
                    data: yVals
                }
            ]

        });
    }

    function Get(yourUrl) {
        var Httpreq = new XMLHttpRequest(); // a new request
        Httpreq.open("GET", yourUrl, false);
        Httpreq.send(null);
        return Httpreq.responseText;
    }

    function graphDataCollection_Chart1() {

        // will have to include code here about fetching data from the 
        // selected features for the specific features on dashboard
        const feature = 'Building'
        const uri_chart1 = `http://127.0.0.1:5000/dashboard/access/${feature}`;
        var res_chart1 = JSON.parse(Get(uri_chart1));
        
        var buildingVals = [];
        labels = [];
        
        //res_chart1.length
        for (let i = 0; i < 500; i++) {
        
            let singleElement = res_chart1[i];
            //console.log(singleElement);
        
            for (let prop in singleElement) {
                if (prop == 'Building')
                {
                    buildingVals.push(singleElement[prop]);
                }
                labels.push(res_chart1[i].Time);
            }           
        }
        renderChart1(buildingVals, 'Total Power Consumption Values', labels);

    }
    function graphDataCollection_Chart2() {

        // will have to include code here about fetching data from the 
        // selected features for the specific features on dashboard
        //const feature = 'Building'
        const uri_chart1 = `http://127.0.0.1:5000/dashboard/access/HVAC1/HVAC2`;
        var res_chart1 = JSON.parse(Get(uri_chart1));
        
        var feature1Vals = [];
        var feature2Vals = []
        var labels = [];
        
        //res_chart1.length
        for (let i = 0; i < 500; i++) {

            let singleElement = res_chart1[i];

            for (let prop in singleElement) {
                if (prop == 'HVAC1')
                    feature1Vals.push(singleElement[prop]);
                if (prop == 'HVAC2')
                    feature2Vals.push(singleElement[prop]);
            }
            labels.push(res_chart1[i].Time);

        }
        renderChart2('HVAC1', 'HVAC2', feature1Vals, feature2Vals, labels);

    }

    function graphDataCollection_Chart4() {

        // will have to include code here about fetching data from the 
        // selected features for the specific features on dashboard
        //const feature = 'Building'
        const uri_chart1 = `http://127.0.0.1:5000/dashboard/PVPowerGenData`;
        var res_chart1 = JSON.parse(Get(uri_chart1));
        
        var PVGenVals = [];
        labels = [];
        
        //res_chart1.length
        for (let i = 0; i < 500; i++) {
        
            let singleElement = res_chart1[i];
            //console.log(singleElement);
        
            for (let prop in singleElement) {
                if (prop == 'PVPower_kW')
                {
                    PVGenVals.push(singleElement[prop]);
                }
                labels.push(res_chart1[i].Date_PT);
            }           
        }
        renderChart4(PVGenVals, 'Total Power Generated Values', labels);

    }

    graphDataCollection_Chart1();
    graphDataCollection_Chart2();
    graphDataCollection_Chart4();

});