var el = x => document.getElementById(x);

function showPicker() {
  el("file-input").click();
}

function showPicked(input) {
  el("upload-label").innerHTML = input.files[0].name;
  var reader = new FileReader();
  reader.onload = function(e) {
    el("image-picked").src = e.target.result;
    el("image-picked").className = "";
  };
  reader.readAsDataURL(input.files[0]);
}

function analyze() {
  var imageURL = el('imagename').value;
  var uploadFiles = el("file-input").files;
  var fileData = new FormData();
  var endpoint = '';
  if (imageURL=="" && uploadFiles.length !== 1) 
    alert("Please enter an image url or select a file to analyze!");
  else if (imageURL !== "" && uploadFiles.length !== 1) {
    fileData.append("url", imageURL);
    endpoint = 'classify-url'
  }
  else {
    fileData.append("file", uploadFiles[0]);
    endpoint = 'analyze';
  }

  el("analyze-button").innerHTML = "Analyzing...";
  var xhr = new XMLHttpRequest();
  var loc = window.location;
  xhr.open("POST", `${loc.protocol}//${loc.hostname}:${loc.port}/${endpoint}`,
    true);
  xhr.onerror = function() {
    alert(xhr.responseText);
  };
  xhr.onload = function(e) {
    if (this.readyState === 4) {
      var response = JSON.parse(e.target.responseText);
      el("result-label").innerHTML = `Result = ${response["result"]}`;
    }
    el("analyze-button").innerHTML = "Analyze";
  };

  xhr.send(fileData);
}

function showURL() {
    el("image-picked").src = el('imagename').value;
    el("image-picked").className = "";
}


