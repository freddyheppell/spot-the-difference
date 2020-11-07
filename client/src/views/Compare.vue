<template>
  <div id="compare">
    <h1 class="title">Compare!</h1>
    {{ $route.params }}
  </div>
</template>

<script>
export default {
  name: 'Compare',
  components: {
  },
  mounted() {
    console.log(this.$route.params)
  }
}
</script>

<style scoped lang="scss">
#compare {
  padding: $spacer*4;

  display:flex;
  flex-direction: column;
  align-items:center;

  text-align:center;

  >* {
    max-width:100%;
  }

  .title {
    margin-bottom: $spacer*4;
    font-size: $font-size-l;
    @media(min-width:$breakpoint-width) {
      font-size: $font-size-ll;
    }
  }
}
</style>
