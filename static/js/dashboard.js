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
