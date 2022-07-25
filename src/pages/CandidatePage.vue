<template>
<v-container>
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
          @blur="saveInput"
        ></v-text-field>
  </b-form-row>
  <b-form-row>
    <v-text-field
      v-model="solitan.birthday"
      label="Date of birth"
      @blur="saveInput"
    ></v-text-field>

     <v-text-field
      v-model="solitan.nationality"
      label="Nationality"
      @blur="saveInput"
    ></v-text-field>
  </b-form-row>

  <b-form-row>
      <v-select class="company-size-dropdown"
        :items="['Male','Female']"
        v-model="solitan.gender"
        v-on:change="saveInput"
        label="Gender">
      </v-select>
      <v-select class="company-size-dropdown"
        :items="['Employee','Freelance']"
        v-model="solitan.work_occupation"
        v-on:change="saveInput"
        label="Availability">
      </v-select>
  </b-form-row>
  <b-form-row>
    <v-text-field
      v-model="solitan.fitness"
      label="Descripe the candidate fit"
      @blur="saveInput"
    ></v-text-field>
  </b-form-row>
    <v-text-field
      v-model="solitan.availability"
      label="Availability date"
      @blur="saveInput"
    ></v-text-field>
  <b-form-row class="d-flex justify-content-end">
    <router-link :to="{path: '/professional'}">
      <b-button variant="info" class="text-white">Next >> Professional Experience</b-button>
    </router-link>
  </b-form-row>

</v-form>


</v-container>
</template>





<script>
import { mapState } from 'vuex'
import axios from 'axios'
export default {

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
        this.$store.commit('setSolitan', this.solitan);
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









