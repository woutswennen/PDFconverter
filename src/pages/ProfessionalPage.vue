<template>
<v-container>


<project-table/>
<certificate-table/>
<education-table/>
  <b-form-row class="d-flex justify-content-end">
    <router-link :to="{path: '/skills'}">
      <b-button variant="info" class="text-white">Next >> Skills</b-button>
    </router-link>
  </b-form-row>
</v-container>
</template>





<script>
import { mapState } from 'vuex'
import ProjectTable from '../components/ProjectTable.vue'
import CertificateTable from '../components/CertificateTable.vue'
import EducationTable from '../components/EducationTable.vue'
import axios from 'axios'
export default {
  components: {
    ProjectTable,
    CertificateTable,
    EducationTable,
  },
  computed: mapState(['solitan']),

  mounted() {
    this.solitan = this.$store.getters.getSolitan;
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
                     fileLink.setAttribute('download', 'file.docx');
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









