<template>
  <div class="home">
    <el-carousel height="300px">
      <el-carousel-item v-for="item in 4" :key="item">
        <h3>{{ item }}</h3>
      </el-carousel-item>
    </el-carousel>
    <el-button @click="getAllProject" type="info">项目</el-button>
    <el-button @click="$router.push({name: 'Host'})" type="success">主机</el-button>
    <el-button @click="$router.push({name: 'Deploy'})" type="primary">部署</el-button>
    <el-button @click="removeToken">登出</el-button>
    <el-button @click="removeAllToken" type="danger">注销</el-button>
    <router-link :to="{ name: 'Base' }">Base</router-link>
    <el-button @click="createUserVisible=true, userInfo={}">添加用户</el-button>
    <el-dialog title="添加Gitlab用户"
      :visible.sync="createUserVisible"
      v-loading="loading"
      width="30%">
      <el-container style="padding:20px 5px;border: 1px solid gray;border-radius:5px">
        <el-form ref="form" :model="userInfo" label-width="80px">
          <el-form-item label="用户名">
            <el-input v-model="userInfo.username"></el-input>
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input v-model="userInfo.email"></el-input>
          </el-form-item>
          <el-form-item label="密码">
            <el-input type="password" v-model="userInfo.password"></el-input>
          </el-form-item>
          <el-form-item label="名字">
            <el-input v-model="userInfo.name"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="danger" @click="createUser">添加</el-button>
            <el-button
              @click="createUserVisible=false,
              userInfo={}">
              取消
            </el-button>
          </el-form-item>
        </el-form>
      </el-container>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      msg: "Login in with gitlab.",
      createUserVisible: false,
      loading: false,
      userInfo: {}
    };
  },
  //created、mounted、updated、destroyed
  created: function() {
    // console.log(localStorage.getItem('access_token'));
    // console.log(localStorage.getItem('refresh_token'));
  },
  mounted: function() {},
  computed: {},
  methods: {
    createUser() {
      this.loading = true;
      this.$http.post("/webhooks", this.userInfo).then(resp => {
        this.loading = false;
        this.createUserVisible = false;
        this.$message({
          type: "success",
          message: resp.data,
          center: true
        });
      });
    },
    removeAllToken() {
      localStorage.clear();
      this.$router.push({ name: "Login" });
      this.$message({
        showClose: true,
        message: "注销成功",
        type: "success"
      });
    },
    removeToken() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("created_at");
      this.$message({
        showClose: true,
        message: "退出成功",
        type: "success"
      });
      this.$router.push({ name: "Login" });
    },
    getAllProject() {
      this.$router.push({ name: "Project" });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
