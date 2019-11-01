
let att = "{{object}}"
console.log(att);
async function getDataTwo(){
    let myDataTwo = await fetch('/challenges/returnAllUserChallenges');
    let myDataCleanTwo = await myDataTwo.json();
    let jsonAwaitTwo = await myDataCleanTwo;
    return(jsonAwaitTwo);} //will return a promise

// only show the chart if there is data for today
// else give the user a button to input data 

getDataTwo().then((data) => {

    showChartTwo(data[0]);
    })

function showChartTwo(data){

    
    window.chart3 = new Highcharts.chart({
    chart: {
        
        renderTo: 'currentChallenge',
        type: 'column',

    },
    title: {
        text: `Challenge: ${data["challenge_info"]['title']}`
    },
    subtitle: {
        text: `Start Date: ${data["challenge_info"]['startDate']}
                End Date: ${data["challenge_info"]['endDate']}`
    },
    xAxis: {
        categories: data['data']['userNames'],
        crosshair: true
    },
    yAxis: {
        min: 0,
        title: {
            text: "Points"
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
        name: `${data["challenge_info"]['field']}`,
        data: data['data']['points']
    }]
    });} 
    

