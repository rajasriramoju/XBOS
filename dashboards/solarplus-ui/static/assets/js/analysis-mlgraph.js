$(document).ready(function () {

    function consumption(value) {
        return (value);
    }

    function renderChart(feature1, feature2, feature1Vals, feature2Vals, dates) {
        var highChart = new Highcharts.chart('predictionChart', {
            chart: {
                //renderTo: "myChart",
                type: 'line',
                zoomType: "x"
            },
            title: {
                text: 'Power Consumption'
            },
            tooltip: {
                valueSuffix: '\xB0C'
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

    function Get(yourUrl) {
        var Httpreq = new XMLHttpRequest(); // a new request
        Httpreq.open("GET", yourUrl, false);
        Httpreq.send(null);
        return Httpreq.responseText;
    }

    function graphData_MLModel() {

        var forecast_TempVals = localStorage.getItem("tempVals");
        forecast_TempVals = JSON.parse(forecast_TempVals);
        console.log(forecast_TempVals)

        var tempVals = [15,19,18,17,18,20,22];
        const uri_chart1 = `http://127.0.0.1:5000/analysis/MLModel/${tempVals}`;
        var res_chart1 = JSON.parse(Get(uri_chart1));
        
        /*
        var feature1Vals = [];
        var feature2Vals = []
        var labels = [];
        
        //res_chart1.length
        for (let i = 0; i < 1000; i++) {

            let singleElement = res_chart1[i];

            for (let prop in singleElement) {
                if (prop == 'HVAC2')
                    feature2Vals.push(singleElement[prop]);
            }
            labels.push(res_chart1[i].Time);

        }
        renderChart('HVAC1', 'HVAC2', feature1Vals, feature2Vals, labels);
        */
    }
    graphData_MLModel();
});