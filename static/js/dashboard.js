var receivers = Array.from(document.getElementsByClassName('receiver'))


var currentReceiver = 0

document.body.onload = function(){
    receivers.forEach(receiver => {
        receiver.style.display = 'none'
    });
    receivers[currentReceiver].style.display = 'block'
}


function switchReceiver(){

}

function updateReceiver(addReceiver=1){
    receivers[currentReceiver].style.display = 'none'
    currentReceiver = (currentReceiver + addReceiver) % receivers.length
    if(currentReceiver < 0){
        currentReceiver = receivers.length - 1
    }
    receivers[currentReceiver].style.display = 'block'
    console.log(currentReceiver)
}


prev = document.getElementById('prev')
next = document.getElementById('next')
seeDetails = document.getElementById('seeDetails')

prev.onclick = function(){
    updateReceiver(-1)
}

next.onclick = function(){
    updateReceiver(1)
}
