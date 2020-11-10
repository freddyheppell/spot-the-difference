<template>
  <div id="compare">
      <div v-if="loading" class="loading-notice">
        <h1 class="title">Loading Your Data</h1>
      </div>

      <div v-else class="results">
        <div class="header">
          <h1 class="title">
            <hr/>
            <span class="comparing">Comparing</span>
            <hr class="alt"/>
            <a class="display-name" target="_blank" 
               :href="data[0].profile.external_urls.spotify"
               >{{ data[0].profile.display_name }}
               <font-awesome-icon class="icon" icon="arrow-up" :transform="{ rotate:45 }"/>
               </a>
            <hr/>
            <span class="and">And</span>
            <hr class="alt"/>
            <a class="display-name" target="_blank" 
               :href="data[1].profile.external_urls.spotify"
               >{{ data[1].profile.display_name }}
               <font-awesome-icon class="icon" icon="arrow-up" :transform="{ rotate:45 }"/>
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
                               : '/assets/img/placeholder_avatar.jpg'"
                    :avatar_2="data[1].profile.images[0] 
                               ? data[1].profile.images[0].url
                               : '/assets/img/placeholder_avatar.jpg'"/>

        <hr>

        <CommonGenres class="common-genres"
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
  max-width:1280px;

  .loading-notice {
    height:100%;

    display:flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    text-align: center;
  }

  .results {
    width:100%;

    .header {
      margin-bottom: $spacer*8;

      .title {
        display:flex;
        flex-direction: column;
        align-items: stretch;

        hr { margin: $spacer*4 0 $spacer*2 0; }
        
        .comparing { @include displayFontHuge(); }
        .and { @include displayFont(); }
        .display-name { 
          @include displayFontAlt();
          align-self: flex-end;
        }
      }
    }
  }
}
</style>
