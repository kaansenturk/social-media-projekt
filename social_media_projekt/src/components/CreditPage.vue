<template>
<div class="animated-background"></div>
    <div class="credits-container">
      
        <span class="contributors">Kaan   Johann   Frederik</span><br>
        <span>Our Techstack, thanks for the nice documentation:</span>
        <div class="credits-content" ref="creditsRef">
        <a href="https://vuejs.org/guide/introduction.html" target="_blank">
        <img src="../assets/logo.png" alt="Vue 3 Logo"></a>
        <a href="https://github.com/vue-leaflet/vue-leaflet" target="_blank">
        <img src="../assets/vue-leaflet-logo.png" alt="Vue3-Leaflet Logo"></a>
        <a href="https://www.python.org/doc/" target="_blank">
        <img src="../assets/Python-logo.png" alt="Python Logo"></a>
        <a href="https://docs.aws.amazon.com/ec2/" target="_blank">
        <img src="../assets/amazon_ec2.webp" alt="AWS Logo"></a>
        <a href="https://axios-http.com/docs/intro" target="_blank">
        <img src="../assets/axios_logo.png" alt="Axios Logo"></a>
        <a href="https://fastapi.tiangolo.com/" target="_blank">
        <img src="../assets/fastapi-logo.png" alt="FastAPI Logo"></a>
        <a href="https://www.sqlite.org/docs.html" target="_blank">
        <img src="../assets/SQLite_logo.png" alt="SQLite Logo"></a> 
        <a href="https://docs.github.com/de" target="_blank">
        <img src="../assets/GitHub-logo.png" alt="SQLite Logo"></a>
      </div>
    </div>
  </template>
  
  <script>
import { ref, onMounted, onUnmounted } from 'vue';

export default {
  name: 'CreditPage',
  setup() {
    const creditsRef = ref(null);
    let scrollInterval;

    const handleScrolling = () => {
      if (!creditsRef.value) return;

      const element = creditsRef.value;
      if (element.scrollTop >= (element.scrollHeight - element.offsetHeight)) {
        element.scrollTop = 0;
      } else {
        element.scrollTop += 1;
      }
    };

    onMounted(() => {
      scrollInterval = setInterval(handleScrolling, 30);
    });

    onUnmounted(() => {
      clearInterval(scrollInterval);
    });

    return { creditsRef };
  }
};
</script>

  
  
<style scoped>
.contributors {
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
  font-size: xx-large;
  font-weight: bold;
  margin-bottom: 20px;
}

.credits-container {
  width: 50%;
  height: 600px;
  margin: 70px auto;
  overflow: auto;
  border: 1px solid #ccc;
  position: relative;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.credits-content {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  bottom: 0;
}

.credits-content img {
  margin: 20px 0;
  max-width: 100px; 
}

.credits-content span {
  margin-bottom: 20px; 
}
</style>
