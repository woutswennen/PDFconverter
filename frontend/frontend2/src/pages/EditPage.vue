<template>
<div>
  <v-form

    ref="form"
    v-model="valid"
    lazy-validation
  >
  <b-form-row>

        <v-text-field
          v-model="solitan.name"
          label="Name"
          @blur="saveInput"
        ></v-text-field>

        <v-text-field
          v-model="solitan.lastname"
          label="Last Name"
        ></v-text-field>
  </b-form-row>
  <b-form-row>
    <v-text-field
      v-model="solitan.birthday"
      label="Date of birth"
    ></v-text-field>

     <v-text-field
      v-model="solitan.nationality"
      label="Nationality"
    ></v-text-field>
  </b-form-row>
  <b-form-row>
    <v-text-field
      v-model="solitan.gender"
      label="Nationality"
    ></v-text-field>
  </b-form-row>
</v-form>

<experience-table/>
<certificate-table/>

<button @click="renderFile">Render</button>

</div>
</template>





<script>
import { mapState } from 'vuex'
import ExperienceTable from '../components/ExperienceTable.vue'
import CertificateTable from '../components/CertificateTable.vue'
import axios from 'axios'
export default {
  components: {
    ExperienceTable,
    CertificateTable,
  },
  computed: mapState(['solitan']),

  mounted() {
    this.solitan = this.$store.getters.getSolitan;
    console.log(this.$store.getters.getSolitan.name)
  },


  data: () => ({
      solitan: {},
      valid: true,
      editedSolitan: {},
      name: '',
      select: null,
      items: [
        'Item 1',
        'Item 2',
        'Item 3',
        'Item 4',
      ],
      checkbox: false,
    }),

    methods: {
      saveInput () {
        this.$store.commit('editSolitan', this.solitan);
      },

      renderFile() {
        axios({
            method: "POST",
            url: "http://localhost:5000/render",
            data: this.solitan,
            responseType: 'blob'
        })
        .then(async response => {
                     var fileURL = window.URL.createObjectURL(new Blob([response.data]));
                     var fileLink = document.createElement('a');

                     fileLink.href = fileURL;
                     fileLink.setAttribute('download', this.solitan.name + '_' + this.solitan.lastname + '_CV.docx');
                     document.body.appendChild(fileLink);

                     fileLink.click();
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
      }

    },

};
</script>









