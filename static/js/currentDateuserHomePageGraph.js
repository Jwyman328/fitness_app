

async function getData(){
    let myData = await fetch('/jsonData');
    let myDataClean = await myData.json();
    let jsonAwait = await myDataClean
    return(jsonAwait);} //will return a promise

// only show the chart if there is data for today
// else give the user a button to input data 

getData().then((data) => {
    if(data[0]){
        showChart(data)
    }else{
    // create own 0 data
    let today = new Date();
    let dd = String(today.getDate()).padStart(2, '0');
    let  mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    let yyyy = today.getFullYear();

    today = yyyy + '-' + mm + '-' + dd;

    let blankData = [{
        clean_eating_points: 0,
        daily_point_goal: 0,
        date: today,
        sleep_points: 0,
        step_points: 0,
        total_points: 0,
        water_points: 0,
        workout_points: 0,
        }];
    showChart(blankData)
    }
    })

function showChart(data){
    
    window.chart2 = new Highcharts.chart({
    chart: {
        renderTo: 'divLandingTodaysPoints',
        backgroundColor: '#8860D0',
        type: 'column'
    },
    title: {
        text: "TODAY'S POINTS",
        style: {
            fontFamily: 'monospace',
            color: "black"
        }
    },
    subtitle: {
        text: data[0].date,
        style: {
            fontFamily: 'monospace',
            color: "black"
        }
    },
    xAxis: {
        categories: [
            'total',
            'sleep',
            'step',
            'Water',
            'Workout',
            'Clean eating',
        ],
        crosshair: true,
        labels: {
            style: {
                color: 'black'
            }
        } 

    },
    yAxis: {
        min: 0,
        title: {
            text: "Points",
            style: {
                fontFamily: 'monospace',
                color: "black"
            },
        },
        labels: {
            style: {
                color: 'black'
            }
        },
        plotLines: [{
            color: 'red', // Color value
            dashStyle: 'solid', // Style of the plot line. Default to solid
            value: data[0].daily_point_goal,// Value of where the line will appear
            width: 2, // Width of the line   ,
            zIndex: 3
        }]
    },
    
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: [{
        name: 'Total',
        data: [
            data[0].total_points
        ],
        color: '#84ceeb'
    }, {
        name: 'Sleep ',
        data: [
            data[0].sleep_points
        ],
        color: 'green'
    }, 
      
        {
        name: 'Water',
        data: [
            data[0].water_points

        ],
        color: 'blue'
    },           
        {
        name: 'Clean Eating',
        data: [
            data[0].clean_eating_points

        ],
        color: 'orange'
    },

        {
        name: 'Steps',
        data: [
            data[0].step_points

        ],
        color: 'Purple'
    },    
    {
        name: 'Workout',
        data: [
            data[0].workout_points
        ],
        color: 'lightgreen'
    },
   ]
    });} 
    

