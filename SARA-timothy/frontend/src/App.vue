<template>
  <div style="display: flex; flex-direction: column; width: 100vw; height: 100vh">
    <div style="flex: 1; display: flex; flex-direction: row">
      <!-- Smiley content -->
      <div class="content">

        <div class="smiley">
          <div class="eyes">
            <!--        left eye + eyebrow-->
            <div v-if="!isBlinked" :class="isThinking ? 'left-eye-thinking' : 'left-eye'">
              <div :class="
            isTalking ? 'eyebrow-talking eyebrow-L-talking' :
            isThinking ? 'eyebrow-thinking eyebrow-L-thinking' : 'eyebrow eyebrow-L'"></div>
            </div>
            <div v-else :class="isThinking ? 'left-blink-thinking' : 'left-blink'">
              <div :class="
            isTalking ? 'eyebrow-talking eyebrow-L-talking' :
            isThinking ? 'eyebrow-thinking eyebrow-L-thinking' : 'eyebrow eyebrow-L'"></div>
            </div>
            <!--        right eye + eyebrow-->
            <div v-if="!isBlinked" :class="isThinking ? 'right-eye-thinking' : 'right-eye'">
              <div :class="
            isTalking ? 'eyebrow-talking eyebrow-R-talking' :
            isThinking ? 'eyebrow-thinking eyebrow-R-thinking' : 'eyebrow eyebrow-R'"></div>
            </div>
            <div v-else :class="isThinking ? 'right-blink-thinking' : 'right-blink'">
              <div :class="
            isTalking ? 'eyebrow-talking eyebrow-R-talking' :
            isThinking ? 'eyebrow-thinking eyebrow-R-thinking' : 'eyebrow eyebrow-R'"></div>
            </div>
          </div>
          <div :class="isTalking ? 'lips-talking' : isThinking ? 'lips-thinking' : 'lips'"></div>
        </div>

        <div class="icon">
          <!-- Thinking icon -->
          <div v-if="isThinking" class="thinking">
            <span></span>
            <span></span>
            <span></span>
          </div>

          <!-- Listening icon -->
          <div v-if="isListening" class="listening">
            <span class="line"></span>
            <span class="line"></span>
            <span class="line"></span>
            <span class="line"></span>
            <span class="line"></span>
          </div>

          <!-- Speaking icon -->
          <div v-if="isTalking">
            <div class="talking">
              <img class="speaker" src="/speaker.svg"/>
              <img class="speaker-1" src="/wave-s.svg"/>
              <img class="speaker-2" src="/wave-b.svg"/>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Text while speaking -->
    <div class="text-bg-speak" v-if="isTalking">
      <div class="text"><p class="animated-text-speak">{{ animatedText }}</p></div>
    </div>

    <!-- Text while listening -->
    <!--    <div class="text-bg" v-if="text && !isThinking && !isListening">-->
    <!--      <div class="text"><p class="animated-text">{{ animatedText }}</p></div>-->
    <!--    </div>-->
  </div>
</template>

<script>
import axios from 'axios';
import io from 'socket.io-client';

// Replace 'http://localhost:5000' with the actual URL of your Flask server
const socket = io('http://127.0.0.1:5000/get_interface_state');

export default {
  name: 'App',
  data() {
    return {
      isBlinked: false,
      isTalking: false,
      isThinking: false,
      isListening: false,
      lastPressedKey: null,
      textFullyTyped: false,
      text: '',
      state: '',
      animatedText: "",
      currentWordIndex: 0,
      currentCharIndex: 0,
    };
  },
  methods: {
    randomBlink() {
      this.isBlinked = true;
      setTimeout(() => {
        this.isBlinked = false;
      }, 100);
    },
    scheduleRandomBlink() {
      const randomTime = Math.random() * 5000; // Random time between 0 and 5 seconds
      setTimeout(() => {
        this.randomBlink();
        this.scheduleRandomBlink();
      }, randomTime);
    },
    getInterfaceState() {
      axios.get('http://127.0.0.1:5000/get_interface_state', {timeout: 5000})
          .then(response => {
            // Successful response, handle the data
            if (this.text !== response.data.text || this.state !== response.data.state) {
              this.handleReceivedState(response.data.state, response.data.text);
            }
          })
          .catch(error => {
            // Log the error for debugging
            console.error('Error fetching interface state:', error);

            // Check for a network error
            if (error.isAxiosError && error.code === 'ERR_NETWORK') {
              console.error('Network error - check your connection or server availability.');
            } else if (error.response) {
              // The request was made and the server responded with a status code
              console.error('Server responded with:', error.response.status, error.response.data);
            } else {
              // Something happened in setting up the request
              console.error('Error message:', error.message);
            }
          });
    },
    handleReceivedState(state, text) {
      this.text = text;
      this.state = state;
      if (this.state === 'talk') {
        this.animatedText = "";
        this.textFullyTyped = false;
        this.currentWordIndex = 0;
        this.currentCharIndex = 0;
        this.typeText();
        this.isTalking = true;
        this.isThinking = false;
        this.isListening = false;
        document.body.classList.add('is-talking');
        document.body.classList.remove('is-thinking', 'is-listening');
        document.documentElement.classList.add('is-talking');
        document.documentElement.classList.remove('is-thinking', 'is-listening');
      } else if (this.state === 'think') {
        this.isTalking = false;
        this.isThinking = true;
        this.isListening = false;
        document.body.classList.add('is-thinking');
        document.body.classList.remove('is-talking', 'is-listening');
        document.documentElement.classList.add('is-thinking');
        document.documentElement.classList.remove('is-talking', 'is-listening');
      } else if (this.state === 'listen') {
        this.animatedText = "";
        this.currentWordIndex = 0;
        this.currentCharIndex = 0;
        this.textFullyTyped = false;
        // this.typeTextSpeak();
        this.isTalking = false;
        this.isThinking = false;
        this.isListening = true;
        document.body.classList.add('is-listening');
        document.body.classList.remove('is-talking', 'is-thinking');
        document.documentElement.classList.add('is-listening');
        document.documentElement.classList.remove('is-talking', 'is-thinking');
      }
    },
    // Function to simulate typing text
    typeText() {
      console.log('Entering typeText');
      const currentWord = this.text.split(" ");
      const currentChar = currentWord[this.currentWordIndex][this.currentCharIndex];

      if (currentChar) {
        this.animatedText += currentChar;
        this.currentCharIndex += 1;
      } else {
        // Move to the next word
        this.animatedText += " ";
        this.currentWordIndex += 1;

        if (this.currentWordIndex >= currentWord.length) {
          this.textFullyTyped = true;
          this.currentWordIndex = 0;
        }
        this.currentCharIndex = 0;
      }

      if (!this.textFullyTyped) {
        setTimeout(this.typeText, 70); // Adjust typing speed
      }
    },
  },
  mounted() {
    this.scheduleRandomBlink();

    // Listen for the 'interface_updated' event from the Flask backend
    socket.on('interface_updated', data => {
      this.text = data.text;
      // Handle other data properties as needed
    });

    // Fetch the initial interface state when the component is mounted
    this.getInterfaceState();

    // Optionally, you can set up a periodic fetch (e.g., every 5 seconds)
    this.intervalId = setInterval(() => this.getInterfaceState(), 1000);
  },

  beforeUnmount() {
    // Clear the interval when the component is destroyed
    clearInterval(this.intervalId);
  }
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #B4F3FF;
  transition: background-color 0.5s ease-in-out;
}

body.is-thinking, html.is-thinking {
  background-color: #FBFFAA;
}

body.is-listening, html.is-listening {
  background-color: #8AFFA1;
}

.thinking {
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  width: 54.4px; /* 0.8 times smaller */
  top: -16%; /* Adjusted for the new size */
}

.thinking span {
  width: 9.6px; /* 0.8 times smaller */
  height: 9.6px; /* 0.8 times smaller */
  margin: 0 4px; /* Adjusted for the new size */
  background-color: #00214A;
  border-radius: 50%;
  display: inline-block;
  opacity: 0.9;
  animation: dots 1.2s infinite ease-in-out; /* Adjusted the animation duration */
}

.thinking span:nth-child(2) {
  animation-delay: 0.25s;
}

.thinking span:nth-child(3) {
  animation-delay: 0.5s;
}

@keyframes dots {
  0%, 100% {
    opacity: 0;
    transform: scale(0.7) translateY(10px);
  }
  50% {
    opacity: 0.9;
    transform: scale(1) translateY(0);
  }
}

.listening {
  width: 56px; /* 0.7 times smaller */
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  position: relative;
  left: 50%;
  top: -20%;
  transform: translateX(-50%);
}

.line {
  width: 5px; /* 0.7 times smaller */
  height: 14px; /* 0.7 times smaller */
  background-color: #00214A;
  border-radius: 4px;
  opacity: 0.9;
}

.line:nth-child(1) {
  animation: speaking 0.7s 600ms infinite;
}

.line:nth-child(2) {
  animation: speaking 0.7s 300ms infinite;
}

.line:nth-child(3) {
  animation: speaking 0.7s infinite;
}

.line:nth-child(4) {
  animation: speaking 0.7s 300ms infinite;
}

.line:nth-child(5) {
  animation: speaking 0.7s 600ms infinite;
}

@keyframes speaking {
  0% {
    height: 14px; /* 0.7 times smaller */
  }
  50% {
    height: 43.4px; /* 0.7 times larger */
  }
  100% {
    height: 14px; /* 0.7 times smaller */
  }
}

@keyframes pulse-animation {
  0% {
    transform: scale(0.8);
    opacity: 0.6;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.3;
  }
  100% {
    transform: scale(0.8);
    opacity: 0.6;
  }
}

.talking {
  width: 41.76px; /* 0.9 times smaller */
  display: flex;
  flex-direction: row;
  position: relative;
  left: 50%;
  top: -20%;
  transform: translateX(-50%);
}

.speaker {
  width: 20.16px; /* 0.9 times smaller */
  position: relative;
  opacity: 0.9;
}

.speaker-1 {
  width: 10.08px; /* 0.9 times smaller */
  left: 5.76px; /* 0.9 times smaller */
  position: relative;
  animation: talking 1s infinite ease-in-out;
}

.speaker-2 {
  width: 14.4px; /* 0.9 times smaller */
  position: relative;
  animation: talking 1s infinite ease-in-out;
  animation-delay: 0.2s;
}


@keyframes talking {
  0% {
    opacity: 0;
    scale: 1;
  }
  100% {
    opacity: 0.9;
    scale: 1.1;
  }
}

.content {
  position: relative;
  top: 50%;
  left: 50%;
  width: 300px;
  height: 100%;
  transform: translate(-50%, -50%);
}

.icon {
  position: absolute;
  top: 77%;
  left: 50%;
  transform: translate(-50%);
}

.smiley {
  position: relative;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 300px;
  transition: transform 0.3s ease-in-out;
}

.left-eye,
.right-eye {
  position: absolute;
  top: 30%;
  background-color: #00214A;
  border-radius: 50%;
  width: 25px;
  height: 25px;
  transition: transform 0.3s ease-in-out;
}

.left-eye-thinking,
.right-eye-thinking {
  position: absolute;
  top: 30%;
  background-color: #00214A;
  border-radius: 50%;
  width: 25px;
  height: 25px;
  transition: transform 0.3s ease-in-out;
}

.left-eye, .left-blink {
  left: 25%;
}

.right-eye, .right-blink {
  right: 25%;
}

.left-eye-thinking, .left-blink-thinking {
  left: 25%;
}

.right-eye-thinking, .right-blink-thinking {
  right: 25%;
}

@keyframes blink {
  0%, 100% {
    transform: scaleY(1); /* Fully closed */
  }
  50% {
    transform: scaleY(0.1); /* Half open */
  }
}

.left-blink, .right-blink {
  position: absolute;
  top: 30%;
  background-color: #00214A;
  border-radius: 50%;
  width: 25px;
  height: 25px;
  transition: width 0.3s ease-in-out, height 0.3s ease-in-out;
  transform-origin: center bottom;
  animation: blink 0.8s alternate;
}

.left-blink-thinking, .right-blink-thinking {
  position: absolute;
  top: 30%;
  background-color: #00214A;
  border-radius: 50%;
  width: 25px;
  height: 25px;
  transition: width 0.3s ease-in-out, height 0.3s ease-in-out;
  transform-origin: center bottom;
  animation: blink 0.8s alternate;
}

.lips {
  position: absolute;
  height: 100px;
  width: 235px;
  border: 6px solid transparent;
  border-bottom: 10px solid #00214A;
  border-radius: 50%;
  top: 25%;
  left: 50%;
  transform: translateX(-50%);
  transition: all 0.3s ease-out;
  transition-property: width;
}

.lips-talking {
  position: absolute;
  height: 100px;
  width: 235px;
  border: 6px solid transparent;
  border-bottom: 10px solid #00214A;
  top: 25%;
  left: 50%;
  transform: translateX(-50%);
  transition: all 0.3s ease-in-out;
  animation: talk 0.5s infinite alternate ease-in-out;
  transition-property: width;
  border-radius: 40%;
}

.lips-thinking {
  position: absolute;
  top: 55%;
  left: 50%;
  transform: translateX(-50%);
  transition: all 0.5s ease-out;
  transition-property: width;
  height: 15px;
  width: 80px;
  background-color: #00214A;
  border-radius: 100%;
  border-bottom-right-radius: 20%;
  border-bottom-left-radius: 20%;
}

.eyebrow {
  position: absolute;
  width: 40px;
  height: 8px;
  background-color: #00214A;
  top: -45%;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 5px;
  transition: top 0.3s ease-in-out;
}

.eyebrow-talking {
  position: absolute;
  width: 40px;
  height: 8px;
  background-color: #00214A;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 5px;
  transition: top 0.3s ease-in-out;
  top: -94%;
}

.eyebrow-thinking {
  position: absolute;
  width: 40px;
  height: 8px;
  background-color: #00214A;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 5px;
  transition: top 0.3s ease-in-out;
  top: -42%;
}

.eyebrow-L {
  rotate: 351deg;
  top: -60%;
}

.eyebrow-R {
  rotate: 8deg;
}

.eyebrow-L-talking {
  rotate: 350deg;
  top: -60%;
}

.eyebrow-R-talking {
  rotate: 10deg;
}


.eyebrow-L-thinking {
  rotate: 355deg;
}

.eyebrow-R-thinking {
  rotate: 6deg;
  top: -26%;
}

@keyframes talk {
  0% {
    transform: translateX(-50%) scaleY(1);
  }
  100% {
    transform: translateX(-50%) scaleY(1.2);
  }
}

.text-bg {
  height: 100vh;
  width: 100%;
  flex: 0.8;
  background-color: black;
  opacity: 0.4;
  justify-content: center;
  animation: slideInFromRight 1s ease forwards;
}

.text-bg-speak {
  height: 100vh;
  width: 100%;
  flex: 0.85;
  background-color: black;
  opacity: 0.4;
  justify-content: center;
  animation: slideInFromBottom 1s ease forwards;
}

.animated-text {
  display: inline-block;
  overflow: auto;
  height: 90%;
  width: 90%;
  margin: 0;
}

.animated-text-speak {
  display: inline-block;
  overflow-y: auto;
  margin: 0;
  height: 90%;
  width: 90%;
}

.text {
  font-size: 32px;
  font-family: monospace;
  color: white;
  height: 100%;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

@keyframes slideInFromBottom {
  0% {
    transform: translateY(200%); /* Start position off-screen to the left */
  }
  100% {
    transform: translateY(0); /* End position (visible on the screen) */
  }
}


@keyframes slideInFromRight {
  0% {
    transform: translateX(100%); /* Start position off-screen to the right */
  }
  100% {
    transform: translateX(0); /* End position (visible on the screen) */
  }
}
</style>

