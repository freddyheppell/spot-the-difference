<template>
  <div id="app">
    {{ $route.params }}
    <h1>Compare!</h1>
    Comparing {{ share_codes[0] }} and {{ share_codes[1] }}!
  </div>
</template>

<script>
export default {
  name: 'Compare',
  components: {
  },
  data() {return {
    share_codes: []
  }}
}
</script>

<style lang="scss">
</style>
