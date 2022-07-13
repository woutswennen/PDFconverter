<template>
<v-container>


<experience-table/>
<certificate-table/>

<v-btn @click="renderFile"
    color='primary'
    elevation='2'>
    Download</v-btn>

</v-container>
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









