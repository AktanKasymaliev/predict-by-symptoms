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
    addMessageToChat('You', "stream", message);
    chatInput.value = '';
  }
});

// Добавляем сообщение в чат
function addMessageToChat(sender, type, message) {
  const messageElem = document.createElement('div');
  messageElem.classList.add('chat-message');
  if (sender === "Bot") {
    messageElem.classList.add('bot-message');
    messageElem.innerHTML = `<p>
                                  <strong>Bot: </strong>
                              </p>`;
    if (type === "info" || type === "stream") {
      let messages = message.split(' ');
      let i = 0;
      const intervalId = setInterval(() => {
        if (i < messages.length) {
          messageElem.lastChild.textContent += messages[i] + " ";
          i++;
        } else {
          clearInterval(intervalId);
        }
      }, 100);  
    } 
  } else  {
    messageElem.innerHTML = `<p><strong>${sender}: </strong>${message}</p>`;
  }
  chatBody.appendChild(messageElem);
};

// Обрабатываем сообщения от WebSocket
socket.addEventListener('message', event => {
  const response = JSON.parse(event.data);
  console.log(response);
  addMessageToChat(response['username'],response['type'], response['message']);
});

// Обрабатываем закрытие соединения WebSocket
socket.addEventListener('close', () => {
  chatContainer.classList.add('disconnected');
});