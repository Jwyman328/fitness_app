
async function getDataTwo(){
    let myDataTwo = await fetch('challenges/returnJsonCurrentChallenge');
    let myDataCleanTwo = await myDataTwo.json();
    let jsonAwaitTwo = await myDataCleanTwo
    return(jsonAwaitTwo);} //will return a promise

// only show the chart if there is data for today
// else give the user a button to input data 

// if there is only one challenge then hide the second challenge div

function hideNonChallengeDiv(data){
    // if it is the challenges home page then we have unlimited charts
    
    if (data.length < 2){
        if (data.length == 1){
            challengeDiv = document.getElementById('challenge1').remove(); // delete div that wont be used 

            // make other div a class="col-12 mx-4 my-4"
            challengeAvailableDivClass = document.getElementById('challenge0'); // delete div that wont be used 
       
            //challengeAvailableDivClass.setAttribute("class", "col-12 mx-4 my-4"); 

        }else{
            challengeDiv = document.getElementById('challenge0').remove(); // delete div that wont be used 
            challengeDiv = document.getElementById('challenge1').remove(); // delete div that wont be used 
        }

    }
}
getDataTwo().then((data) => {
    hideNonChallengeDiv(data),
    showChartThree(data);
    })

function showChartThree(data){
    dataLength = data.length
    maxChallengesToGraph = [];

    // this loop fills array with amount of maps to pull from data variable
    for (let x = 0; x <data.length; x++ ){
        maxChallengesToGraph.push(x)
    }
    graphColors = ['#84ceeb','#5680E9'];
    pointColors = ['#8860D0','#84ceeb'];
    for (let challengeNum of maxChallengesToGraph ){
    
        //let func_name = 'challenge' + `${challengeNum}`;
    new Highcharts.Chart({ 
    chart: {
        backgroundColor: graphColors[challengeNum] ,
        renderTo: 'challenge' + `${challengeNum}`, //change what div to put it in
        type: 'column'
    },
    title: {
        text: `CHALLENGE: ${data[challengeNum]["challenge_info"]['title']}`
    },
    subtitle: {
        text: `Start Date: ${data[challengeNum]["challenge_info"]['startDate']}
                End Date: ${data[challengeNum]["challenge_info"]['endDate']}`,
        style: {
            fontFamily: 'monospace',
            color: "black"
        }

    },
    xAxis: {
        categories: data[challengeNum]['data']['userNames'],
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
            }
        },
        labels: {
            style: {
                color: 'black'
            }
        } 
    },
    tooltip: {
        headerFormat: '<span style="font-size:10px"></span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f} points</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: [{
        color: pointColors[challengeNum],
        name: `${data[challengeNum]["challenge_info"]['field']}`,
        data: data[challengeNum]['data']['points']

    }]
    });}} 
    

