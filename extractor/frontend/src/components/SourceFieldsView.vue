<template>
  <div>
    <h3>Source Fields</h3>
    {{source_id}}
    <b-table striped hover :items="sourceFields" :fields="tableFields"></b-table>
    <b-form-group>
      <b-form-input v-model="newSourceField.name" placeholder="Enter field name"></b-form-input>
      <b-form-input v-model="newSourceField.operations" placeholder="Operations"></b-form-input>
      <b-button @click="addField">Add Field</b-button>
    </b-form-group>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    source_id: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      newFieldName: '',
      sourceFields: [],
      newSourceField: {
        name: '',
        operations: '',
        source_id: '',
      }
    }
  },
  computed: {
    tableFields() {
      return [
        { key: 'id', label: 'ID', sortable: true },
        { key: 'name', label: 'Name', sortable: true },
        { key: 'operations', label: 'Operations' }
      ]
    }
  },
  methods: {
    addField() {
      const formData = new FormData();
      formData.append('name', this.newSourceField.name)
      formData.append('operations', this.newSourceField.operations)
      formData.append('source_id', this.source_id)
      axios.post('/api/source_fields', formData)
          .then(response => {
            console.log(response)
            this.getSourceFields()
          })
          .catch(error => {
            console.log(error)
          })
      this.newFieldName = ''
    },
    getSourceFields() {
      const params = {
        id: this.source_id,
      };
      axios.get('/api/source_fields/', {params})
          .then(response => {
            this.sourceFields = response.data.items
          })
          .catch(error => {
            console.log(error)
          })
    }
  },
  updated() {
    this.getSourceFields()
  }
}
</script>
