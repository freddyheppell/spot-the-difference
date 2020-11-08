<template>
  <div class="container">
    <h1 class="title">Tracks</h1>
    <p class="desc">A track {{ display_name_2 }} likes that {{ display_name_1 }} might like, and vice versa.</p>

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
      <div class="track" id="track1">
        <hr>
        <span>
          {{ display_name_1 }} Should Try Listening To: 
          <span class="track-title">{{ best_track_for_user(display_name_1).title }}</span>
        </span>
        <hr>
      </div>
      <div class="track" id="track2">
        <hr>
        <span>
          {{ display_name_2 }} Should Try Listening To: 
          <span class="track-title">{{ best_track_for_user(display_name_2).title }}</span>
        </span>
        <hr>
      </div>
    </div>

    <hr class="alt">
  </div>
</template>

<script>
export default {
  name: 'TrackTrade',
  props: ["artists_1_raw", "artists_2_raw", "tracks_1_raw", "tracks_2_raw", "display_name_1", "display_name_2", "avatar_1", "avatar_2"],
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
            genres[genre] = { }
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
            genres[genre] = { }
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

      return genres
    },
  },
  methods:{
    best_track_for_user(display_name) {
      var artist_scores = {}
      var artists_raw = display_name == this.display_name_1 ? this.artists_2_raw : this.artists_1_raw
      var tracks_raw = display_name == this.display_name_1 ? this.tracks_2_raw : this.tracks_1_raw

      for (var artist of artists_raw) {
        if (!artist_scores[artist.name]) {
          artist_scores[artist.name] = 0
        }
        for (var genre of artist.genres) {
          artist_scores[artist.name] += this.genres[genre][display_name]
        }
      }

      var track_scores = {}
      var max_score = 0

      for (var track of tracks_raw) {
        track.title = track.artists[0].name + " - " + track.name
        track_scores[track.title] = { title: track.title, score: 0 }
        for (artist of track.artists) {
          if (artist_scores[artist.name]) {
            track_scores[track.title].score += artist_scores[artist.name]
          }
        }
        track_scores[track.title].popularity = track.popularity
        track_scores[track.title].score = track_scores[track.title].score * track.popularity
        if (track_scores[track.title].score > max_score) {
          max_score = track_scores[track.title].score
        }
      }

      console.log(track_scores)

      if (max_score == 0) {
        return Object.values(track_scores).sort(
          (a,b) => b.popularity-a.popularity
        )[0]
      }

      return Object.values(track_scores).sort(
        (a,b) => b.score-a.score
      )[0]
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
     #track1 { grid-area: b }
     #track2 { grid-area: c }
     @media (min-width: $breakpoint-width) {
      margin-top: $spacer*8;
      #avatar1 { grid-area: a }
      #avatar2 { grid-area: b }
      #track1 { grid-area: c }
      #track2 { grid-area: d }
      .track {
        padding-top: $spacer*4;
        height:100%;
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
      max-width:200px;
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
    .track {
      .track-title {
        display:block;
        font-family: 'Lato', sans-serif;
        font-weight:700;
        text-transform: uppercase;
        text-shadow: 0px 0px 20px $cyan-d;
        color: $cyan-l;
      }
    }
  }
}
</style>
