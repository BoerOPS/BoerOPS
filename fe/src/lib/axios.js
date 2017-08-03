/**
 * Created by 2ue on 2017/8/3.
 */
import Vue from 'vue'
import axios from 'axios'

const instance = axios.create({
  timeout: 30000,
  headers: {
    'Accept': 'application/json'
  }
})

instance.interceptors.request.use(config => {
  return config
}, error => {
  console.log('error==>',error)
  return Promise.reject(error)
})

instance.interceptors.response.use(response => {
  return typeof response.data.code !== 'undefined' ? response.data : {code:response.status,data:response.data}
}, error => {
  Promise.resolve(error.response)
})


Vue.prototype.$https = instance;
