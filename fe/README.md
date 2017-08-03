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
> 最开始采用vue-cli的默认写法配置proxyTbale但是发现配置之后，每次run dev之后都无法正常打开连接，需要手动更正一遍地址。
所以后来自己在build/dev-server.js里面自己重新写了个配置。But...配置之后发现无法热刷新...醉，先暂时这么用着。
