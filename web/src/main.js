import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'           //  ajax请求插件
import VueAxios from 'vue-axios'    //  用户讲axios装到vue脚手架上的工具

// // 自动设置 Webpack 的 publicPath
// (function () {
//   // 1. 查找当前正在执行的脚本（即组件库的主 JS）
//   const scripts = document.getElementsByTagName('script');
//   const currentScript = [].slice.call(scripts).find(script => {
//     return script.src.includes('/datafocus-chart/'); // 替换为你的库名关键词
//   });

//   if (currentScript) {
//     // 2. 提取主 JS 的路径
//     const scriptUrl = new URL(currentScript.src);
//     const basePath = scriptUrl.href.split('/').slice(0, -1).join('/') + '/';
    
//     // 3. 设置 Webpack 动态路径
//     __webpack_public_path__ = basePath;
//   }
// })();


Vue.config.productionTip = false
Vue.use(VueAxios, axios)         //  使用axios插件
// new Vue({
// 	el: '#app' ,
//   components: { App },
//   template: '<App/>',
// })

new Vue({
  render: h => h(App)
}).$mount('#app')      //  挂载到app上