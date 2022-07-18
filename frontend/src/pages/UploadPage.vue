<template>
  <b-container class="position-relative p-4">
    <b-row class="mb-2 d-flex justify-content-center">
      <div class="col-md-11" style="text-align: center">
        <h1 class="text-secondary" style="font-size:50px">Welcome to Solita CV Transformer</h1>
        <p class="text-secondary">This tool uses NLP (Natural Language Processing) to extract the information from the 
          solitan CV, and then write them down in the template of the clien (Bv. BNP consultant template)
        </p>
      </div>
    </b-row>
    <b-row >
      <b-col class="d-flex justify-content-center">
        <b-card 
          title="Please upload the solitan CV"
          style="max-width:30rem; text-align: center;"
          class="mb-2 d-flex justify-content-center text-secondary"
        >
          <svg width="10em" height="10em" viewBox="0 0 16 12" class="dropZoneImage" fill="#14a2b8" xmlns="http://www.w3.org/2000/svg">
            <path
              fill-rule="evenodd"
              d="m 8.0274054,0.49415269 a 5.53,5.53 0 0 0 -3.594,1.34200001 c -0.766,0.66 -1.321,1.52 -1.464,2.383 -1.676,0.37 -2.94199993,1.83 -2.94199993,3.593 0,2.048 1.70799993,3.6820003 3.78099993,3.6820003 h 8.9059996 c 1.815,0 3.313,-1.43 3.313,-3.2270003 0,-1.636 -1.242,-2.969 -2.834,-3.194 -0.243,-2.58 -2.476,-4.57900001 -5.1659996,-4.57900001 z m 2.3539996,5.14600001 -1.9999996,-2 a 0.5,0.5 0 0 0 -0.708,0 l -2,2 a 0.5006316,0.5006316 0 1 0 0.708,0.708 l 1.146,-1.147 v 3.793 a 0.5,0.5 0 0 0 1,0 v -3.793 l 1.146,1.147 a 0.5006316,0.5006316 0 0 0 0.7079996,-0.708 z"
              />
          </svg>
          <b-form-file
            v-model="file"
            :state="Boolean(file)"
            placeholder="Choose a file or drop it here..."
            drop-placeholder="Drop file here..."
            accept="image/*,.pdf"
            ref="fileInput"
            @change="handleFileUpload($event)"
          ></b-form-file>
          <b-row class="mt-3">
            <b-button variant="info" v-on:click="submitFile()" class="m-3 text-white mx-auto" style="width: 200px;">Submit</b-button>
          </b-row>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
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
          if(response.data.success == true){
              return this.$store.dispatch("fetchSolitan")
            } else{
               this.has_error = true;
            }
     })
     .then(() => {
        this.$refs.fileInput.value = "";
        this.$router.push('/personal');
     })
    }
  }
}
</script>

