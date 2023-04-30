<template>
  <div>
    <div>
      <!-- Кнопка для открытия модального окна -->
      <b-button @click="showModal = true">Добавить Source</b-button>
      <!-- Модальное окно -->
      <b-modal v-model="showModal" title="Добавить Source" @ok="addSource" @cancel="showModal = false">
        <div>
          <form>
            <div class="form-group">
              <label for="name">Name:</label>
              <input type="text" class="form-control" id="name" v-model="newSource.name">
            </div>
            <div class="form-group">
              <label for="index_name">Index Name:</label>
              <input type="text" class="form-control" id="index_name" v-model="newSource.index_name">
            </div>
            <div class="form-group">
              <label for="target_field">Target Field:</label>
              <input type="text" class="form-control" id="target_field" v-model="newSource.target_field">
            </div>
            <div class="form-group">
              <label for="target_field">Search Object:</label>
              <input type="text" class="form-control" id="search_object" v-model="newSource.search_object">
            </div>
          </form>
        </div>
      </b-modal>
    </div>
    <br>
    <div v-for="source in sources" :key="source.id">
      <h2>{{ source.name }}</h2>
      <p>Id: {{ source.id }}</p>
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
      showModal: false,
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
      const data = {
        id: id
      }
      console.log(data)
      axios.delete(`/api/sources/`, {data}).then(response => {
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
