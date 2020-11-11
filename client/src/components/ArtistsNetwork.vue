<template>
  <div class="container">
    <h2 class="title">Artists Network</h2>
    <ol class="key">
      <li class="display-name-1">{{ display_name_1 }}</li>
      <li class="both">Both</li>
      <li class="display-name-2">{{ display_name_2 }}</li>
    </ol>
    <p class="desc">Links represent mutual genres.</p>
    <p class="desc">Click nodes to expand.</p>
    <div class="network-graph-container">
      <d3-network class="d3-network"
                  :net-nodes="Object.values(artists).map(a=>a.node)" 
                  :net-links="net_links" 
                  :selection="selection"
                  :options="{ canvas:false }"
                  @node-click="artist_clicked"/>
    </div>
    <div v-if="artist_selected" class="selected-artist">
      <hr class="alt">
      <a :href="artist_selected.external_urls.spotify" target="_blank" class="artist-name">
        <h2 class="alt">
          {{ artist_selected.name 
          }}<font-awesome-icon class="icon" icon="external-link-alt" transform="shrink-5"/>
        </h2>
      </a>
      <section class="genres">
        Genres:
        <div v-if="artist_selected.genres.length==0" class="genres-err">
          Couldn't find any! :(
        </div>
        <ul v-else class="artist-genres-ul">
          <li v-for="genre of artist_selected.genres" :key="genre" 
              class="artist-genres-li"
              >{{ genre }}</li>
        </ul>
      </section>
      <section class="mutual-artists">
        Artists With Mutual Genres:
        <div v-if="similar_artists.length==0" class="mutual-artists-err">
          Couldn't find any! :(
        </div>
        <ul v-else class="similar-artists-ul">
          <li v-for="artist of similar_artists" :key="artist"
              class="similar-artists-li"
              >{{ artist }}</li>
        </ul>
      </section>
    </div>
  </div>
</template>

<script>
import D3Network from 'vue-d3-network'

export default {
  name: 'ArtistNetwork',
  components: {
    D3Network
  },
  props: ["artists_1_raw", "artists_2_raw", "display_name_1", "display_name_2"],
  watch: {
    artists_1_raw: function(){this.artist_selected=undefined;this.selection.nodes={}},
    artists_2_raw: function(){this.artist_selected=undefined;this.selection.nodes={}}
  },
  data(){return{
    artist_selected:undefined,
    selection:{nodes:{},links:{}},
  }},
  methods:{
    artist_clicked(event,node) {
      this.selection.nodes={}
      if (!this.artist_selected || !(node.id === this.artist_selected.node.id)) {
        this.selection.nodes[node.id] = node
        this.artist_selected = this.artists[node.id]
      } else {
        this.artist_selected = undefined
      }
    }
  },
  computed: {
    similar_artists() {
      var similar_artists = {}
      for (var genre of this.artist_selected.genres) {
        for (var artist of this.genres[genre]) {
          if (artist === this.artist_selected.name) {
            continue
          }
          similar_artists[artist] = true
        }
      }
      return Object.keys(similar_artists)
    },
    artists() {
      var artists = {}
      for (var artist of this.artists_1_raw.slice(0,25)) {
        artists[artist.name] = artist
        artists[artist.name].node = {
          id:artist.name, _cssClass:"user1-artist-node"
        }
      }
      for (artist of this.artists_2_raw.slice(0,25)) {
        if (artists[artist.name]) {
          artists[artist.name].node._cssClass="both-artist-node"
        } else {
          artists[artist.name] = artist
          artists[artist.name].node = {
            id:artist.name, _cssClass:"user2-artist-node"
          }
        }
      }
      return artists
    },
    genres() {
      var genres = {}
      for (var artist of Object.values(this.artists)) {
        for (var genre of artist.genres) {
          if (genres[genre]) {
            genres[genre].push(artist.node.id)
          } else {
            genres[genre] = [artist.node.id]
          }
        }
      }   
      return genres   
    },
    net_links() {
      var net_links = []
      var all_artists = Object.values(this.artists)
      for (var [i, artist_1] of all_artists.entries()) {
        for (var artist_2 of all_artists.slice(i)) {
          if (artist_1.genres.filter(g => artist_2.genres.includes(g))
                             .length > 0) {
            net_links.push({
              sid: artist_1.name,
              tid: artist_2.name
            })
            
          }
        }
      }
      return net_links
    },
  }
}
</script>

<style lang="scss" scoped>
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
  
  .network-graph-container {
    height:70vh;
    max-height: 500px;
  }
  
  .selected-artist {
    padding: $spacer*4;
    hr { margin-bottom: $spacer*4; }
    h2 { display:inline-block; }
    .genres-err, .mutual-artists-err { 
      display:inline-block; 
    }
    .genres-err { @include sansUpper() }
    .mutual-artists-err { @include sansUpperAlt() }
    .genres, .mutual-artists {
      @include sansUpperWhite();
      margin-top: $spacer*3;
      .artist-genres-ul { @include sansUpper(); }
      .similar-artists-ul { @include sansUpperAlt(); }
      .artist-genres-ul, .similar-artists-ul {
        display:inline;
        line-height:1;
        li {
          display: inline;
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

<style lang="scss">
.d3-network {
  width:100%;height:100%;

  .node {
    stroke:transparent;
    stroke-width:30px;
    r: 5px;
    &.selected {
      r:10px;
    }
    &.user1-artist-node { fill: $magenta; }
    &.user2-artist-node { fill: $cyan; }
    &.both-artist-node { fill: $white; }
  }

  .link { 
    stroke: $white;
    opacity: 0.4;
  }
}
</style>
