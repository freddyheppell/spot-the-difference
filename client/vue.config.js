module.exports = {
  publicPath: '/',
  css: {
    loaderOptions: {
      sass: {
        additionalData: `
        @import "~@/assets/styles/reset.css";
        @import "~@/assets/styles/_vars.scss";
        @import "~@/assets/styles/_mixins.scss";
        @import "~@/assets/styles/_fonts.scss";
        @import "~@/assets/styles/style.scss";        
        `
      }
    }
  }
};