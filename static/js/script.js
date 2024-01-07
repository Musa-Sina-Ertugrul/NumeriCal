

function fetchData() {
  let func = document.getElementById("Function").value;
  // let x0 = document.getElementById("x0").value;
  let max_iter = document.getElementById("max_iter").value;
  let tolerance = document.getElementById("tolerance").value;
  // func_value.innerHTML = func;
  // x0_value.innerHTML = event.target.value;
  // max_iter_value.innerHTML = max_iter;
  // tolerance_value.innerHTML = tolerance;


  fetch("http://127.0.0.1:5000/calculate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      func: func,
      // x0: x0,
      max_iter: max_iter,
      tolerance: tolerance
    }),
  })
    .then(response => response.json())
    .then(data => {
      
      const roots = data.roots.map(Number); 
      const iterations = data.iterations; 

      myChart.data.labels = iterations; 
      myChart.data.datasets[0].data = roots; 
      myChart.update(); 
    })
    .catch(error => {
      console.error("Error fetching data:", error);
    });
}


// Fonksiyon verisini içeren data objesi
const data = {
  labels: [],
  datasets: [{
    label: 'Function',
    data: [],
    fill: false,
    borderColor: 'blue',
    borderWidth: 2
  }]
};

// Canvas elementini seç
var canvas = document.getElementById("myChart").getContext('2d');

// Çizgi grafiği oluştur
var myChart = new Chart(canvas, {
  type: 'line',
  data: data,
  options:{
    scales:{

      }
    }
  }
);
myChart.update();

document.getElementById("Function").addEventListener("input", function () {
  var functionInput = document.getElementById("Function").value || "Math.sin(x)";
  myChart.data.labels = getLabels();
  myChart.data.datasets[0].data = getDataPoints(functionInput);
  myChart.update();
});

function getLabels() {
  var labels = [];
  for (var i = 1; i <= 10; i++) {
    labels.push(i);
  }
  return labels;
}


function getDataPoints(func) {
  var dataPoints = [];
  for (var i = 1; i <= 10; i++) {
    try {
      var result = math.evaluate(func.replace(/x/g, `(${i})`));
      dataPoints.push(result);
    } catch (error) {
      console.error("Error evaluating expression:", error);
    }
  }
  return dataPoints;
}
