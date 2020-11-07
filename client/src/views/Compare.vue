<template>
  <div id="compare">
    <div class="container">
      <div v-if="loading" class="loading-notice">
        <h1 class="title">Loading Your Data</h1>
      </div>

      <div v-else class="results">
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

        <!-- Different data visualisation components will live here! -->

      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"
const API_Path = "https://negka4m5ph.execute-api.eu-west-1.amazonaws.com/dev"

export default {
  name: 'Compare',
  data(){return{
    data: undefined,
    loading: true
  }},
  mounted() {
    axios.post(API_Path+"/compare",{
        share_code_1: this.$route.params.share_code_1,
        share_code_2: this.$route.params.share_code_2
     }).then(function(response) {
       console.log(response.data)
       //TODO - Waiting for Freddy to implement this endpoint xoxo
        this.loading = false;
     }.bind(this)
     ).catch(function(reason) {
        console.log("/compare failed: ", reason)
        this.data = [
          {
            profile: {
              display_name: "TheTeaCat",
              external_urls: { spotify: "" },
              images: [ { url: " "} ],
            },
            listening_data: {
              short_term: { artists: [], tracks: [] },
              medium_term: { artists: require("../assets/mock_data/mock_artists_1.json"), tracks: [] },
              long_term: { artists: [], tracks: [] }
            }
          },
          {
            profile: {
              display_name: "Freddy",
              external_urls: { spotify: "" },
              images: [ { url: " "} ],
            },
            listening_data: {
              short_term: { artists: [], tracks: [] },
              medium_term: { artists: require("../assets/mock_data/mock_artists_2.json"), tracks: [] },
              long_term: { artists: [], tracks: [] }
            }
          }
        ]
        this.loading = false;
     }.bind(this))
  }
}
</script>

<style scoped lang="scss">
#compare {
  padding: $spacer*4;

  display:flex;
  flex-direction: column;
  align-items:center;

  text-align:center;

  .container {
    width:100%;
    max-width:1280px;

    .loading-notice {
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
        margin-bottom: $spacer*4;
        word-break: break-all;

        span {
          display:block;
        }

        hr {
          border:none;
          margin: $spacer*4 0 $spacer*2 0;
          height:2px;
          background: $cyan;
          box-shadow: 0px 0px 10px $cyan-d;
          &.alt {
            background: $magenta-l;
            box-shadow: 0px 0px 10px $magenta-d;
          }
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
        }

        .comparing {
          font-size: $font-size-l;
          @media(min-width:$breakpoint-width) {
            font-size: $font-size-ll;
          }
        }    
      }
    }
  }
}
</style>
