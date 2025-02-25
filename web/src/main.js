import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'           //  ajax请求插件
import VueAxios from 'vue-axios'    //  用户讲axios装到vue脚手架上的工具

Vue.config.productionTip = false
Vue.use(VueAxios, axios)         //  使用axios插件

new Vue({
  render: h => h(App)
}).$mount('#app')      //  挂载到app上