<template>
  <div class="project" style="margin-top: 20px;width: 1200px">
    <el-table
      v-loading="loading"
      :data="allProject.projects"
      height="800"
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
        prop="name"
        label="Name"
        width="160">
      </el-table-column>
      <el-table-column
        prop="owner"
        label="Owner"
        width="80">
      </el-table-column>
      <el-table-column
        prop="visibility"
        label="Visibility"
        width="80">
      </el-table-column>
      <el-table-column
        prop="ssh_url_to_repo"
        label="Repo URL"
        width="360">
      </el-table-column>
      <el-table-column
        prop="web_url"
        label="Web URL"
        width="360">
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作"
        width="160">
        <template slot-scope="scope">
          <el-button @click="getDetailInfo(scope.row)" type="info" size="mini">查看</el-button>
          <el-button @click="setProject(scope.row)" type="danger" size="mini">操作</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="block">
      <el-pagination
        layout="prev, pager, next"
        :total="50">
      </el-pagination>
    </div>
    <p>Total: {{ allProject.total }}</p>
    <el-button @click="removeToken">登出</el-button>
    <router-link :to="{name: 'Home'}">
      <el-button>Home</el-button>
    </router-link>

    <el-dialog title="详细信息"
      :visible.sync="detailInfoVisible"
      v-loading="loading"
      width="30">
      <pre>
        <code data-language="javascript">
        {{projectDetailInfo}}
        </code>
      </pre>
    </el-dialog>
    <el-dialog title="项目操作"
      :visible.sync="projectSettings"
      v-loading="loading"
      width="30%">
      <!-- 保护分支 -->
      <el-container style="margin-top:5px;padding:20px 5px;border: 1px solid gray;border-radius:5px">
        <el-select v-model="branch" placeholder="请选择分支">
          <el-option
            v-for="branch in branches"
            :key="branch"
            :label="branch"
            :value="branch">
          </el-option>
        </el-select>
        <el-button @click="protectBranch" type="success" size="small" style="margin-left: 10px">
          <i class="fa fa-lock" aria-hidden="true"></i>
          锁定
        </el-button>
        <el-button @click="unprotectBranch" type="info" size="small" style="margin-left: 10px">
          <i class="fa fa-unlock" aria-hidden="true"></i>
          解锁
        </el-button>
      </el-container>
      <!-- 选择提交 -->
      <el-container style="margin-top:5px;padding:20px 5px;border: 1px solid gray;border-radius:5px">
        <el-cascader
          :options="preBranchCommites"
          v-model="commit"
          @change="selectCommit">
        </el-cascader>
      </el-container>
      <!-- 新建部署 -->
      <el-container style="margin-top:5px;padding:20px 5px;border: 1px solid gray;border-radius:5px">
        <el-button @click="newDeploy" type="danger">
          <i v-if="currentUser === adminNewDeploy" class="fa fa-eye" aria-hidden="true"></i>
          <i v-else class="fa fa-eye-slash" aria-hidden="true"></i>
          新建部署
        </el-button>
        <el-dialog
          width="36%"
          title="新建部署"
          :visible.sync="newDeployVisible"
          append-to-body>
          <el-form ref="form" :model="form" label-width="80px">
            <el-form-item label="项目名称">
              <el-input v-model="form.name"></el-input>
            </el-form-item>
            <el-form-item label="beforeCMD">
              <el-input
              type="textarea"
              placeholder="部署代码前执行的命令 example: rsync/fe complie/chown/tar 每行一条命令"
              v-model="form.beforeCmd"
              :rows="3"
              >
              </el-input>
            </el-form-item>
            <el-form-item label="afterCMD">
              <el-input
              type="textarea"
              placeholder="部署代码后执行的命令 example: restart service"
              v-model="form.afterCmd"
              :rows="3"
              >
              </el-input>
            </el-form-item>

            <el-form-item label="生产主机">
              <el-checkbox-group v-model="form.hosts">
                <el-checkbox v-for="host in prodHosts" :key="host.id" :label="host.id">{{host.ip | shortIP}}</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item label="测试30">
              <el-checkbox-group v-model="form.hosts">
                <el-checkbox v-for="host in test30Hosts" :key="host.id" :label="host.id">{{host.ip | shortIP}}</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item label="测试31">
              <el-checkbox-group v-model="form.hosts">
                <el-checkbox v-for="host in test31Hosts" :key="host.id" :label="host.id">{{host.ip | shortIP}}</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item>
              <el-button @click="newDeployVisible=false">取消</el-button>
              <el-button type="primary" @click="saveDeploy">保存</el-button>
            </el-form-item>
          </el-form>
        </el-dialog>
      </el-container>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "Project",
  data() {
    return {
      form: {
        name: "",
        beforeCmd: "",
        afterCmd: "",
        hosts: []
      },
      prodHosts: [],
      test30Hosts: [],
      test31Hosts: [],
      // Admin User
      adminNewDeploy: "zhanghaibo",
      currentUser: "",
      allProject: {},
      loading: false,
      newDeployVisible: false,
      detailInfoVisible: false,
      projectDetailInfo: {},
      projectSettings: false,
      branches: [],
      // 当前项目 @click setProject()
      project: 0,
      // 当前分支 v-model template el-select
      branch: "",
      operation: "",
      preBranchCommites: [],
      // 当前提交 v-model template el-cascader
      commit: []
    };
  },
  // created、mounted、updated、destroyed
  created: function() {
    this.getAllProject();
    this.getCurrentUser();
  },
  filters: {
    shortIP: function(ip) {
      if (!ip) {
        return false;
      }
      let tmp = ip.split(".");
      return tmp[2] + "." + tmp[3];
    }
  },
  mounted: function() {},
  computed: {},
  methods: {
    getHosts(env) {
      this.$http
        .get("/hosts", {
          params: {
            env: env
          }
        })
        .then(resp => {
          if (env == 1) {
            this.test30Hosts = resp.data;
          } else if (env == 2) {
            this.test31Hosts = resp.data;
          } else {
            this.prodHosts = resp.data;
          }
        });
    },
    getCurrentUser() {
      this.$http.get("/currentuser").then(resp => {
        this.currentUser = resp.data["username"];
      });
    },
    newDeploy() {
      this.form = { hosts: [] };
      if (this.currentUser === this.adminNewDeploy) {
        this.newDeployVisible = true;
        this.getHosts(2);
        this.getHosts(1);
        this.getHosts(0);
        return false;
      }
      this.$message({
        showClose: true,
        message: "你没有此操作权限",
        type: "warning"
      });
    },
    saveDeploy() {
      this.form.project_id = this.project;
      this.$http.post("/projects", this.form).then(resp => {
        this.$message({
          showClose: true,
          message: resp.data,
          type: "success"
        });
        this.$router.push({
          name: "Deploy",
          params: { project_id: this.project }
        });
      });
      this.newDeployVisible = false;
    },
    selectCommit() {
      console.log("项目：", this.project);
      console.log("分支", this.commit[0]);
      console.log("提交", this.commit[1]);
    },
    protectBranch() {
      this.operation = "protect";
      this.operationBranch();
    },
    unprotectBranch() {
      this.operation = "unprotect";
      this.operationBranch();
    },
    operationBranch() {
      this.$confirm("确认此操作吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          // "/branches/1?project_id=123"
          this.$http
            .patch("/branches/" + this.branch, {
              project_id: this.project,
              operation: this.operation
            })
            .then(resp => {
              this.projectSettings = false;
              this.$message({
                showClose: true,
                message: resp.data,
                type: "success"
              });
            });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    },
    getDetailInfo(row) {
      this.loading = true;
      this.detailInfoVisible = true;
      this.$http.get("/projects/" + row.id).then(resp => {
        this.projectDetailInfo = resp.data;
        this.loading = false;
      });
    },
    setProject(row) {
      this.loading = true;
      this.projectSettings = true;
      this.project = row.id;
      this.branch = "";
      this.$http
        .get("/branches", {
          params: {
            project_id: row.id
          }
        })
        .then(resp => {
          this.branches = resp.data;
          this.loading = false;
        });
      this.$http
        .get("/commits", {
          params: {
            project_id: row.id
          }
        })
        .then(resp => {
          this.preBranchCommites = resp.data;
        });
    },
    removeToken() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("created_at");
      this.$router.push({ name: "Login" });
    },
    getAllProject() {
      this.loading = true;
      this.$http
        .get("/projects")
        .then(resp => {
          this.allProject = resp.data;
          this.loading = false;
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

pre {
  font-family: Consolas, "Liberation Mono", Courier, monospace;
  font-size: 13px;
  color: #333;
  border: 1px solid #ccc;
  word-wrap: break-word;
  padding: 6px 10px;
  margin: 0;
  line-height: 19px;
  min-height: 200px;
  background-color: #f5f5f5;
  border-radius: 4px;
  max-width: 100%;
  white-space: pre-wrap;
  position: relative;
  overflow: hidden;
  code {
    word-wrap: break-word;
    word-break: normal;
    text-align: left;
    max-width: 100%;
    border: 0;
    padding: 0;
    margin: 0;
    font-family: Consolas, "Liberation Mono", Courier, monospace;
    color: #333;
    float: left;
  }
}
</style>
