<template>
  <div class="container">
    <hr class="alt">
    <h1 class="title">Artists</h1>
    <ol class="key">
      <li class="display-name-1">{{ display_name_1 }}</li>
      <li class="both">Both</li>
      <li class="display-name-2">{{ display_name_2 }}</li>
    </ol>
    <p class="desc">Links represent mutual genres.</p>
    <div class="network-graph-container">
      <d3-network class="d3-network"
                  :net-nodes="Object.values(artists).map(a=>a.node)" 
                  :net-links="net_links" 
                  :selection="selection"
                  :options="{ canvas:false }"
                  @node-click="artist_clicked"/>
    </div>
    <hr v-if="artist_selected">
    <div v-if="artist_selected" class="selected-artist">
      <h2 class="artist-name alt">{{ artist_selected.name }}</h2>
      <ul class="artist-genres-ul" v-if="artist_selected.genres.length>0">
        <li v-for="genre of artist_selected.genres" :key="genre" 
            class="artist-genres-li"
            >{{ genre }}</li>
      </ul>
      <ul class="similar-artists-ul" v-if="similar_artists.length>0">
        <li v-for="artist of similar_artists" :key="artist"
            class="similar-artists-li"
            >{{ artist }}</li>
      </ul>
    </div>
    <hr class="alt">
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
      for (var artist of this.artists_1_raw.slice(0,15)) {
        artists[artist.name] = artist
        artists[artist.name].node = {
          id:artist.name, _cssClass:"user1-artist-node"
        }
      }
      for (artist of this.artists_2_raw.slice(0,15)) {
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
      for (var genre in this.genres) {
        for (var artist_1 of this.genres[genre]) {
          for (var artist_2 of this.genres[genre]) {
            if (artist_1 === artist_2) { continue }
            net_links.push({
              tid: artist_1,
              sid: artist_2,
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
  .title {
    text-align:left;
    font-size: $font-size-m;
    @media(min-width:$breakpoint-width) {
      font-size: $font-size-l;
    }
  }
  .key {
    font-family: 'Lato', sans-serif;
    font-weight:700;

    text-align:left;
    text-transform: uppercase;

    >*{ display:inline-block }
    :first-child::after {content:"|"}
    :last-child::before {content:"|"}

    .display-name-1 {
      text-shadow: 0px 0px 20px $magenta-d;
      color: $magenta-l;    
    }  
    .display-name-2 {
      text-shadow: 0px 0px 20px $cyan-d;
      color: $cyan-l;    
    }  
  }
  .desc {
    text-align:left;
  }
  .network-graph-container {
    height:70vh;
  }
  .selected-artist {
    font-family: 'Lato', sans-serif;
    line-height:1;
    padding: $spacer*2;
    .artist-name {
      text-align:left;
      font-size: $font-size-m;
      @media(min-width:$breakpoint-width) {
        font-size: $font-size-l;
      }
    }
    .artist-genres-ul {
      padding-top: $spacer*3;
      text-align:left;
      .artist-genres-li {
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
    .similar-artists-ul {
      padding-top: $spacer*3;

      font-family: 'Lato', sans-serif;
      font-weight:700;
      font-size: $font-size;
      @media(min-width:$breakpoint-width) {
        font-size: $font-size-m;
      }

      text-align:left;
      text-transform: uppercase;
      text-shadow: 0px 0px 20px $magenta-d;
      color: $magenta-l;

      .similar-artists-li {
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
</style>

<style lang="scss">
.d3-network {
  width:100%;height:100%;

  .user1-artist-node { fill: $magenta; }
  .user2-artist-node { fill: $cyan; }
  .both-artist-node { fill: $white; }

  .node {
    r: 5px;
    &.selected {
      r:10px;
    }
  }
  .link { 
    stroke: $white;
    opacity: 0.15;
  }
}
</style>
