

async function getDataTwo(){
    let myDataGoals = await fetch('/goals/returnCurrentGoals'); // get just the current goals 
    let myDataPoints = await fetch('/returnAllUserDailyJson');
    let myDataInput = await fetch('/returnAllUserDailyActivityInputJson');

    let myDataGoalsClean = await myDataGoals.json();
    let myDataPointsClean = await myDataPoints.json();
    let myDataInputClean = await myDataInput.json();
    
    return({'pointData':myDataPointsClean  , 'goalData':myDataGoalsClean,
     'inputData': myDataInputClean });
    } //will return a promise

function hideNonChallengeDiv(data){
    // if it is the challenges home page then we have unlimited charts
    // for each challenge make a div 
    let maxChallengesToCreateDiv = []
    let allDivs = []
    let challengeDivBaseName = 'challenge'
    for (let x = 0; x <data['goalData'].length; x++ ){
        maxChallengesToCreateDiv.push(x)
        let newDiv = document.createElement('div')
        newDiv.id = challengeDivBaseName + x;
        newDiv.style.height = '400px;'; 
        newDiv.setAttribute('class', "col-12 mx-2 my-4")
        allDivs.push(newDiv)
        document.getElementById('graphsContainer').appendChild(newDiv)
    }
    return [allDivs,maxChallengesToCreateDiv]

}
getDataTwo().then((data) => {
    dataToBeLoopedForGraphing = cleanData(data) 

    let divsList = hideNonChallengeDiv(data);
    let allDivs = divsList[0]
    let maxChallengesToGraph = divsList[1]
    
    // send the divs, send parsed data, send a div
    for (let goal = 0; goal < dataToBeLoopedForGraphing.length; goal++){
        let goalAll = dataToBeLoopedForGraphing[goal];
        let divForThisGoal = allDivs[goal];
        let goalInfo = goalAll[0];
        let goalDatesPoints = goalAll[1];

        let dates = [...goalDatesPoints.keys()] 
        let points = [...goalDatesPoints.values()]

        let datesWithoutYear = removeYear(dates);

        objActivityTypePointsOptions = ['total_points','sleep_points','water_points',
        'clean_eating_points','workout_points','step_points' ]
        objActivityMetricPoints= ["Points","Points","Points","Points","Points","Points"]

        objActivityTypeNotPointsOptions = [undefined,'Hours_of_sleep', 'Water_100oz',
        'clean_eating', 'workout_amount_of_time', 'steps' ]
        objActivityMetricNotPoints = [undefined, 'Hours','100 OZ','24Hours','Minutes','Steps' ]

        let metricName = undefined;
        let objectActivityType = undefined;              
        if (goalInfo.goal_metric_field == 'total_points' || goalInfo.goal_health_field == 'total_points'){
          returnedValues = setObjActivityTypeAndMetricName(goalInfo.goal_health_field, objActivityTypePointsOptions, objActivityMetricPoints)
          objectActivityType = returnedValues[0]
          metricName = returnedValues[1]
        }else{
          returnedValues = setObjActivityTypeAndMetricName(goalInfo.goal_health_field, objActivityTypeNotPointsOptions, objActivityMetricNotPoints)
          objectActivityType = returnedValues[0]
          metricName = returnedValues[1]
        }

        // if points is a boolean channge it to a number         
        if (goalInfo.goal_metric_field == 'activityMetric' && 
            (goalInfo.goal_health_field == 'water_points' || goalInfo.goal_health_field == 'clean_eating_points')){
            let booleanConvertedPoints = [];
            points.forEach((x) => {booleanConvertedPoints.push(+x)});
            // send to the graph
            showChartThree(datesWithoutYear,booleanConvertedPoints,goalInfo,divForThisGoal, metricName,objectActivityType );

            }else{
                //send to the graph
                showChartThree(datesWithoutYear,points,goalInfo,divForThisGoal, metricName, objectActivityType);

            }

    }

})

function cleanData(data){
    goalData = data['goalData'];
    pointData = data['pointData'];
    inputData = data['inputData'];

    /*for each goal, need the start date, end date, goal_health_field, goal_metric_field
    i wnat to end with goalData, pointData/inputData sum of that goal_health_field, 
    during those dates */
    goalsAndData = []// goalsAndData = [[goal,{date:point, date:points}], [goal,{date:point}]]
    for (let goal of goalData){

        // make array of all dates
        let allDatesStartDateEndDate = getDateArray(goal.goal_start_date, goal.goal_end_date);
        let allDates = allDatesStartDateEndDate[0];
        let startDate = allDatesStartDateEndDate[1];
        let endDate = allDatesStartDateEndDate[2];

        let goalDatesPointsArray = [] 

        goalDatesPointsArray.push(goal)
        

        if (goal.goal_metric_field == "activityMetric" && goal.goal_health_field != "total_points"){ 
            // must convert goal.goal_health_field to one that relates to inputData
            // total points will always access the point data 
            let goal_health_field_input_name = undefined;
            switch (goal.goal_health_field){
                case 'total_points':
                        goal_health_field_input_name = undefined;// error
                        break;
                case 'sleep_points':
                        goal_health_field_input_name = 'Hours_of_sleep';// error
                        break;
                case 'water_points':
                        goal_health_field_input_name = 'Water_100oz';// error
                        break;
                case 'clean_eating_points':
                        goal_health_field_input_name =  'clean_eating';// error
                        break;
                case 'workout_points':
                        goal_health_field_input_name = 'workout_amount_of_time';// error
                        break;
                case 'step_points':
                        goal_health_field_input_name =  'steps';// error
                        break;
            }
            for (let input of inputData){

                let yearEnd = input.date.slice(0,4);
                let correctDate = input.date.slice(5) + `-${yearEnd}`;
                let newDate = new Date(correctDate); // need to get modified data 
                if ( startDate <= newDate && newDate <= endDate){
                    allDates.set(input.date, input[goal_health_field_input_name ])
                }
            } 
        }else{
            for (let point of pointData){
                
                let yearEnd = point.date.slice(0,4);
                let correctDate = point.date.slice(5) + `-${yearEnd}`;
                let newDate = new Date(correctDate); // need to get modified data 
                if ( startDate <= newDate && newDate <= endDate){
                    allDates.set(point.date, point[goal.goal_health_field]);
                    
                    
                }
            } 
            
        }
    goalDatesPointsArray.push(allDates);

    goalsAndData.push(goalDatesPointsArray)
    } 
    return goalsAndData
}

    
function showChartThree(dates,points,goalInfo,divToUse, metricName, objActivityType){

    new Highcharts.Chart({ 
    chart: {
        backgroundColor: '#5AB9EA' ,
        renderTo: divToUse, 
        type: 'line'
    },

    title: {
        text: `Start Date: ${goalInfo.goal_start_date}
                End Date: ${goalInfo.goal_end_date}`,
        style: {
            fontFamily: 'monospace',
            color: "black"
        }

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
            text: metricName,
            style: {
                fontFamily: 'monospace',
                color: "black"
            }
        },
        labels: {
            style: {
                color: 'black'
            }
        },
        plotLines: [{
            color: 'red', // Color value
            dashStyle: 'solid', // Style of the plot line. Default to solid
            value: goalInfo.point_goal,// Value of where the line will appear
            width: 2, // Width of the line   ,
            zIndex: 3
        }]
   
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
        color: 'green',
        name: `${goalInfo.goal_health_field}`,
        data: points,

    }]
    });} 
    

function getDateArray(start, end) {
    // make an array containing dates ranging from a start date to end date
    // change date to month day then year to combat wierd date time manipulation

    let yearEnd = start.slice(0,4);
    let startMMDDyyyy = start.slice(5) + `-${yearEnd}`;
    let endMMDDyyyy = end.slice(5) + `-${yearEnd}`;

    let arr = new Map()
    let dt = new Date(startMMDDyyyy); // will be manipulated
    let endDate = new Date(endMMDDyyyy)
    let startDate = new Date(startMMDDyyyy) // not manipulated can be sent back as startDate
        
    while (dt <= endDate) {
        let newt = new Date(dt)
        let useThis = convertDate(newt)
        arr.set(useThis, 0);
        dt.setDate(dt.getDate() + 1);
        }
    
    return [arr, startDate, endDate];
}

function convertDate(date) {
    var yyyy = date.getFullYear().toString();
    var mm = (date.getMonth()+1).toString();
    var dd  = date.getDate().toString();

    var mmChars = mm.split('');
    var ddChars = dd.split('');
  
    return yyyy + '-' + (mmChars[1]?mm:"0"+mmChars[0]) + '-' + (ddChars[1]?dd:"0"+ddChars[0]);
  }

function setObjActivityTypeAndMetricName(healthField, objActivityTypeOptions, metricNameOptions){
    // function decides value for metricName, objectActivityType
    let metricName = undefined;
    let objectActivityType = undefined;

    switch(healthField){
        case "total_points":
            metricName = metricNameOptions[0]
            objectActivityType = objActivityTypeOptions[0];
            break;
        case "sleep_points":
            metricName = metricNameOptions[1];
            objectActivityType = objActivityTypeOptions[1];
            break;
        case "water_points":
            metricName = metricNameOptions[2];
            objectActivityType = objActivityTypeOptions[2];
            break;
        case "clean_eating_points":
            metricName = metricNameOptions[3];
            objectActivityType = objActivityTypeOptions[3];
            break;
        case "workout_points":
            metricName = metricNameOptions[4];
            objectActivityType = objActivityTypeOptions[4]
            break;
        case "step_points":
            metricName = metricNameOptions[5];
            objectActivityType = objActivityTypeOptions[5]
            break;
}
    // return the two values
    return [objectActivityType, metricName]
  }

function removeYear(dates){
    let finalDates = []
    for (let item of dates){
        let newDate = item.slice(5);
        finalDates.push(newDate)
    }
    return finalDates
}