/*<script>
var contex = document.getElementById("myChart");
var myChart = new Chart(contex, {
    type: 'line',
    data: {
        labels: ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", 
        "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"],
        datasets: [
            {
                label: "2017-12-31",
                data: ["2240", "2176", "2120", "2120", "2116", "2120", "2124", "2116", "2108", 
                "2116", "2120", "2115.555556", "2116","2727.272727", "2736", "2781.818182", "2152", "2148", "2164", 
                "2155.55556"]
            }
        ]
    }
});
</script>*/
$(document).ready(function() {
    function consumption(value){
        return (value);
    }
    
    function renderChart(data, labels) {
        var ctx = document.getElementById("myChart").getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Power consumption values',
                    data: data,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    fill: false,
                    //backgroundColor: 'rgba(75, 192, 192, 0.2)',
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
    
    function getData() {
        
        const uri = `http://localhost:5000/cieeData`;
        var res = fetch(uri);  
        //console.log(res.json());
        fetch(uri).then(res => console.log(res.json()));
        return res; 
    }
    

    function Get(yourUrl){
        var Httpreq = new XMLHttpRequest(); // a new request
        Httpreq.open("GET",yourUrl,false);
        Httpreq.send(null);
        console.log("print");
        return Httpreq.responseText;          
    }
    

    $("#renderBtn").click(
        function () {
            var startDate = document.getElementById("Date1").value;
            var endDate = document.getElementById("Date2").value;
    
            const uri = `http://localhost:5000/cieeData/${startDate}/${endDate}`;
            
            var res = JSON.parse(Get(uri)); //"http://localhost:5000/cieeData/2018-01-04/2018-01-05"));
            console.log(res);
            
            var data = [];
            var labels = [];
            
            for (i = 0; i < 250; i++) {
                data.push(res[i].ciee);
                labels.push(res[i].TimeStamp);  
    
            }
            
            console.log(labels)
            renderChart(data, labels);
            
        }
    );
    
    $("#linechartCSV").click(
        function () {
            var startDate = document.getElementById("Date1").value;
            var endDate = document.getElementById("Date2").value;
    
            const uri = `http://localhost:5000/cieeData/${startDate}/${endDate}`;
            
            var res = JSON.parse(Get(uri)); //"http://localhost:5000/cieeData/2018-01-04/2018-01-05"));
            //console.log(res);
            
            var result, ctr, keys, columnDelimiter, lineDelimiter, data, csv, eCSV;
            data = res;
            columnDelimiter =  ',';
            lineDelimiter =  '\n';
    
            keys = Object.keys(data[0]);
    
            result = '';
            result += keys.join(columnDelimiter);
            result += lineDelimiter;
    
            data.forEach(function(item) {
                ctr = 0;
                keys.forEach(function(key) {
                    if (ctr > 0) result += columnDelimiter;
    
                    result += item[key];
                    ctr++;
                });
                result += lineDelimiter;
            });
            //console.log(result);
            csv = 'data:text/csv;charset=utf-8,' + result;
            eCSV = encodeURI(csv);
    
            //console.log(eCSV);
    
            var hiddenElement = document.createElement('a');
            hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(result);
            hiddenElement.target = '_blank';
            hiddenElement.download = 'linechart.csv';
            hiddenElement.click();
            console.log("print")
    
        }
    );



});



