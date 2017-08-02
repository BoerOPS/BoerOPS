<template>
  <div id="app">
    <router-link to="/hello">To Hello</router-link>
    <router-view></router-view>
  </div>
</template>

<script>
  import axios from 'axios';
  export default {
    name: 'app',
    mounted: function () {
      axios.get('/user/1')
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  }

</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>