console.log("app.js loaded");

function getFilenameWithoutExtension(filename) {
  var segments = filename.split(".");
  var extLength = segments[segments.length - 1].length;

  return filename.substr(0, filename.length - (extLength + 1));
}

function shortenString(str, max_length, substitute_string = "...") {
  if (str.length > max_length) {
    startIndex = str.length - max_length;
    return substitute_string + str.substring(startIndex);
  } else {
    return str;
  }
}

// Init Custom Drag Drop
document.querySelectorAll("label[data-drag-drop]").forEach((label) => {
  console.log("Init Drag Drop:");
  console.log(label);

  var srcEl = document.getElementById(label.dataset.inputId);
  var isMultiple = srcEl.multiple;

  var imgEl = label.querySelector("img.preview");
  var errorList = label.querySelector("ul.errors");

  // Details
  var detailsEl = label.querySelector(".details");
  var detailsHeaderEl = detailsEl.querySelector("h4");
  var listOfFilesEl = detailsEl.querySelector("ul");

  // Hide details on load
  detailsEl.style.visibility = "hidden";

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

    // Parse Accepted File Types from <input [accept]>
    var acceptedFileTypes = srcEl.accept
      .split(",")
      .map((type) => type.trim().replace("*", ""));

    // For each file selected
    for (var f of srcEl.files) {
      var isFileValid = false;

      // Check the file against each accepted file types
      for (var type of acceptedFileTypes) {
        if (f.type.includes(type) || f.name.includes(type)) {
          isFileValid = true;
          break;
        }
      }

      if (!isFileValid) {
        errors.push(
          `Only accepts ${acceptedFileTypes.join(", ")}. Detected a "${
            f.type
          }" file (${f.name}).`
        );
        break;
      }
    }

    showErrors(errors);

    // #endregion

    // Show Details of selected files
    var hasFiles = srcEl.files.length > 0;
    var hasErrors = errors.length > 0;

    if (!!detailsEl && isMultiple) {
      var showDetails = hasFiles && !hasErrors;

      if (showDetails) {
        // Set File Count in Header
        detailsHeaderEl.innerText = ` ${srcEl.files.length} Selected Files`;

        // Clear first
        listOfFilesEl.innerHTML = "";

        for (var f of srcEl.files) {
          var listItem = document.createElement("li");
          var shortenedName = shortenString(f.name, 30);

          listItem.innerText = shortenedName;

          listOfFilesEl.appendChild(listItem);
        }
      }

      label.firstElementChild.style.visibility = showDetails
        ? "hidden"
        : "visible";

      detailsEl.style.visibility = showDetails ? "visible" : "hidden";
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

  var toggles = dropdown.querySelectorAll("[data-toggle]");
  var dropdownContent = dropdown.querySelector(".dropdown_content");

  toggles.forEach((toggle) => {
    toggle.addEventListener("click", (e) => {
      if (!!dropdownContent) {
        dropdownContent.classList.toggle("active");
      }
    });
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
