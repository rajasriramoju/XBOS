$(document).ready(function () {

    function consumption(value) {
        return (value);
    }

    function renderChart(feature1, feature1Vals, dates) {
        var highChart = new Highcharts.chart('predictionChart', {
            chart: {
                type: 'line',
                zoomType: "x"
            },
            title: {
                text: 'Predicted Solar production values'
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

        // TODO: have to extract daily values instead of static ones for now
        //var forecast_TempVals = localStorage.getItem("tempVals");
        //forecast_TempVals = JSON.parse(forecast_TempVals);
        //console.log(forecast_TempVals)

        var tempVals = [15,19,18,17,18,20,22];
        const uri_chart1 = `http://127.0.0.1:5000/analysis/MLModel/15/19/18/17/18/20/22`;
        var res_chart1 = JSON.parse(Get(uri_chart1));
        console.log(res_chart1);
        
        var predictedSolarVals = [];
        var labels = [];
        
        //res_chart1.length
        for (let i = 0; i < 7; i++) {

            let singleElement = res_chart1[i];

            for (let prop in singleElement) {
                if (prop == 'Column1')
                predictedSolarVals.push(singleElement[prop]);
            }
        }
        renderChart('Solar power values', predictedSolarVals, tempVals);
        
    }
    graphData_MLModel();
});