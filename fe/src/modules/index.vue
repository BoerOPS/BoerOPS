<template>
  <div class="index">
    <el-button type="primary"><router-link to="/test">To Test</router-link></el-button>
    <p>{{msg}}</p>
  </div>
</template>

<script>
  export default {
    name: 'hello',
    data () {
      return {
        msg: 'this is BoerOPS index page'
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
