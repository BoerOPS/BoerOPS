# fe

> A Vue.js project

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

## 目录结构

``` shell
.
├── ./build
├── ./config
└── ./src
    ├── ./src/assets
    │   ├── ./src/assets/css
    │   ├── ./src/assets/img
    │   ├── ./src/assets/font
    │   └── ...
    ├── ./src/components --- 一些公共组件存放的地方
    │   ├── ./src/components/bottom.vue
    │   ├── ./src/components/menu.vue
    │   ├── ./src/components/header.vue
    │   └── ...
    ├── ./src/lib  --- 一些团队开发或者三方插件库的引用，以及一些配置
    │   ├── ./src/lib/axios.js
    │   ├── ./src/lib/elementUi.js
    │   └── ...
    ├── ./src/modules  --- 页面功能模块
    │   ├── ./src/modules/mod1/...
    │   ├── ./src/modules/mod2/...
    │   ├── ...
    │   └── ./src/modules/index.vue
    ├── ./src/router --- 定义顶层路由，建议各个模块的路由写到对应的模块
    │   └── ./src/router/index.js
    ├── ./src/main.js
    └── ./src/App.vue
```
## 代理配置说明
> 最开始采用`vue-cli`的默认写法配置`proxyTbale`但是发现配置之后，每次`run dev`之后都无法正常打开连接，需要手动更正一遍地址。
所以后来自己在`build/dev-server.js`里面自己重新写了个配置。`But`...配置之后发现无法热刷新...醉，先暂时这么用着。

## axios
> 全局注册到了`vue`原型链上,后期考虑是否对其进行类`jq`的`ajax`封装，以减少学习成本
```javascript
import Vue from 'vue'
import axios from 'axios'

Vue.prototype.$https = axios;
```
## less/sass/...
- 如果需要以上`css`预处理语言，请自行安装对应依赖
- 如果按照·sass·相关依赖失败，请参考[安装node-sass的正确姿势](https://github.com/lmk123/blog/issues/28)

## Tips
- 慎用`style`标签上的`scoped`属性: 在某些情况下会导致你无法修改三方组件的样式
