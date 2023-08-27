<template>
  <div style="width: max-content;">
    <Line v-if="loaded" :data="chartData" :chart-data="chartData" :style="myStyles"/>
    <b-button @click="getData(source_id)" variant="primary">Refresh</b-button>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend } from 'chart.js'
import axios from "axios";
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)
export default {
  props: {
    source_id: {
      type: String,
      required: false
    }
  },
  name: 'BarChart',
  components: { Line },
  data() {
    return {
      loaded: false,
      //responsive: true,
      options: {
        // maintainAspectRatio: true
      },
      chartData: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: '#f87979',
            data: [40, 20, 12, 35, 56, 45, 67, 89, 80, 150]
          }
        ]
      },
    }
  },
  methods: {
    getDate(ms) {
      if (ms) {
        let a = new Date(ms);
        let months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        let year = a.getFullYear();
        let month = months[a.getMonth()];
        let date = a.getDate();
        let hour = a.getHours();
        let min = a.getMinutes();
        let sec = a.getSeconds();
        let time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
        return time;
      }
    },
    getData(id) {
      this.loaded = false
      console.log(id)
      const params = {
        "id": id
      }
      axios.get(`/api/model/predict/`, {params}).then(response => {
        console.log(this.chartData, 'received chart data')
        this.chartData.labels = response.data.legend.map(this.getDate)
        this.chartData.datasets = []
        this.chartData.datasets.push(
            {
              label: "Model prediction difference",
              data: response.data.result
            }
        )
        console.log(this.chartData, response)
        this.loaded = true
      })
          .catch(error => {
            console.log(error)
          })
    }
  },
  computed: {
    myStyles () {
      return {
        width: '450px',
        height: '300px',
        position: 'relative'
      }
    }
  },
  mounted() {
    this.getData(this.source_id)
  }
}
</script>