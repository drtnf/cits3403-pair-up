let table_data = [];
let current_guess = 0;
let current_cell = 0;


function init(){
  let table = document.getElementById("guesses");
  table.innerHTML="";
  let tbody = document.createElement("tbody");
  for(let i = 0; i<6; i++){
    let row_data = [];
    let row = document.createElement("TR");
    for(let j = 0; j<5; j++){
      let cell = document.createElement("TD");
      cell.innerHTML="&nbsp&nbsp&nbsp";
      row.appendChild(cell);
      row_data[j] = cell;
    }
    table_data[i] = row_data;
    tbody.appendChild(row);
  }
  tbody.children[0].classList.add("active");
  table.appendChild(tbody);
  current_guess = 0;
  current_cell = 0;
  getTimeLeft();
  document.getElementById("close").addEventListener("click", function(){
    document.getElementById("end_game").style.display = 'none';
  });
}

function getTimeLeft(){
    const xhttp = new XMLHttpRequest();
    xhttp.open("GET", "https://drtnf.net/wordle_time_left", true);
    xhttp.onload = function(e) {
      time_left = JSON.parse(xhttp.responseText).time_left;
      let x = setInterval(function() {
        document.getElementById("time_left").innerHTML = time_left--;
        if(time_left<0){
          clearInterval(x);
          init();
        }
      }, 1000);

    };
    xhttp.send();
}

function wait(){

}

function isAlpha(c){
  return /^[A-Z]$/i.test(c);
}

document.addEventListener("keydown", evt =>{
  let key = evt.key;
  if(key.length==1 && isAlpha(key) && current_cell<5 && current_guess<6){
    table_data[current_guess][current_cell].innerHTML=key.toUpperCase();
    current_cell++;  
  }
  else if((key=="Delete" || key == "Backspace") && current_cell>0 && current_guess<6){
    current_cell--;
    table_data[current_guess][current_cell].innerHTML="&nbsp&nbsp&nbsp";
  }
  else if(key == "Enter" && current_cell == 5 && current_guess<6){
    let guess="";
    for(let i = 0; i<5; i++){
      guess = guess + table_data[current_guess][i].innerHTML;
    }
    const xhttp = new XMLHttpRequest();
    
    xhttp.open("GET", "https://drtnf.net/wordle_guess?guess="+guess, true);
    xhttp.onload = function(e) {
      let result = JSON.parse(xhttp.responseText).outcome;
      let sum = 0
      for(let i = 0; i<5; i++){
        if(result[i]==2){
          sum+=result[i];
          table_data[current_guess][i].classList.add('correct');
        }
        if(result[i]==1){
          table_data[current_guess][i].classList.add('misplaced');
        }
      }
      let tbody = document.getElementById("guesses").firstChild;
      tbody.children[current_guess++].classList.remove('active');
      if(sum==10){
        document.getElementById('end_game').style.display="block";
        document.getElementById('congrats').innerHTML="Congratulations!";
      }
      else{
        current_cell = 0;
        if(current_guess>5){
          document.getElementById('end_game').style.display="block";
          document.getElementById('congrats').innerHTML="Out of guesses!";
        }
        else tbody.children[current_guess].classList.add('active');
      }
    }
    xhttp.send();
  }
});



window.onload = init;


  
