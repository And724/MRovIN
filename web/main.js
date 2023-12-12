//Initialize Rover related constants
const possibleCameras = {
  Perseverance :   ["EDL_RUCAM", "EDL_RDCAM", "EDL_DDCAM", "EDL_PUCAM1", "EDL_PUCAM2", 
                    "NAVCAM_LEFT", "NAVCAM_RIGHT", "MCZ_RIGHT", "MCZ_LEFT", "FRONT_HAZCAM_LEFT_A", 
                    "FRONT_HAZCAM_RIGHT_A", "REAR_HAZCAM_LEFT", "REAR_HAZCAM_RIGHT", "SKYCAM", "SHERLOC_WATSON"],
  Curiosity    :   ["FHAZ", "RHAZ", "MAST", "CHEMCAM", "MAHLI", "MARDI", "NAVCAM"],
  Opportunity  :   ["FHAZ", "RHAZ", "NAVCAM", "PANCAM", "MINITES"],
  Spirit       :   ["FHAZ", "RHAZ", "NAVCAM", "PANCAM", "MINITES"]
};

const defaultRover = "Perseverance";
const defaultCamera = possibleCameras[defaultRover][0];
const configContainer = document.getElementById("currentConfig")

function currentConfig(config) {
  configContainer.innerHTML = " ";
  const configElement = document.createElement("div");
  configElement.classList.add("config");

  configElement.innerHTML = `
    <h2>${config[0]} : ${config[1]}</h2>
  `;
  configContainer.appendChild(configElement);
};

//Updates list of available cameras for a given rover. Uses possibleCameras constant
//and the rover name to populate the list with the appropriate cameras.  
function populateCameras(roverName) {
  const cameraList = document.getElementById("cameraNames");
  cameraList.innerHTML = ""; 

  const cameras = possibleCameras[roverName] || [];

  cameras.forEach(camera => {
    const listItem = document.createElement("li");
    const cameraName = document.createElement("button");
    cameraName.classList.add("buttonList");
    cameraName.textContent = camera;
    cameraName.onclick = function() {
      eel.set_camera(camera);
      let config = [roverName, camera]
      currentConfig(config)
    };
    
    listItem.appendChild(cameraName);
    cameraList.appendChild(listItem);
  });
  
  cameraList.addEventListener("click", cameraSelect);
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
document.addEventListener("DOMContentLoaded", function() { 
  const roverButtons = document.querySelectorAll('.menuList');

roverButtons.forEach(button => {
  button.addEventListener('click', function() {
    getRover(button.innerText);
  });
 });
});

//Passes user entered text to python backend. Checks that text is valid. 
function userQuery() {
  document.body.classList.add('loading');
  let text = document.getElementById("enterQuery").value;

   const integerRegex = /^\d+$/;
   const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
   
   if (integerRegex.test(text)) {
     eel.query(text);
     queryWait()
   } else if (dateRegex.test(text)) {
     queryWait()
     eel.query(text);
   } else {
     window.alert("Please enter a non-negative integer or a date in the format YYYY-MM-DD!");
   };
 };

function randomQuery(){
  eel.random_query();
  document.body.classList.add('loading');
  queryWait()
};

function recentPhoto(){
  document.body.classList.add('loading');
  eel.query("latest_photos");
};

const dataContainer = document.getElementById("dataContainer");

eel.expose(displayData);
function displayData(returnedData) {
  dataContainer.innerHTML = " ";
  const dataElements = document.createElement("div");
  dataElements.classList.add("data");

  dataElements.innerHTML = `
    <h2>Rover: ${returnedData.rover} <br> Camera: ${returnedData.camera}</h2>
    <p>Earth Date: ${returnedData.earth_date} Equivalent Sol: ${returnedData.sol}</p>
    <p>It has been ${returnedData.elapsed_days} day(s) since this photo was taken by ${returnedData.rover}!</p>
    <img src="${returnedData.img_link}" alt="Mars Rover Image" class="imageSize"/> 
  `;
  dataContainer.appendChild(dataElements);

  const savedData = JSON.parse(localStorage.getItem("savedData")) || [];
  const uniqueData = new Set(savedData.map(query => query.imgLink));
  document.body.classList.remove('loading');

  if (!uniqueData.has(returnedData.img_link)) {
  const currentQuery = {
    rover: returnedData.rover,
    camera: returnedData.camera,
    earthDate: returnedData.earth_date,
    sol: returnedData.sol,
    elapsedDays: returnedData.elapsed_days,
    imgLink: returnedData.img_link
  };

  savedData.push(currentQuery)
  localStorage.setItem("savedData", JSON.stringify(savedData))
  };
};

document.addEventListener("DOMContentLoaded", function() {
  // Retrieve the saved data from local storage
  const savedData = JSON.parse(localStorage.getItem("savedData")) || [];

  // Check if there is any saved data
  if (savedData.length > 0) {
    const sessionSummary = document.getElementById("sessionSummary");

    // Loop through each saved query and display it on the summary page
    savedData.forEach(query => {
      const queryResult = document.createElement("div");
      queryResult.innerHTML = `
        <h2>Rover: ${query.rover} Camera: ${query.camera}</h2>
        <p>Earth Date: ${query.earthDate} Equivalent Sol: ${query.sol}</p>
        <p>It has been ${query.elapsedDays} day(s) since this photo was taken by ${query.rover}!</p>
        <img src="${query.imgLink}" alt="Mars Rover Image" class="imageSize"/> 
      `;
      sessionSummary.appendChild(queryResult);
    });
  }
});

function clearSummary() {
  summary = document.getElementById("sessionSummary");
  localStorage.removeItem("savedData")
  summary.innerHTML = " ";
}

function queryWait() {
  window.alert("Please Wait. If a query is not found, we will find the next available option. Searching.......");
};

function setDefaultRoverAndCamera() {
  const defaultConfig = document.getElementById("currentConfig")
  defaultConfig.innerHTML = `
    <h2> Perseverance : EDL_RUCAM </h2>
  `
};

window.addEventListener("load", setDefaultRoverAndCamera)