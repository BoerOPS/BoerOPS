<template>
  <div name="hello">
    <p>{{msg}}</p>
    <router-link to="/home">
      <el-button type="primary">Home</el-button>
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'hello',
  data () {
    return {
      msg: '这是Hello页面'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
