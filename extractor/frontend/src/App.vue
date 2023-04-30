<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <SourceView/>
</template>

<script>
import SourceView from './components/SourceView.vue'

export default {
  name: 'App',
  components: {
    SourceView
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
