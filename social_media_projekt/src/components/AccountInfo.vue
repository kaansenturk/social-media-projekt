<template>
    <div class="account-info">
      <h2 class="title">Account Information</h2>
      <div class="info-item">
        <strong>Username:</strong> {{ username }}
      </div>
      <div class="info-item">
        <strong>Email:</strong> {{ email }}
      </div>
      <div class="info-item">
        <strong>Role:</strong> {{ role }}
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AccountInfo',
    data() {
      return {
        username: 'Fr@dt',
        email: 'fredmetzler@battlenet.com',
        role: 'CEO',
      };
    },
  };
  </script>
  
  <style scoped>
  .account-info {
    background-color: #2200cd;
    color: white;
    padding: 20px;
  }
  
  .title {
    font-size: 24px;
    margin-bottom: 10px;
  }
  
  .info-item {
    margin-bottom: 5px;
  }
  </style>
  