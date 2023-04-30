<template>
  <div>
    <h3>Source Fields</h3>
    <table>
      <thead>
      <tr>
        <th>Name</th>
        <th>Operations</th>
        <th></th> <!-- добавляем столбец для кнопки удаления -->
      </tr>
      </thead>
      <tbody>
      <tr v-for="field in sourceFields" :key="field.id">
        <td>{{ field.name }}</td>
        <td>{{ field.operations }}</td>
        <td>
          <b-button variant="danger" size="sm" @click="deleteSourceField(field.id)">
            Delete
          </b-button>
        </td>
      </tr>
      </tbody>
    </table>
    <table>
      <tr v-for="item in fetchedData" :key="item.key">
        <td>{{item.key}}</td><td>{{item.value}}</td>
      </tr>
    </table>
    <b-button @click="clearData">Clear</b-button>
    <b-button @click="fetchData">Fetch</b-button>
<!--    <b-table striped hover :items="sourceFields" :fields="tableFields"></b-table>-->
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
      required: false
    }
  },
  data() {
    return {
      sourceFields: [],
      result: [],
      newSourceField: {
        name: '',
        operations: '',
        source_id: '',
      }
    }
  },
  watch: {
    source_id() {
      this.getSourceFields()
    }
  },
  computed: {
    tableFields() {
      return [
        // { key: 'id', label: 'ID', sortable: true },
        { key: 'name', label: 'Name', sortable: true },
        { key: 'operations', label: 'Operations' }
      ]
    },
    fetchedData() {
      const data = []
      for (const key in this.result) {
        data.push({key: key, value: this.result[key]})
      }
      console.log(data)
      return data
    }
  },
  methods: {
    clearData() {
      this.result = []
    },
    fetchData() {
      const params = {
        id: this.source_id,
      }
      if (this.source_id) {
        axios.get('/api/model/fetch', {params})
            .then(response => {
              this.result = response.data.items
            })
            .catch(error => {
              console.log(error)
            })
      }
    },
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
    deleteSourceField(id) {
      const params = {
        "id": id
      }
      axios.delete(`/api/source_fields/`, {params}).then(response => {
            console.log(response)
            this.getSourceFields()
          })
          .catch(error => {
            console.log(error)
          })
    },
    getSourceFields() {
      const params = {
        id: this.source_id,
      };
      if (this.source_id) {
        axios.get('/api/source_fields/', {params})
            .then(response => {
              this.sourceFields = response.data.items
            })
            .catch(error => {
              console.log(error)
            })
      }

    }
  }
}
</script>
