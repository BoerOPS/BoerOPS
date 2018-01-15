<template>
  <div class="user-message">
    <el-dropdown trigger="click" @command="handleCommand">
      <el-badge :value="userMessages.length + okIncrement" class="el-dropdown-link">
        <el-button size="small">最新消息</el-button>
      </el-badge>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item v-for="m in userMessages" :key="m.id" :command="m.id">{{ m.msg }}</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>
<script>
export default {
  data() {
    return {
      userMessages: []
    };
  },
  props: {
    okIncrement: {
      type: Number,
      default: 0
    }
  },
  mounted: function() {
    debugger;
    this.getMessages();
  },
  methods: {
    handleCommand(command) {
      this.userMessages = this.userMessages.filter(el => el.id != command);
      // this.userMessages.forEach(element => {
      //   if (element.id == command) {
      //     let index = this.userMessages.indexOf(element);
      //     this.userMessages.splice(index, 1);
      //   }
      // });
      this.$message("消息: " + command + " 已标记为已读状态");
      this.$http.patch("/logs/" + command).then(resp => {
        console.log(resp.data, "from components!");
      });
    },
    getMessages() {
      this.$http.get("/logs").then(resp => {
        this.userMessages = resp.data;
      });
    }
  }
};
</script>
<style lang="scss" scoped>

</style>
