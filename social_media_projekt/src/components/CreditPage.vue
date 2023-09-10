<template>
<div class="animated-background"></div>
  <div class="credits-container">
    <span class="contributors">Kaan Johann Frederik</span><br />
    <span>Our Techstack, thanks for the nice documentation:</span><br />
    <transition name="fade" mode="out-in">
      <a :href="currentLogo.link" target="_blank" :key="currentLogo.title">
        <img
          class="image"
          :src="currentLogo.src"
          :title="currentLogo.title"
          :alt="currentLogo.alt" />
      </a>
    </transition>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";
export default {
  name: "CreditPage",
  setup() {
    const logos = [
      {
        src: require("../assets/logo.png"),
        title: "Vue3",
        alt: "Vue 3 Logo",
        link: "https://vuejs.org/guide/introduction.html",
      },
      {
        src: require("../assets/vue-leaflet-logo.png"),
        title: "Vue-leaflet",
        alt: "Vue3-Leaflet Logo",
        link: "https://github.com/vue-leaflet/vue-leaflet",
      },
      {
        src: require("../assets/Python-logo.png"),
        title: "Python",
        alt: "Python Logo",
        link: "https://www.python.org/doc/",
      },
      {
        src: require("../assets/amazon_ec2.webp"),
        title: "AWS EC2",
        alt: "AWS Logo",
        link: "https://docs.aws.amazon.com/ec2/",
      },
      {
        src: require("../assets/axios_logo.png"),
        title: "Axios",
        alt: "Axios Logo",
        link: "https://axios-http.com/docs/intro",
      },
      {
        src: require("../assets/fastapi-logo.png"),
        title: "FastAPI",
        alt: "FastAPI Logo",
        link: "https://fastapi.tiangolo.com/",
      },
      {
        src: require("../assets/SQLite_logo.png"),
        title: "SQLite",
        alt: "SQLite Logo",
        link: "https://www.sqlite.org/docs.html",
      },
      {
        src: require("../assets/GitHub-logo.png"),
        title: "Github",
        alt: "Github Logo",
        link: "https://docs.github.com/de",
      },
    ];

    const currentLogoIndex = ref(0);

    const currentLogo = ref(logos[currentLogoIndex.value]);

    let interval;
    onMounted(() => {
      interval = setInterval(() => {
        currentLogoIndex.value = (currentLogoIndex.value + 1) % logos.length;
        currentLogo.value = logos[currentLogoIndex.value];
      }, 4000);
    });

    onUnmounted(() => {
      clearInterval(interval);
    });

    return {
      currentLogo,
    };
  },
};
</script>

<style scoped>
.image {
  margin-top: 30px;
  max-width: 250px;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.contributors {
  font-family: "Trebuchet MS", "Lucida Sans Unicode", "Lucida Grande",
    "Lucida Sans", Arial, sans-serif;
  font-size: xx-large;
  font-weight: bold;
  margin-bottom: 20px;
}

.credits-container {
  width: 50%;
  height: 400px;
  margin: 70px auto;
  overflow: auto;
  border: 1px solid #ccc;
  position: relative;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

</style>
