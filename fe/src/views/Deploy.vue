<template>
<div>
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
          <el-radio-group v-model="deployData.env" size="small">
            <el-radio-button :label="1" >30测试</el-radio-button>
            <el-radio-button :label="2">31测试</el-radio-button>
            <el-radio-button :label="0">线上</el-radio-button>
          </el-radio-group>
          <!-- <el-switch v-model="deployData.env"></el-switch> -->
        </el-form-item>
        <el-form-item label="重启服务">
          <el-switch v-model="deployData.service"></el-switch>
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
        <el-form-item label="相关人员">
          <el-checkbox-group v-model="deployData.members">
            <el-checkbox v-for="m in allMembers" :key="m.email" :label="m.email">{{m.name}}</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item>
          <!-- <el-button type="success" size="mini">multi</el-button> -->
          <el-button v-if="deployData.env == 0" type="danger" @click="createDeploy">上线</el-button>
          <el-button v-else type="primary" @click="createDeploy">提测</el-button>
          <el-button @click="cancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-container>
  </el-dialog>
</el-container>
<user-message ref="userMsg"></user-message>
</div>
</template>
<script>
import userMessage from "@/components/userMessage";
const DEFAULT = {
  commit: [],
  env: 1,
  members: []
};
export default {
  name: "Deploy",
  data() {
    return {
      loading: false,
      project: 0,
      allProject: [],
      deployProjectVisible: false,
      preBranchCommites: [],
      deployData: { ...DEFAULT },
      currentUser: null,
      allMembers: []
    };
  },
  components: {
    userMessage
  },
  created() {},
  mounted() {
    this.allDeployProject();
    this.getCurrentUser();
  },
  sockets: {
    // connect(msg) {
    //   // console.log(msg);
    //   this.$socket.emit("my_event", { data: "wo lianjiedao le !" });
    // },
    my_response(msg) {
      var _this = this;
      console.log(msg.data);
      let msg_data = JSON.parse(msg.data);
      if (msg_data.msg.endsWith("部署成功")) {
        _this.$refs.userMsg.userMessages.push(msg_data);
      }
    }
  },
  computed: {},
  methods: {
    getMessages() {
      this.$http.get("/logs").then(resp => {
        this.userMessages = resp.data;
      });
    },
    cancel() {
      this.deployProjectVisible = false;
      this.deployData = { ...DEFAULT };
      this.preBranchCommites = [];
    },
    projectMembers(project) {
      this.$http
        .get("/projects/" + project, {
          params: {
            members: "all"
          }
        })
        .then(resp => {
          this.allMembers = resp.data;
          console.log(resp.data);
        });
    },
    getCurrentUser() {
      this.$http.get("/currentuser").then(resp => {
        this.currentUser = resp.data["id"];
      });
    },
    createDeploy() {
      this.$http.get("/joke").then(resp => {
        console.log(resp.data.joke);
      });
      this.deployProjectVisible = false;
      this.$message({
        dangerouslyUseHTMLString: true,
        type: "warning",
        message: "<h3>部署请求已发出，部署需要时间，请耐心等待！</h3><p>太无聊，可以打开console看个笑话哟！</p>"
        // center: true
      });
      this.deployData["current_user"] = this.currentUser;
      this.deployData["project_id"] = this.project;
      this.$http.post("/deploys", this.deployData).then(resp => {
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
      this.deployData = { ...DEFAULT };
      this.preBranchCommites = [];
      this.deployProjectVisible = true;
      this.project = row.project_id;
      this.projectMembers(row.project_id);
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
.el-checkbox + .el-checkbox {
  margin: 0;
}
.el-checkbox-group {
  text-align: left;
}
.el-checkbox {
  display: inline-block;
  width: 25%;
  box-sizing: border-box;
}
</style>
