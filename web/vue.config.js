module.exports = {
  publicPath: './' ,
  devServer: {
    host: 'localhost', // can be overwritten by process.env.HOST
    https: false, // 开启https
    port: 8081, // can be overwritten by process.env.PORT, if port is in use, a free one will be determined
    proxy: {   
      '/listTables': {
        target: 'http://192.168.0.9:8080',
        changeOrigin: true ,
        proxyTimeout: 30 * 60 * 10000 ,
        timeout: 30 * 60 * 10000
      } ,
      '/init': {
        target: 'http://192.168.0.9:8080',
        changeOrigin: true ,
        proxyTimeout: 30 * 60 * 10000 ,
        timeout: 30 * 60 * 10000
      } ,
      '/chat': {
        target: 'http://192.168.0.9:8080',
        changeOrigin: true ,
        proxyTimeout: 30 * 60 * 10000 ,
        timeout: 30 * 60 * 10000
      } ,
      
    }
  }
}