const inputBox = document.getElementById("input-box");
const listContainer = document.getElementById("list-container");

const clearTasks = () => {
  listContainer.innerHTML = "";
  saveData();
};

const addTask = () => {
  if (inputBox.value === "") {
    alert("Please enter a task.");
  } else {
    let li = document.createElement("li");

    li.innerHTML = inputBox.value;
    listContainer.appendChild(li);

    let imgCheck = document.createElement("img");
    imgCheck.src = "images/unchecked.png";
    imgCheck.alt = "image of a blank checkbox";
    imgCheck.id = "imgCheck";
    li.insertBefore(imgCheck, li.firstChild);

    let imgCross = document.createElement("img");
    imgCross.src = "images/cross.png";
    imgCross.alt = "image of a cross";
    imgCross.id = "imgCross";
    li.appendChild(imgCross);
  }
  inputBox.value = "";
  saveData();
};

listContainer.addEventListener(
  "click",
  function (e) {
    if (e.target.id == "imgCheck") {
      e.target.parentElement.classList.toggle("checked");
      if (e.target.parentElement.classList.contains("checked")) {
        e.target.src = "images/checked.png";
      } else {
        e.target.src = "images/unchecked.png";
      }
    } else if (e.target.id == "imgCross") {
      e.target.parentElement.remove();
    }
    saveData();
  },
  false
);

// The event listener is added to the listContainer element. This technique, known as event delegation, allows you to handle events for multiple child elements with a single event listener on a parent element.
// Event delegation is efficient because it reduces the number of event listeners and takes advantage of event bubbling, where events propagate up the DOM tree.
// The event object e contains information about the event, including the target element that was clicked (e.target).

const saveData = () => {
  localStorage.setItem("data", listContainer.innerHTML);
};

// The saveData function saves the current content of listContainer to local storage. Local storage is a web storage API that allows you to store data in the browser, which persists even after the browser is closed.
// localStorage.setItem(key, value): This method stores a key-value pair in local storage.

function showTask() {
  listContainer.innerHTML = localStorage.getItem("data");
}

// The showTask function retrieves the saved list content from local storage and displays it inside the listContainer.
// localStorage.getItem(key): This method retrieves the value associated with the given key from local storage.

showTask();

// This line of code calls the showTask function when the script is first executed. This ensures that any saved list data is loaded and displayed when the page is loaded or refreshed.
