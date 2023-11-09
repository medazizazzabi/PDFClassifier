let images;
let boxes;
let pagecoutner = 0;
let canvasInfo = [];
let scaleFactor;
let canvasContainerWidth;
let canvas = new fabric.Canvas("c", { selection: true, lockUniScaling: true });
canvas.uniScaleTransform = true;

let isDrawing = false;
let rect;

function setImage(image) {
  return new Promise((resolve, reject) => {
    let dataURL = "data:image/png;base64," + image;
    fabric.Image.fromURL(dataURL, function (oImg) {
      canvasContainerWidth =
        document.getElementById("canvasContainer").offsetWidth - 16;
      scaleFactor = canvasContainerWidth / oImg.width;

      // Set canvas dimensions
      canvas.setWidth(canvasContainerWidth);
      canvas.setHeight(oImg.height * scaleFactor);

      oImg.set({
        scaleX: scaleFactor,
        scaleY: scaleFactor,
        left: 0,
        top: 0,
        selectable: false,
        evented: false,
      });

      canvas.add(oImg);
      canvas.sendToBack(oImg);
      canvas.renderAll();

      resolve(); // Resolve the promise here
    });
  });
}

async function loadBoxes(boxes) {
  //for image in images load the boxes and draw them then add them to the canvas and save the canvas info
  for (let i = 0; i < Object.keys(images).length; i++) {
    await setImage(images["page" + i]);

    for (let j = 0; j < boxes["page" + i].length; j++) {
      let rect = new fabric.Rect({
        left: boxes["page" + i][j].x * scaleFactor,
        top: boxes["page" + i][j].y * scaleFactor,
        width: boxes["page" + i][j].w * scaleFactor,
        height: boxes["page" + i][j].h * scaleFactor,
        fill: "transparent",
        strokeWidth: 4,
        stroke: "red",
        hasRotatingPoint: false, // Disable rotation
        selectable: true,
        lockRotation: true,
      });
      canvas.add(rect);
    }
    canvas.renderAll();
    canvasInfo[i] = canvas.toJSON();
    canvas.clear();
  }
}

canvas.on("mouse:down", function (o) {
  if (canvas.getActiveObject()) {
    isDrawing = false;
    // If there's an active object, don't start drawing a new rectangle
    return;
  }

  isDrawing = true;
  let pointer = canvas.getPointer(o.e);
  startPoint = { x: pointer.x, y: pointer.y };

  rect = new fabric.Rect({
    left: startPoint.x,
    top: startPoint.y,
    width: 0,
    height: 0,
    fill: "transparent",
    strokeWidth: 4,
    stroke: "red",
    hasRotatingPoint: false, // Disable rotation
    selectable: true,
    lockRotation: true,
  });

  canvas.add(rect);
  if (canvas.getActiveObject()) {
    // If there's an active object, discard it before starting to draw a new rectangle
    canvas.discardActiveObject().renderAll();
  }
});

canvas.on("mouse:move", function (o) {
  if (!isDrawing) return;
  let pointer = canvas.getPointer(o.e);

  // Calculate the rectangle's position and size taking into account the scaling factor
  let origX = startPoint.x / scaleFactor;
  let origY = startPoint.y / scaleFactor;
  let width = Math.abs(startPoint.x - pointer.x) / scaleFactor;
  let height = Math.abs(startPoint.y - pointer.y) / scaleFactor;

  if (origX > pointer.x / scaleFactor) {
    rect.set({ left: pointer.x });
  } else {
    rect.set({ left: startPoint.x });
  }

  if (origY > pointer.y / scaleFactor) {
    rect.set({ top: pointer.y });
  } else {
    rect.set({ top: startPoint.y });
  }

  rect.set({
    width: width * scaleFactor, // scale width to the canvas scale
    height: height * scaleFactor, // scale height to the canvas scale
  });

  canvas.renderAll();
});

function getWordFromRect(rect, page) {
  return new Promise((resolve, reject) => {
    let text = "";
    //convert the rect bound to original pdf size
    let pdfRect = {
      x: rect.left / scaleFactor,
      y: rect.top / scaleFactor,
      w: rect.getScaledWidth() / scaleFactor, //getScaledWidth()
      h: rect.getScaledHeight() / scaleFactor, //getScaledHeight()
    };

    //send the rect to the server
    formData = new FormData();
    formData.append("box", JSON.stringify(pdfRect));
    formData.append("image", images["page" + page]);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "api/OCR", true);
    xhr.onload = function () {
      if (this.status == 200) {
        json = JSON.parse(this.response);
        text = json.text;
        resolve(text); // Resolve the promise here
      } else {
        reject(new Error("Failed to fetch text from server"));
      }
    };
    xhr.onerror = function () {
      reject(new Error("Request error"));
    };
    xhr.send(formData);
  });
}

canvas.on("mouse:up", async function () {
  if (isDrawing && ((rect && rect.width === 0) || rect.height === 0)) {
    canvas.remove(rect);
    isDrawing = false;
    return;
  }
  if (rect === "rect") {
    getWordFromRect(rect, pagecoutner).then((text) => {
      rect.set("text", text);
      canvas.renderAll();
      setTitleList();
    });
  }
  isDrawing = false;
});

document.addEventListener("keydown", function (e) {
  // Check if the delete key (or backspace key) is pressed
  if (e.keyCode === 46 || e.keyCode === 8) {
    let activeObject = canvas.getActiveObject();
    if (activeObject) {
      canvas.remove(activeObject);
      canvas.renderAll();
    }
  }
});

let nextBtn = document.getElementById("NextPage");
let prevBtn = document.getElementById("PrevPage");

nextBtn.addEventListener("click", function () {
  if (pagecoutner < Object.keys(images).length - 1) {
    canvasInfo[pagecoutner] = canvas.toJSON(); // save the canvas info for the current page
    canvas.clear();
    pagecoutner++;
    setImage(images["page" + pagecoutner]);
    //load the canvas info for the next page
    if (canvasInfo[pagecoutner]) {
      canvas.loadFromJSON(canvasInfo[pagecoutner], function () {
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
    }
  }
});

prevBtn.addEventListener("click", function () {
  canvasInfo[pagecoutner] = canvas.toJSON();
  if (pagecoutner > 0) {
    canvas.clear();
    pagecoutner--;
    setImage(images["page" + pagecoutner]);
    if (canvasInfo[pagecoutner]) {
      canvas.loadFromJSON(canvasInfo[pagecoutner], function () {
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
      canvas._objects[0].hoverCursor = "default";
    }
  }
});
//on canvas _objects change
canvas.on("object:added", function (e) {
  if (e.target.type === "rect") {
    getWordFromRect(e.target, pagecoutner).then((text) => {
      e.target.set("text", text);
      canvas.renderAll();
      setTitleList();
    });
  }
});

canvas.on("object:modified", function (e) {
  if (e.target.type === "rect") {
    getWordFromRect(e.target, pagecoutner).then((text) => {
      e.target.set("text", text);
      canvas.renderAll();
      setTitleList();
    });
  }
});

canvas.on("object:removed", function (e) {
  if (e.target.type === "rect") {
    e.target.set("text", "");
    canvas.renderAll();
    setTitleList();
  }
});

// For rect in canvas._objects add a li in  #titleList with the text
function setTitleList() {
  let titleList = document.getElementById("titleList");
  titleList.innerHTML = "";
  //inverse the loop to get the last rect first
  for (let i = canvas._objects.length - 1; i >= 0; i--) {
    if (canvas._objects[i].type === "rect") {
      let li = document.createElement("li");
      li.innerHTML = canvas._objects[i].text;
      titleList.appendChild(li);
    }
  }
}
let saveTitle = document.getElementById("saveTitle");
saveTitle.addEventListener("click", saveTitles);

let titles = [];
async function saveTitles() {
  //loop canvasInfo and save the titles in titles
  for (let i = 0; i < canvasInfo.length; i++) {
    canvas.loadFromJSON(canvasInfo[i], function () {
      // After loading, iterate over all objects
      canvas.getObjects().forEach(async function (obj) {
        // Check if the object is an image (or use other criteria to identify the background image)
        if (obj.type === "rect") {
          title = {
            x: obj.left / scaleFactor,
            y: obj.top / scaleFactor,
            w: obj.getScaledWidth() / scaleFactor,
            h: obj.getScaledHeight() / scaleFactor,
            text: await getWordFromRect(obj, i),
            page: i+1,
          };
          titles.push(title);
        }
      });
    });
  }
}
