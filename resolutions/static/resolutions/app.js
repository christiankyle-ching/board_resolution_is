console.log("app.js loaded");

function getFilenameWithoutExtension(filename) {
  var segments = filename.split(".");
  var extLength = segments[segments.length - 1].length;

  return filename.substr(0, filename.length - (extLength + 1));
}

// Init Custom Drag Drop
document.querySelectorAll("label[data-drag-drop]").forEach((label) => {
  console.log("Init Drag Drop:");
  console.log(label);

  var srcEl = document.getElementById(label.dataset.inputId);
  var isMultiple = srcEl.multiple;

  var imgEl = label.querySelector("img.preview");
  var countEl = label.querySelector(".counter");
  var errorList = label.querySelector("ul.errors");

  if (!isMultiple && !!imgEl) {
    imgEl.dataset.imagePreview = "";
    imgEl.dataset.inputId = label.dataset.inputId;
  }

  var filenamesPreview = document.querySelector(
    "textarea[data-filename-preview]"
  );

  // Hides the original <input type="file"> element
  srcEl.parentElement.classList.add("hiddenField");

  var showErrors = (errors) => {
    if (!!errorList) {
      errorList.innerHTML = "";

      errors.forEach((err) => {
        var el = document.createElement("li");
        el.innerText = err;
        errorList.appendChild(el);
      });
    }
  };

  // Handles every <input> file change
  var onInputFileChange = function (e) {
    // #region Check for errors first
    errors = [];

    if (!isMultiple && srcEl.files.length > 1) {
      errors.push(
        `Multiple images selected. ${srcEl.files[0].name} will only be uploaded.`
      );
    }

    for (var f of srcEl.files) {
      if (!f.type.startsWith("image/")) {
        errors.push(
          `Only images are accepted. Detected a "${f.type}" file (${f.name}).`
        );
        break;
      }
    }

    showErrors(errors);

    // #endregion

    var hasFiles = srcEl.files.length > 0;
    var hasErrors = errors.length > 0;

    // If there's a counter element (use only on multiple)
    if (!!countEl && isMultiple) {
      countEl.innerText =
        hasFiles && !hasErrors ? `${srcEl.files.length} Selected Files` : "";
      label.firstElementChild.style.visibility =
        hasFiles && !hasErrors ? "hidden" : "visible";
    }

    // If there's a <select> for list of filenames
    if (!!filenamesPreview) {
      filenames = [];

      // Clear First
      filenamesPreview.value = "";

      for (var i = 0; i < srcEl.files.length; i++) {
        filenames.push(srcEl.files[i].name);
      }

      filenamesPreview.value = filenames.sort().join(", ");
    }
  };

  srcEl.onchange = onInputFileChange;

  // Custom default drag-drop event
  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    label.addEventListener(
      eventName,
      (e) => {
        e.preventDefault();
        e.stopPropagation();
      },
      false
    );
  });
  label.addEventListener(
    "drop",
    (e) => {
      var dt = e.dataTransfer;
      var files = dt.files;

      srcEl.files = files;

      srcEl.onchange();
    },
    false
  );
});

document.querySelectorAll("[data-image-preview]").forEach((img) => {
  console.log("Init Input Image Preview:");
  console.log(img);

  var srcEl = document.getElementById(img.dataset.inputId);

  if (!!srcEl) {
    srcEl.addEventListener("change", (e) => {
      if (srcEl.files.length > 0) {
        var fr = new FileReader();
        fr.onload = function () {
          img.src = fr.result;
        };
        fr.readAsDataURL(srcEl.files[0]);
      } else {
        img.src = "";
      }
    });
  }
});

// Hide images when not loaded (removes default broken image icon + border)
document.querySelectorAll("img[data-no-broken]").forEach((img) => {
  if (img.src === "") img.style.display = "none";
  img.onload = () => (img.style.display = "unset");
  img.onerror = () => (img.style.display = "none");
});

// Init Dropdown Menus
document.querySelectorAll(".dropdown").forEach((dropdown) => {
  console.log("Init Dropdown:");
  console.log(dropdown);

  var toggle = dropdown.querySelector("[data-toggle]");
  var dropdownContent = dropdown.querySelector(".dropdown_content");

  if (!!toggle) {
    toggle.addEventListener("click", (e) => {
      if (!!dropdownContent) {
        dropdownContent.classList.toggle("active");
      }
    });
  }

  dropdownContent.addEventListener("click", (e) => {
    dropdownContent.classList.remove("active");
  });
});

// Init Multiple Inputs
// Init Dropdown Menus
document.querySelectorAll("form [data-multi-input]").forEach((multiInput) => {
  console.log("Init Multiple Input:");
  console.log(multiInput);

  var inputItem = multiInput.querySelector(".multi-input-item");
  var extraFields = multiInput.querySelector(".extra-fields");
  var addButton = multiInput.querySelector("button[data-add]");

  function addNewItem() {
    var newItem = inputItem.cloneNode(true);

    var deleteButton = newItem.querySelector("button");
    deleteButton.addEventListener("click", (e) => {
      newItem.remove();
    });
    deleteButton.disabled = false;

    newItem.querySelectorAll("input").forEach((input) => (input.value = ""));

    newItem.appendChild(deleteButton);
    extraFields.appendChild(newItem);
  }

  addButton.addEventListener("click", (e) => {
    addNewItem();
  });
});

function deleteParent(e) {
  console.log(e.target);
}
