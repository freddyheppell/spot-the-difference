<template>
  <div id="app">
    {{ $route.params }}
    <h1>Login!</h1>
    <LoginForm :sharecode="sharecode"/>
  </div>
</template>

<script>
import LoginForm from '../components/LoginForm.vue'

export default {
  name: 'Login',
  components: {
    LoginForm
  },
  data() {return {
    share_code: null
  }}
}
</script>

<style lang="scss">
</style>
