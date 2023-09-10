<template>
  <div class="message-Background">
    <div class="private-messenger">
      <div v-if="selectedUser" class="message-container">
        <h2 style="color: white">Messages with {{ this.friendName }}</h2>
        <div class="message-list" ref="messageList">
          <div v-for="message in selectedUser.messages" :key="message.id">
            <div :class="getMessageContainerClass(message.sender)">
              <div :class="getMessageClass(message.sender)">
                {{ message.content }}
              </div>
              <div style="clear: both"></div>
            </div>
          </div>
        </div>
        <div class="message-input">
          <input
            v-model="newMessage"
            placeholder="Type a message..."
            @keyup.enter="sendMessage" />
          <button @click="sendMessage">Send</button>
        </div>
      </div>
      <div v-else>
        <p>Choose a user to chat with</p>
      </div>
    </div>
    <Friendslist
      :fromMessenger="true"
      @userSelected="onFriendSelected"></Friendslist>
  </div>
</template>

<script>
import axios from "axios";
import Friendslist from "./Friendslist.vue";
import { mapState } from "vuex";
export default {
  name: "PrivateMessenger",
  components: {
    Friendslist,
  },
  props: {
    receiver: null,
  },
  async created() {
    await this.fetchFollowers();
    if (this.receiver) {
      const friend = this.friends.find((f) => f.name === this.receiver);
      this.onFriendSelected(friend);
    }
  },
  mounted() {
    this.messageRefreshInterval = setInterval(() => {
      if (this.friendId) {
        this.onFriendSelected(this.friendId, this.friendName);
      }
    }, 10000);
  },
  data() {
    return {
      API: this.$store.state.API,
      selectedUser: {},
      newMessage: "",
      currentUser: this.$store.state.logged_user,
      currentUserId: this.$store.state.logged_user_id,
      selectedFriend: null,
      friendId: null,
      friendName: null,
      friends: [],
      messageRefreshInterval: null,
    };
  },
  beforeUnmount() {
    // Clear the interval when the component is destroyed
    clearInterval(this.messageRefreshInterval);
  },
  computed: {
    selectedUserMessages() {
      return this.selectedUser ? this.selectedUser.messages : [];
    },
    ...mapState(["friendsList"]),
    getFriends() {
      return this.friendsList;
    },
  },
  methods: {
    async fetchFollowers() {
      try {
        const followee_id = this.$store.state.logged_user_id;
        const response = await axios.get(
          this.API + `/getAllFollowers/${followee_id}`
        );
        this.friends = response.data;
      } catch (error) {
        console.error("Error fetching followers:", error);
      }
    },
    async onFriendSelected(id, friendsname) {
      this.friendName = friendsname;
      this.friendId = id;
      try {
        const response = await axios.get(
          this.$store.state.API + `/get_messages/${this.currentUserId}/${id}`
        );
        this.selectedUser.messages = response.data.map((msg) => ({
          id: msg.id,
          sender: msg.sender_id,
          content: msg.content,
          created_at: msg.created_at,
        }));
        this.sortMessagesByDate();
      } catch (error) {
        console.error("Error fetching messages:", error);
      }
    },
    async sendMessage() {
      if (this.newMessage.trim() === "") {
        return;
      }
      try {
        const response = await axios.post(
          this.$store.state.API + "/send_message/",
          null,
          {
            params: {
              sender_id: this.currentUserId,
              receiver_id: this.friendId,
              content: this.newMessage,
            },
          }
        );
        setTimeout(() => {
          this.onFriendSelected(this.friendId, this.friendName);
        }, 1000);
        console.log(response.data);

        this.newMessage = "";
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      } catch (error) {
        console.error("Error sending message:", error);
      }
    },

    getMessageClass(sender) {
      return {
        message: true,
        "sent-message": sender == this.currentUserId,
        "received-message": sender != this.currentUserId,
      };
    },

    getMessageContainerClass(sender) {
      return {
        message: true,
        "sent-message-container": sender == this.currentUserId,
        "received-message-container": sender != this.currentUserId,
      };
    },

    shouldDisplayUserName(index) {
      if (index === 0) {
        return true;
      } else {
        return (
          this.selectedUser.messages[index].sender !==
          this.selectedUser.messages[index - 1].sender
        );
      }
    },

    isSelectedFriend(friend) {
      return this.selectedFriend === friend;
    },

    getFriendClass(friend) {
      return {
        "friend-item": true,
        "selected-friend": this.isSelectedFriend(friend),
      };
    },

    getUserNameClass(sender) {
      return {
        "user-name-sent": sender == this.currentUser,
        "user-name-received": sender != this.currentUser,
      };
    },

    scrollToBottom() {
      const messageList = this.$refs.messageList;
      messageList.scrollTop = messageList.scrollHeight;
    },

    // To sort the messages by date
    sortMessagesByDate() {
      this.selectedUser.messages.sort(
        (a, b) => new Date(a.created_at) - new Date(b.created_at)
      );
    },
  },
};
</script>

<style scoped>
.message-Background {
  background-color: #3c4e74;
  min-height: 90vh;
}
.private-messenger {
  width: 900px;
  padding: 20px;
  position: absolute;
  top: 15%;
  left: 25%;
  background-color: #142957;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
  font-family: "Trebuchet MS", sans-serif;
}

.message-list {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  max-height: 600px;
  overflow-y: auto;
  background-color: #3c4e74;
}

.message {
  margin-bottom: 3px;
  padding: 10px;
  border-radius: 5px;
  word-break: break-word;
  clear: both;
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
  background-color: #dcf8c6;
  padding: 10px;
  max-width: 70%;
  border-radius: 15px;
  word-wrap: break-word;
}

.received-message {
  display: inline-block;
  background-color: #f3f3f3;
  padding: 10px;
  max-width: 70%;
  border-radius: 15px;
  word-wrap: break-word;
}

.message-input {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.message-input input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.message-input button {
  background-color: #2200cd;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  margin-left: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.message-input button:hover {
  background-color: #1a0099;
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
  background-color: #f3f3f3;
}
</style>
