<template>
  <div id="compare">
    <div class="container">
      <div v-if="loading" class="loading-notice">
        <h1 class="title">Loading Your Data</h1>
      </div>

      <div v-else class="results">
        <hr class="alt"/>
        <div class="header">
          <h1 class="title">
            <span class="comparing">Comparing</span>
            <hr/>
            <span class="display-name">{{ data[0].profile.display_name }}</span>
            <hr class="alt"/>
            <span class="and">And</span>
            <hr/>
            <span class="display-name">{{ data[1].profile.display_name }}</span>
          </h1>
        </div>

        <TermSelector class="term-selector" :selected_term="selected_term" @select="selected_term = $event"/>

        <hr class="alt">
        <!-- Different data visualisation components will live here! -->

        <ArtistsNetwork class="artists-network"
                        :artists_1_raw="data[0].listening_data[selected_term].artists"
                        :artists_2_raw="data[1].listening_data[selected_term].artists"
                        :display_name_1="data[0].profile.display_name"
                        :display_name_2="data[1].profile.display_name"/>

        <hr class="alt">

        <TasteTrader class="taste-trader"
                    :artists_1_raw="data[0].listening_data[selected_term].artists"
                    :artists_2_raw="data[1].listening_data[selected_term].artists"
                    :tracks_1_raw="data[0].listening_data[selected_term].tracks"
                    :tracks_2_raw="data[1].listening_data[selected_term].tracks"
                    :display_name_1="data[0].profile.display_name"
                    :display_name_2="data[1].profile.display_name"
                    :avatar_1="data[0].profile.images[0].url"
                    :avatar_2="data[1].profile.images[0].url"/>

        <hr class="alt">

        <CommonGenres class="common-genres"
                      :artists_1_raw="data[0].listening_data[selected_term].artists"
                      :artists_2_raw="data[1].listening_data[selected_term].artists"
                      :display_name_1="data[0].profile.display_name"
                      :display_name_2="data[1].profile.display_name"/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"
import TermSelector from "../components/TermSelector.vue"
import ArtistsNetwork from "../components/ArtistsNetwork.vue"
import CommonGenres from "../components/CommonGenres.vue"
import TasteTrader from "../components/TasteTrader.vue"

const API_Path = process.env.VUE_APP_API_BASE_URI ? process.env.VUE_APP_API_BASE_URI : "https://api-dev.spotdiff.online"

export default {
  name: 'Compare',
  components: { 
    TermSelector,
    ArtistsNetwork,
    CommonGenres,
    TasteTrader,
 },
  data(){return{
    data: undefined,
    loading: true,
    selected_term:"medium_term",
  }},
  mounted() {
    axios.post(API_Path+"/compare",{
        share_code_1: this.$route.params.share_code_1,
        share_code_2: this.$route.params.share_code_2
     }).then(function(response) {
       this.data = response.data.data
       this.loading = false;
     }.bind(this)
     ).catch(function(reason) {
        console.log("/compare failed: ", reason)
     }.bind(this))
  }
}
</script>

<style scoped lang="scss">
#compare {
  padding: $spacer*2;

  width:100%;

  text-align:center;

  .container {
    width:100%;
    height:100%;
    max-width:1280px;
    margin: 0 auto;

    .loading-notice {
      height:100%;
      display:flex;
      justify-content: center;
      align-items: center;
      .title {
        font-size: $font-size-m;
        @media(min-width:$breakpoint-width) {
          font-size: $font-size-l;
        }
      }
    }

    .results {
      width:100%;

      .title {
        word-break: break-all;

        span {
          display:block;
        }

        hr {
          margin: $spacer*4 0 $spacer*2 0;
        }

        .comparing, .and { text-align: left }
        .and, .display-name {
          font-size: $font-size-m;
          @media(min-width:$breakpoint-width) {
            font-size: $font-size-l;
          }
        }
        .display-name { 
          text-align: right;
          color: $cyan;
          text-shadow: 0px 0px 20px $cyan-d;
        }

        .comparing {
          font-size: $font-size-l;
          @media(min-width:$breakpoint-width) {
            font-size: $font-size-ll;
          }
        }
      }

      .term-selector {
        margin-top: $spacer*8;
      }
    }
  }
}
</style>
