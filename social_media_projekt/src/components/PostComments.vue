<template>
  <div class="row">
    <div class="col-md-2 account-info">
      <div class="title">
        <img v-if="this.profileImageUrl == null" src="../assets/blank_profile_pic.webp" alt="Kein Profilbild" class="profile-picture" />
        <img v-else :src="this.profileImageUrl" alt="Profilbild" class="profile-picture">
        <div>{{ username }}</div>
      </div>
    </div>
    <CommentCreator class="col-md-7" :postId="postId"/>
    <FriendsList class="col-md-2" :friends="friendsList"/>
  </div>
</template>
    <script>
import FriendsList from "./Friendslist.vue"
import CommentCreator from "./commentCreator.vue";
import axios from "axios";
//import { watch } from 'vue';
export default {
    name: 'PostComments',
    components: {
    FriendsList,
    CommentCreator,
    },
    data() {
      return {
        API: this.$store.state.API,
        post: {},
        photoData: {},
        postId: null,
        username: null
      };
    },
    created() {
        this.postId = this.$route.query.postId;
    },
    async mounted() {
        await this.fetchPost();
        await this.fetchData();

        if (this.post.photo_id !== null) {
            this.photoData[this.post.photo_id] = await this.getPhoto(this.post.photo_id);
        }
    },
    methods: {
        // method to get the image appended to a post
        async getPhoto(photoId) {
        try {
            const response = await axios.get(this.API + `/getPhoto`, {params: {id: photoId}, responseType: 'arraybuffer'});
            const base64 = btoa(
            new Uint8Array(response.data).reduce(
            (data, byte) => data + String.fromCharCode(byte),
            '',
            ),
        );
            const imageSrc = `data:image/png;base64,${base64}`;
            return imageSrc
            } catch (error) {
                console.error("Error fetching photo:", error);
            }
        },
        async fetchPost() {
            try {
                const response = await axios.get(this.API + `/getPost/${this.postId}`);
                this.post = response.data;
                } catch (error) {
                console.error("Error fetching post:", error);
            }
        },
        async fetchData() {
            try {
                const response = await axios.get(this.API + `/users/${this.post.user_id}`);
                this.username = response.data.username;
                } catch (error) {
                console.error("Error fetching user:", error);
            }
        },
    }
}


    </script>
    
    <style scoped>
.account-info {
  background-color: #2200cd;
  color: white;
  padding: 35px;
  margin-left: 15px;
  height: fit-content;
}

.title {
  font-size: 24px;
  margin-bottom: 10px;
}

.info-item {
  margin-bottom: 5px;
}


.profile-picture {
  width: 70px; 
  height: 70px; 
  border-radius: 50%;
  margin-bottom: 10px; 
}

    </style>
    