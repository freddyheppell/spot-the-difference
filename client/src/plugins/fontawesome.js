import Vue from 'vue'

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'

import { faArrowUp } from '@fortawesome/free-solid-svg-icons'

library.add(
  faArrowUp,
)

Vue.component('font-awesome-icon', FontAwesomeIcon)