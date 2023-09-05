<template>
  <div class="private-messenger">
    <div v-if="selectedUser">
      <h2>Nachrichten mit {{ this.friendName }}</h2>
      <div class="message-list" ref="messageList">
        <div v-for="(message) in selectedUser.messages" :key="message.id">
          <div :class="getMessageContainerClass(message.sender)">
            <!-- <div v-if="shouldDisplayUserName(index)" class="user-name" :class="getUserNameClass(message.sender)">
              {{ message.sender }}
            </div> -->
            <div :class="getMessageClass(message.sender)">
              {{ message.content }}
            </div>
            <div style="clear: both;"></div>
          </div>
        </div>
      </div>
      <div class="message-input">
    <input v-model="newMessage" placeholder="Nachricht eingeben..." />
    <button @click="sendMessage">Send</button>
  </div>
    </div>
    <div v-else>
      <p>Wähle einen Nutzer aus, um Nachrichten anzuzeigen.</p>
    </div>
      <Friendslist :fromMessenger="true" @userSelected="onFriendSelected"></Friendslist>
  </div>
</template>
<script>
import axios from "axios";
import Friendslist from "./Friendslist.vue";
import { mapState } from 'vuex';
export default {
  name: 'PrivateMessenger',
  components: {
    Friendslist
  },
  props: {
    receiver: null,
  },
  async created() {
    await this.fetchFollowers();
    if (this.receiver) {
      const friend = this.friends.find(f => f.name === this.receiver);
      this.onFriendSelected(friend);
    }
  },
  data() {
    return {
      API: this.$store.state.API,
      selectedUser: {},
      newMessage: '',
      currentUser: this.$store.state.logged_user,
      currentUserId: this.$store.state.logged_user_id,
      selectedFriend: null,
      friendId: null,
      friendName: null,
      friends: [],
    };
  },
  computed: {
    selectedUserMessages() {
      return this.selectedUser ? this.selectedUser.messages : [];
    },
    ...mapState(['friendsList']),
    getFriends() {
      return this.friendsList;
    },
  },
  methods: {
    async fetchFollowers() {
      try {
        const followee_id = this.$store.state.logged_user_id 
        const response = await axios.get(this.API + "/getAllFollowers", {
          params: { followee: followee_id }
        });
        this.friends = response.data;
      } catch (error) {
        console.error('Error fetching followers:', error);
      }
    },
    async onFriendSelected(id, friendsname) {
      this.friendName = friendsname
      //this.selectedUser = friend;
      this.friendId = id;
      try {
        const response = await axios.get(this.$store.state.API + `/get_messages/${this.currentUserId}/${id}`);
        this.selectedUser.messages = response.data.map(msg => ({
          id: msg.id,
          sender: msg.sender_id,
          content: msg.content,
          created_at: msg.created_at // We include this field now for sorting
        }));
       this.sortMessagesByDate();
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    },
    async sendMessage() {
      if (this.newMessage.trim() === '') {
        return;
      }
      try {
        const response = await axios.post(this.$store.state.API + '/send_message/', null,  {params: {
          sender_id: this.currentUserId, 
          receiver_id: this.friendId,
          content: this.newMessage,
        }});
        setTimeout(() => {
      this.onFriendSelected(this.friendId);
    }, 1000);
    console.log(response.data)

        this.newMessage = '';
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      } catch (error) {
        console.error('Error sending message:', error);
      }
    },
    
    getMessageClass(sender) {
    return {
      'message': true,
      'sent-message': sender == this.currentUserId,
      'received-message': sender != this.currentUserId,
    };
  },
  
  getMessageContainerClass(sender) {
    return {
      'message': true,
      'sent-message-container': sender == this.currentUserId,
      'received-message-container': sender != this.currentUserId,
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
      'user-name-sent': sender == this.currentUser,
      'user-name-received': sender != this.currentUser,
    };
  },
  
  scrollToBottom() {
    const messageList = this.$refs.messageList;
    messageList.scrollTop = messageList.scrollHeight;
  },
  
  // To sort the messages by date
  sortMessagesByDate() {
    this.selectedUser.messages.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
  },
  },
};
</script>

<style>
/* Style for compoennt*/
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
