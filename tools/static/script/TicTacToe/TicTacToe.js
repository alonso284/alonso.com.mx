var turn = "X", next = "O";
var xwins = 0, owins = 0;

function isFull(arr){
  var q = 0;
  
  for(var i = 0; i < 9; i++){
    if(arr[i].innerText != "") q++;
  }

  if(q == 9){
    restart(arr);
  }
  return;
}

function winner(arr){
  var complete = "";

  for(var i = 0, j = 0; i <= 3, j <= 6; i++, j+=3){
    
    if(arr[i].innerText != "" && arr[i].innerText == arr[i+3].innerText && arr[i].innerText == arr[i+6].innerText)
    complete = arr[i].innerText;


    if(arr[j].innerText != "" && arr[j].innerText == arr[j+1].innerText && arr[j].innerText == arr[j+2].innerText)
    complete = arr[j].innerText;

  }

  if(arr[4].innerText != "" && arr[4].innerText == arr[0].innerText && arr[4].innerText == arr[8].innerText)
    complete = arr[4].innerText;

  if((arr[4].innerText != "") && arr[4].innerText == arr[2].innerText && arr[4].innerText == arr[6].innerText)
    complete = arr[4].innerText;

  if(complete){
    restart(arr);
  }

  return complete;

}

function restart(arr){
  for(var i = 0; i < 9; i++){
    arr[i].innerHTML = "";
  }
  return;
}


document.addEventListener('click', function(event) {

    var block = document.getElementById(event.target.id);

    if(block.innerText == "" && block.id != ""){
      block.innerHTML = turn;
      block.className = turn;
      [turn, next] = [next, turn];
    }

    var arr = document.querySelectorAll("td");

    var complete = winner(arr);
    isFull(arr);
    
    if(complete != ""){
      if(complete == "O"){
        document.getElementById("O").innerHTML = ++owins;
      }else{
        document.getElementById("X").innerHTML = ++xwins;
      }
    }
    
}, true);