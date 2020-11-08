<template>
  <div class="artists-network">
    <d3-network class="d3-network"
                :net-nodes="net_data['net-nodes']" 
                :net-links="net_data['net-links']" 
                :options="net_data['options']"/>
  </div>
</template>

<script>
import D3Network from 'vue-d3-network'

export default {
  name: 'ArtistNetwork',
  props: ["artists_1_raw", "artists_2_raw"],
  components: {
    D3Network
  },
  computed: {
    net_data() {
      var artists = {}
      for (var artist of this.artists_1_raw.slice(25)) {
        artists[artist.name] = {
          node: {
            id:artist.name,
            _cssClass:"user1-artist-node",
          },
          genres: artist.genres
        }
      }
      for (artist of this.artists_2_raw.slice(25)) {
        if (artists[artist.name]) {
          artists[artist.name].node._cssClass="both-artist-node"
        } else {
          artists[artist.name] = {
          node: {
            id:artist.name,
            _cssClass:"user2-artist-node",
          },
          genres: artist.genres
          }
        }
      }

      var genres = {}
      for (artist of Object.values(artists)) {
        for (var genre of artist.genres) {
          if (genres[genre]) {
            genres[genre].push(artist.node.id)
          } else {
            genres[genre] = [artist.node.id]
          }
        }
      }

      var net_links = []
      for (genre in genres) {
        for (var artist_1 of genres[genre]) {
          for (var artist_2 of genres[genre]) {
            if (artist_1 === artist_2) { continue }
            net_links.push({
              tid: artist_1,
              sid: artist_2,
            })
          }
        }
      }

      return {
        "net-nodes":Object.values(artists).map(a=>a.node),
        "net-links":net_links,
        "options":{
          canvas:false,
        }
      }
    },
  }
}
</script>

<style lang="scss">
.d3-network {
  width:100%;height:100%;

  .user1-artist-node { fill: $magenta; }
  .user2-artist-node { fill: $cyan; }
  .both-artist-node { fill: $white; }

  .node {
    r: 5;
  }
  .link { 
    stroke: $cyan;
    opacity: 0.075;
  }
}
</style>
