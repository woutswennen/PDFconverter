<template>
<v-container>

  <h4>Skills seperated with a comma</h4>
  <v-form

    ref="form"
    v-model="valid"
    lazy-validation
    class="my-5"
  >
  <b-form-row>

        <v-text-field
          v-model="solitan.man_skills"
          label="Management skills"
          @blur="saveInput"
        ></v-text-field>


  </b-form-row>





  <b-form-row>
    <v-text-field
      v-model="solitan.other_skills"
      label="Other skills"
      @blur="saveInput"
    ></v-text-field>
  </b-form-row>

</v-form>

<TechSkillsTable/>
<b-form-row class="d-flex justify-content-end">
    <router-link :to="{path: '/'}">
      <v-btn @click="renderFile"
      color='primary'
      elevation='2'>
      Render and Download</v-btn>
    </router-link>
</b-form-row>



</v-container>
</template>





<script>
import { mapState } from 'vuex'
import axios from 'axios'
import TechSkillsTable from '../components/TechSkillsTable.vue'
export default {
  computed: mapState(['solitan']),

  components: {
    TechSkillsTable
  },

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
      saveInput() {
        this.$store.commit('setSolitan', this.solitan);
      },

      loadInfo() {
        this.$router.push('/login');
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
                     fileLink.setAttribute('download', this.solitan.name + '-' + this.solitan.lastname + '.docx');
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











