// /*dashboard-graphs.js*/


// "strict mode";

// console.log("ABOVE EVENT LISTENER");
// $(document).ready(function () {
//     function createCORSRequest(method, url) {

//         let xhr = new XMLHttpRequest();
//         xhr.open(method, url, true); // call its open method
//         return xhr;
//     }
//     function graphDataCollection_Chart1() {

//         console.log("trying to request for data");
//         // will have to include code here about fetching data from the 
//         // selected features for the specific features on dashboard
//         let uri_chart1 = `https://cors-anywhere.herokuapp.com/127.0.0.1:5000/dashboard/access/Building`;

//         console.log("url created successfully")
//         let xhr = createCORSRequest('GET', uri_chart1);

//         console.log("url CORS request happened")
//         // checking if browser does CORS
//         if (!xhr) {
//             alert('CORS not supported');
//             return;
//         }

//         xhr.onload = function () {
//             console.log("Building the chart")
//             let responseStr = xhr.responseText; // get the JSON string 
//             let res_chart1 = JSON.parse(responseStr); // turn it into an object
//             console.log(JSON.stringify(res_chart1, undefined, 2)); // print it out as a string, nicely formatted

//             var buildingVals = [];
//             var labels = [];

//             for (let i = 0; i < res_chart1.size; i++) {

//                 let singleElement = res_chart1[i];

//                 for (let prop in singleElement) {
//                     if (prop == 'Building')
//                         buildingVals.push(singleElement[prop]);
//                 }
//                 labels.push(res[i].Time);
//             }

//             console.log(labels);
//             console.log(buildingValsVals);
//             renderChart1(buildingVals, 'Total Power Consumption Values', labels);

//         };

//         xhr.onerror = function () {
//             alert('Woops, there was an error making the request.');
//         };

//         console.log("Just before send statement")
//         // Actually send request to server
//         xhr.send();

//         //var res_chart1 = JSON.parse(Get(uri_chart1));
//         //console.log(res_chart1);

//     }






//     function consumption(value) {
//         return (value);
//     }

//     function renderChart1(yVals, yValsTitle, dates) {
//         var highChart = new Highcharts.chart('chart1', {
//             chart: {
//                 type: 'line',
//                 zoomType: "x"
//             },
//             title: {
//                 text: yValsTitle
//             },
//             tooltip: {
//                 valueSuffix: '\xB0C'
//             },
//             xAxis: {
//                 categories: dates
//             },
//             yAxis: {
//                 title: {
//                     text: 'Consumption'
//                 },
//                 plotLines: [{
//                     value: 0
//                 }]
//             },
//             series: [{
//                 name: 'Building consumption',
//                 data: yVals
//             }]

//         });
//     }

//     function renderChart2(yVals, yValsTitle, dates) {
//         var highChart = new Highcharts.chart('chart2', {
//             chart: {
//                 type: 'line',
//                 zoomType: "x"
//             },
//             title: {
//                 text: yValsTitle
//             },
//             tooltip: {
//                 valueSuffix: '\xB0C'
//             },
//             xAxis: {
//                 categories: dates
//             },
//             yAxis: {
//                 title: {
//                     text: 'Power generated'
//                 },
//                 plotLines: [{
//                     value: 0
//                 }]
//             },
//             series: [{
//                 name: 'PV Power Generated',
//                 data: yVals
//             }]

//         });
//     }

//     /*
//     function createCORSRequest(method, url) {

//         let xhr = new XMLHttpRequest();
//         xhr.open(method, url, true);  // call its open method
//         return xhr;
//       }*/
//     graphDataCollection_Chart1();
//     /*
//         function Get(yourUrl) {
//             var Httpreq = new XMLHttpRequest(); // a new request
//             Httpreq.open("GET", yourUrl, true);
//             Httpreq.send();
//             return Httpreq.responseText;
//         }

//         function loadAllGraphs() {
//             console.log("in the load function");
//             graphDataCollection_Chart1();
//         }

//         function graphDataCollection_Chart1() {

//             // will have to include code here about fetching data from the 
//             // selected features for the specific features on dashboard
//             const uri_chart1 = `https://cors-anywhere.herokuapp.com/localhost:5000/dashboard/Building`;
//             var res_chart1 = JSON.parse(Get(uri_chart1));
//             console.log(res_chart1);

//             var buildingVals = [];
//             //var feature2Vals = []
//             var labels = [];


//             for (let i = 0; i < res_chart1.size; i++) {

//                 let singleElement = res_chart1[i];

//                 for (let prop in singleElement) {
//                     if (prop == 'Building')
//                         buildingVals.push(singleElement[prop]);
//                 }
//                 labels.push(res[i].Time);
//             }

//             console.log(labels);
//             console.log(buildingValsVals);
//             renderChart(buildingVals, 'Total Power Consumption Values', labels);

//         }

//         function graphDataCollection_Chart2() {
//             // will have to include code here about fetching data from the 
//             // selected features for the specific features on dashboard
//             const uri_chart1 = `http://localhost:5000/dashboard/PVPowerGenData`;        
//             var res_chart1 = JSON.parse(Get(uri_chart1)); 
//             console.log(res_chart1);

//             var powerGenVals = [];
//             //var feature2Vals = []
//             var labels = [];


//             for(let i = 0; i < res_chart1.size; i++){

//                 let singleElement = res_chart1[i];

//                 for(let prop in singleElement){
//                     if(prop == 'PVPower_kW')
//                         powerGenVals.push(singleElement[prop]);           
//                 }
//                 labels.push(res[i].Time);
//             }        
//             console.log(labels);
//             console.log(powerGenVals);
//             renderChart(powerGenVals, labels);

//         }*/


// });

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
                    name: yValsTitle,
                    data: yVals
                }
            ]

        });
    }
    function renderChart2(feature1, feature2, feature1Vals, feature2Vals, dates) {
        //var ctx = document.getElementById("myChart").getContext('2d');
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
    function renderChart3(feature1, feature2, feature1Vals, feature2Vals, dates) {
        //var ctx = document.getElementById("myChart").getContext('2d');
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
    function renderChart4(feature1, feature2, feature1Vals, feature2Vals, dates) {
        //var ctx = document.getElementById("myChart").getContext('2d');
        var highChart = new Highcharts.chart('chart4', {
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

    function render() {

        var startDate = '2018-06-01';
        var endDate = '2018-06-02';

        var filename = 'Control2';
        var feature1 = 'HVAC2';
        var feature2 = 'HVAC1';

        console.log(startDate);
        console.log(endDate);
        console.log(filename);
        console.log(feature1);
        console.log(feature2);

        const uri = `http://127.0.0.1:5000/${filename}/${startDate}/${endDate}/${feature1}/${feature2}`;
        //const uri = 'http://127.0.0.1:5000/dashboard/access/HVAC1/HVAC2';
        var res = JSON.parse(Get(uri)); 
        console.log(res);

        var feature1Vals = [];
        var feature2Vals = []
        var labels = [];


        for (let i = 0; i < 500; i++) {

            let singleElement = res[i];

            for (let prop in singleElement) {
                if (prop == feature1)
                    feature1Vals.push(singleElement[prop]);
                if (prop == feature2)
                    feature2Vals.push(singleElement[prop]);
            }
            labels.push(res[i].Time);

        }

        console.log(labels);
        console.log(feature1Vals);
        console.log(feature2Vals)
        //renderChart1(feature1, feature2, feature1Vals, feature2Vals, labels);
        renderChart2(feature1, feature2, feature1Vals, feature2Vals, labels);
        renderChart3(feature1, feature2, feature1Vals, feature2Vals, labels);
        renderChart4(feature1, feature2, feature1Vals, feature2Vals, labels);
    };
    //render();
    graphDataCollection_Chart1();
    graphDataCollection_Chart2();
});