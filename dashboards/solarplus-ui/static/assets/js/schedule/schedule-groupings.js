$(document).ready(function() {
	M.AutoInit();
	var zoneSel = 0;
	var zoneArr = [];
	console.log(temperature6)
	/*const url = 'http://127.0.0.1:5000/setpoints/getEntry';
	var Httpreq = new XMLHttpRequest(); // a new request
	Httpreq.open(“POST”, yourUrl, false);
	Httpreq.send(null);
	var entry = JSON.parse(Httpreq.responseText);*/

	document.getElementById('temp1').value = temperature1;
	document.getElementById('temp2').value = temperature2;
	document.getElementById('temp3').value = temperature3;
	document.getElementById('temp4').value = temperature4;

	document.getElementById('temp5').value = temperature5;
	document.getElementById('temp6').value = temperature6;
	document.getElementById('temp7').value = temperature7;
	document.getElementById('temp8').value = temperature8;

	$(".filled-in").each(function() {
		$(this).click(function() {
			var t = $(this).find("span").prevObject["0"]["labels"][0]["innerText"];
			if ($(this).prop("checked")) {
				zoneSel += 1;
				zoneArr.push(t);
				console.log(zoneArr);
			} else {
				zoneSel -= 1;
				zoneArr.splice($.inArray(t, zoneArr), 1);
				console.log(zoneArr);
			}
			setGB();
		});
	});

	function setGB() {
		$("#group-btn").html("Group Selected (" + zoneSel + ")");
	}

	$("#group-btn").click(function() {
		if (zoneSel == 0) {
			$("#modal-continue").addClass("disabled");
			$("#modal-header").html("Select at least one zone to form a group");
			$("#modal-text").html("");
		} else {
			$("#modal-continue").removeClass("disabled");
			var s = "Form a group with the following ";
			if (zoneSel == 1) { s += "zone:"; } else { s += zoneSel + " zones:"; }
			$("#modal-header").html(s);
			$("#modal-text").html(zoneArr.join("<br>"));
		}
	});

	$("#modal-continue").click(function() {
		sessionStorage.setItem("modesToGroup", "areh");
		location.href = "schedule-epochs.html";
	});

	// $("#save-modes").click(function() {
	// 	var obj = new Object();
	// 	modes = [];
	// 	$(".mode-card").each(function(i) {
	// 		var m = new Object();
	// 		m.id = i;
	// 		var inputs = $(this).find("input");
	// 		m.name = inputs[0].value;
	// 		m.heating = inputs[1].value;
	// 		m.cooling = inputs[2].value;
	// 		m.enabled = $(inputs[3]).prop("checked");
	// 		obj.modes.push(m);
	// 	});
	// 	M.toast({html: 'Current modes successfully updated.', classes:"rounded", displayLength: 2000});
	// 	console.log(obj);
	// });

	$("#save-therm").click(function() {
		//var obj = new Object();
		modes = [];
		$(".thermostat-card").each(function(i) {
			var m = new Object();
			m.id = i;
			var inputs = $(this).find("input");
			m.name = inputs[0].value;
			m.heating = inputs[1].value;
			m.cooling = inputs[2].value;

			modes.push(m);
		});
		M.toast({html: 'Current setpoints successfully updated.', classes:"rounded", displayLength: 2000});
		var temp1 = document.getElementById('temp1').value;
		var temp2 = document.getElementById('temp2').value;
		var temp3 = document.getElementById('temp3').value;
		var temp4 = document.getElementById('temp4').value;

		// the finalized elements
		sessionStorage.setItem('tempOne',temp1);
		sessionStorage.setItem('tempTwo',temp2);
		sessionStorage.setItem('tempThree',temp3);
		sessionStorage.setItem('tempFour',temp4);

		// post request
		$.ajax({
			type: 'POST',
			url: '/setpoints/getEntry1',
			dataType: "json",
			data: JSON.stringify({
				'temp1': temp1,
				'temp2': temp2,
				'temp3': temp3,
				'temp4': temp4
			}),
			success: function(data) {
				console.log(data);
			},
			failure: function(err) {
				console.log(err);
			}
		})



		// console.log(temp1);
		// console.log(temp2);
		// console.log(temp3);
		// console.log(temp4);
		// console.log(temp);

		// asynchronous http get request
		/*function httpGetAsync(theUrl, callback)
		{
    	var xmlHttp = new XMLHttpRequest();
    	xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
			}
    	xmlHttp.open("POST", theUrl, true); // true for asynchronous
    	xmlHttp.send();
		}*/


		/*
		using jquery post request:
		(brower) frontend -> (flask) backend
		1. turn values into json object (ex: {therm1: temp1}) -> javascript
		2. send the request to the backend using $.post() following the rest of the API -> javascript
		3. write the code for the route backend in flask (python) / method is post only -> python

		(flask) backend -> database
		1. convert the json object to python dictionary
		2. save the python dictionary into the database (influxdb)

		flask -> browser
		1. reply to the request object
		*/

		var result, ctr, keys, columnDelimiter, lineDelimiter, data, csv, eCSV;
		data = modes;
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

		csv = 'data:text/csv;charset=utf-8,' + result;
		eCSV = encodeURI(csv);

		//console.log(eCSV);

		var hiddenElement = document.createElement('a');
		hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(result);
		hiddenElement.target = '_blank';
		hiddenElement.download = 'thermostatSetpoints.csv';
		hiddenElement.click();


		// console.log("name" + modes[0].name);
	});
	$("#save-sp").click(function() {
		//var obj = new Object();
		modes = [];
		$(".refrigerator-freezer-card").each(function(i) {
			var m = new Object();
			m.id = i;
			var inputs = $(this).find("input");
			m.name = inputs[0].value;
			m.heating = inputs[1].value;
			m.cooling = inputs[2].value;

			modes.push(m);
		});
		M.toast({html: 'Current setpoints successfully updated.', classes:"rounded", displayLength: 2000});
		var temp5 = document.getElementById('temp5').value;
		var temp6 = document.getElementById('temp6').value;
		var temp7 = document.getElementById('temp7').value;
		var temp8 = document.getElementById('temp8').value;

		sessionStorage.setItem('tempFive',temp5);
		sessionStorage.setItem('tempSix',temp6);
		sessionStorage.setItem('tempSeven',temp7);
		sessionStorage.setItem('tempEight',temp8);

		// post request
		$.ajax({
			type: 'POST',
			url: '/setpoints/getEntry2',
			dataType: "json",
			data: JSON.stringify({
				//TODO: figure out what to do with the key (next step)

				'temp5': temp5,
				'temp6': temp6,
				'temp7': temp7,
				'temp8': temp8
			}),
			success: function(data) {
				console.log(data);
			},
			failure: function(err) {
				console.log(err);
			}
		})

	// requesting the new new url page & sending the json obj
	/*
	$.post("/setpoints/updated", { therm1: temp1, therm2: temp2, therm3: temp3,
																therm4: temp4, therm5: temp5, therm6: temp6,
															 	therm7: temp7, therm8: temp8 });*/


		var result, ctr, keys, columnDelimiter, lineDelimiter, data, csv, eCSV;
		data = modes;
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

		csv = 'data:text/csv;charset=utf-8,' + result;
		eCSV = encodeURI(csv);

		//console.log(eCSV);

		var hiddenElement = document.createElement('a');
		hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(result);
		hiddenElement.target = '_blank';
		hiddenElement.download = 'Refrigerator-Freezer-Setpoints.csv';
		hiddenElement.click();


		// console.log("name" + modes[0].name);
	});
});
