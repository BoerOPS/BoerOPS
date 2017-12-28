<template>
<el-container>
  <el-table
    v-loading="loading"
    :data="allProject"
    height="600"
    max-height="800"
    stripe
    border
    :default-sort = "{prop: 'id', order: 'descending'}"
    style="width: 100%">
    <el-table-column
      prop="project_id"
      sortable
      label="ID"
      width="60">
    </el-table-column>
    <el-table-column
      prop="name"
      label="项目名称"
      width="320">
    </el-table-column>
    <el-table-column
      label="操作"
      width="160">
      <template slot-scope="deploy">
        <el-button @click="deployProject(deploy.row)" type="primary" size="mini">部署</el-button>
        <el-button @click="delProject(deploy.row)" type="danger" size="mini">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-dialog title="发布版本"
    :visible.sync="deployProjectVisible"
    v-loading="loading"
    width="30%">
    <!-- 选择提交 -->
    <el-container style="padding:20px 5px;border: 1px solid gray;border-radius:5px">
      <el-form ref="form" :model="deployData" label-width="80px">
        <el-form-item label="选择版本">
          <el-cascader
            :options="preBranchCommites"
            v-model="deployData.commit">
            <!-- @change="selectCommit" -->
          </el-cascader>
        </el-form-item>
        <el-form-item label="提测/上线">
          <el-switch v-model="deployData.env"></el-switch>
        </el-form-item>
        <el-form-item label="版本说明">
          <el-input
          type="textarea"
          placeholder="版本说明"
          v-model="deployData.version_intro"
          :rows="5"
          >
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="success" size="mini">multi</el-button>
          <el-button v-if="deployData.env" type="danger" @click="createDeploy">上线</el-button>
          <el-button v-else type="primary" @click="createDeploy">提测</el-button>
          <el-button
            @click="deployProjectVisible=false,
            deployData={},
            preBranchCommites=[]">
            取消
          </el-button>
        </el-form-item>
      </el-form>
    </el-container>
  </el-dialog>
</el-container>
</template>
<script>
export default {
  name: "Deploy",
  data() {
    return {
      loading: false,
      project: 0,
      allProject: [],
      deployProjectVisible: false,
      preBranchCommites: [],
      deployData: {
        commit: [],
        env: 0
      },
      currentUser: null
    };
  },
  created() {},
  mounted() {
    this.allDeployProject();
    this.getCurrentUser();
  },
  computed: {},
  methods: {
    getCurrentUser() {
      this.$http.get("/currentuser").then(resp => {
        // console.log(resp.data);
        this.currentUser = resp.data["id"];
      });
    },
    createDeploy() {
      var loadingText;
      var loading
      this.$http.get("/joke").then(resp => {
        console.log(resp.data.joke);
        loadingText = resp.data.joke;
      });
      setTimeout(() => {
        loading = this.$loading({
          lock: true,
          // text: 'Loading',
          text: loadingText,
          spinner: "el-icon-loading",
          background: "rgba(0, 0, 0, 0.7)"
        });
      }, 2000);
      this.deployProjectVisible = false;
      this.$message({
        dangerouslyUseHTMLString: true,
        type: "warning",
        message: "<h3>部署请求已发出，部署需要时间，请耐心等待！</h3>",
        center: true
      });
      // this.loading = true;
      this.deployData["current_user"] = this.currentUser;
      this.deployData["project_id"] = this.project;
      console.log(this.deployData);
      this.$http.post("/deploys", this.deployData).then(resp => {
        // this.loading = false;
        loading.close();
        this.$message({
          type: "success",
          message: resp.data
        });
      });
    },
    allDeployProject() {
      this.loading = true;
      this.$http
        .get("/projects", {
          params: {
            ops: true
          }
        })
        .then(resp => {
          // console.log(resp.data);
          this.allProject = resp.data;
          this.loading = false;
        });
    },
    deployProject(row) {
      this.deployData = {};
      this.preBranchCommites = [];
      this.deployProjectVisible = true;
      this.project = row.project_id;
      this.$http
        .get("/commits", {
          params: {
            project_id: row.project_id
          }
        })
        .then(resp => {
          this.preBranchCommites = resp.data;
        });
    },
    delProject(row) {
      this.$message({
        message: "不是你想删就能删！"
      });
    }
  }
};
</script>
<style lang="scss" scoped>

</style>
