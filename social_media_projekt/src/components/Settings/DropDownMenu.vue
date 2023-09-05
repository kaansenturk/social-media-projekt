<template>
    <div class="dropdown-container">
      <button @click="toggleDropdown" class="dropdown-button">☰</button>
      <div v-if="isDropdownOpen" class="overlay">
        <button @click="toggleDropdown" class="dropdown-button2">☰</button>
        <img class="app_icon" alt="App Logo" src="@/assets/hacker.png">
        <button @click="goToHome" class="menu-item">Home</button>
        <button @click="goToAccount" class="menu-item">Account Info</button>
        <button @click="goToMessenger" class="menu-item">Messenger</button>
        <!--<button @click="goToGeneralSettings" class="menu-item">Settings</button>-->
        <!--<button @click="goToNews" class="menu-item">Benachrichtigungen</button>-->
        <!--<button @click="goToPrivacy" class="menu-item">Datenschutz</button>-->
        <!--<button @click="goToProfile" class="menu-item">Konto</button>-->
        <!--<button @click="goToLanguage" class="menu-item">Sprache und Region</button>-->
        <!--<button @click="goToThemes" class="menu-item">Themes und Erscheinungsbild</button>-->
        <!--<button @click="goToSafety" class="menu-item">Sicherheit</button>-->
        <!--<button @click="goToSupport" class="menu-item">Hilfe und Support</button>-->
        <button type="submit" @click="logout" class="menu-item">Logout</button>
        <!--<button @click="goToPolicy" class="menu-item">Nutzungsbedingungen und Datenschutzrichtlinien</button>-->
      </div>
      <div v-if="isDropdownOpen" class="background" @click="closeDropdown"></div>
    </div>
</template>

<script>
export default {
  components: {
  },
  data() {
    return {
      isDropdownOpen: false
    };
  },
  methods: {
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    goToAccount() {
      this.closeDropdown();
      this.$router.push('/account');
    },
    goToHome() {
      this.closeDropdown();
      this.$router.push('/');
    },
    goToMessenger() {
      this.closeDropdown();
      this.$router.push('/messenger');
    },
    goToGeneralSettings() {
      this.closeDropdown();
      this.$router.push('/general-settings');
    },
    goToNews() {
      this.closeDropdown();
      this.$router.push('/news');
    },
    goToPrivacy() {
      this.closeDropdown();
      this.$router.push('/privacy');
    },
    goToProfile() {
      this.closeDropdown();
      this.$router.push('/profile');
    },
    goToLanguage() {
      this.closeDropdown();
      this.$router.push('/language');
    },
    goToThemes() {
      this.closeDropdown();
      this.$router.push('/themes');
    },
    goToSafety() {
      this.closeDropdown();
      this.$router.push('/safety');
    },
    goToSupport() {
      this.closeDropdown();
      this.$router.push('/support');
    },
    logout() {
      localStorage.removeItem('logegd_user_id');
      localStorage.removeItem('logged_user');
      this.$store.commit('setUser', null)
      this.$store.commit('setUserId', null)
      this.$router.push('/login')
},
    goToPolicy() {
      this.closeDropdown();
      this.$router.push('/policy');
    },
    closeDropdown() {
      this.isDropdownOpen = false;
    },
  },
};
</script>

<style>

.dropdown-container {
  position: absolute;
  display: inline-block;
  top: 20px; 
  left: 10px; 
}

.dropdown-button {
  background-color: transparent;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color:purple;
}

.dropdown-button2 {
  background-color: transparent;
  border: none;
  font-size: 24px;
  cursor: pointer;
  position: absolute;
  display: inline-block;
  top: 19px; 
  left: 9px; 
  color:purple;
}


.app_icon{
  width: 100px;
}

.menu-item {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  padding: 15px 15px;
  width: 100%;
  text-align: left;
  color:purple;
}

.menu-item:hover {
  background-color: #ECF0F1;
}
.background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999; 
  animation: fadeIn 1s;
}

.overlay {
  position: absolute;
  top: -20px;
  left: -10px;
  background-color:#F8F9F9;
  border: 1px solid #ccc;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 40px;
  font-size: 18px;
  z-index: 1000;
}

/* Animationen */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideInLeft {
  from {
    transform: translateX(-20%);
  }
  to {
    transform: translateX(0%);
  }
}

.overlay {
  animation: slideInLeft 0.5s;
}

</style>