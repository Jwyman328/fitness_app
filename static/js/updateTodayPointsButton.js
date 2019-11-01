// check if a point model exists for today
// if it does make the 'updateTodayPoints' button visibile
// and make its href to the update of todays point model

// make a fetch to the all point modles 
async function getData(){
    let myData = await fetch('/returnAllUserDailyJson');
    let myDataClean = await myData.json();
    let jsonAwait = await myDataClean
    return(jsonAwait);} //will return a promise


getData().then((data) => {
        showButton(data)})

function showButton(data){
    let today = new Date();
    let dd = today.getDate();
    let mm = today.getMonth() + 1; //January is 0!

    let yyyy = today.getFullYear();
        if (dd < 10) {
        dd = '0' + dd;
        } 
        if (mm < 10) {
        mm = '0' + mm;
        } 
     today = yyyy + '-' + mm + '-' + dd;

    let pointDiv = document.getElementById('updateTodayPoints');
    let pointButton = pointDiv.firstElementChild;
    for (let pointModel of data){
        if (pointModel.date == today){
            pointDiv.style.display = 'block';
            pointButton.setAttribute('href', `/daily_input_update/${pointModel.one_to_one_workout}/`) 
        }

    }
}