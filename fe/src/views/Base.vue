<template>
  <el-container>
    <el-aside width="200px">Aside</el-aside>
    <el-container>
      <el-header>Header</el-header>
      <el-main>
        <button class="button is-info">{{ now }}</button>
        <div class="field">
          <div class="control">
            <input class="input is-primary" type="text" placeholder="Primary input" v-model="message">
          </div>
        </div>
        <div class="content is-small">
          <input type="checkbox" id="jack" value="Jack" v-model="checkedIDs">
          <label class="checkbox" for="jack">Jack</label>
          <input type="checkbox" id="john" value="John" v-model="checkedIDs">
          <label class="checkbox" for="john">John</label>
          <input disabled type="checkbox" id="mike" value="Mike" v-model="checkedIDs">
          <label disabled class="checkbox" for="mike">Mike</label>
          <p>
            MSG: {{message}}
          </p>
          <el-button @click="doPost" type="success">Post</el-button>
        </div>
      </el-main>
      <el-footer>Footer</el-footer>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      message: "",
      checkedIDs: []
    };
  },
  watch: {},
  computed: {
    now: function() {
      return Date.now();
    }
  },
  created: function() {},
  methods: {
    doPost() {
      this.$http.defaults.headers.common["TOKEN"] = localStorage.getItem(
        "access_token"
      );
      this.$http
        .post("/api/projects", {
          id: JSON.stringify(this.checkedIDs)
        })
        .then(resp => {
          console.log(resp.data);
        });
    }
  }
};
</script>


<style lang="scss">
.el-header,
.el-footer {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #d3dce6;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
  line-height: 160px;
}

body > .el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}
</style>
