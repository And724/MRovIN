const possibleCameras = {
  Perseverance : ['edl_rucam', 'edl_rdcam', 'edl_ddcam', 'edl_pucam1', 'edl_pucam2', 
                  'navcam_left', 'navcam_right', 'mcz_right', 'mcz_left', 'front_hazcam_left_a', 
                  'front_hazcam_right_a', 'rear_hazcam_left', 'rear_hazcam_right', 'skycam', 'sherloc_watson'],
  Curiosity :   ['fhaz', 'rhaz', 'mast', 'chemcam', 'mahli', 'mardi', 'navcam'],
  Opportunity : ['fhaz', 'rhaz', 'navcam', 'pancam', 'minites'],
  Spirit :      ['fhaz', 'rhaz', 'navcam', 'pancam', 'minites']
};

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
}

function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}

function getP() {
  document.getElementById("P").addEventListener("click", function() {
    let rover = document.getElementById("P").innerText; 
    console.log("Clicked");
    getRover(rover);
    }
  )
};

function getC() {
  document.getElementById("C").addEventListener("click", function() {
    let rover = document.getElementById("C").innerText; 
    console.log("Clicked");
    getRover(rover);
    }
  )
};

function getO() {
  document.getElementById("O").addEventListener("click", function() {
    let rover = document.getElementById("O").innerText; 
    console.log("Clicked");
    getRover(rover);
    }
  )
};

function getS() {
  document.getElementById("S").addEventListener("click", function() {
    let rover = document.getElementById("S").innerText; 
    console.log("Clicked");
    getRover(rover);
    }
  )
};

function getRover(roverName) {
  console.log("clicked")
  eel.set_rover(roverName);
  populateCameras(roverName)
};