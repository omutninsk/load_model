<template>
  <div>
    <div>
      <b-button @click="showModal = true">Add Source</b-button>
      <b-modal v-model="showModal" title="Add Source" @ok="addSource" @cancel="showModal = false">
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
      <b-modal v-model="showEdit" size="xl" title="Edit" @ok="addSource" @cancel="clear">
        <div>
          <SourceFieldsView :source_id="current_source_id"/>
        </div>
      </b-modal>
    </div>
    <br>
    <b-card-group>
      
      <div class="row">
        <div v-for="source in sources" :key="source.id" class="col-4">
            <b-tabs>
              <b-tab title="Settings">
                <b-card
                    :title="source.name"
                    :sub-title="source.target_field">
                  <p class="card-text"><strong>Index name:</strong> {{ source.index_name }}</p>
                  <p class="card-text"><strong>Search object:</strong> {{ source.search_object }}</p>
                  <p class="card-text"><strong>ID:</strong> {{ source.id }}</p>
                  <b-button @click="showEditWindow(source.id)">Edit</b-button>
                  <b-button @click="deleteSource(source.id)" variant="danger">Delete</b-button>
                </b-card>
              </b-tab>
              <b-tab title="Graph">
                <b-card>
                  <ChartView :source_id="source.id"/>
                  {{ r2score }}
                  <b-button @click="fit(source.id)" variant="danger">Fit</b-button>
                </b-card>

              </b-tab>
            </b-tabs>
        </div>
      </div>
    </b-card-group>
  </div>
</template>

<script>
import axios from 'axios'
import SourceFieldsView from '@/components/SourceFieldsView.vue'
import ChartView from "@/components/ChartView.vue";
export default {
  components: {SourceFieldsView, ChartView},
  data() {
    return {
      r2score: null,
      showModal: false,
      showEdit: false,
      current_source_id: null,
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
    showEditWindow(id){
      this.current_source_id = id
      console.log(id)
      this.showEdit = true
    },
    clear() {
      this.showEdit = false
      this.current_source_id=false
    },
    fit(id) {
      console.log(id)
      const params = {
        "id": id
      }
      axios.get(`/api/model/fit/`, {params}).then(response => {
            this.r2score = response.data.items.r2score
          })
          .catch(error => {
            console.log(error)
          })
    },
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
      const params = {
        "id": id
      }
      axios.delete(`/api/sources/`, {params}).then(response => {
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
