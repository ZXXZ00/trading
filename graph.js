var chart;
var times; // times is an array of time
var data;  // data is an array [ {field: ..., data: [...]}, {...} ...]

var legendClickHandler = function(e, legendItem) {
	let index = legendItem.datasetIndex;
	let ci = this.chart;
	let meta = ci.getDatasetMeta(index);
	meta.hidden = meta.hidden === null ?
		!ci.data.datasets[index].hidden : null;
	ci.options.scales.yAxes[index].display =
		!ci.options.scales.yAxes[index].display;
	console.log(ci.options.scales.yAxes);
	ci.update();
}

function getData() {
	var form = document.getElementById('frm');
	var link = "http://127.0.0.1:5000/data?symbol="+form['symbol'].value+
		"&strike_price="+form['strike'].value+
		"&expiration_date="+form['exp_date'].value+
		"&type="+form['type'].value;
	var request = new XMLHttpRequest();
	request.open("GET", link)
	request.send();
	request.onload = function(e) {
		if (request.status == 200) {
			response = JSON.parse(request.response);
			times = response['time'];
			data = response['data'];
			console.log(data);
			draw();
		} else {
			alert('error');
			return;
		}
	}
}

function draw() {
	var datasets = [];
	var y = [];
	data.forEach((entry) => {
		let color = 'rgb('+
			Math.floor(Math.random()*256)+','+
			Math.floor(Math.random()*256)+','+
			Math.floor(Math.random()*256);
		let element = {
			label: entry.field,
			yAxisID: entry.field,
			borderColor: color+')',
			backgroundColor: color+',0)',
			data: entry.data,
			type: 'line',
			hidden: true
		};
		let yElement = {
			id: entry.field,
			type: 'linear',
			display: false,
			position: Math.random() < 0.5 ? 'left' : 'right',
			ticks: {
				fontColor: color+')'
			}
		}
		datasets.push(element);
		y.push(yElement);
	})
	drawHelper(datasets, y);
}

function drawHelper(datas, y) {	
	var ctx = document.getElementById('myChart').getContext('2d');
	chart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: times,
			datasets: datas,
		},
		options: {
			scales: {
				xAxes: [{
					type: 'time',
					time: {
						unit: 'minute'
					},
					bounds: 'ticks',
					ticks: {
						source: 'labels'
					}
				}],
				yAxes: y
			},
			legend: {
				onClick: legendClickHandler
			}
		}
	})
}


