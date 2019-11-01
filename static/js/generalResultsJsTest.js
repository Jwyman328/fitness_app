
function convertDate(date) {
  var yyyy = date.getFullYear().toString();
  var mm = (date.getMonth()+1).toString();
  var dd  = date.getDate().toString();

  var mmChars = mm.split('');
  var ddChars = dd.split('');

  return yyyy + '-' + (mmChars[1]?mm:"0"+mmChars[0]) + '-' + (ddChars[1]?dd:"0"+ddChars[0]);
}


// get both value for the select 
function getDateArray(start, end) {
    // make an array containing dates ranging from a start date to end date
    var
        arr = new Map(),
        dt = new Date(start);
    
    while (dt < end) {
        let newt = new Date(dt)
        let useThis = convertDate(newt)
        arr.set(useThis, 0);
        dt.setDate(dt.getDate() + 1);
        }
    return arr;
}
      
let DataRangeSelect = document.getElementById('dataRangeSelect')
let DataTypeSelect = document.getElementById('dataTypeSelect')
    

// call the graph maker on startup  
changeGraph();    

// add event listener on change of type or date range
DataRangeSelect.addEventListener('change', (ev) => {changeGraph(ev)})
DataTypeSelect.addEventListener('change', (ev) => {changeGraph(ev)})


function changeGraph(ev){
    
    async function getDataOne(){
        ///get user point data
        let myDataOne = await fetch('/returnAllUserDailyJson');
        let myDataCleanOne = await myDataOne.json();
        let jsonAwaitOne = await myDataCleanOne
        return(jsonAwaitOne);} //will return a promise


    // parse the data form the promise and send it 
    getDataOne().then((data) => {
        renderSelectedDate(data);
        });

    function renderSelectedDate(data){
        // get the selected data range and type
        // then send that data to build graph 
        let DataRangeSelect = document.getElementById('dataRangeSelect')
        let DataTypeSelect = document.getElementById('dataTypeSelect')
        
        // depending on the data range, create different data array to display
        if (DataRangeSelect.value == '30Days'){
            DaysAgo(data, 30);
        }else if (DataRangeSelect.value == '7Days'){
            DaysAgo(data, 7);
        }else if (DataRangeSelect.value == '60Days'){
            DaysAgo(data, 60);
        }else if (DataRangeSelect.value == '90Days'){
            DaysAgo(data, 90);}
        
        
        // make this a function that returns an array of data the user has requested
        function DaysAgo(data, daysAgo){
                let arrayValidObjs = [];
                let today = new Date()
                let AmountDaysAgo = new Date().setDate(today.getDate()-daysAgo);
                let AmountDaysAgoDate = new Date(AmountDaysAgo);

                for (let pointObj of data){
                    let newDate = new Date(pointObj.date);
                    if ( AmountDaysAgoDate < newDate && newDate <= today){
                        arrayValidObjs.push(pointObj)
                    }
                }
                
                
                // make array of [date, 0]
                let datePointArray = getDateArray(AmountDaysAgoDate, today);
                
                let objectActivityType = undefined;
                // get a model attribute name from selected type
                switch(DataTypeSelect.value){
                    case "total":
                        objectActivityType = 'total_points';
                        break;
                    case "sleep":
                    objectActivityType = 'sleep_points';
                        break;
                    case "water":
                        objectActivityType = 'water_points';
                        break;
                    case "cleanEating":
                        objectActivityType = 'clean_eating_points'
                        break;
                    case "workout":
                        objectActivityType = 'workout_points'
                        break;
                    case "steps":
                        objectActivityType = 'step_points'
                        break;
                }
                
                //input the correct type points in the full data array
                for (let item of  arrayValidObjs){
                    
                    datePointArray.set(item.date, item[objectActivityType])
                }
                // turn maps to arrays
                let dates = [...datePointArray.keys()] 
                let points = [...datePointArray.values()]
                // send to be plotted
                showChartOne(dates, points, DataTypeSelect.value);
                dataStats(dates, points, DataTypeSelect.value, datePointArray)
        }
  
    }
        

    function showChartOne(dates, points, typeOfPoints){ 
        window.chart2 = new Highcharts.chart({
        chart: {
            backgroundColor: '#5AB9EA',
            renderTo: 'graphContainer',
            type: 'line'
        },
        title: {
            text: typeOfPoints
        },
        
        xAxis: {
            categories: dates,
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
            name: typeOfPoints + ' Points',
            data: points
    
        }]
        });} 
}

function dataStats(dates, points, typeOfPoints, datePointMap){
    // produce statistics with the data 
    var datePointMap = {};
    dates.forEach((key, i) => datePointMap[key] = points[i]);

    // get the average 
    let AvgPoints = points.reduce((a,b) => a + b, 0) / points.length;

    // get Max, MaxDate
    const arrMax = arr => Math.max(...arr);
    
    function getKeyByValue(object, value) {
        return Object.keys(object).find(key => object[key] === value);}

    let maxPoints = arrMax(points);
    let maxDate = getKeyByValue(datePointMap, maxPoints);

    //get min, minDate
    const arrMin = arr => Math.min(...arr);
    minPoints = arrMin(points);
    let minDate = getKeyByValue(datePointMap, minPoints);

    // total points
    let totalPoints = points.reduce((a,b) => a + b, 0);
    let datatype = typeOfPoints;
    // get elements
    let maxP = document.getElementById('max');
    let minP = document.getElementById('min');
    let avgTitle = document.getElementById('avgTitle');
    let avgBody = document.getElementById('avgBody');
    let totalP = document.getElementById('total');

    maxP.textContent =  `${maxPoints} points on ${maxDate}` ;
    minP.textContent = `${minPoints} points on ${minDate} `;
    avgTitle.textContent = 'Avg ' + typeOfPoints + ' Points';
    avgBody.textContent = Math.round(AvgPoints);
    totalP.textContent = totalPoints;



  

    

    






}
