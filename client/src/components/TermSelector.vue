<template>
  <ol class="terms-ol">
    <li :class="{ 'term-li':true, 'selected':selected_term=='long_term' }" 
        @click="selectTerm('long_term')">
        Long
        Term
        <hr v-if="selected_term=='long_term'"/>
    </li>
    <li :class="{ 'term-li':true, 'selected':selected_term=='medium_term' }" 
        @click="selectTerm('medium_term')">
        Medium
        Term
        <hr v-if="selected_term=='medium_term'"/>
    </li>
    <li :class="{ 'term-li':true, 'selected':selected_term=='short_term' }" 
        @click="selectTerm('short_term')">
        Short
        Term
        <hr v-if="selected_term=='short_term'"/>
    </li>
  </ol>
</template>

<script>
export default {
  name: 'ArtistNetwork',
  props: ["selected_term"],
  methods:{
    selectTerm(term) {
      this.$emit("select",term)
    }
  }
}
</script>

<style scoped lang="scss">
.terms-ol {
  font-family: 'Lato', sans-serif;
  text-transform: uppercase;
  display:flex;
  width:100%;
  flex-wrap: nowrap;
  overflow-x:auto;
  .term-li {
    flex-grow:1;
    padding: 0 $spacer*2;
    color: $magenta-l;
    text-shadow: 0px 0px 15px $magenta-d;
    &.selected {
      color: $cyan-l;
      text-shadow: 0px 0px 15px $cyan-d;
    }
    white-space:pre-line;
    @media(min-width:$breakpoint-width) {
      white-space: normal;
    }
  }
}
</style>
