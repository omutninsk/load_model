<template>
  <div>
    <h3>Source Fields</h3>
    <b-card no-body>
    <b-tabs card>
      <b-tab title="Data Rows">
        <b-form-group>
            <b-form-input v-model="newSourceField.name" placeholder="Enter rule name"></b-form-input>
            <b-form-input v-model="newSourceField.operations" placeholder="Operations"></b-form-input>
            <b-form-select v-model="newSourceField.variable_type" :options="options"></b-form-select>
            <b-button @click="addField(source_id)">Add Field</b-button>
        </b-form-group>
        <table v-if="sourceFields.length > 0">
          <thead>
          <tr>
            <th>Rule</th>
            <th>Operations</th>
            <th>Var type</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="field in sourceFields" :key="field.id">
            <td>{{ field.name }}</td>
            <td>{{ field.operations }}</td>
            <td>{{ field.variable_type }}</td>
            <td>
              <b-button variant="danger" size="sm" @click="deleteSourceField(field.id)">
                Delete
              </b-button>
            </td>
          </tr>
          </tbody>
        </table>
      </b-tab>
      <b-tab title="Raw Data" active>
        <table>
          <tr v-for="item in sourceData" :key="item.key">
            <td>{{item.key}}</td><td>{{item.value}}</td>
          </tr>
        </table>
        <b-button @click="clearData">Clear</b-button>
        <b-button @click="fetchData">Fetch</b-button>
      </b-tab>
      <b-tab title="Processed Data">
        <table>
          <tr v-for="item in fetchedData" :key="item.key">
            <td>{{item.key}}</td><td>{{item.value}}</td>
          </tr>
        </table>
      </b-tab>
    </b-tabs>
  </b-card>
    
    
<!--    <b-table striped hover :items="sourceFields" :fields="tableFields"></b-table>-->
    
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
      source: [],
      options: [
          { value: 'categorical', text: 'categorical' },
          { value: 'quantitative', text: 'quantitative' }
        ],
      newSourceField: {
        name: '',
        operations: '',
        source_id: '',
        variable_type: 'categorical'
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
        { key: 'operations', label: 'Operations' },
        { key: 'variable_type', label: 'Variable Type' }
      ]
    },
    sourceData() {
      const data = []
      for (const key in this.source) {
        data.push({key: key, value: this.source[key]})
      }
      return data
    },
    fetchedData() {
      const data = []
      if (this.result) {
        for (const key in this.result) {
          data.push({key: key, value: this.result[key]})
        }
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
              this.source = response.data.source
            })
            .catch(error => {
              console.log(error)
            })
      }
    },
    addField(id) {
      const formData = new FormData();
      formData.append('name', this.newSourceField.name)
      formData.append('operations', this.newSourceField.operations)
      formData.append('variable_type', this.newSourceField.variable_type)
      formData.append('source_id', id)
      axios.post('/api/source_fields', formData)
          .then(response => {
            this.newSourceField = {
              name: '',
              operations: '',
              variable_type: 'categorical',
              source_id: '',
            }
            console.log(response, 'get source fields')
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
              console.log('Ошибочка вышла', error)
            })
      }

    }
  }
}
</script>
