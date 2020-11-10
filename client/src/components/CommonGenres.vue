<template>
  <div class="container">
    <h2 class="title">Genres</h2>
    <ol class="key">
      <li class="display-name-1">{{ display_name_1 }}</li>
      <li class="both">Both</li>
      <li class="display-name-2">{{ display_name_2 }}</li>
    </ol>
    <p class="desc">Up to 10 genres you have in common.</p>
    <ol class="genres-ol">
      <li v-for="genre of stats.common_genres" :key="genre.name" 
          class="genres-li">
          <span class="freq-1">{{ genre[display_name_1] + (genre[display_name_1] > 1 ? ' artists' : ' artist')}} |</span>
          {{ genre.name }}
          <span class="freq-2">| {{ genre[display_name_2] + (genre[display_name_2] > 1 ? ' artists' : ' artist')}}</span>
          <div class="bars-cont">
            <hr class="bar-1" 
                :style="{ width: 50*genre[display_name_1]/stats.max_frequency + '%' }"/>
            <hr class="bar-2 alt" 
                :style="{ width: 50*genre[display_name_2]/stats.max_frequency + '%' }"/>
          </div>
      </li>
    </ol>
  </div>
</template>

<script>
export default {
  name: 'CommonGenres',
  props: ["artists_1_raw", "artists_2_raw", "display_name_1", "display_name_2"],
  computed:{
    stats() {
      var genre_frequencies = {}
      
      /**
       * Counting up all the frequencies of each tag on each users' artists
       */
      for (var artist of this.artists_1_raw) {
        for (var genre of artist.genres) {
          if (genre_frequencies[genre]) {
            genre_frequencies[genre][this.display_name_1] += 1
          } else {
            genre_frequencies[genre] = { name: genre }
            genre_frequencies[genre][this.display_name_1] = 1
            genre_frequencies[genre][this.display_name_2] = 0
          }
        }
      }
      for (artist of this.artists_2_raw) {
        for (genre of artist.genres) {
          if (genre_frequencies[genre]) {
            genre_frequencies[genre][this.display_name_2] += 1
          } else {
            genre_frequencies[genre] = { name: genre }
            genre_frequencies[genre][this.display_name_1] = 0
            genre_frequencies[genre][this.display_name_2] = 1
          }
        }
      }

      /**
       * Scoring the genres based upon the product of the frequencies in each
       * user's artists sample.
       */
      for (genre of Object.values(genre_frequencies)) {
        genre_frequencies[genre.name].score = genre[this.display_name_1]
                                              * genre[this.display_name_2]
      }

      //Filtering down to the top 10 genres the users have in common
      var common_genres = Object.values(genre_frequencies)
                                .filter(g => g.score > 0)
                                .sort((a,b) => b.score-a.score)
                                .slice(0,10)

      //Finding the maximum frequency on any common genre on any artist
      var max_frequency = common_genres.reduce(
        (prev_freq, curr_genre) => {
          var curr_freq = 
            curr_genre[this.display_name_1] > curr_genre[this.display_name_2]
            ? curr_genre[this.display_name_1]
            : curr_genre[this.display_name_2]
          return curr_freq > prev_freq ? curr_freq : prev_freq
        }, 0
      )

      console.log(genre_frequencies, max_frequency)

      return {
        common_genres: common_genres,
        max_frequency: max_frequency
      }
    },
  }
}
</script>

<style scoped lang="scss">
.container {
  .key {
    margin-top:$spacer*1.5;
    @include sansUpperWhite();
    >*{ display:inline-block }
    :first-child::after {content:"|"}
    :last-child::before {content:"|"}
    .display-name-1 { @include sansUpper(); }  
    .display-name-2 { @include sansUpperAlt(); }  
  }
  .genres-ol {
    display:flex;
    flex-direction: column;
    align-items: stretch;
    margin-top: $spacer*3;
    margin-bottom: $spacer*6;
    .genres-li {
      text-align:center;
      margin: $spacer 0;
      .freq-1 {
        @include sansLower();
      }
      .freq-2 {
        @include sansLowerAlt();
      }
      .bars-cont {
        width:100%;
        height:$spacer*2;
        position:relative;
        .bar-1, .bar-2 {
          margin:0;
          position:absolute;
          bottom:0;
        }
        .bar-1 { right:50%; }
        .bar-2 { left:50%; }
      }
    }
  }  
}
</style>