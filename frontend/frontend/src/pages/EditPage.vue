<template>
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




    <v-btn
      :disabled="!valid"
      color="success"
      class="mr-4"
      @click="render"
    >
      Render
    </v-btn>



  </v-form>
</template>



<script>

</script>





<script>
import { mapState } from 'vuex'


export default {
  date: () => ({
    solitan: {}
  }),
  components: {

  },
  computed: mapState(['solitan']),

  mounted() {

    this.solitan = this.$store.getters.getSolitan;
  },

  methods: {

  },
  data: () => ({
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
      render () {
        this.$store.commit('editSolitan', this.solitan);
      },
    },

};
</script>









