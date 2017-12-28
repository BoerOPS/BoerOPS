<template>
  <div>
    <el-container>
      <el-table
          v-loading="loading"
          :data="allHost.hosts"
          height="600"
          max-height="800"
          stripe
          border
          :default-sort = "{prop: 'id', order: 'descending'}"
          style="width: 100%">
          <el-table-column
            prop="id"
            sortable
            label="ID"
            width="60">
          </el-table-column>
          <el-table-column
            prop="ip_addr"
            label="IP地址"
            width="160">
          </el-table-column>
          <el-table-column
            prop="env"
            label="所属环境"
            width="160">
            <el-tag
              slot-scope="scope"
              :type="scope.row.env === 1 ? 'primary' : 'danger'">
              {{scope.row.env === 1 ? '测试' : '生产'}}
            </el-tag>
          </el-table-column>
      </el-table>
    </el-container>
    <el-button @click="createHostVisible=true, host={}" type="primary">添加主机</el-button>
    <el-button @click="$router.push({name: 'Home'})" type="info">Home</el-button>
    <el-dialog title="添加主机"
      :visible.sync="createHostVisible"
      v-loading="loading"
      width="30%">
      <el-form ref="form" :model="host" label-width="80px">
        <el-form-item label="IP地址">
          <el-input v-model="host.ip_addr"></el-input>
        </el-form-item>
        <el-form-item label="测试/生产">
          <el-switch v-model="host.env"></el-switch>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="createHost">添加</el-button>
          <el-button @click="createHostVisible = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
<script>
export default {
  name: "Host",
  data() {
    return {
      loading: false,
      allHost: {},
      createHostVisible: false,
      host: {}
    };
  },
  filters: {},
  created() {},
  mounted() {
    this.getAllHost();
  },
  computed: {},
  methods: {
    getAllHost() {
      this.loading = true;
      this.$http.get("/api/hosts").then(resp => {
        this.allHost = resp.data;
        this.loading = false;
      });
    },
    createHost() {
      this.$http.post("/api/hosts", this.host).then(resp => {
        this.createHostVisible = false;
        this.$message({
          showClose: true,
          message: resp.data,
          type: "success"
        });
        this.getAllHost();
      });
    }
  }
};
</script>
<style lang="scss" scoped>

</style>
