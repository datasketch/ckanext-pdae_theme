'use strict';

ckan.module('pdae_theme_navbar', function($) {
  return {
    initialize: function() {
      const trigger = document.getElementById(this.options.trigger)
      const target = document.getElementById(this.options.target)
      trigger.addEventListener('click', function() {
        target.classList.toggle('navbar-open')
      })
    }
  }
})