<template>
    <div class="impressum-container">
      <h1>Impressum</h1>
      <hr />
  
      <h2>Hochschule Flensburg</h2>
      <h3>Flensburg University of Applied Sciences</h3>
  
      <p>Kanzleistraße 91-93</p>
      <p>24943 Flensburg</p>
      <p>Germany</p>
      <br />
  
      <p><strong>Telefon:</strong> +49 (0)461 805 01</p>
      <p><strong>Telefax:</strong> +49 (0)461 805 1300</p>
      <p><strong>Email:</strong> <a href="mailto:infopoint@hs-flensburg.de">infopoint@hs-flensburg.de</a></p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ImpressumPage',
  };
  </script>
  
  <style scoped>
  .impressum-container {
    max-width: 600px;
    margin: 40px auto;
    padding: 20px;
    border: 1px solid #e1e1e1;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0,0,0,0.05);
  }
  
  h1 {
    font-size: 2em;
    margin-bottom: 20px;
  }
  
  h2 {
    font-size: 1.5em;
    margin-top: 20px;
  }
  
  h3 {
    font-size: 1.2em;
    margin-bottom: 20px;
    font-weight: 400;
    color: #555;
  }
  
  p {
    font-size: 1em;
    margin-bottom: 10px;
    line-height: 1.6;
  }
  
  a {
    color: #0077cc;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  </style>
  