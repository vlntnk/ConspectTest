document.addEventListener('DOMContentLoaded', (event) => {
  let noSub = document.querySelector('.noSub');
  let subjectCards = document.querySelectorAll('.subject-card');

  if (subjectCards.length > 0) {
    noSub.style.display = 'none';
  }

  colorGenerate(subjectCards);
});

function colorGenerate(cards) {
  cards.forEach((card) => {
    let red = Math.floor(Math.random() * 256);
    let blue = Math.floor(Math.random() * 256);
    card.style.backgroundColor = `rgb(${red}, 0, ${blue})`;
  });
}

function openModal() {
  let modal = document.querySelector('.modal');
  modal.classList.add('active');

  // Добавляем обработчик события click на модальное окно
  modal.addEventListener('click', closeModal);
}

function closeModal(event) {
  // Проверяем, является ли целевой элемент клика модальным окном
  if (event.target.classList.contains('modal')) {
    let modal = document.querySelector('.modal');
    modal.classList.remove('active');

    // Удаляем обработчик события click с модального окна
    modal.removeEventListener('click', closeModal);
  }
}

let openModalButton = document.getElementById('add');
openModalButton.addEventListener('click', openModal);
function closeButtonModel() {
  let modal = document.querySelector('.modal');
  modal.classList.remove('active');
}
let closeButtons = document.querySelector('.close');
closeButtons.addEventListener('click', closeButtonModel);

