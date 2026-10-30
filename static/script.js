const algorithmSelect = document.getElementById("algorithm");
const memoryField = document.getElementById("memory-field");
const blocksField = document.getElementById("blocks-field");
const priorityField = document.getElementById("priority-field");
const memoryInput = document.getElementById("memory");
const blocksInput = document.getElementById("blocks");
const prioritiesInput = document.getElementById("priorities");

function updateFields() {
  const algorithm = algorithmSelect.value;
  const usesTotalMemory = ["equal", "proportional", "priority"].includes(algorithm);
  const usesBlocks = ["first_fit", "best_fit", "worst_fit", "next_fit"].includes(algorithm);

  memoryField.hidden = !usesTotalMemory;
  memoryInput.required = usesTotalMemory;

  blocksField.hidden = !usesBlocks;
  blocksInput.required = usesBlocks;

  priorityField.hidden = algorithm !== "priority";
  prioritiesInput.required = false;
}

algorithmSelect.addEventListener("change", updateFields);
updateFields();


// Dark mode toggle; remembers the user's preference in this browser.
const themeToggle = document.getElementById("theme-toggle");
const savedTheme = localStorage.getItem("memory-simulator-theme");
if (savedTheme === "dark") document.body.classList.add("dark-mode");

function updateThemeButton() {
  const dark = document.body.classList.contains("dark-mode");
  themeToggle.textContent = dark ? "☀️ Light mode" : "🌙 Dark mode";
  themeToggle.setAttribute("aria-pressed", String(dark));
}

updateThemeButton();
themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  const theme = document.body.classList.contains("dark-mode") ? "dark" : "light";
  localStorage.setItem("memory-simulator-theme", theme);
  updateThemeButton();
});
