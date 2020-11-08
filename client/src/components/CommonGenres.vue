<template>
  <div class="container">
    <h1 class="title">Genres</h1>
    <ol class="key">
      <li class="display-name-1">{{ display_name_1 }}</li>
      <li class="both">Both</li>
      <li class="display-name-2">{{ display_name_2 }}</li>
    </ol>
    <p class="desc">Up to 50 genres you might share in common.</p>
    <ol class="genres-ol">
      <li :class="{ 'genres-li':true, 
                    'user1':genre[display_name_1], 
                    'user2':genre[display_name_2],
                    'both':genre[display_name_1]&&genre[display_name_2] }" 
          v-for="genre of genres" :key="genre.name"
          >{{ genre.name }}</li>
    </ol>
    <hr class="alt">
  </div>
</template>

<script>
export default {
  name: 'CommonGenres',
  props: ["artists_1_raw", "artists_2_raw", "display_name_1", "display_name_2"],
  computed:{
    genres() {
      var genres = {}
      var denoms = {}
      denoms[this.display_name_1]=0
      denoms[this.display_name_2]=0
      
      for (var artist of this.artists_1_raw) {
        for (var genre of artist.genres) {
          if (genres[genre]) {
            genres[genre][this.display_name_1] += 1
          } else {
            genres[genre] = { name: genre }
            genres[genre][this.display_name_1] = 1
            genres[genre][this.display_name_2] = 0
          }
          denoms[this.display_name_1] += 1
        }
      }

      for (artist of this.artists_2_raw) {
        for (genre of artist.genres) {
          if (genres[genre]) {
            genres[genre][this.display_name_2] += 1
          } else {
            genres[genre] = { name: genre }
            genres[genre][this.display_name_1] = 0
            genres[genre][this.display_name_2] = 1
          }
          denoms[this.display_name_2] += 1
        }
      }

      for (genre in genres) {
        if (genres[genre][this.display_name_1]) {
          genres[genre][this.display_name_1] = genres[genre][this.display_name_1]/denoms[this.display_name_1]
        }
        if (genres[genre][this.display_name_2]) {
          genres[genre][this.display_name_2] = genres[genre][this.display_name_2]/denoms[this.display_name_2]
        }
      }
      
      return Object.values(genres).sort(
        (a, b) => { return (b[this.display_name_1]+b[this.display_name_2])
                          -(a[this.display_name_1]+a[this.display_name_2])}
                          ).slice(0,50)
    },
  }
}
</script>

<style scoped lang="scss">
.container {
  .title {
    text-align:left;
    font-size: $font-size-m;
    @media(min-width:$breakpoint-width) {
      font-size: $font-size-l;
    }
  }
  .key {
    font-family: 'Lato', sans-serif;
    font-weight:700;

    text-align:left;
    text-transform: uppercase;

    >*{ display:inline-block }
    :first-child::after {content:"|"}
    :last-child::before {content:"|"}

    .display-name-1 {
      text-shadow: 0px 0px 20px $magenta-d;
      color: $magenta-l;    
    }  
    .display-name-2 {
      text-shadow: 0px 0px 20px $cyan-d;
      color: $cyan-l;    
    }  
  }
  .desc {
    text-align:left;
  }
  .genres-ol {
    padding-top: $spacer*2;

    text-align:left;

    .genres-li {
      display: inline;
      &.user1 {
        text-shadow: 0px 0px 20px $magenta-d;
        color: $magenta-l;
      }
      &.user2 {
        text-shadow: 0px 0px 20px $cyan-d;
        color: $cyan-l;
      }
      &.both {
        text-shadow: 0px 0px 20px $white;
        color: $white;
      }
      &::after {
        content:", "
      }
      &:last-child {
        &::after {
          content:""
        }
      }
    }
  }
}
</style>
