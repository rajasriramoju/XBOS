/*lineChart.js*/
function consumption(value){
    return (value);
}

function renderChart(feature1, feature2, feature1Vals, feature2Vals, labels) {
    var ctx = document.getElementById("myChart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets:[{
                    label: feature1+" Values",
                    data: feature1Vals,
                    borderColor:"red",
                    backgroundColor:"transparent",
                    fill: false,
		          },
		      {
                    label:feature2+" Values",
                    data: feature2Vals,
                    borderColor:"rgba(75, 192, 192, 1)",
                    backgroundColor:"transparent",
                    fill: false,
		      }]
        },
        options: {            
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        callback: function(value, index, values) {
                            return consumption(value);
                        }
                    }
                }]                
            }
        },
    });
}

function Get(yourUrl){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);
    Httpreq.send(null);
    return Httpreq.responseText;          
}

$("#renderBtn").click(
    function () {
        var startDate = document.getElementById("Date1").value;
        var endDate = document.getElementById("Date2").value;

            var filename = document.getElementById("filename").value;
            var feature1 = document.getElementById("feature1").value;
            var feature2 = document.getElementById("feature2").value;

            const uri = `http://localhost:5000/${filename}/${startDate}/${endDate}/${feature1}/${feature2}`;        
        var res = JSON.parse(Get(uri)); //"http://localhost:5000/cieeData/2018-01-04/2018-01-05"));
        console.log(res);
        
        var feature1Vals = [];
        var feature2Vals = []
        var labels = [];
        
        
        for(let i = 0; i < 250; i++){

            let singleElement = res[i];

            for(let prop in singleElement){
                if(prop == feature1)
                    feature1Vals.push(singleElement[prop]);
                if(prop == feature2)
                    feature2Vals.push(singleElement[prop]);           
            }
            labels.push(res[i].Time);

        }        
        
        console.log(labels);
        console.log(feature1Vals);
        console.log(feature2Vals)
        renderChart(feature1, feature2, feature1Vals, feature2Vals, labels);
        
    }
);
