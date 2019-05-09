/*dashboard-graphs.js*/
$(document).ready(function() {

        function consumption(value){
        return (value);
    }

    function renderChart(buildingVals, dates) {
        var highChart = new Highcharts.chart('Chart1',{
            chart: {
                type: 'line',
                zoomType: "x"
            },
            title: {
                text: 'Total Power Consumption'
            },
            tooltip : {
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
                    value:0
                }]
            },
            series: [
            {
                name: 'Building consumption',
                data: buildingVals
            }]

        });
    }

    function Get(yourUrl){
        var Httpreq = new XMLHttpRequest(); // a new request
        Httpreq.open("GET",yourUrl,false);
        Httpreq.send(null);
        return Httpreq.responseText;          
    }
    
        function init() {

            const uri_chart1 = `http://localhost:5000/dashboard/Building`;        
            var res_chart1 = JSON.parse(Get(uri_chart1)); 
            console.log(res_chart1);
            
            var buildingVals = [];
            //var feature2Vals = []
            var labels = [];
            
            
            for(let i = 0; i < res_chart1.size; i++){

                let singleElement = res_chart1[i];

                for(let prop in singleElement){
                    if(prop == 'Building')
                        buildingVals.push(singleElement[prop]);           
                }
                labels.push(res[i].Time);
            }        
            
            console.log(labels);
            console.log(buildingValsVals);
            //console.log(feature2Vals)
            renderChart(buildingVals, labels);
            
        }

});