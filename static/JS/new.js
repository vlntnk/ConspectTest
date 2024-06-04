function arrowRotate() {
  let arrow = document.getElementById('arrow'); // убрали #
  arrow.classList.toggle('rotate');
}
document.addEventListener('DOMContentLoaded', function() { // добавили событие
  let openPanel = document.querySelector('.open-panel'); // добавили точку
  openPanel.addEventListener('click', arrowRotate);
});
// Получаем элементы по их идентификаторам
let sidebar = document.getElementById("sidebar");
let content = document.getElementById("content");
let toggleButton = document.getElementById("toggle-button");

// Флаг, который показывает, открыта ли панель
let sidebarOpen = false;

// Функция, которая открывает или закрывает панель
function toggleSidebar() {
  sidebarOpen = !sidebarOpen;
  if (sidebarOpen) {
    sidebar.classList.add("sidebar-open");
    content.classList.add("content-open");
  } else {
    sidebar.classList.remove("sidebar-open");
    content.classList.remove("content-open");
  }
}

// Добавляем обработчик события клика на кнопку
document.addEventListener("DOMContentLoaded", function() {
  let openPanel = document.querySelector(".open-panel");
  openPanel.addEventListener("click", toggleSidebar);
});

