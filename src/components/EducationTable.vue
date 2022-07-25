<template>
    <v-data-table
      :headers="headers"
      :items="education"
      sort-by="end_date"
      :single-expand="singleExpand"
      :expanded.sync="expanded"
      item-key="institution"
      show-expand
      class="elevation-1 my-4"
    >

        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            {{ item.education_description }}
          </td>
        </template>
      <template v-slot:top>
        <v-toolbar
          flat
        >

          <v-toolbar-title>Education</v-toolbar-title>
          <v-divider
            class="mx-4"
            inset
            vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-dialog
            v-model="dialog"
            max-width="500px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="primary"
                dark
                class="mb-2"
                v-bind="attrs"
                v-on="on"
              >
                New Item
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.title"
                        label="Education title"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.institution"
                        label="Institution"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.education_description"
                        label="Education Description"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.end_date"
                        label="End date"
                      ></v-text-field>
                    </v-col>


                  </v-row>

                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="close"
                >
                  Cancel
                </v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="save"
                >
                  Save
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="text-h5">Are you sure you want to delete this item?</v-card-title>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
                <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon
          small
          class="mr-2"
          @click="editItem(item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon
          small
          @click="deleteItem(item)"
        >
          mdi-delete
        </v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn
          color="primary"
          @click="initialize"
        >
          Reset
        </v-btn>
      </template>
    </v-data-table>
</template>


<script>
  export default {
      data: () => ({
        dialog: false,
        dialogDelete: false,
        expanded: [],
        singleExpand: true,
        headers: [
          {
            text: 'Education title',
            align: 'start',
            sortable: true,
            value: 'title',
          },
          { text: 'Institution', value: 'institution' },
          { text: 'End date', value: 'end_date' },
          { text: '', value: 'data-table-expand', sortable: false },
          { text: 'Actions', value: 'actions', sortable: false },

        ],
        education: [],
        editedIndex: -1,
        editedItem: {
          title: '',
          institution: '',
          education_description: '',
          end_date: '',
        },
        defaultItem: {
          title: '',
          institution: '',
          education_description: '',
          end_date: '',
        },
      }),

      computed: {
        formTitle () {
          return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
        },
      },

      watch: {
        dialog (val) {
          val || this.close()
        },
        dialogDelete (val) {
          val || this.closeDelete()
        },
      },

      created () {
        this.initialize()
      },

      methods: {
        initialize () {
          this.education = this.$store.getters.getSolitan.education
        },


        editItem (item) {
          this.editedIndex = this.education.indexOf(item)
          this.editedItem = Object.assign({}, item)
          this.dialog = true
        },

        deleteItem (item) {
          this.editedIndex = this.education.indexOf(item)
          this.editedItem = Object.assign({}, item)
          this.dialogDelete = true
        },

        deleteItemConfirm () {
          this.education.splice(this.editedIndex, 1)
          this.closeDelete()
          this.$store.commit('setEducation', this.education)
        },

        close () {
          this.dialog = false
          this.$nextTick(() => {
            this.editedItem = Object.assign({}, this.defaultItem)
            this.editedIndex = -1
          })
        },

        closeDelete () {
          this.dialogDelete = false
          this.$nextTick(() => {
            this.editedItem = Object.assign({}, this.defaultItem)
            this.editedIndex = -1
          })
        },

        save () {
          if (this.editedIndex > -1) {
            Object.assign(this.education[this.editedIndex], this.editedItem)
          } else {
            this.education.push(this.editedItem)
            console.log(this.education)
          }
          this.close()
          this.$store.commit('setEducation', this.education)
        },
      },
  }
</script>
