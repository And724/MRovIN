//Initialize constants
const possibleCameras = {
  Perseverance :   ['edl_rucam', 'edl_rdcam', 'edl_ddcam', 'edl_pucam1', 'edl_pucam2', 
                    'navcam_left', 'navcam_right', 'mcz_right', 'mcz_left', 'front_hazcam_left_a', 
                    'front_hazcam_right_a', 'rear_hazcam_left', 'rear_hazcam_right', 'skycam', 'sherloc_watson'],
  Curiosity    :   ['fhaz', 'rhaz', 'mast', 'chemcam', 'mahli', 'mardi', 'navcam'],
  Opportunity  :   ['fhaz', 'rhaz', 'navcam', 'pancam', 'minites'],
  Spirit       :   ['fhaz', 'rhaz', 'navcam', 'pancam', 'minites']
};

const defaultRover = 'Perseverance';
const defaultCamera = possibleCameras[defaultRover][0];

//Updates list of available cameras for a given rover. Uses possibleCameras constant
//and the rover name to populate the list with the appropriate cameras.  
function populateCameras(roverName) {
  const cameraList = document.getElementById('cameraNames');
  cameraList.innerHTML = ''; 

  const cameras = possibleCameras[roverName] || [];

  cameras.forEach(camera => {
    const listItem = document.createElement('li');
    const cameraName = document.createElement('button');
    cameraName.textContent = camera;
    listItem.appendChild(cameraName);
    cameraList.appendChild(listItem);
  });
  
  cameraList.addEventListener('click', cameraSelect);
}

function getRover(roverName) {
  eel.set_rover(roverName);
  populateCameras(roverName);
};

//Passes the user rover selection to the backend and populateCameras.
function getRover(roverName) {
  eel.set_rover(roverName);
  populateCameras(roverName);
};

//Sidebar navigation behavior 
function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
};

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
};

//Individual functions to handle the selection of each rover separately
//            NOTE: See if this can be combined. It should be able to.
function getP() {
  document.getElementById("P").addEventListener("click", function() {
    let rover = document.getElementById("P").innerText; 
    getRover(rover);
    }
  )
};

function getC() {
  document.getElementById("C").addEventListener("click", function() {
    let rover = document.getElementById("C").innerText; 
    getRover(rover);
    }
  )
};

function getO() {
  document.getElementById("O").addEventListener("click", function() {
    let rover = document.getElementById("O").innerText; 
    getRover(rover);
    }
  )
};

function getS() {
  document.getElementById("S").addEventListener("click", function() {
    let rover = document.getElementById("S").innerText; 
    getRover(rover);
    }
  )
};

//Passes user entered text to python backend. Checks that text is valid. 
function userQuery() {
  let text = document.getElementById("enterQuery").value;
  eel.query(text)
};

function randomQuery(){
  eel.random_query()
};

window.addEventListener('load', setDefaultRoverAndCamera)