<template>
  <div id="compare">
      <div v-if="loading || err" class="loading-notice">
        <h1 class="title">
          Loading Your 
          <span class="data alt">Data</span>
        </h1>
        <div v-if="loading" class="bar">
          <hr class="slider alt">
        </div>
        <p v-if="err" class="err">
          Something went wrong! :(
          <span class="msg">{{ err }}</span>
        </p>
      </div>

      <div v-else class="results">
        <div class="header">
          <h1 class="title">
            <hr/>
            <span class="comparing">Comparing</span>
            <hr class="alt"/>
            <a class="display-name" target="_blank" 
               :href="data[0].profile.external_urls.spotify"
               >{{ data[0].profile.display_name 
               }}<font-awesome-icon class="icon" icon="external-link-alt" transform="shrink-5"/>
               </a>
            <hr/>
            <span class="and">And</span>
            <hr class="alt"/>
            <a class="display-name" target="_blank" 
               :href="data[1].profile.external_urls.spotify"
               >{{ data[1].profile.display_name 
               }}<font-awesome-icon class="icon" icon="external-link-alt" transform="shrink-5"/>
               </a>
          </h1>
        </div>

        <TermSelector class="term-selector" :selected_term="selected_term" @select="selected_term = $event"/>

        <hr>

        <!-- Different data visualisation components will live here! -->

        <ArtistsNetwork class="artists-network"
                        :artists_1_raw="data[0].listening_data[selected_term].artists"
                        :artists_2_raw="data[1].listening_data[selected_term].artists"
                        :display_name_1="data[0].profile.display_name"
                        :display_name_2="data[1].profile.display_name"/>

        <hr>

        <TasteTrader class="taste-trader"
                    :artists_1_raw="data[0].listening_data[selected_term].artists"
                    :artists_2_raw="data[1].listening_data[selected_term].artists"
                    :tracks_1_raw="data[0].listening_data[selected_term].tracks"
                    :tracks_2_raw="data[1].listening_data[selected_term].tracks"
                    :display_name_1="data[0].profile.display_name"
                    :display_name_2="data[1].profile.display_name"
                    :avatar_1="data[0].profile.images[0] 
                               ? data[0].profile.images[0].url
                               : '/assets/img/placeholder_avatar_1.jpg'"
                    :avatar_2="data[1].profile.images[0] 
                               ? data[1].profile.images[0].url
                               : '/assets/img/placeholder_avatar_2.jpg'"/>

        <hr>

        <MutualGenres class="mutual-genres"
                      :artists_1_raw="data[0].listening_data[selected_term].artists"
                      :artists_2_raw="data[1].listening_data[selected_term].artists"
                      :display_name_1="data[0].profile.display_name"
                      :display_name_2="data[1].profile.display_name"/>

        <hr>
      </div>
  </div>
</template>

<script>
import axios from "axios"
import TermSelector from "../components/TermSelector.vue"
import ArtistsNetwork from "../components/ArtistsNetwork.vue"
import MutualGenres from "../components/MutualGenres.vue"
import TasteTrader from "../components/TasteTrader.vue"

const API_Path = process.env.VUE_APP_API_BASE_URI ? process.env.VUE_APP_API_BASE_URI : "https://api-dev.spotdiff.online"

export default {
  name: 'Compare',
  components: { 
    TermSelector,
    ArtistsNetwork,
    MutualGenres,
    TasteTrader,
 },
  data(){return{
    data: undefined,
    loading: true,
    err: undefined,
    selected_term:"medium_term",
  }},
  mounted() {
    axios.post(API_Path+"/compare",{
        share_code_1: this.$route.params.share_code_1,
        share_code_2: this.$route.params.share_code_2
     }).then(function(response) {
       this.data = response.data.data
       this.loading = false
     }.bind(this)
     ).catch(function(reason) {
        console.log("/compare failed: ", reason)
         this.loading = false
        this.err = reason
     }.bind(this))
  }
}
</script>

<style scoped lang="scss">
#compare {
  padding: $spacer*2;

  width:100%;
  max-width:1280px;

  .loading-notice {
    height:100%;

    display:flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    text-align: center;

    .title {
      @include glowThrob();
      .data {
        @include displayFontAltHuge();
        @include glowThrobAlt();
      }
    }

    .bar {
      margin-top: $spacer*4;

      height:2px;
      width:600px;
      max-width:80%;

      background: $magenta;
      @include glowBox();

      position:relative;

      .slider {
        margin: 0;

        position:absolute;
        top:0;left:0;
        width: 25%;
        height:100%;

        @keyframes slide {
          0% { left: 0; width:0; }
          25% { left: 0; width:25%; }
          75% { left: 75%; width:25%; }
          100% { left: 100%; width:0; }
        }
        animation-name: slide;
        animation-duration: 1.5s;
        animation-iteration-count: infinite;
        animation-timing-function: linear;
      }
    }

    .err {
      margin-top: $spacer*4;

      .msg {
        margin-top: $spacer*4;
        display:block;

        @include sansUpperAlt();
      }
    }
  }

  .results {
    width:100%;

    .header {
      margin-bottom: $spacer*8;

      .title {
        display:flex;
        flex-direction: column;
        align-items: stretch;

        >:first-child {
          margin-top:$spacer;
        }
        
        .comparing { @include displayFontHuge(); }
        .and { @include displayFont(); }
        .display-name { 
          @include displayFontAlt();
          align-self: flex-end;
        }
      }
    }

    >:last-child {
      margin-bottom: $spacer;
    }
  }
}
</style>
