const uploadInputEl = document.getElementById("uploadInput");
const dropAreaEl = document.getElementById("dropArea");
const uploadedFileContEl = document.getElementById("uploadedFileCont");
const uploadBtnContEl = document.getElementById("uploadBtnCont");
const browseBtnEl = document.getElementById("browseBtn");
const dropTextEl = document.getElementById("dropText");

dropAreaEl.addEventListener("dragover", dragOver);
dropAreaEl.addEventListener("dragleave", dragLeave);
dropAreaEl.addEventListener("drop", dropItem);
browseBtnEl.addEventListener("click", browseFile);
uploadInputEl.addEventListener("change", uploadFile);

let file = null;

function dragOver(e) {
  e.preventDefault();
  this.classList.add("content-over");
  dropTextEl.innerHTML = `Release to Upload file`;
}

function dragLeave(e) {
  e.preventDefault();
  this.classList.remove("content-over");
  dropTextEl.innerHTML = `Drag & Drop your file`;
}

function browseFile() {
  uploadInputEl.click();
}

function uploadFile() {
  file = this.files[0];
  if (file) {
    file.fileId = getRandomFileId();
    displayFile(file);
  }
}

function dropItem(e) {
  e.preventDefault();
  file = e.dataTransfer.files[0];
  if (file) {
    file.fileId = getRandomFileId();
    displayFile(file);
  }
}

function displayFile(currentFile) {
  uploadedFileContEl.innerHTML = null;
  createFileHolderEl(currentFile);
}

function createFileHolderEl(file) {
  const uploadedFileEl = document.createElement("div");
  uploadedFileEl.classList.add("uploadedFile");

  // Filename
  const fileNameCont = document.createElement("div");
  fileNameCont.classList.add("fileName");

  const fileName = document.createElement("p");
  fileNameCont.appendChild(fileName);
  fileName.innerHTML = file.name;
  uploadedFileEl.appendChild(fileNameCont);

  const closeBtn = document.createElement("div");
  closeBtn.classList.add("closeBtn");
  uploadedFileEl.appendChild(closeBtn);
  closeBtn.innerHTML = `<ion-icon name="close"></ion-icon>`;
  uploadedFileContEl.prepend(uploadedFileEl);
  closeBtn.addEventListener("click", (e) => {
    uploadedFileEl.remove();
    file = null;
    uploadBtnContEl.classList.remove("content-here");
  });
  if (file) {
    uploadBtnContEl.classList.add("content-here");
  }
  dropAreaEl.classList.remove("content-over");
  dropTextEl.innerHTML = `Drag & Drop your file`;
}

function getRandomFileId() {
  return Math.floor(Math.random() * 10000000).toString(16);
}

spinner = document.getElementById("spinner");
yolo = document.getElementById("yolo");
//html load event
window.addEventListener("load", function () {
  spinner.style.display = "block";
  //yolo top 200vh
  yolo.style.top = "200vh";
});

function uploadPDF() {
  var formData = new FormData();
  formData.append("PDF", file);
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "api/uploadPDF", true);
  xhr.onload = async function () {
    if (this.status == 200) {
      //get the images from the server {"images":{"page0":"base64","page1":"base64"}}
      images = JSON.parse(this.response).images;
      boxes = JSON.parse(this.response).boxes;

      await loadBoxes(boxes);

      //load the images
      canvas.loadFromJSON(canvasInfo[0], function () {
        // After loading, iterate over all objects
        canvas.getObjects().forEach(function (obj) {
          // Check if the object is an image (or use other criteria to identify the background image)
          if (obj.type === "image") {
            obj.set("selectable", false);
            obj.set("evented", false);
            obj.set("hoverCursor", "default");
          }
        });
        canvas.renderAll();
      });
      spinner.style.display = "none";
      yolo.style.top = "0";

      //if reponse have fields
      if (JSON.parse(this.response).fields) {
        file1 = JSON.parse(this.response).fields;
      }
    }
  };
  xhr.send(formData);
  file = null;
}

document.getElementById("uploadbtn").addEventListener("click", uploadPDF);

//JSON FILE
const uploadInputEl1 = document.getElementById("uploadInput1");
const dropAreaEl1 = document.getElementById("dropArea1");
const uploadedFileContEl1 = document.getElementById("uploadedFileCont1");
const uploadBtnContEl1 = document.getElementById("uploadBtnCont1");
const browseBtnEl1 = document.getElementById("browseBtn1");
const dropTextEl1 = document.getElementById("dropText1");

dropAreaEl1.addEventListener("dragover", dragOver1);
dropAreaEl1.addEventListener("dragleave", dragLeave1);
dropAreaEl1.addEventListener("drop", dropItem1);
browseBtnEl1.addEventListener("click", browseFile1);
uploadInputEl1.addEventListener("change", uploadFile1);

let file1 = null;

function dragOver1(e) {
  e.preventDefault();
  this.classList.add("content-over");
  dropTextEl.innerHTML = `Release to Upload file`;
}

function dragLeave1(e) {
  e.preventDefault();
  this.classList.remove("content-over");
  dropTextEl.innerHTML = `Drag & Drop your file`;
}

function browseFile1() {
  uploadInputEl1.click();
}

function uploadFile1() {
  file1 = this.files[0];
  if (file1) {
    file1.fileId = getRandomFileId();
    displayFile1(file1);
  }
}

function dropItem1(e) {
  e.preventDefault();
  file1 = e.dataTransfer.files[0];
  if (file1) {
    file1.fileId = getRandomFileId();
    displayFile1(file1);
  }
}

function displayFile1(currentFile) {
  uploadedFileContEl1.innerHTML = null;
  createFileHolderEl1(currentFile);
}

function createFileHolderEl1(file) {
  const uploadedFileEl = document.createElement("div");
  uploadedFileEl.classList.add("uploadedFile");

  // Filename
  const fileNameCont = document.createElement("div");
  fileNameCont.classList.add("fileName");

  const fileName = document.createElement("p");
  fileNameCont.appendChild(fileName);
  fileName.innerHTML = file.name;
  uploadedFileEl.appendChild(fileNameCont);

  const closeBtn = document.createElement("div");
  closeBtn.classList.add("closeBtn");
  uploadedFileEl.appendChild(closeBtn);
  closeBtn.innerHTML = `<ion-icon name="close"></ion-icon>`;
  uploadedFileContEl1.prepend(uploadedFileEl);
  closeBtn.addEventListener("click", (e) => {
    uploadedFileEl.remove();
    file1 = null;
    uploadBtnContEl1.classList.remove("content-here");
  });
  if (file1) {
    uploadBtnContEl1.classList.add("content-here");
  }
  dropAreaEl1.classList.remove("content-over");
  dropTextEl1.innerHTML = `Drag & Drop your file`;
}

const uploadbtn1 = document.getElementById("uploadbtn1");
uploadbtn1.addEventListener("click", uploadJSON);

function convertToNestableList(dataArray) {
  let listHtml = '<ol class="dd-list">';

  dataArray.forEach((data, mainIndex) => {
    // Main item
    listHtml += `<li class="dd-item" data-id="${
      mainIndex + 1
    }"><div class="dd-handle">${data.text}</div>`;

    if (data.fields && data.fields.length) {
      listHtml += '<ol class="dd-list">';
      data.fields.forEach((field, index) => {
        listHtml += `<li class="dd-item" data-id="${mainIndex + 1}-${
          index + 2
        }"><div class="dd-handle">${field.lines}</div></li>`;
      });
      listHtml += "</ol>";
    }

    listHtml += "</li>";
  });

  listHtml += "</ol>";

  return listHtml;
}

let jsonObject;
async function uploadJSON() {
  //post titles as 'categories' and uploaded json file as 'fields' in the request.form
  var formData = new FormData();
  formData.append("categories", JSON.stringify(titles));
  formData.append("fields", file1);
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "api/classify", true);
  xhr.onload = async function () {
    if (this.status == 200) {
      //get the images from the server {"images":{"page0":"base64","page1":"base64"}}
      jsonObject = JSON.parse(this.response);
      document.querySelector("#nestableContainer").innerHTML =
        convertToNestableList(jsonObject.result);

      // Initialize Nestable
      $(".dd").nestable();
    }
  };
  xhr.send(formData);
}

function convertToNestableJSON(dataArray) {
  const result = [];

  dataArray.forEach((data, mainIndex) => {
    let mainItem = {
      id: mainIndex + 1,
      content: data.text,
    };

    if (data.fields && data.fields.length) {
      mainItem.children = [];
      data.fields.forEach((field, index) => {
        let childItem = {
          id: `${mainIndex + 1}-${index + 2}`,
          content: field.lines,
        };
        mainItem.children.push(childItem);
      });
    }

    result.push(mainItem);
  });

  return result;
}

function downloadJSON(data, filename) {
  if (!data) {
    console.error("No data to download");
    return;
  }

  if (!filename) filename = "data.json";

  if (typeof data === "object") {
    data = JSON.stringify(data, null, 4);
  }

  const blob = new Blob([data], { type: "application/json" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.style.display = "none";
  a.href = url;
  a.download = filename;

  document.body.appendChild(a);
  a.click();

  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}
// on #download click
document.getElementById("download").addEventListener("click", function () {
  downloadJSON(convertToNestableJSON(jsonObject.result), "result.json");
});
