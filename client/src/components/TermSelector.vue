<template>
  <ol class="terms-ol">
    <li v-for="term of [{ val:'short_term', display:'Short \nTerm' },
                        { val:'medium_term', display:'Medium \nTerm' },
                        { val:'long_term', display:'Long \nTerm' }]" 
        :key="term.val"
        :class="{ 'term-li':true, 'selected':selected_term==term.val }" 
        @click="selectTerm(term.val)">
        {{ term.display }}
        <hr v-if="selected_term==term.val" class="alt"/>
    </li>
  </ol>
</template>

<script>
export default {
  name: 'TermSelector',
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
