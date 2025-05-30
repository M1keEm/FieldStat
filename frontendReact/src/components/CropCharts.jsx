import { useEffect, useState } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, PointElement, LineElement, ArcElement, Title, Tooltip, Legend, RadialLinearScale, BubbleController, ScatterController } from 'chart.js';
import { Bar, Doughnut, Line, PolarArea, Scatter, Bubble } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    ArcElement,
    RadialLinearScale,
    BubbleController,
    ScatterController,
    Title,
    Tooltip,
    Legend
);

const CropCharts = ({ plotData, commodity, year }) => {
  const [chartData, setChartData] = useState({
    yieldData: null,
    areaData: null,
    productionData: null,
    temperatureData: null,
    precipitationData: null,
    yieldWeatherCorrelationData: null
  });

  // Custom color palette
  const colorPalette = [
    'rgba(66, 133, 244, 0.7)',  // Google Blue
    'rgba(219, 68, 55, 0.7)',   // Google Red
    'rgba(244, 180, 0, 0.7)',   // Google Yellow
    'rgba(15, 157, 88, 0.7)',   // Google Green
    'rgba(171, 71, 188, 0.7)',  // Purple
    'rgba(255, 112, 67, 0.7)',  // Deep Orange
    'rgba(0, 172, 193, 0.7)',   // Cyan
    'rgba(124, 179, 66, 0.7)'   // Light Green
  ];

  // Prepare data for charts when plotData changes
  useEffect(() => {
    if (!plotData || plotData.length === 0) return;

    // Sort states by yield for better visualization
    const sortedByYield = [...plotData].sort((a, b) =>
        (b.average_yield || 0) - (a.average_yield || 0));

    // Take top 10 states for better readability
    const topStates = sortedByYield.slice(0, 10);

    // Extract data for charts
    const states = topStates.map(item => item.state);
    const yields = topStates.map(item => item.average_yield);
    const areas = topStates.map(item => item.area_planted_acres);
    const productions = topStates.map(item => item.total_production);
    const temperatures = topStates.map(item => item.avg_temp_C);
    const precipitations = topStates.map(item => item.total_precip_mm);

    // Prepare correlation data
    const correlationData = topStates.map(item => ({
      x: item.avg_temp_C,
      y: item.average_yield,
      r: Math.max(5, Math.min(20, (item.area_planted_acres || 0) / 50000)),  // Size based on area, min 5, max 20
      state: item.state
    }));

    // Generate background colors
    const backgroundColors = states.map((_, index) => colorPalette[index % colorPalette.length]);
    const precipColorsByAmount = precipitations.map(precip =>
        precip > 1000 ? 'rgba(0, 0, 255, 0.7)' :  // Very wet (blue)
            precip > 750 ? 'rgba(30, 144, 255, 0.7)' : // Wet (lighter blue)
                precip > 500 ? 'rgba(95, 158, 160, 0.7)' : // Moderate (teal)
                    precip > 250 ? 'rgba(240, 230, 140, 0.7)' : // Dry (yellow)
                        'rgba(255, 140, 0, 0.7)'  // Very dry (orange)
    );

    // Create chart data objects
    setChartData({
      yieldData: {
        labels: states,
        datasets: [{
          label: 'Yield by State',
          data: yields,
          backgroundColor: backgroundColors,
          borderColor: backgroundColors.map(color => color.replace('0.7', '1')),
          borderWidth: 1,
        }]
      },
      areaData: {
        labels: states,
        datasets: [{
          label: 'Planted Area by State (acres)',
          data: areas,
          backgroundColor: backgroundColors,
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          tension: 0.4
        }]
      },
      productionData: {
        labels: states,
        datasets: [{
          label: 'Total Production by State',
          data: productions,
          backgroundColor: backgroundColors,
        }]
      },
      temperatureData: {
        labels: states,
        datasets: [{
          label: 'Average Temperature (°C)',
          data: temperatures,
          backgroundColor: temperatures.map(temp =>
              temp > 20 ? 'rgba(255, 99, 132, 0.7)' :
                  temp > 15 ? 'rgba(255, 159, 64, 0.7)' :
                      temp > 10 ? 'rgba(255, 205, 86, 0.7)' :
                          'rgba(75, 192, 192, 0.7)'
          ),
          borderWidth: 1,
        }]
      },
      precipitationData: {
        labels: states,
        datasets: [{
          label: 'Total Precipitation (mm)',
          data: precipitations,
          backgroundColor: precipColorsByAmount,
          borderColor: precipColorsByAmount.map(color => color.replace('0.7', '1')),
          borderWidth: 1,
        }]
      },
      yieldWeatherCorrelationData: {
        datasets: [{
          label: 'Yield vs Temperature',
          data: correlationData,
          backgroundColor: backgroundColors,
          hoverBackgroundColor: backgroundColors.map(color => color.replace('0.7', '0.9')),
        }]
      }
    });
  }, [plotData]);

  // Chart options
  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        display: false,
      },
      title: {
        display: true,
        text: `${commodity} Yield by State (${year})`,
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `Yield: ${context.parsed.y?.toFixed(2) || 'N/A'}`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Yield (tons/acre)'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      x: {
        grid: {
          display: false
        }
      }
    },
    animation: {
      duration: 2000,
      easing: 'easeOutQuart'
    }
  };

  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `${commodity} Planted Area by State (${year})`,
        font: {
          size: 16,
          weight: 'bold'
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return value >= 1000000 ? (value/1000000).toFixed(1) + 'M' :
                value >= 1000 ? (value/1000).toFixed(1) + 'K' : value;
          }
        }
      }
    },
    animation: {
      duration: 2000,
      easing: 'easeOutQuart'
    }
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `${commodity} Total Production by State (${year})`,
        font: {
          size: 16,
          weight: 'bold'
        }
      }
    },
    animation: {
      animateRotate: true,
      animateScale: true,
      duration: 2000
    }
  };

  const polarAreaOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
      },
      title: {
        display: true,
        text: `${commodity} Average Temperature by State (${year})`,
        font: {
          size: 16,
          weight: 'bold'
        }
      }
    },
    scales: {
      r: {
        beginAtZero: true
      }
    },
    animation: {
      duration: 2000,
      easing: 'easeOutQuart'
    }
  };

  const precipitationOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        display: false,
      },
      title: {
        display: true,
        text: `${commodity} Total Precipitation by State (${year})`,
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `Precipitation: ${context.parsed.y?.toFixed(0) || 'N/A'} mm`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Precipitation (mm)'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      x: {
        grid: {
          display: false
        }
      }
    },
    animation: {
      duration: 2000,
      easing: 'easeOutQuart'
    }
  };

  const bubbleOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        display: false,
      },
      title: {
        display: true,
        text: `${commodity} Yield vs Temperature (${year})`,
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const dataPoint = context.raw;
            return [
              `State: ${dataPoint.state}`,
              `Temperature: ${dataPoint.x?.toFixed(1) || 'N/A'}°C`,
              `Yield: ${dataPoint.y?.toFixed(2) || 'N/A'}`
            ];
          }
        }
      }
    },
    scales: {
      y: {
        title: {
          display: true,
          text: 'Yield'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Average Temperature (°C)'
        },
        grid: {
          display: true,
          color: 'rgba(0, 0, 0, 0.05)'
        }
      }
    },
    animation: {
      duration: 2000,
      easing: 'easeOutQuart'
    }
  };

  // If no data, display a message
  if (!plotData || plotData.length === 0) {
    const currentYear = new Date().getFullYear();
    let message = "No data available for the selected commodity and year.";

    if (year > currentYear) {
      message = `Data for ${year} is not available yet as it's a future year. Please select ${currentYear} or earlier.`;
    } else if (year === currentYear) {
      message = `Data for ${currentYear} might not be complete. Try selecting ${currentYear-1} for more complete data.`;
    }

    return (
        <div className="no-data-message">
          <h3>No Data Available</h3>
          <p>{message}</p>
          <p>Try selecting a different commodity or an earlier year.</p>
        </div>
    );
  }

  return (
      <div className="charts-container">
        <h2 className="charts-title">Data Visualization for {commodity} ({year})</h2>

        <div className="charts-grid">
          <div className="chart-card">
            <div className="chart-wrapper">
              {chartData.yieldData && <Bar data={chartData.yieldData} options={barOptions} />}
            </div>
          </div>

          <div className="chart-card">
            <div className="chart-wrapper">
              {chartData.areaData && <Line data={chartData.areaData} options={lineOptions} />}
            </div>
          </div>

          <div className="chart-card">
            <div className="chart-wrapper">
              {chartData.productionData && <Doughnut data={chartData.productionData} options={doughnutOptions} />}
            </div>
          </div>

          <div className="chart-card">
            <div className="chart-wrapper">
              {chartData.temperatureData && <PolarArea data={chartData.temperatureData} options={polarAreaOptions} />}
            </div>
          </div>

          <div className="chart-card">
            <div className="chart-wrapper">
              {chartData.precipitationData && <Bar data={chartData.precipitationData} options={precipitationOptions} />}
            </div>
          </div>

          <div className="chart-card">
            <div className="chart-wrapper">
              {chartData.yieldWeatherCorrelationData && <Bubble data={chartData.yieldWeatherCorrelationData} options={bubbleOptions} />}
            </div>
          </div>
        </div>
      </div>
  );
};

export default CropCharts;
