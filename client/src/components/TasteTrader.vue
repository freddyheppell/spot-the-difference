<template>
  <div class="container">
    <h1 class="title">Taste Trader</h1>
    <p class="desc">
      Something for {{ display_name_1 }} from 
      {{ display_name_2 + (display_name_2.slice(-1) === "s" ? "'" : "'s") }} 
      library & vice versa.
    </p>

    <div class="grid">
      <div class="avatar-cont-cont" id="avatar1">
        <div class="avatar-cont">
          <img class="avatar" :src="avatar_1"/>
        </div>
      </div>
      <div class="avatar-cont-cont" id="avatar2">
        <div class="avatar-cont">
          <img class="avatar" :src="avatar_2"/>
        </div>
      </div>
      <div class="rec" id="rec1">
        <hr>
        <span>
          {{ display_name_1 }} Probably Likes: 
          <span class="rec-title">
            {{ 
              recommendation_1.name +
              (recommendation_1.top_track 
                 ? " - " + recommendation_1.top_track.name 
                 : ""
              )
            }}
          </span>
          <ul class="matching-genres-ul">
            <li class="matching-genres-li"
                v-for="genre of recommendation_1.genres" :key="genre">
                {{ genre }}</li>
          </ul>
        </span>
        <hr>
      </div>
      <div class="rec" id="rec2">
        <hr>
        <span>
          {{ display_name_2 }} Probably Likes: 
          <span class="rec-title">
            {{ 
              recommendation_2.name +
              (recommendation_2.top_track 
                 ? " - " + recommendation_2.top_track.name 
                 : ""
              )
            }}
          </span>
          <ul class="matching-genres-ul">
            <li class="matching-genres-li"
                v-for="genre of recommendation_2.genres" :key="genre">
                {{ genre }}</li>
          </ul>
        </span>
        <hr>
      </div>
    </div>

    <hr class="alt">
  </div>
</template>

<script>
export default {
  name: 'TasteTrader',
  props: ["artists_1_raw", "artists_2_raw", "tracks_1_raw", "tracks_2_raw", "display_name_1", "display_name_2", "avatar_1", "avatar_2"],
  computed:{
    recommendation_1() {
      return this.recommendation_for_user(this.display_name_1)
    },
    recommendation_2() {
      return this.recommendation_for_user(this.display_name_2)
    }
  },
  methods:{
    recommendation_for_user(display_name) {
      /** 
       * Performing TF.IDF ranking. The query is the union of all the genres 
       * used on the artists in the user's artists sample. The documents are 
       * all the artists in the other user's artists sample that have tracks
       * in their top tracks.
      */
      var genres_query = {}
      for (var artist of display_name == this.display_name_1 
                         ? this.artists_1_raw : this.artists_2_raw) {
        for (var genre of artist.genres) {
          genres_query[genre] = genres_query[genre] ? genres_query[genre]+1 : 1
        }
      }
      /**
       * Because the "term frequencies" in this kind of query are going to look
       * more like this:
       *  | .                  we need to   | 
       *  | .                  take their   |
       *  |  .                 logarithms   | 
       *  |   ..               instead so   |
       *  |     ...            they look    | ......
       *  |        ....        like this -> |       ......
       *  |            .....   (linear)     |             ......
       *  +-------------------              +-------------------
       * because otherwise the genre "pop" is probably going to have a weight of
       * shinty-six billion while other more niche genres that express the 
       * subtle differences in people's tastes will have a weight of 1 and be
       * practically insignificant.
       */
      for (genre of Object.keys(genres_query)) {
        genres_query[genre] = Math.log(genres_query[genre]+Math.E)
      }

      var artists = {}
      /** 
       * Iterating over all the artists and adding them to the artists object if
       * they have genres associated them them. 
      */
      for (artist of display_name == this.display_name_1
                     ? this.artists_2_raw : this.artists_1_raw) {
        if (artist.genres.length > 0) {
          artists[artist.name] = { name: artist.name, genres: artist.genres }
        }
      }

      var iafs = {} //Inverse Artist FrequencieS
      for (artist of Object.values(artists)) {
        for (genre of artist.genres) {
          iafs[genre] = iafs[genre] ? iafs[genre]+1 : 1
        }
      }
      for (genre in iafs) {
        iafs[genre] = 1/iafs[genre]
      }

      /**
       * We can now work out the cosine distances (ommitting the constant in 
       * the denominator from the query term frequencies)
       *     sqrt(sum(qf.iafs x af.iafs))
       *    ------------------------------
       *         sqrt(sum(af.idfs))
       * I've slightly modified this to take into account the number of common
       * genres between the query and the artist. Essentially, it's scaled 
       * logarithmically such that having three common genres doubles the score
       * over simply having one common genre.
       */
      const genres_to_double = 2
      for (artist of Object.keys(artists)) {
        artists[artist].score = 0
        var common_genres = 0
        for (genre of artists[artist].genres) {
          if (iafs[genre] && genres_query[genre]) {
            common_genres += 1
            artists[artist].score += 
              (genres_query[genre]*iafs[genre])
              * (1*iafs[genre]) //The genre frequencies on artists are always 1
          }
        }
        artists[artist].score = 
          (Math.sqrt(artists[artist].score)
          / Math.sqrt(
            artists[artist].genres.map(g => (1*iafs[g])**2)
                                  .reduce((a,b) => a+b, 0)
            )   // This does the funky scaling so an artist with 1 genre will be
          ) * ( // multiplied by 1 while an artist with genres_to_double+1 will 
            (   // be multiplied by 2:
              Math.log(( 
                  ((Math.E-1)*(common_genres-1))
                  /genres_to_double
                ) + 1)
            ) + 1
          )
      }

      //Determining which artists the users have in common in their top artists
      for (artist of Object.keys(artists)) {
        artists[artist].new = true
      }
      for (artist of display_name == this.display_name_1 
                     ? this.artists_1_raw : this.artists_2_raw) {
        if (artists[artist.name]) {
          artists[artist.name].new = false
        }
      }

      //Determining the best new artist.
      var bestArtist = artists[Object.keys(artists)
        .filter(a => artists[a].new)
        .reduce((a, b) => a && artists[a].score > artists[b].score ? a : b,
                undefined)]
      //If there is no best _new_ artist, we revert to just the best artist.
      if (bestArtist === undefined) {
        bestArtist = artists[Object.keys(artists)
          .reduce((a, b) => a && artists[a].score > artists[b].score ? a : b,
                  undefined)]
      }

      /**
       * Iterating over all the other user's top tracks to find if the best 
       * artist has a track that features in the other user's top tracks. 
      */
      for (var track of display_name == this.display_name_1
                        ? this.tracks_2_raw : this.tracks_1_raw) {
        for (artist of track.artists) {
          if (bestArtist.name === artist.name) {
            bestArtist.top_track = 
              bestArtist.top_track &&
              bestArtist.top_track.popularity >= track.popularity 
              ? bestArtist.top_track
              : track
          }
        }
      }

      /**
       * Filtering out the genres field in the bestArtist to include only those 
       * that appear in the genres_query, sorting them by their weight in the
       * genres query and then taking up to the first three.
       */
      bestArtist.genres = 
        bestArtist.genres.filter(g => genres_query[g] ? true : false)
                         .sort((a,b) => genres_query[b]-genres_query[a])
                         .slice(0,3)

      return bestArtist
    }
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
  .desc {
    text-align:left;
  }
  .grid {
    margin: $spacer*4 0;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
    grid-column-gap: 0px;
    grid-row-gap: 0px;

    grid-template-areas:
     "a b"
     "c d";
     #avatar1 { grid-area: a }
     #avatar2 { grid-area: d }
     #rec1 { grid-area: b }
     #rec2 { grid-area: c }
     @media (min-width: $breakpoint-width) {
      margin-top: $spacer*8;
      #avatar1 { grid-area: a }
      #avatar2 { grid-area: b }
      #rec1 { grid-area: c }
      #rec2 { grid-area: d }
      .rec {
        padding-top: $spacer*4;
        height:100%;
        width:100%;
        padding-left: $spacer*4;
        padding-right:$spacer*4;
        display:flex;
        flex-direction: column;
        align-items: stretch;
        hr {
          width:100%;
        }
        justify-content: space-between;
      }
     }

    align-items: center;
    justify-items: center;
    >* {
      margin: 0 auto;
    }
    .avatar-cont-cont {
      width:100%;
      max-width:200px+$spacer*4;
      padding: 0 $spacer*2;
      .avatar-cont {
        width:100%;
        padding-top: 100%;
        height:0;
        position:relative;
        .avatar {
          position:absolute;
          top:0;left:0;
          width:100%;height:100%;
          object-fit: cover;
          border-radius:50%;
        }
      }
    }
    .rec {
      .rec-title {
        display:block;
        font-family: 'Lato', sans-serif;
        font-weight:700;
        text-transform: uppercase;
        text-shadow: 0px 0px 20px $cyan-d;
        color: $cyan-l;
      }
      .matching-genres-ul {
        overflow:visible;
        .matching-genres-li {
          display: inline;
          text-shadow: 0px 0px 20px $magenta-d;
          color: $magenta-l;
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
  }
}
</style>
