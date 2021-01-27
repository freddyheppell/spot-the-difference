<template>
  <ol class="terms-ol">
    <li v-for="term of [{ val:'long_term', display:'Long \nTerm' },
                        { val:'medium_term', display:'Medium \nTerm' },
                        { val:'short_term', display:'Short \nTerm' }]" 
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
  mounted(){
      this.$gtag.event("success",{
        "event_category":"Term Selector",
        "event_label":"Selected term set to: " + this.selected_term,
      })
  },
  methods:{
    selectTerm(term) {
      this.$gtag.event("success",{
        "event_category":"Term Selector",
        "event_label":"Selected term set to: " + term,
      })
      this.$emit("select",term)
    }
  }
}
</script>

<style scoped lang="scss">
.terms-ol {
  width:100%;

  display:flex;
  flex-wrap: nowrap;

  .term-li {
    padding: 0 $spacer*2;
    flex-grow:1;

    @include sansUpper();
    &.selected {
      @include glowTextAlt();
    }

    text-align: center;

    white-space:pre-line;
    @media(min-width:$breakpoint-width) {
      white-space: normal;
    }
  }
}
</style>
