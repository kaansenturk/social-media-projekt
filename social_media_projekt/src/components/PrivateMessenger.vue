<template>
    <div class="private-messenger">
      <div v-if="selectedUser">
        <h2>Nachrichten mit {{ selectedUser.name }}</h2>
        <div class="message-list">
          <div v-for="message in selectedUserMessages" :key="message.id" :class="getMessageClass(message)">
            <span>{{ message.sender }}: {{ message.content }}</span>
          </div>
        </div>
        <div class="message-input">
          <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Nachricht eingeben..." />
          <button @click="sendMessage">Senden</button>
        </div>
      </div>
      <div v-else>
        <p>Wähle einen Nutzer aus, um Nachrichten anzuzeigen.</p>
      </div>
      <FriendsList :friends="friends" @friendSelected="onFriendSelected" />
      <div class="friends-container">
        <div v-for="friend in friends" :key="friend.id" :class="getFriendClass(friend)" @click="onFriendSelected(friend)">
          {{ friend.name }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import FriendsList from "./Friendslist.vue";
  
  export default {
    name: 'PrivateMessenger',
    components: {
      FriendsList,
    },
    data() {
      return {
        selectedUser: null,
        newMessage: '',
        currentUser: 'Fr@dt',
        friends: [
          { id: 1, name: "Daniel", messages: [{ id: 1, sender: 'Daniel', content: 'Hallo Fr@dt' }] },
          { id: 2, name: "Johann", messages: [{ id: 2, sender: 'Johann', content: 'Hi Fr@dt' }] },
          { id: 3, name: "Kaan", messages: [{ id: 3, sender: 'Kaan', content: 'Moin Fr@dt' }] },
        ],
        selectedFriend: null,
      };
    },
    computed: {
      selectedUserMessages() {
        return this.selectedUser ? this.selectedUser.messages : [];
      },
    },
    methods: {
      sendMessage() {
        if (this.newMessage.trim() !== '') {
          this.selectedUser.messages.push({
            id: this.selectedUser.messages.length + 1,
            sender: this.currentUser,
            content: this.newMessage,
          });
          this.newMessage = '';
        }
      },
      onFriendSelected(friend) {
        this.selectedUser = friend;
        this.selectedFriend = friend;
      },
      getMessageClass(message) {
      return {
        'message': true,
        'sent-message': message.sender === this.currentUser,
        'received-message': message.sender !== this.currentUser,
      }; // Correctly placed the closing brace
    },
    isSelectedFriend(friend) {
      return this.selectedFriend === friend;
    },
    getFriendClass(friend) {
      return {
        'friend-item': true,
        'selected-friend': this.isSelectedFriend(friend),
      };
    },
  },
};
</script>
  
  <style>
  /* Stil für die Komponente */
  .private-messenger {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .message-list {
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
    max-height: 200px;
    overflow-y: auto;
  }
  
  .message {
    margin-bottom: 5px;
    padding: 5px;
    border-radius: 5px;
  }
  
  .sent-message {
    background-color: #DCF8C6;
    text-align: right;
  }
  
  .received-message {
    background-color: #F3F3F3;
    text-align: left;
  }
  
  .own-message {
    color: blue;
  }

  .selected-friend {
    background-color: #DCF8C6;
    font-weight: bold;
  }
  </style>
  