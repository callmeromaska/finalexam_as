const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // Ваш Flask сервер
        changeOrigin: true,
      },
    },
  },
  transpileDependencies: true
})
