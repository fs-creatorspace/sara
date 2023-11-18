let typewriter_timeout = null

function typeWriterEffect(text, speed = 50) {
  if (typewriter_timeout != null){
    clearTimeout(typewriter_timeout);
  }
    const container = document.getElementById('container-right');
    let i = 0;
    container.innerHTML = "";
    function type() {
        if (i < text.length) {
            container.innerHTML += text.charAt(i);
            i++;
            typewriter_timeout = setTimeout(type, speed);
        }
    }
    type();
}

function changeEmotion(emotion){
    const animation = document.getElementById("animation");
    const emotion_paths = {
        listen: "listen.gif",
        think: "think.gif",
        speak: "speak.gif"
    }
    console.log("Changing emotion to: ", emotion);
    console.log("static/img/" + emotion_paths[emotion])
    animation.src = "static/img/" + emotion_paths[emotion];
}

var socket = io();
  socket.on('connect', function() {
    console.log("Socket connected!");
    socket.emit('message', "Hello from the client!");
  });

  socket.on('text', (data) => {
    console.log("Server says (text):", data);
    typeWriterEffect(data);
  });

  socket.on("emotion", (data) => {
    console.log("Server says (emotion): ", data);
    changeEmotion(data)
    socket.emit(data)
  });

  socket.on("play", (data) => {
    var audio = new Audio(data);
    audio.play();
  })