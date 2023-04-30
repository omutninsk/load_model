<template>
  <div>
    <form @submit.prevent="addSource">
      <label>Source Name:</label>
      <input type="text" v-model="newSource.name" required>
      <br><br>
      <label>Index Name:</label>
      <input type="text" v-model="newSource.index_name" required>
      <br><br>
      <label>Target Field:</label>
      <input type="text" v-model="newSource.target_field" required>
      <br><br>
      <label>Search Object:</label>
      <textarea v-model="newSource.search_object"></textarea>
      <br><br>
      <button type="submit">Add Source</button>
    </form>
    <br>
    <div v-for="source in sources" :key="source.id">
      <h2>{{ source.name }}</h2>
      <p>Index Name: {{ source.index_name }}</p>
      <p>Target Field: {{ source.target_field }}</p>
      <p>Search Object: {{ source.search_object }}</p>
      <button @click="deleteSource(source.id)">Delete Source</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      sources: [],
      newSource: {
        name: '',
        index_name: '',
        target_field: '',
        search_object: ''
      }
    }
  },
  methods: {
    addSource() {
      axios.post('http://localhost:5000/api/sources/', this.newSource)
          .then(response => {
            this.sources.push(response.data)
            this.newSource = {
              name: '',
              index_name: '',
              target_field: '',
              search_object: ''
            }
          })
          .catch(error => {
            console.log(error)
          })
    },
    deleteSource(id) {
      axios.delete(`http://localhost:5000/api/sources/${id}`)
          .then(response => {
            console.log(response)
            this.sources = this.sources.filter(source => source.id !== id)
          })
          .catch(error => {
            console.log(error)
          })
    },
    getSources() {
      axios.get('http://localhost:5000/api/sources/list/')
          .then(response => {
            this.sources = response.data.items
          })
          .catch(error => {
            console.log(error)
          })
    }
  },
  mounted() {
    this.getSources()
  }
}
</script>
