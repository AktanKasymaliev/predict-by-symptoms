// Получаем элементы страницы
const chatContainer = document.querySelector('.chat-container');
const chatBody = document.querySelector('.chat-body');
const chatInput = document.getElementById('chat-input');
const sendButton = document.getElementById('send-button');

// Создаем WebSocket объект
const socket = new WebSocket('ws://' + window.location.host);

// Отправляем сообщение по WebSocket при нажатии на кнопку отправки
sendButton.addEventListener('click', () => {
  const message = chatInput.value;
  if (message) {
    socket.send(message);
    addMessageToChat('You', message);
    chatInput.value = '';
  }
});

// Добавляем сообщение в чат
function addMessageToChat(sender, message) {
  const messageElem = document.createElement('div');
  messageElem.classList.add('chat-message');
  if (sender === 'Bot') {
    messageElem.classList.add('bot-message');
  }
  messageElem.innerHTML = `<p><strong>${sender}: </strong>${message}</p>`;
  chatBody.appendChild(messageElem);
}

// Обрабатываем сообщения от WebSocket
socket.addEventListener('message', event => {
  const response = JSON.parse(event.data);
  console.log(response);
  addMessageToChat(response['username'], response['message']);
});

// Обрабатываем закрытие соединения WebSocket
socket.addEventListener('close', () => {
  chatContainer.classList.add('disconnected');
});
