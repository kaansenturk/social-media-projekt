<template>
    <div class="post-container">  
    <form>
      <textarea  id="post_text" placeholder="What's on your mind..." required v-model="text" />
      <div class="file-list">
      <div class="file-item" v-for="(file, index) in droppedFiles" :key="index">
        {{ file.name }}
        <img v-if="isImage(file)" :src="file.preview" alt="Preview" class="image-preview"/>
        <video v-else-if="isVideo(file)" controls>
          <source :src="file.preview" type="video/mp4" />
        </video>
      </div>
      </div>
      <div class="file-uploader">
    <div
      class="drop-area"
      @dragover.prevent="handleDragOver"
      @dragleave="handleDragLeave"
      @drop="handleFileDrop"
      :class="{ 'active': isDragging }"
    >
      <p v-if="isDragging">Drop files here</p>
      <p v-else>Drag and drop files here</p>
    </div>
    <input type="file" ref="fileInput" @change="handleFileChange" style="display: none" />
    <div class="file-list">
      <div class="file-item" v-for="(file, index) in droppedFiles" :key="index">
        {{ file.name }}
      </div>
    </div>
  
    <input type="file" ref="fileInput" @change="handleFileChange" style="display: none" />
  </div>
      <button type="button" @click.prevent="upload_post(this.text)">posten</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'postCreator',
  props: {
    
  },
  data() {
    return {
      API: "http://localhost:8000",
      isDragging: false,
      droppedFiles: [],
    }},
   
    methods: {
      uploadFiles() {
      for (const file of this.droppedFiles) {
        if (this.isImage){
        axios.post(this.API + "upload_photo", null, {
        params: {
          image_data: file,
        }
      })
        }
        console.log('Uploading file:', file.name);
      }
    },

    isImage(file) {
      return file.type.startsWith('image/');
    },

    isVideo(file) {
      return file.type.startsWith('video/');
    },
      handleDragOver(event) {
      event.preventDefault();
      this.isDragging = true;
    },
    handleDragLeave() {
      this.isDragging = false;
    },
    handleFileDrop(event) {
      event.preventDefault();
      this.isDragging = false;
      const files = event.dataTransfer.files;
      this.processDroppedFiles(files);
    },
    handleFileChange(event) {
      const file = event.target.files[0];
      this.processDroppedFiles([file]);
    },
    processDroppedFiles(files) {
      for (const file of files) {
        if (this.isValidFileType(file)) {
          // Read the image file and generate a data URL for preview
          if (this.isImage(file)) {
            const reader = new FileReader();
            reader.onload = (event) => {
              file.preview = event.target.result;
              this.droppedFiles.push(file);
            };
            reader.readAsDataURL(file);
          } else {
            this.droppedFiles.push(file);
          }
        }
      }
    },
    isValidFileType(file) {
      const allowedTypes = ['image/jpeg', 'image/png', 'video/mp4'];
      return allowedTypes.includes(file.type);
    },
      upload_post(text){
        if (this.droppedFiles.length == 0)
          {
            try
            {
              const response =  axios.post(this.API + "/create_post", null, {
      params: {
        username: this.username,
        text: text,
      }
      
    })
    console.log(response)
              console.log("Fred")
            }
            catch
            {
              return
            }
          }
          else {
            this.uploadFiles()
          }
      },
  getUser(name){
    this.username = name
  }
  
}
}

</script>

<style>
.image-preview {
  max-width: 100%;
  max-height: 200px; /* Adjust the maximum height as needed */
  object-fit: contain; /* Maintain aspect ratio */
}
.active {
  border: 2px dashed #0066ff;
}

.file-list {
  margin-top: 20px;
}

.file-item {
  margin: 5px 0;
}
.file-uploader {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100px;
}

.drop-area {
  border: 2px dashed #ccc;
  padding: 20px;
  text-align: center;
  cursor: pointer;
}
#post_text {
  width: 100%;
  height: 100px;
}
  
  .post-container {
    height: 20%;
    padding: 30px;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .login-container h1 {
    text-align: center;
  }
  
  .login-container input[type="text"],
  .login-container input[type="password"] {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }
  
  .login-container button {
    width: 100%;
    padding: 10px;
    background-color: #2200cd;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .login-container button:hover {
    background-color: #2200cd;
  }
  
</style>