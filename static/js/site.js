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
  