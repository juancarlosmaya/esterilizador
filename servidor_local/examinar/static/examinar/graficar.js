// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
console.log(temperaturas.length);  // Output the array to check it's accessible
console.log(presiones.length);  // Output the array to check it's accessible

// Area Chart Example  
var ejeX =[];
for (i=0;i<temperaturas.length;i++){
  ejeX[i]=i;
}

var ctx = document.getElementById("grafica");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ejeX,  // Your X-axis labels (e.g., time or dates)
    datasets: [
      {
        label: "Temperatura (°C)",  // Label for the first dataset
        lineTension: 0.3,
        backgroundColor: "rgba(2,117,216,0.2)",
        borderColor: "rgba(2,117,216,1)",
        pointRadius: 5,
        pointBackgroundColor: "rgba(2,117,216,1)",
        pointBorderColor: "rgba(255,255,255,0.8)",
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "rgba(2,117,216,1)",
        pointHitRadius: 50,
        pointBorderWidth: 2,
        data: temperaturas,  // Your pressure data
        fill: false,
        yAxisID: 'y-axis-1'  // Assign this dataset to the first Y axis
      },
      {
        label: "Presion (kPa)",  // Label for the second dataset
        lineTension: 0.3,
        backgroundColor: "rgba(255,99,132,0.2)",
        borderColor: "rgba(255,99,132,1)",
        pointRadius: 5,
        pointBackgroundColor: "rgba(255,99,132,1)",
        pointBorderColor: "rgba(255,255,255,0.8)",
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "rgba(255,99,132,1)",
        pointHitRadius: 50,
        pointBorderWidth: 2,
        data: presiones,  // Your temperature data
        fill: false,
        yAxisID: 'y-axis-2'  // Assign this dataset to the second Y axis
      }
    ]
  },
  options: {
    animation: {
      duration: 0 // General animation time
    },
    hover: {
      animationDuration: 0 // Duration of animations when hovering an item
    },
    responsiveAnimationDuration: 0, // Animation duration after a resize
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [
        {
          id: 'y-axis-1',  // First Y axis (for presiones)
          position: 'left',  // Position it on the right side
          ticks: {
            // Adjust the Y axis range for pressure if needed
            // min: 0, max: 40000,
            maxTicksLimit: 5
          },
          gridLines: {
            color: "rgba(0, 0, 0, .125)"
          },
          scaleLabel: {
            display: true,
            labelString: 'Temperatura (°C)'
          }
        },
        {
          id: 'y-axis-2',  // Second Y axis (for temperaturas)
          position: 'right',  // Position it on the right side
          ticks: {
            // Adjust the Y axis range for temperature if needed
            // min: 0, max: 50,
            maxTicksLimit: 5
          },
          gridLines: {
            color: "rgba(0, 0, 0, .125)"
          },
          scaleLabel: {
            display: true,
            labelString: 'Presion (Kpa)'
          }
        }
      ]
    },
    legend: {
      display: true
    }
  }
});