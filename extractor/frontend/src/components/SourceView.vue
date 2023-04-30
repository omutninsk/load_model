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
      const formData = new FormData();
      formData.append('name', this.newSource.name)
      formData.append('index_name', this.newSource.index_name)
      formData.append('target_field', this.newSource.target_field)
      formData.append('search_object', this.newSource.search_object)
      axios.post('/api/sources', formData)
          .then(response => {
            console.log(response)
            this.getSources()
          })
          .catch(error => {
            console.log(error)
          })
    },
    deleteSource(id) {
      axios.delete(`/api/sources/${id}`)
          .then(response => {
            console.log(response)
            this.sources = this.sources.filter(source => source.id !== id)
          })
          .catch(error => {
            console.log(error)
          })
    },
    getSources() {
      axios.get('/api/sources/list/')
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
