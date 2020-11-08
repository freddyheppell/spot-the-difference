<template>
  <div id="app">
    <router-view class="view"/>
  </div>
</template>

<style lang="scss">
#app {
  background-image: url("/assets/backgrounds/sean-foley-0JD7kvxAq0Y-unsplash.jpg");
  background-size: cover;
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
