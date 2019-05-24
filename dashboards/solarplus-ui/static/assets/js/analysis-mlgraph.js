$(document).ready(function () {

    function consumption(value) {
        return (value);
    }

    function renderChart(predictedSolarVals, tempVals, daysArray) {
        var highChart = new Highcharts.chart('predictionChart', {
            chart: {
                //type: 'line',
                zoomType: "xy"
            },
            title: {
                text: 'Predicted Solar production values'
            },
            tooltip: {
                valueSuffix: '\xB0C'
            },
            xAxis: {
                categories: daysArray,
                crosshair: true
            },
            yAxis: [
            {
                labels: {
                    format:  '{value}°C'
                },
                opposite: true,
                title: {
                    text: 'Forecast Temperature'
                },
                plotLines:[{
                    values: 0
                }]
            },
            {
                labels: {
                    format: '{value} kWh'
                },
                title: {
                    text: 'Power Production'
                }
            }],
            tooltip: {
                shared: true
            },
            series: [
                {
                    name: "Forecast Temperature",
                    type: 'column',
                    data: tempVals,
                    tooltip: {
                        valueSuffix: '°C'
                    }
                },
                {
                    name: 'Solar Power values',
                    type: 'spline',
                    yAxis: 1,
                    data: predictedSolarVals,
                    tooltip: {
                        valueSuffix: ' kWh'
                    }
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
        var forecast_TempVals = sessionStorage.getItem("temperatureVals");
        forecast_TempVals = JSON.parse(forecast_TempVals);
        console.log("Printing vals from weather tab");
        console.log(forecast_TempVals);

        //var tempVals = [14,19,18,17,18,20,22];
        const uri_chart1 = 
            `http://127.0.0.1:5000/analysis/MLModel/${forecast_TempVals[0]}/${forecast_TempVals[1]}/${forecast_TempVals[2]}/${forecast_TempVals[3]}/${forecast_TempVals[4]}/${forecast_TempVals[5]}/${forecast_TempVals[6]}`;
        var res_chart1 = JSON.parse(Get(uri_chart1));
        console.log(res_chart1);

        var d = new Date();
        var today = d.getDay();
        var days = [];

        for(let j = 0; j < 7; j++)
        {
            switch(today){
                case 0: days[j] = "Mon";
                    break;
                case 1: days[j] = "Tues";
                    break;
                case 2: days[j] = "Wed";
                    break;
                case 3: days[j] = "Thu";
                    break;
                case 4: days[j] = "Fri";
                    break;
                case 5: days[j] = "Sat";
                    break;
                case 6: days[j] = "Sun";
                    break;          
            }
            if( today == 6)
                today = 0;
            else
                today = today+1;
        }
        
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
        renderChart(predictedSolarVals, forecast_TempVals, days);
        
    }
    graphData_MLModel();
});