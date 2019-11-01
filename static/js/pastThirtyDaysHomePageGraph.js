

async function getDataOne(){
    let myDataOne = await fetch('json30Past30Days');
    let myDataCleanOne = await myDataOne.json();
    let jsonAwaitOne = await myDataCleanOne
    return(jsonAwaitOne);} //will return a promise


getDataOne().then((data) => {

    showChartOne(data)}
    );


    function showChartOne(data){        
        window.chart2 = new Highcharts.chart({
        chart: {
            backgroundColor: '#5AB9EA',
            renderTo: 'pastThirtyDays',
            type: 'line'
        },
        title: {
            text: "PAST 30 DAYS"
        },
        subtitle: {
            text: "Total Daily Points",
            style: {
                fontFamily: 'monospace',
                color: "black"
            }
        },
        xAxis: {
            categories: data[2].onlyDates,
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
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
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
            color: '#8860D0',
            name: 'Health Points',
            data: data[1].pointList
    
        }]
        });} 