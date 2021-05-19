'use strict';

ckan.module('pdae_theme_navbar', function ($) {
  return {
    initialize: function () {
      const triggers = document.querySelectorAll('.' + this.options.trigger)
      const target = document.getElementById(this.options.target)
      triggers.forEach(function (trigger) {
        trigger.addEventListener('click', function () {
          target.classList.toggle('navbar-open')
          document.body.classList.toggle('dark')
        })
      })
    }
  }
})