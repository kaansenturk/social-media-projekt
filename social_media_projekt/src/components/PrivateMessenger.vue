<template>
  <div class="private-messenger">
    <div v-if="selectedUser">
      <h2>Nachrichten mit {{ selectedUser.name }}</h2>
      <div class="message-list" ref="messageList">
        <div v-for="(message, index) in selectedUser.messages" :key="message.id">
          <div :class="getMessageContainerClass(message.sender)">
            <div v-if="shouldDisplayUserName(index)" class="user-name" :class="getUserNameClass(message.sender)">
              {{ message.sender }}
            </div>
            <div :class="getMessageClass(message.sender)">
              {{ message.content }}
            </div>
            <div style="clear: both;"></div>
          </div>
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

        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },
    onFriendSelected(friend) {
      this.selectedUser = friend;
      this.selectedFriend = friend;
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    },
    getMessageClass(sender) {
      return {
        'message': true,
        'sent-message': sender === this.currentUser,
        'received-message': sender !== this.currentUser,
      };
    },
    getMessageContainerClass(sender) {
      return {
        'message': true,
        'sent-message-container': sender === this.currentUser,
        'received-message-container': sender !== this.currentUser,
      };
    },
    shouldDisplayUserName(index) {
      if (index === 0) {
        return true;
      } else {
        return this.selectedUser.messages[index].sender !== this.selectedUser.messages[index - 1].sender;
      }
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
    getUserNameClass(sender) {
      return {
        'user-name-sent': sender === this.currentUser,
        'user-name-received': sender !== this.currentUser,
      };
    },
    scrollToBottom() {
      const messageList = this.$refs.messageList;
      messageList.scrollTop = messageList.scrollHeight;
    },
  },
};
</script>

<style>
/* Stil für die Komponente */
.private-messenger {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.message-list {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  max-height: 300px;
  overflow-y: auto;
}

.message {
  margin-bottom: 3px;
  padding: 3px;
  border-radius: 3px;
  word-break: break-word;
}

.sent-message-container {
  text-align: right;
  margin-right: 20px;
}

.received-message-container {
  text-align: left;
  margin-left: 20px;
}

.sent-message {
  display: inline-block;
  background-color: #DCF8C6;
  max-width: 300px;
}

.received-message {
  display: inline-block;
  background-color: #F3F3F3;
  max-width: 300px;
}

.user-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.user-name-sent {
  text-align: right;
}

.user-name-received {
  text-align: left;
}

.selected-friend {
  font-weight: bold;
  background-color: #F3F3F3;
}

</style>
