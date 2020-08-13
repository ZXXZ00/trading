var chart;
var times; // times is an array of time
var data;  // data is an array [ {field: ..., data: [...]}, {...} ...]

var legendClickHandler = function(e, legendItem) {
	var index = legendItem.datasetIndex;
	var ci = this.chart;
	var meta = ci.getDatasetMeta(index);
	meta.hidden = meta.hidden === null ?
		!ci.data.datasets[index].hidden : null;
	ci.options.scales.yAxes[index].display =
		!ci.options.scales.yAxes[index].display;
	ci.update();
}

function draw() {
	var datasets = [];
	var y = [];
	data.forEach((entry) => {
		var color = 'rgb('+
			Math.floor(Math.random()*256)+','+
			Math.floor(Math.random()*256)+','+
			Math.floor(Math.random()*256);
		var element = {
			label: entry.field,
			yAixsID: entry.field,
			borderColor: color+')',
			backgroundColor: color+',0)'
			data: entry.data,
			type: 'line'
		};
		var yElement = {
			id: entry.field,
			type: 'linear',
			position: Math.random() < 0.5 ? 'left' : 'right',
			ticks: {
				fontColor: color+',0)'
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
					bounds: 'ticks',
					ticks: {
						source: 'labels'
					}
				}],
				yAxes: y
			},
			legend: {
				onclick: legendClickHandler
			}
		}
	}
}


