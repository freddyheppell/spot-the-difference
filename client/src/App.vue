<template>
  <div id="app" ref="app">
    <router-view class="view"/>
  </div>
</template>

<script>
export default {
  mounted() {
    const backgrounds = [
      "/assets/backgrounds/sean-foley-0JD7kvxAq0Y-unsplash.jpg",
      "/assets/backgrounds/sean-foley-eTTNCwG2Fgw-unsplash.jpg",
      "/assets/backgrounds/sean-foley-qEWEz-U5p8Q-unsplash.jpg",
      "/assets/backgrounds/sean-foley-YWzLb_7MpAg-unsplash.jpg",
      "/assets/backgrounds/sean-foley-1KE-j9H1Chg-unsplash.jpg",
      "/assets/backgrounds/sean-foley-fEWl-Q5vIks-unsplash.jpg",
      "/assets/backgrounds/sean-foley-qwlkNzlDf5I-unsplash.jpg",
      "/assets/backgrounds/sean-foley-z4gWzj0p93c-unsplash.jpg",
      "/assets/backgrounds/sean-foley-3uZ7GI2boJ0-unsplash.jpg",
      "/assets/backgrounds/sean-foley-hErJCi76EhA-unsplash.jpg",
      "/assets/backgrounds/sean-foley-SEfbeMpjxaM-unsplash.jpg",
      "/assets/backgrounds/sean-foley-ZPhMNf0ljjM-unsplash.jpg",
      "/assets/backgrounds/sean-foley-aPDCEoW7B78-unsplash.jpg",
      "/assets/backgrounds/sean-foley-icrpUWv6VR8-unsplash.jpg",
      "/assets/backgrounds/sean-foley-uwYDsDlaJTo-unsplash.jpg",
      "/assets/backgrounds/sean-foley-Bu95Rz43y3o-unsplash.jpg",
      "/assets/backgrounds/sean-foley-mElF6eRHps0-unsplash.jpg",
      "/assets/backgrounds/sean-foley-xZysXBRzlRI-unsplash.jpg",
      "/assets/backgrounds/sean-foley-0JD7kvxAq0Y-unsplash.jpg",
    ]
    this.$refs["app"].style["background-image"] = 
      "url('"+backgrounds[Math.floor(Math.random()*backgrounds.length)]+"')"
    console.log(this.$refs["app"].style)
  }
}
</script>

<style lang="scss">
#app {
  background-image: url("/assets/backgrounds/sean-foley-0JD7kvxAq0Y-unsplash.jpg");
  background-size: cover;
  background-position: center;

  min-height:100%;

  z-index: 0;

  position:relative;

  display:flex;
  justify-content: center;
  align-items: stretch;

  &::before {
    z-index: 1;
    content:"";
    position:absolute;
    top:0;right:0;
    width:100%;height:100%;
    background: rgba(0,0,0,0.7);
  }

  .view {
    position:relative;
    z-index: 2;
    min-height:100%;
  }
}
</style>
