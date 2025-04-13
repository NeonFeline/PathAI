<script setup>
import { ref } from "vue";

var r = document.querySelector(":root");

const colorError = "#fa5252";

function setMainColor(color) {
  r.style.setProperty("--main-color", color);
}

function getDataFromAPI() {
  return [0.54, 0.24, 0.14, 0.44, 0.14, 0.24, 0.64, 0.54, 0.564];
}

const labelList = [
  "adipose",
  "background",
  "debris",
  "lymphocytes",
  "mucus",
  "smooth muscle",
  "ncm",
  "cas",
  "cae",
];

const labesls = ref({
  adipose: 0.1,
  background: 0.1,
  debris: 0.1,
  lymphocytes: 0.1,
  mucus: 0.1,
  "smooth muscle": 0.1,
  ncm: 0.1,
  cas: 0.1,
  cae: 0.1,
});

const dataBar = ref(getDataFromAPI());

const imageSrc = ref("");
const spinnerActive = ref(false);

const rankText = ref("Test1");

function updateRank(value) {
  let ans;
  let color;

  rankText.value = ans;

  setMainColor(color);
}

async function sendImageToAPI(data) {
  spinnerActive.value = true;
  // Send image
  const json = await fetch("http://127.0.0.1:9400/checkimage/", {
    method: "POST",
    body: JSON.stringify({
      imageData: data,
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  });

  // Get value
  const resp = await json.json();
  if (!resp.value && resp.error) {
    rankText.value = "Unsupported extension";

    setMainColor(colorError);
    return;
  }
  const arr = resp.value[0];

  for (let i = 0; i < arr.length; i++) {
    console.log(i);
    labesls.value[labelList[i]] = arr[i];
  }
  console.log(labesls.value);
  updateRank(resp.value);
  spinnerActive.value = false;
}

const checkImage = (event) => {
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");

  const file = event.target.files[0];
  if (!file) {
    console.error("No file selected.");
    return;
  }

  const reader = new FileReader();
  reader.onload = (loadEvent) => {
    const img = new Image();
    img.onload = () => {
      // Calculate the scaling factor
      const scaleFactor = 512 / Math.min(img.width, img.height);
      const scaledWidth = img.width * scaleFactor;
      const scaledHeight = img.height * scaleFactor;

      // Determine cropping offsets
      const offsetX = (scaledWidth - 512) / 2;
      const offsetY = (scaledHeight - 512) / 2;

      // Draw the image to the canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(
        img,
        -offsetX,
        -offsetY, // Start cropping
        scaledWidth,
        scaledHeight // Draw dimensions
      );
    };

    sendImageToAPI(loadEvent.target.result); // Send Base64 data to the API
    img.src = loadEvent.target.result; // Base64 image data
  };

  reader.readAsDataURL(file);
};
</script>

<template>
  <div class="main_wrapper">
    <div class="main">
      <div class="main__box">
        <div
          :class="{
            main__box__spinner: true,
            'main__box__spinner--active': spinnerActive,
          }"
        >
          <span class="loader"></span>
        </div>
        <canvas
          id="canvas"
          width="512"
          height="512"
          class="main__box__image"
        ></canvas>
      </div>
      <div class="main__interface">
        <div class="main__interface__output">
          <div
            class="main__interface__data_point"
            v-for="(key, label) in labesls"
          >
            <div class="main__interface__label">
              {{ label }}
            </div>
            <div class="main__interface__bar__outer">
              <div
                class="main__interface__bar__inner"
                :style="{ width: `${key * 100}%` }"
              ></div>
            </div>
          </div>
        </div>
        <input
          type="file"
          class="main__interface__input"
          @change="checkImage"
          id="file-input"
        />
        <label for="file-input" class="main__interface__label"
          >Choose Image</label
        >
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.main {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2.4rem;

  &_wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 100%;
  }

  ///////////
  // Main box
  &__box {
    width: 51.2rem;
    height: 51.2rem;
    overflow: hidden;
    position: relative;
    border: solid 2px var(--main-color);

    &__image {
      width: 51.2rem;
    }

    &__spinner {
      display: none;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);

      &--active {
        display: block;
      }
    }
  }
  ///////////

  ////////////
  // Interface
  &__interface {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    margin-top: -9rem;

    &__input {
      display: none;
    }

    &__label {
      width: 22.4rem;
    }

    &__bar {
      &__inner {
        height: 1.2rem;
        background-color: red;
        transition: all 0.2s;
      }

      &__outer {
        width: 100%;
      }
    }
    &__output {
      color: var(--main-color);
      font-size: 3.6rem;
      font-weight: 300;
      margin: 0;
      text-align: center;
      text-transform: uppercase;
    }

    &__label {
      font-size: 1.2rem;
      color: #333;
    }

    &__data_point {
      display: flex;
      align-items: center;
      justify-content: start;
      gap: 1.2rem;
    }
  }

  ////////////
}

.loader {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: inline-block;
  position: relative;
  border: 3px solid;
  border-color: #fff #fff transparent transparent;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}
.loader::after,
.loader::before {
  content: "";
  box-sizing: border-box;
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  margin: auto;
  border: 3px solid;
  border-color: transparent transparent var(--main-color) var(--main-color);
  width: 112px;
  height: 112px;
  border-radius: 50%;
  box-sizing: border-box;
  animation: rotationBack 0.5s linear infinite;
  transform-origin: center center;
}
.loader::before {
  width: 104px;
  height: 104px;
  border-color: #fff #fff transparent transparent;
  animation: rotation 1.5s linear infinite;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
@keyframes rotationBack {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(-360deg);
  }
}
</style>
