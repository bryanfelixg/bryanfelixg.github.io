// Chart Data & Configurations
const chartData = {
    accuracy: {
        labels: [
            ['Syntactic','Tuples','Validation','Conformity'],
            ['Average','Ratio','Expected'],
            ['Average','Compliance'],
            ['Average','Staleness',],
            ['Syntactic','Tuples','Validation','Conformity'],
            ['Syntactic','Tuples','Validation','Conformity'],
            ['col0','col1','col2','col3','col4','col5','col6','col7','col8','col9']
        ],
        data: [
            [23, 56, 81, 12, 90, 34, 67, 78, 45, 3],
            [98, 7, 43, 65, 21, 89, 54, 32, 10, 60],
            [5, 72, 38, 91, 6, 47, 29, 83, 51, 17],
            [64, 19, 75, 2, 57, 30, 94, 40, 11, 70],
            [87, 33, 14, 48],
            [33, 14, 48],
            [99, 85],
            [17, 85],
            [16, 68, 41, 36, 8, 73, 58, 20, 85, 49],
            [76, 27, 9, 55, 39, 13, 69, 80, 42, 31],
            [99, 1, 46, 63, 24, 86, 53, 35, 15, 66],
            [18, 71, 37, 93, 22, 44, 28, 82, 50, 77],
            [62, 25, 74, 0, 59, 88, 3, 67, 97, 43],
        ],
    },
    completeness: {
        labels: ['col1','col2','col3','col4','col5','col6','col7','col8','col9'],
        data: [76,96,34,65,78,12,63,89,76,96,34,65,78],
    }
};

const defaultChartOptions = {
    scales: {
        y: {
            beginAtZero: true,
            max: 100
        }
    }
};

const chartConfigurations = {
    accuracyOverall: {
        type: 'polarArea',
        data: {
            labels: chartData.accuracy.labels[0],
            datasets: [{
                data: chartData.accuracy.data[4], 
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'left',
                },
            }
        },
    },
    completenessOverall: {
        type: 'polarArea',
        data: {
            labels: chartData.accuracy.labels[1],
            datasets: [{
                data: chartData.accuracy.data[5], 
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'left',
                },
            }
        },
    },
    consistencyOverall: {
        type: 'polarArea',
        data: {
            labels: chartData.accuracy.labels[2],
            datasets: [{
                data: chartData.accuracy.data[6], 
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'left',
                },
            }
        },
    },
    timelinessOverall: {
        type: 'polarArea',
        data: {
            labels: chartData.accuracy.labels[3],
            datasets: [{
                data: chartData.accuracy.data[7], 
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'left',
                },
            }
        },
    },
    accuracyChart: {
        type: 'bar',
        data: {
            labels: chartData.accuracy.labels[6],
            datasets: [{
                label: 'Syntactic Accuracy',
                data: chartData.accuracy.data[0],
                backgroundColor: 'rgba(54, 162, 235, 0.5)', 
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: defaultChartOptions 
    },
    tuplesChart: {
        type: 'bar',
        data: {
            labels: chartData.accuracy.labels[6],
            datasets: [{
                label: 'Accurate Tuples Ratio',
                data: chartData.accuracy.data[1],
                backgroundColor: 'rgba(54, 162, 235, 0.5)', 
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: defaultChartOptions 
    },
    validationChart: {
        type: 'bar',
        data: {
            labels: chartData.accuracy.labels[6],
            datasets: [{
                label: 'Domain-Specific Validation Rules',
                data: chartData.accuracy.data[2],
                backgroundColor: 'rgba(54, 162, 235, 0.5)', 
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: defaultChartOptions 
    },
    externalChart: {
        type: 'bar',
        data: {
            labels: chartData.accuracy.labels[6],
            datasets: [{
                label: 'Conformity',
                data: chartData.accuracy.data[3],
                backgroundColor: 'rgba(54, 162, 235, 0.5)', 
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: defaultChartOptions 
    },
};

// Utility Functions 
function applyConditionalColors(chartConfig, datasetIndex, threshold, belowColor, aboveColor) {
    chartConfig.data.datasets[datasetIndex].backgroundColor = chartConfig.data.datasets[datasetIndex].data.map(value => {
        return value < threshold ? belowColor : aboveColor; 
    });
}

function renderChart(chartId, chartConfig) {
    const chartCanvas = document.getElementById(chartId);
    new Chart(chartCanvas, chartConfig);
}

// Apply conditional colors
applyConditionalColors(chartConfigurations.accuracyOverall, 0, 50, 'rgba(255, 0, 0, 0.5)', 'rgba(54, 162, 235, 0.5)');
applyConditionalColors(chartConfigurations.completenessOverall, 0, 50, 'rgba(255, 0, 0, 0.5)', 'rgba(54, 162, 235, 0.5)');
applyConditionalColors(chartConfigurations.consistencyOverall, 0, 50, 'rgba(255, 0, 0, 0.5)', 'rgba(54, 162, 235, 0.5)');
applyConditionalColors(chartConfigurations.timelinessOverall, 0, 50, 'rgba(255, 0, 0, 0.5)', 'rgba(54, 162, 235, 0.5)');
applyConditionalColors(chartConfigurations.accuracyChart, 0, 50, 'rgba(255, 0, 0, 0.5)', 'rgba(54, 162, 235, 0.5)');
applyConditionalColors(chartConfigurations.tuplesChart, 0, 50, 'rgba(255, 0, 0, 0.5)', 'rgba(54, 162, 235, 0.5)');
applyConditionalColors(chartConfigurations.validationChart, 0, 50, 'rgba(255, 0, 0, 0.5)', 'rgba(54, 162, 235, 0.5)');
applyConditionalColors(chartConfigurations.externalChart, 0, 50, 'rgba(255, 0, 0, 0.5)', 'rgba(54, 162, 235, 0.5)');

// Render charts
renderChart('accuracyOverall', chartConfigurations.accuracyOverall); 
renderChart('completenessOverall', chartConfigurations.completenessOverall); 
renderChart('consistencyOverall', chartConfigurations.consistencyOverall); 
renderChart('timelinessOverall', chartConfigurations.timelinessOverall); 
renderChart('accuracyChart', chartConfigurations.accuracyChart); 
renderChart('tuplesChart', chartConfigurations.tuplesChart);    
renderChart('validationChart', chartConfigurations.validationChart);    
renderChart('externalChart', chartConfigurations.externalChart);    

