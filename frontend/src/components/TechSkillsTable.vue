<template>
    <v-data-table
      :headers="headers"
      :items="tech_skills"
      sort-by="start_date"
      item-key="cert_title"
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

          <v-toolbar-title>Tech Skills</v-toolbar-title>
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
                        v-model="editedItem.skill"
                        label="Skill"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.level"
                        label="Level"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="editedItem.year_exp"
                        label="Years experience"
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
            text: 'Skill',
            align: 'start',
            sortable: true,
            value: 'skill',
          },
          { text: 'Level', value: 'level' },
          { text: 'Years experience', value: 'year_exp' },
          { text: 'Actions', value: 'actions', sortable: false },

        ],
        tech_skills: [],
        editedIndex: -1,
        editedItem: {
          skill: '',
          level: '',
          year_exp: '',
        },
        defaultItem: {
          skill: '',
          level: '',
          year_exp: '',
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
          this.tech_skills = this.$store.getters.getSolitan.tech_skills
        },


        editItem (item) {
          this.editedIndex = this.tech_skills.indexOf(item)
          this.editedItem = Object.assign({}, item)
          this.dialog = true
        },

        deleteItem (item) {
          this.editedIndex = this.tech_skills.indexOf(item)
          this.editedItem = Object.assign({}, item)
          this.dialogDelete = true
          this.deleteItemConfirm()
        },

        deleteItemConfirm () {
          this.tech_skills.splice(this.editedIndex, 1)
          this.closeDelete()
          this.$store.commit('editTechSkills', this.tech_skills)
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
            Object.assign(this.tech_skills[this.editedIndex], this.editedItem)
          } else {
            this.tech_skills.push(this.editedItem)
          }
          this.close()
          this.$store.commit('setTechSkills', this.tech_skills)
        },

        clickConfirm() {
            this.close()
            console.log("ja")
            document.getElementById('confirmBtn').click()

        }

      },
  }
</script>
