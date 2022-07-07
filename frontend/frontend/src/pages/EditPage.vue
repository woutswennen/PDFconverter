<template>
<div>
  <v-form

    ref="form"
    v-model="valid"
    lazy-validation
  >
  <b-form-row>
    <b-column>
        <v-text-field
          v-model="solitan.name"
          label="Name"
          @blur="saveInput"
        ></v-text-field>
    </b-column>
    <b-column>
        <v-text-field
          v-model="solitan.lastname"
          label="Last Name"
        ></v-text-field>
    </b-column>
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

</div>
</template>





<script>
import { mapState } from 'vuex'
import ExperienceTable from '../components/ExperienceTable.vue'
import CertificateTable from '../components/CertificateTable.vue'
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
      saveInput () {
        console.log(this.solitan.name)
        this.$store.commit('editSolitan', this.solitan);
      },

    },

};
</script>









