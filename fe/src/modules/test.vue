<template>
  <div class="test">
    <el-button type="primary"><router-link to="/">To Index</router-link></el-button>
    <p>{{msg}}</p>
  </div>
</template>

<script>
  export default {
    name: 'hello',
    data () {
      return {
        msg: 'this a test page'
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
