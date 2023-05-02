import { Bar } from 'vue-chartjs'

export default {
    extends: Bar,
    mounted () {
        // Overwriting base render method with actual data.
        this.renderChart({
            labels: ['January', 'February', 'March'],
            datasets: [
                {
                    label: 'GitHub Commits',
                    backgroundColor: '#af6262',
                    data: [40, 20, 12]
                }
            ]
        })
    }
}