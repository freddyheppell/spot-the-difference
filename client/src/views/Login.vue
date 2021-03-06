<template>
  <div id="login">
    <h1 class="title">Spot The <span class="difference alt">Difference</span></h1>
    <div v-if="profile_data" class="about">
      {{ (profile_data.self ? "Hey " : "Compare your music taste with ")
         + profile_data.display_name }}!
      <img class="avatar" :src="profile_data.images[0].url"/>
    </div>
    <p v-if="!profile_data" class="desc">Compare music tastes with your friends by creating a shareable link.</p>
    <a v-if="!profile_data || !profile_data.self" class="login-button button" :href="spotify_auth_link">
      Log In With Spotify
    </a>
    <div class="shareables" v-if="profile_data">
      <hr>
      Share this link so others can compare their tastes with {{ profile_data.self ? "you" : profile_data.display_name }}!
      <button class="copy-link button" @click="share">
        {{ can_share ? 'Copy Link' : 'Copy Link To Clipboard' }}
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios"
const API_Path = process.env.VUE_APP_SPOT_DIFF_API_BASE_URI 
                 ? process.env.VUE_APP_SPOT_DIFF_API_BASE_URI 
                 : "https://api-dev.spotdiff.online"

export default {
  name: 'Login',
  data() {return {
    profile_data: undefined,
    can_share: navigator.canShare,
  }},
  mounted() {
    //Check the route query for a code given to us by the spotify API after redirect...
    if (this.$route.query.code) {
      var params = {
        spotify_code: this.$route.query.code
      }
      //If we've also got someone else's share code in the state then we add that to the params given to /authorise
      if (this.$route.query.state) {
        params.share_code = this.$route.query.state
      }
      axios.post(API_Path+"/authorise", params
                ).then(
                  function(response) {
                    //We redirect to a new path which will contain one or two share codes!
                    if (response.data.share_codes[1]) {
                      this.$router.push(response.data.share_codes[1]+"/"+response.data.share_codes[0])
                    } else {
                      this.$router.push(response.data.share_codes[0])
                      this.get_profile(response.data.share_codes[0],true)
                    }
                  }.bind(this)
                ).catch(
                  function(reason) {
                    console.log("/authorise failed: ", reason)
                  }
                )
    } else if (this.$route.params.share_code_1) {
      this.get_profile(this.$route.params.share_code_1,false)
    }
  },
  methods: {
    get_profile(share_code,self) {
      //We get the profile's data from the /profile endpoint.
      axios.post(API_Path+"/profile", { share_code: share_code }
      ).then(function(response){
        response.data.self = self
        this.profile_data = response.data
        //TODO!
      }.bind(this)).catch(
        function(reason) {
          console.log("/profile failed: ", reason)
        }.bind(this)
      )
    },
    share() {
      if (navigator.canShare) {
        navigator.share({
          url: window.location.href,
          title: "Spot The Difference",
          text: "Compare your music taste to " + this.profile_data.display_name + "!"
        })
      } else {
        navigator.clipboard.writeText(window.location.href)
      }
    }
  },
  computed: {
    spotify_auth_link() {
      const client_id = "4c4fa8272fc04f028b61d332524d2611";
      const redirect_uri = window.location.origin;
      const scope = "user-top-read";
      return "https://accounts.spotify.com/authorize"+
             "?response_type=code"+
             "&client_id="+client_id+
             "&redirect_uri="+redirect_uri+
             "&scope="+scope+
             (this.$route.params.share_code_1 ? "&state="+this.$route.params.share_code_1 : "")
    }
  }
}
</script>

<style scoped lang="scss">
#login {
  align-self: center;

  padding: $spacer*2;

  display:flex;
  flex-direction: column;
  align-items:center;

  text-align:center;

  >* {
    max-width:100%;
  }

  .title {
    margin-bottom: $spacer*4;
    .difference {
      @include displayFontAltHuge();
      display:block;
    }
  }

  .desc {
    margin-bottom: $spacer*6;
  }

  .about {
    margin-top: $spacer*4;
    .avatar {
      margin:$spacer*4 auto;
      display:block;
      width:200px;
      height:200px;
      object-fit: cover;
      border-radius:50%;
    }
  }

  .shareables {
    margin-top: $spacer*8;
    hr {
      margin-bottom: $spacer*4;
    }
    .copy-link {
      margin: $spacer*4 auto 0 auto;
      display:block;
    }
  }
}
</style>
