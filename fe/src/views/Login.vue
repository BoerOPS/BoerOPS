<template>
  <el-form :model="loginForm" :rules="loginFormRule" ref="loginFormRule" label-position="left" label-width="0px" class="demo-ruleForm login-container">
    <h3 class="title">系统登录</h3>
    <el-form-item prop="username">
      <el-input type="text" v-model="loginForm.username" auto-complete="off" placeholder="账号"></el-input>
    </el-form-item>
    <el-form-item prop="password">
      <el-input type="password" v-model="loginForm.password" auto-complete="off" placeholder="密码"></el-input>
    </el-form-item>
    <el-checkbox v-model="checked" checked class="remember">记住密码</el-checkbox>
    <el-form-item style="width:100%;">
      <el-button type="primary" style="width:100%;" @click.native.prevent="doLogin" :loading="logining">登录</el-button>
      <!-- <el-button @click.native.prevent="doReset">重置</el-button> -->
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data() {
    return {
      logining: false,
      loginForm: {
        username: 'admin',
        password: '123456'
      },
      loginFormRule: {
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' },
          //{ validator: validaeUsername }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          //{ validator: validaePassword }
        ]
      },
      checked: true
    };
  },
  methods: {
    doReset() {
      this.$refs.loginForm.resetFields();
    },
    doLogin(ev) {
      this.$refs.loginFormRule.validate((valid) => {
        if (valid) {
          this.logining = true;
          this.$http.get('/user/token')
            .then(resp => {
              this.logining = false;
              this.$router.push({ path: '/home' });
            })
          // var loginParams = { username: this.loginForm.username, password: this.loginForm.password };
          // // 登录
          // this.$http.post('/api/login', loginParams)
          //   .then(resp => {
          //     this.logining = false;
          //     let { code, msg, user } = resp.data;
          //     if (code !== 200) {
          //       this.$message({
          //         message: msg,
          //         type: 'error',
          //         duration: 1000
          //       });
          //     } else {
          //       sessionStorage.setItem('user', JSON.stringify(user));
          //       this.$router.push({ path: '/home' });
          //     }
          //   });
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    }
  }
}

</script>

<style lang="less" scoped>
.login-container {
  // box-shadow: 0 0px 8px 0 rgba(0, 0, 0, 0.06), 0 1px 0px 0 rgba(0, 0, 0, 0.02);
  -webkit-border-radius: 5px;
  border-radius: 5px;
  -moz-border-radius: 5px;
  background-clip: padding-box;
  margin: 180px auto;
  width: 350px;
  padding: 35px 35px 15px 35px;
  background: #fff;
  border: 1px solid #eaeaea;
  box-shadow: 0 0 25px #cac6c6;
  .title {
    margin: 0px auto 40px auto;
    text-align: center;
    color: #505458;
  }
  .remember {
    margin: 0px 0px 35px 0px;
  }
}
</style>