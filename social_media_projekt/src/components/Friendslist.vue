<template>
    <div class="friends-container">
    <div v-for="friend in friends" :key="friend.id" class="friend-item">
      {{ friend.name }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'FriendsList',
  props: {
    friends: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
        friends12: [
        { id: 1, name: "Daniel" },
        { id: 2, name: "Johann" },
        { id: 3, name: "Kaan" },
      ],
    }},
    methods: {
  getFriendState(){
    // Checken ob Online oder nicht
  },
}

}

</script>

<style>
  
  .friends-container {
  display: flex;
  flex-direction: column;
}

.friend-item {
  margin: 0px 5px 0px 5px;
}

.friends-container {
    width: 12%;
  position: fixed;
  right: 20px; 
  top: 40%; 
  height: 40%;
  transform: translateY(-50%);
  border: solid 2px blue;
  border-radius: 2px;
}
  
</style>