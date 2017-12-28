<template>
  <div class="login">
    <img src="../assets/plastic_pet_dog.jpg">
    <el-button
      class="button is-success"
      v-if="refreshed"
      @click="getAccessToken"
      v-loading="loading">
      <strong style="font-size: 18px">登录</strong> with gitlab
    </el-button>
    <el-button
      class="button is-primary"
      v-else
      type="primary"
      icon="el-icon-arrow-right"
      onclick="window.location.href='/auth/login'">
      <strong style="font-size: 18px">登录</strong> with gitlab
    </el-button>
  </div>
</template>
<script>
export default {
  name: "Login",
  data() {
    return {
      msg: "Login in with gitlab.",
      refreshed: localStorage.getItem("refresh_token"),
      loading: false,
      activator: false
    };
  },
  //created、mounted、updated、destroyed
  created: function() {
    if (JSON.stringify(this.$route.query) !== "{}") {
      let data = this.$route.query;
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      localStorage.setItem("created_at", data.created_at);
      localStorage.setItem("scope", data.scope);
      localStorage.setItem("token_type", data.token_type);
      this.$router.push({ name: "Home" });
    }
  },
  mounted: function() {},
  computed: {
    now: function() {
      return Date.now();
    }
  },
  methods: {
    getBurger() {
      this.activator = !this.activator;
      return this.activator;
    },
    promptMsg(msg) {
      this.$message({
        message: msg,
        // center: true,
        showClose: true,
        type: "error"
      });
    },
    getAccessToken() {
      this.loading = true;
      setTimeout(() => {
        this.loading = false;
      }, 8000);
      var _this = this;
      let refresh_token = localStorage.getItem("refresh_token");
      let scope = localStorage.getItem("scope");
      if (
        !refresh_token ||
        refresh_token === "undefined" ||
        refresh_token === "null"
      ) {
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("scope");
        this.loading = false;
        this.$router.push({ name: "Login" });
        return false;
      }
      this.$http
        .get("/oauth2/welcome", {
          params: {
            refresh_token: refresh_token,
            scope: scope
          }
        })
        .then(resp => {
          let data = resp.data;
          if (data.error === "invalid_grant") {
            localStorage.removeItem("refresh_token");
            localStorage.removeItem("scope");
            localStorage.removeItem("token_type");
            this.refreshed = false;
            this.loading = false;
            this.promptMsg(data.error_description);
            return false;
          }
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("refresh_token", data.refresh_token);
          localStorage.setItem("created_at", data.created_at);
          localStorage.setItem("scope", data.scope);
          localStorage.setItem("token_type", data.token_type);
          this.$router.push({ name: "Home" });
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
