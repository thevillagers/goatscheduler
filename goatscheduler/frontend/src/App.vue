<template>
  <div id="app">
    <Scheduler />
    <ProgressBar :percent.sync='p' />
  </div>
</template>

<script>
import Scheduler from './components/Scheduler.vue'
import ProgressBar from './components/ProgressBar.vue'

export default {
  name: 'App',
  components: {
    Scheduler, ProgressBar
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
