async function getDataTwo(){
    let myDataTwo = await fetch('/returnPendingInvitations');
    let myDataCleanTwo = await myDataTwo.json();
    let jsonAwaitTwo = await myDataCleanTwo;
    return(jsonAwaitTwo);} //will return a promise

getDataTwo().then((data) => {
        showPending(data);
        })

function showPending(data){
    if (data.length == 0){
        //
    }else{

    
    if (document.getElementById("PendingChalengeAlert")){
        // do nothing alert exists
    }else{
        msg = 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations'
        newDiv = document.createElement('div');
        newDiv.setAttribute('class', "alert alert-warning alert-danger fade show")
        newDiv.setAttribute('id', "PendingChalengeAlert")
        
        newDiv.textContent = 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations'
        navArray = document.getElementsByTagName('nav');
        navArray[0].insertAdjacentElement('afterend', newDiv )
    }}
      ;
    
   

}
