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
  display:flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: center;
  &::before {
    content:"";
    position:absolute;
    top:0;right:0;
    width:100%;height:100%;
    background: rgba(0,0,0,0.7);
  }
  .view {
    z-index: 1;
    height:100%;
  }
}
</style>
