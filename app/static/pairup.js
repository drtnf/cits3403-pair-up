//script for java script functions for SPA pair-up app  
//

///Data
var authToken=null;//or store in a cookie?
var snum=null;//or store in a cookie?
var student=null;
var url=location.hostname; //use navigator to compute current url for requests
var project = null;

///DOM elements
var loginButton, projectButton, loginPanel, projectPanel, projectTable, snum, pin, partnerNum, projectDesc, labSelect;


////////////////HTML Rendering Functions//////////////
function setUp(){
  loginButton = document.getElementById('log');
  projectButton = document.getElementById('project');
  loginPanel = document.getElementById('login-panel');
  snum = document.getElementById('snum');
  pin = document.getElementById('pin');
  projectPanel = document.getElementById('project-panel');
  partnerNum1 = document.getElementById('partnerNum1');
  partnerNum2 = document.getElementById('partnerNum2');
  partnerNum3 = document.getElementById('partnerNum3');
  projectDesc = document.getElementById('projectDesc');
  labSelect = document.getElementById('labs');
  projectTable = document.getElementById('projectTable');
  loginButton.onclick = function(){
    if(authToken==null)
      loginPanel.hidden=!loginPanel.hidden;
    else{
      logout();
      loginButton.innerHTML='Login';
      loginPanel.hidden=true;
      projectPanel.hidden=true;
      renderTable([]);
    }
  };
  projectButton.onclick=function(){
    projectPanel.hidden=!projectPanel.hidden;
  };
}

function renderTable(projectList){
  tableHeader=document.getElementById('tableHeader');
  projectTable.innerText='';
  projectTable.appendChild(tableHeader);
  for(var i =0; i<projectList.length; i++){
    tr = document.createElement('TR');
    if(project!=null && project['pid']==projectList[i]['pid']) tr.setAttribute('bg-color','green');
    td=document.createElement('TD');
    td.innerHTML=i+1;
    tr.appendChild(td);
    td=document.createElement('TD');
    td.innerHTML=projectList[i]['team'];
    tr.appendChild(td);
    td=document.createElement('TD');
    td.innerHTML=projectList[i]['description'];
    tr.appendChild(td);
    td=document.createElement('TD');
    td.innerHTML=projectList[i]['lab'];
    tr.appendChild(td);
    projectTable.appendChild(tr);
  }
  projectTable.hidden=false;
}

function renderProject(){
  if(project==null){
    projectPanel.title.innerHTML='New Project';
    partnerNum.hidden=False;
    projectDesc.value='';
    projectPanel.delete.hidden=true;
  }
  else{
    document.getElementById('title').innerHTML=project['team']+"'s Project";
    partnerNum.hidden=true;
    projectDesc.value=project['description'];
    document.getElementById('delete').hidden=false;
  }
  //getlabs with callback
  //expected format {available_labs:[{labid:3,lab:'lab2.01, Monday 3pm'},...]
  if(authToken==null) return;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if(this.readyState==4 && this.status==200){
      responseData = JSON.parse(this.responseText);
      availableLabs = responseData['available_labs'];
      if(project!=null){
        availableLabs.unshift({'lab_id': project['lab_id'], 'lab': project['lab_name']});
      }
      labSelect.innerHtml='';
      for(var i = 0; i<availableLabs.length; i++){
        opt = document.createElement('OPTION');
        opt.value = availableLabs[i]['lab_id'];
        opt.innerText = availableLabs[i]['lab'];
        labSelect.appendChild(opt);
      }
    }
    else if(this.readyState==4){
      alert(this.statusText);
    }
  }
  xhttp.open('GET','/api/labs/',true);
  xhttp.setRequestHeader("Authorization","Bearer "+authToken);
  xhttp.send();
}


//////////////HTTP Request handlers//////////////////////

//Expected data format 
//{token:"HASHef+HASH', expiry:'2019-5-30T12:00'}
function login(){
  if(authToken!=null) logout();
  else{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
      if(this.readyState==4 && this.status==200){
        responseData = JSON.parse(this.responseText);
        authToken = responseData['token'];
        loginButton.innerHTML='Logout';
        loginPanel.hidden=true;
        projectButton.hidden=false;
        getStudent(snum.value);
      }
      else if(this.readyState==4)
        alert(this.statusText);
    };
    xhttp.open('POST','/api/tokens',true,user=snum.value, psw=pin.value);
    xhttp.send();
  }
}

function logout(){
  if(authToken==null) return;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if(this.readyState==4 && this.status==204){
      authToken=null;
      student=null;
      project=null;
      document.getElementById('log').value='Login';
      loginPanel.hidden=true;
      projectPanel.hidden=true;
      projectButton.hidden=true;
      renderTable([]);
    }
    else{
      alert(this.statusText);
    }
  }
  xhttp.open('DELETE','/api/tokens',true);
  xhttp.setRequestHeader("Authorization","Bearer "+authToken);
  xhttp.send();
}


//Assumes data format {id:19617810, name:'Tim'}
function getStudent(id){
  if(authToken==null) return;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if(this.readyState==4 && this.status==200){
      responseData = JSON.parse(this.responseText);
      student = responseData;
      getProject();
    }
    else if(this.readyState==4 && this.status!=404){
      alert(this.statusText);
    }
  }
  xhttp.open('GET','/api/students/'+id,true);
  xhttp.setRequestHeader("Authorization","Bearer "+authToken);
  xhttp.send();
}

//Assumes data format {'projectList': [p1,p2,p3]}
//where pi = {pid:23, team:'Tim & Friends', description:'Project', lab_id:3, lab='2.01 Mon 3pm'}
function getProjectList(){
  if(authToken==null) return;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if(this.readyState==4 && this.status==200){
      responseData = JSON.parse(this.responseText);
      projectList = responseData['projectList'];
      renderTable(projectList);
    }
    else if(this.readyState==4){
      alert(this.statusText);
    }
  }
  xhttp.open('GET','/api/projects/',true);
  xhttp.setRequestHeader("Authorization","Bearer "+authToken);
  xhttp.send();
}



//Assumes data format 
//{pid:23, team:'Tim & Friends', description:'Project', lab_id:3, lab='2.01 Mon 3pm'}
function getProject(){
  if(authToken==null) return;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if(this.readyState==4 && this.status==200){
      responseData = JSON.parse(this.responseText);
      project = responseData;
      renderProject();
      getProjectList();
    }
    else if(this.readyState==4 && this.status!=404){
      alert(this.statusText);
    }
  }
  xhttp.open('GET','/api/students/'+student['id']+'/project',true);
  xhttp.setRequestHeader("Authorization","Bearer "+authToken);
  xhttp.send();
}

//sends data {partnerNUmber:'19617810', description:'Project', lab_id:3}
function newProject(){
  //POST request with new fields for project
  if(authToken==null) return;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if(this.readystate==4 && this.status==201){
      getProject();
    }
    else if(this.readystate==4){
      alert(this.statusText);
    }
  }
  var project={};
  project['partnerNumber1']=partnerNum1.value;
  project['partnerNumber2']=partnerNum2.value;
  project['partnerNumber3']=partnerNum3.value;
  project['description']=projectDesc.value;
  project['lab_id']=labSelect.value;
  xhttp.open('POST','/api/students/'+student['id']+'/project',true);
  xhttp.setRequestHeader("Authorization","Bearer "+authToken);
  xhttp.setRequestHeader('Content-Type','application/json');
  xhttp.send(JSON.stringify(project));
}

//sends data {description:'Project', lab_id:3}
function updateProject(){
  //PUT request with new fields for project
  if(project==null) newProject();
  else{
    if(authToken==null) return;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
      if(this.readystate==4 && this.status==200){
        renderProject();
      }
      else if(this.readystate==4){
        alert(this.statusText);
      }
    }
    project['description']=projectDesc.value;
    project['lab_id']=labSelect.value;
    xhttp.open('PUT','/api/students/'+student['id']+'/project',true);
    xhttp.setRequestHeader("Authorization","Bearer "+authToken);
    xhttp.setRequestHeader('Content-Type','application/json');
    xhttp.send(JSON.stringify(project));
  }
}

function deleteProject(){
  if(authToken==null) return;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function(){
    if(this.readystate==4 && this.status==200){
      project = null;
      renderProject();
    }
    else if(this.readystate==4){
      alert(this.statusText);
    }
  }
  xhttp.open('DELETE','/api/students/'+student['id']+'/project',true);
  xhttp.setRequestHeader("Authorization","Bearer "+authToken);
  xhttp.send();
}


