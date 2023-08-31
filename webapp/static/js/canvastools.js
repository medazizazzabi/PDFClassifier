let images;
let boxes;
let pagecoutner = 0;
let canvasInfo = [];
let scaleFactor;
let canvasContainerWidth;

function setImage(image) {
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
  });
}

function loadBoxes(Boxes) {
  //for image in images load the boxes and draw them then add them to the canvas and save the canvas info
  for (let i = 0; i < Object.keys(images).length; i++) {
    setImage(images["page" + i]);

    for (let j = 0; j < boxes["page" + i].length; j++) {
      let rect = new fabric.Rect({
        left: Boxes["page" + i][j].x * scaleFactor,
        top: Boxes["page" + i][j].y * scaleFactor,
        width: Boxes["page" + i][j].w * scaleFactor,
        height: Boxes["page" + i][j].h * scaleFactor,
        fill: "transparent",
        strokeWidth: 2,
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

//temp function to simulate the upload of pdf
function uploadPDF() {
  var file = document.getElementById("PDF").files[0];
  //upload it to  server
  var formData = new FormData();
  formData.append("PDF", file);
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "api/uploadPDF", true);
  xhr.onload = function () {
    if (this.status == 200) {
      //get the images from the server {"images":{"page0":"base64","page1":"base64"}}
      images = JSON.parse(this.response).images;
      boxes = JSON.parse(this.response).boxes;

      loadBoxes(boxes);

      //load the images
      canvas.loadFromJSON(canvasInfo[0], function () {
        // After loading, iterate over all objects
        canvas.getObjects().forEach(function (obj) {
          // Check if the object is an image (or use other criteria to identify the background image)
          if (obj.type === "image") {
            obj.set("selectable", false);
          }
        });
        canvas.renderAll();
      });
    }
  };
  xhr.send(formData);
}
//on click of upload button
document.getElementById("uploadbtn").addEventListener("click", uploadPDF);

let canvas = new fabric.Canvas("c", { selection: true, lockUniScaling: true });
canvas.uniScaleTransform = true;
let isDrawing = false;
let rect;

canvas.on("mouse:down", function (o) {
  if (canvas.getActiveObject()) {
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
    strokeWidth: 2,
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

function getWordFromRect(rect) {
  let text = "";
  //convert the rect bound to original pdf size
  let pdfRect = {
    x: rect.left / scaleFactor,
    y: rect.top / scaleFactor,
    w: rect.getScaledWidth() / scaleFactor,
    h: rect.getScaledHeight() / scaleFactor,
  };

  //send the rect to the server
  formData = new FormData();
  formData.append("box", JSON.stringify(pdfRect));
  formData.append("image", images["page" + pagecoutner]);
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "api/OCR", true);
  xhr.onload = function () {
    if (this.status == 200) {
      text = JSON.parse(this.response).text;
      console.log(text);
    }
  };
  xhr.send(formData);
  return text;
}

canvas.on("mouse:up", function () {
  if ((rect && rect.width === 0) || rect.height === 0) {
    canvas.remove(rect);
  }
  getWordFromRect(canvas.getActiveObject());
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
          }
        });
        canvas.renderAll();
      });
    }
  }
});
