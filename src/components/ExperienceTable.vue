<template>
    <v-data-table
      :headers="headers"
      :items="experiences"
      sort-by="start_date"
      :single-expand="singleExpand"
      :expanded.sync="expanded"
      item-key="role"
      show-expand
      class="elevation-1 my-4"
    >

        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            {{ item.job_description }}
          </td>
        </template>
      <template v-slot:top>
        <v-toolbar
          flat
        >

          <v-toolbar-title>Experiences</v-toolbar-title>
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
                        v-model="editedItem.role"
                        label="Job Title"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.company"
                        label="Company"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.start_date"
                        label="Start Date"
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
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.client"
                        label="Client"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.job_description"
                        label="Description"
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
            text: 'Role',
            align: 'start',
            sortable: true,
            value: 'role',
          },
          { text: 'Company', value: 'company' },
          { text: 'Start date', value: 'start_date' },
          { text: 'End date', value: 'end_date' },
          { text: 'Client', value: 'client' },
          { text: '', value: 'data-table-expand', sortable: false },
          { text: 'Actions', value: 'actions', sortable: false },

        ],
        experiences: [],
        editedIndex: -1,
        editedItem: {
          role: '',
          company: '',
          start_date: '',
          end_date: '',
          client: '',
        },
        defaultItem: {
          role: '',
          company: '',
          start_date: '',
          end_date: '',
          client: '',
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
          this.experiences = this.$store.getters.getSolitan.work_experience
        },


        editItem (item) {
          this.editedIndex = this.experiences.indexOf(item)
          this.editedItem = Object.assign({}, item)
          this.dialog = true
        },

        deleteItem (item) {
          this.editedIndex = this.experiences.indexOf(item)
          this.editedItem = Object.assign({}, item)
          this.dialogDelete = true
        },

        deleteItemConfirm () {
          this.experiences.splice(this.editedIndex, 1)
          this.closeDelete()
          this.$store.commit('setProjects', this.experiences)
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
            Object.assign(this.experiences[this.editedIndex], this.editedItem)
          } else {
            this.experiences.push(this.editedItem)
          }
          this.close()
          this.$store.commit('setProjects', this.experiences)
        },
      },
  }
</script>