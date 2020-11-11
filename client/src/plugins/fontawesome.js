import Vue from 'vue'

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'

import { faExternalLinkAlt } from '@fortawesome/free-solid-svg-icons'

library.add(
  faExternalLinkAlt,
)

Vue.component('font-awesome-icon', FontAwesomeIcon)