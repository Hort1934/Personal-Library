// Показати повідомлення з анімацією
showErrorWithAnimation("Unsuccessful registration. Invalid information.");

function showErrorWithAnimation(message) {
  var errorMessage = document.createElement('p');
  errorMessage.className = 'animated fadeInUp error-message';
  errorMessage.textContent = message;
  document.body.appendChild(errorMessage);

  // Закрити повідомлення після певного часу
  setTimeout(function() {
    document.body.removeChild(errorMessage);
  }, 5000); // Закрити через 5 секунд
}
// При валідації форми, якщо є помилка, додайте клас "error-input" до поля вводу.
var inputElement = document.getElementById('email-input'); // Змініть id на відповідний
inputElement.classList.add('error-input');
