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
                label: '2017-12-31',
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
    return Httpreq.responseText;          
}

$("#renderBtn").click(
    function () {
        var res = JSON.parse(Get("http://localhost:5000/cieeData"));
        console.log(res);
        
        var data = [];
        var labels = [];
        
        for (i = 0; i < 20; i++) {
            data.push(res[i].ciee);
            labels.push(res[i].TimeStamp);  

        }
        
        console.log(labels)
        renderChart(data, labels);
        
        //print(res);
 /*      
        data = ["2240", "2176", "2120", "2120", "2116", "2120", "2124", "2116", "2108", 
        "2116", "2120", "2115.555556", "2116","2727.272727", "2736", "2781.818182", "2152", "2148", "2164", 
        "2155.55556"];
        labels =  ["16:01", "16:02", "16:03", "16:04", "16:05", "16:06", "16:07", "16:08", "16:09", 
        "16:10", "16:11", "16:12", "16:13", "16:14", "16:15", "16:16", "16:17", "16:18", "16:19", "16:20"];
        renderChart(data, labels);
        */
        
    }
);
