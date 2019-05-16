/*dashboard-graphs.js*/


"strict mode";

console.log("ABOVE EVENT LISTENER");

function graphDataCollection_Chart1() {

    // will have to include code here about fetching data from the 
    // selected features for the specific features on dashboard
    let uri_chart1 = `https://cors-anywhere.herokuapp.com/localhost:5000/dashboard/Building`;

    let xhr = createCORSRequest('GET', url);

    // checking if browser does CORS
    if (!xhr) {
        alert('CORS not supported');
        return;
    }

    xhr.onload = function() {
        let responseStr = xhr.responseText;  // get the JSON string 
        let res_chart1 = JSON.parse(responseStr);  // turn it into an object
        console.log(JSON.stringify(res_chart1, undefined, 2));  // print it out as a string, nicely formatted

        var buildingVals = [];
        //var feature2Vals = []
        var labels = [];
    
        for (let i = 0; i < res_chart1.size; i++) {
    
            let singleElement = res_chart1[i];
    
            for (let prop in singleElement) {
                if (prop == 'Building')
                    buildingVals.push(singleElement[prop]);
            }
            labels.push(res[i].Time);
        }
    
        console.log(labels);
        console.log(buildingValsVals);
        renderChart(buildingVals, 'Total Power Consumption Values', labels);

    };
  
    xhr.onerror = function() {
      alert('Woops, there was an error making the request.');
    };
  
    // Actually send request to server
    xhr.send();
  
    //var res_chart1 = JSON.parse(Get(uri_chart1));
    //console.log(res_chart1);

}
$(document).ready(function () {

    console.log("in the js file fam");

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
                text: yValsTitle
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
                name: 'Building consumption',
                data: yVals
            }]

        });
    }

    function renderChart2(yVals, yValsTitle, dates) {
        var highChart = new Highcharts.chart('chart2', {
            chart: {
                type: 'line',
                zoomType: "x"
            },
            title: {
                text: yValsTitle
            },
            tooltip: {
                valueSuffix: '\xB0C'
            },
            xAxis: {
                categories: dates
            },
            yAxis: {
                title: {
                    text: 'Power generated'
                },
                plotLines: [{
                    value: 0
                }]
            },
            series: [{
                name: 'PV Power Generated',
                data: yVals
            }]

        });
    }

    function createCORSRequest(method, url) {
        
        let xhr = new XMLHttpRequest();
        xhr.open(method, url, true);  // call its open method
        return xhr;
      }
/*
    function Get(yourUrl) {
        var Httpreq = new XMLHttpRequest(); // a new request
        Httpreq.open("GET", yourUrl, true);
        Httpreq.send();
        return Httpreq.responseText;
    }

    function loadAllGraphs() {
        console.log("in the load function");
        graphDataCollection_Chart1();
    }

    function graphDataCollection_Chart1() {

        // will have to include code here about fetching data from the 
        // selected features for the specific features on dashboard
        const uri_chart1 = `https://cors-anywhere.herokuapp.com/localhost:5000/dashboard/Building`;
        var res_chart1 = JSON.parse(Get(uri_chart1));
        console.log(res_chart1);

        var buildingVals = [];
        //var feature2Vals = []
        var labels = [];


        for (let i = 0; i < res_chart1.size; i++) {

            let singleElement = res_chart1[i];

            for (let prop in singleElement) {
                if (prop == 'Building')
                    buildingVals.push(singleElement[prop]);
            }
            labels.push(res[i].Time);
        }

        console.log(labels);
        console.log(buildingValsVals);
        renderChart(buildingVals, 'Total Power Consumption Values', labels);

    }
    loadAllGraphs();
    
    function graphDataCollection_Chart2() {
        // will have to include code here about fetching data from the 
        // selected features for the specific features on dashboard
        const uri_chart1 = `http://localhost:5000/dashboard/PVPowerGenData`;        
        var res_chart1 = JSON.parse(Get(uri_chart1)); 
        console.log(res_chart1);
        
        var powerGenVals = [];
        //var feature2Vals = []
        var labels = [];
        
        
        for(let i = 0; i < res_chart1.size; i++){

            let singleElement = res_chart1[i];

            for(let prop in singleElement){
                if(prop == 'PVPower_kW')
                    powerGenVals.push(singleElement[prop]);           
            }
            labels.push(res[i].Time);
        }        
        console.log(labels);
        console.log(powerGenVals);
        renderChart(powerGenVals, labels);
        
    }*/

});
