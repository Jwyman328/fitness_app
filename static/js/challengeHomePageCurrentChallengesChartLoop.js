//console.log(window.location);

async function getDataTwo(){
    let myDataTwo = await fetch('/challenges/returnJsonCurrentChallenge');
    let myDataCleanTwo = await myDataTwo.json();
    let jsonAwaitTwo = await myDataCleanTwo
    return(jsonAwaitTwo);} //will return a promise

// only show the chart if there is data for today
// else give the user a button to input data 

// if there is only one challenge then hide the second challenge div

function hideNonChallengeDiv(data){
    // if it is the challenges home page then we have unlimited charts
    // for each challenge make a div 
    let maxChallengesToCreateDiv = []
    let allDivs = []
    let challengeDivBaseName = 'challenge'
    for (let x = 0; x <data.length; x++ ){
        maxChallengesToCreateDiv.push(x)
        let newDiv = document.createElement('div')
        newDiv.id = challengeDivBaseName + x;
        newDiv.style.height = '400px;'; // might not work
        newDiv.setAttribute('class', "col-12 mx-2 my-4")
        allDivs.push(newDiv)
        document.getElementById('graphsContainer').appendChild(newDiv)
    }
    return [allDivs,maxChallengesToCreateDiv]


}
getDataTwo().then((data) => {
     let divsList = hideNonChallengeDiv(data);
    let allDivs = divsList[0]
    let maxChallengesToGraph = divsList[1]
    showChartThree(data, allDivs, maxChallengesToGraph );
    })

function showChartThree(data,challengeDivs,maxChallengesToGraph){
    // this loop fills array with amount of maps to pull from data variable

    graphColors = ['#84ceeb','#5680E9','#D484EB', '#9AEB84', '#EBA184'];
    pointColors = ['#8860D0','#84ceeb','#9BEB84','#EBA084'];
    for (let challengeNum of maxChallengesToGraph ){
    
        //let func_name = 'challenge' + `${challengeNum}`;
    new Highcharts.Chart({ 
    chart: {
        backgroundColor: graphColors[challengeNum] ,
        renderTo: challengeDivs[challengeNum], //change what div to put it in
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
    

