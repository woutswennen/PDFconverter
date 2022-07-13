<template>
  <div class="container">
    <div>
      <label>File
        <input type="file" ref="fileInput" accept="image/*,.pdf" @change="handleFileUpload($event)"/>
      </label>
      <br/>
      <br/>
      <button v-on:click="submitFile()">Submit</button>
    </div>
  </div>
</template>





<script>
/* eslint-disable */
import axios from 'axios'

export default {
  data () {
    return {
      file: null
    }
  },
  methods: {
    /**
     * Uploads file to server.
     * @param {Event} event The form change event with the file to be uploaded.
     */
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    /**
     * Uploads the file to the server.
     */
    submitFile() {
      if (this.file == null) {
        return;
      }

      console.log("Submitting file for upload...");
      let formData = new FormData();
      formData.append('file', this.file);

      axios.post(`http://localhost:5000/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 5000
      })
        .then(response => {
          //load the solitan object into the object store.
          this.$store.dispatch("fetchSolitan")
          console.log(this.$store.getters.getSolitan.name)
          this.$refs.fileInput.value = "";

        }).catch(error => {
          console.log("File upload failed.");
          console.error(error);
        });
    }
  }
}
</script>

