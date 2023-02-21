// Tailwind Config

tailwind.config = {
  darkMode: "class",
};

// Base Html


// DropDowm
document.getElementById("drop-btn").addEventListener("click", () => {
  toogle();
});
const toogle = () => {
  let dropdown = document.getElementById("drop");
  if (dropdown.classList.contains("scale-0")) {
    dropdown.classList.remove("scale-0");
    dropdown.classList.remove("opacity-0");
  } else {
    dropdown.classList.add("opacity-0");
    dropdown.classList.add("scale-0");
  }
};

// Menu Dropdown

let dropdownBg = document.getElementById("bg-menu");
let dropdown = document.getElementById("menu");
document.getElementById("menu-btn").addEventListener("click", (e) => {
  menu();
  e.stopPropagation();
});
dropdownBg.addEventListener("click", () => {
  menu();
});
dropdown.addEventListener("click", (e) => {
  e.stopPropagation();
});

const menu = () => {
  if (dropdown.classList.contains("-ml-80")) {
    dropdownBg.classList.remove("hidden");
    setTimeout(() => {
      dropdown.classList.remove("-ml-80");
    }, 50);
  } else {
    dropdown.classList.add("-ml-80");
    setTimeout(() => {
      dropdownBg.classList.add("hidden");
    }, 300);
  }
};

//Theme
let darkButton = document.getElementById("dark-button");
let darkIcon = document.getElementById("dark-icon");

if (localStorage.getItem("dark") == "true") {
  document.getElementsByTagName("html")[0].classList.add("dark");
} else {
  document.getElementsByTagName("html")[0].classList.remove("dark");
}

const toggleTheme = () => {
  document.getElementsByTagName("html")[0].classList.toggle("dark");
  if (localStorage.getItem("dark") === "true") {
    localStorage.setItem("dark", "false");
  } else {
    localStorage.setItem("dark", "true");
  }
  if (darkIcon.classList.contains("fa-sun")) {
    darkIcon.classList.remove("fa-sun");
    darkIcon.classList.add("fa-moon");
  } else {
    darkIcon.classList.remove("fa-moon");
    darkIcon.classList.add("fa-sun");
  }
};
darkButton.addEventListener("click", () => {
  toggleTheme();
});

// For Comment
const toggle = (id) => {
  document.getElementById(id).classList.toggle("hidden");
  document.querySelector("#" + id + " textarea").focus();
};

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function deleteComment(id) {
  let csrftoken = getCookie("csrftoken");

  fetch("/blog/delete-comment/", {
    method: "post",
    body: JSON.stringify({
      id: id,
    }),
    headers: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  })
    .then((res) => {
      return res.json();
    })
    .then((i) => {
      document.getElementById(id).remove();
    });
}
