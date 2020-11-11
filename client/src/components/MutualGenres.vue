<template>
  <div class="container">
    <h2 class="title">Mutual Genres</h2>
    <ol class="key">
      <li class="display-name-1">{{ display_name_1 }}</li>
      |
      <li class="display-name-2">{{ display_name_2 }}</li>
    </ol>
    <p class="desc">Up to 10 genres you have in common.</p>
    <div v-if="stats.common_genres.length == 0" class="err">
      You don't have any genres in common! :(
    </div>
    <ol v-else class="genres-ol">
      <li v-for="genre of stats.common_genres" :key="genre.name" 
          class="genres-li">
          {{ genre.name }}
          <div class="freqs">
            <span class="freq-1">{{ genre[display_name_1].frequency + (genre[display_name_1].frequency > 1 ? ' artists' : ' artist')}} |</span>
            <span class="freq-2">| {{ genre[display_name_2].frequency + (genre[display_name_2].frequency > 1 ? ' artists' : ' artist')}}</span>
          </div>
          <div class="bars-cont">
            <hr class="bar-1" 
                :style="{ width: 50*genre[display_name_1].frequency/stats.max_frequency + '%' }"/>
            <hr class="bar-2 alt" 
                :style="{ width: 50*genre[display_name_2].frequency/stats.max_frequency + '%' }"/>
          </div>
      </li>
    </ol>
  </div>
</template>

<script>
export default {
  name: 'MutualGenres',
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
            genre_frequencies[genre][this.display_name_1].frequency += 1
          } else {
            genre_frequencies[genre] = { name: genre }
            genre_frequencies[genre][this.display_name_1] = { frequency: 1 }
            genre_frequencies[genre][this.display_name_2] = { frequency: 0 }
          }
        }
      }
      for (artist of this.artists_2_raw) {
        for (genre of artist.genres) {
          if (genre_frequencies[genre]) {
            genre_frequencies[genre][this.display_name_2].frequency += 1
          } else {
            genre_frequencies[genre] = { name: genre }
            genre_frequencies[genre][this.display_name_1] = { frequency: 0 }
            genre_frequencies[genre][this.display_name_2] = { frequency: 1 }
          }
        }
      }

      /**
       * Scoring the genres based upon the product of the normalised 
       * frequencies in each user's artists sample.
       */
      for (genre of Object.values(genre_frequencies)) {
        genre_frequencies[genre.name].score = 
          genre[this.display_name_1].frequency
          * genre[this.display_name_2].frequency
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
            curr_genre[this.display_name_1].frequency 
            > curr_genre[this.display_name_2].frequency
            ? curr_genre[this.display_name_1].frequency
            : curr_genre[this.display_name_2].frequency
          return curr_freq > prev_freq ? curr_freq : prev_freq
        }, 0
      )

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
    .display-name-1 { @include sansUpper(); }  
    .display-name-2 { @include sansUpperAlt(); }  
  }
  .err {
    @include sansUpperAlt();
    text-align: center;
    margin-top: $spacer*3;
    margin-bottom: $spacer*6;
  }
  .genres-ol {
    margin-top: $spacer*3;
    margin-bottom: $spacer*4;
    padding: 0 $spacer*4;
    line-height:1;
    display:flex;
    flex-direction: column;
    align-items: stretch;
    .genres-li {
      text-align:center;
      margin: $spacer 0;
      .freq-1, .freq-2 {
        display:inline-block;
        width:50%;
      }
      .freq-1 {
        text-align:right;
        @include sansLower();
      }
      .freq-2 {
        text-align:left;
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