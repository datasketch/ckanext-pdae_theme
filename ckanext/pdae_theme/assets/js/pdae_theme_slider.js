'use strict';

ckan.module('pdae_theme_slider', function ($) {
  return {
    initialize: function () {
      if (!window.Swiper) {
        console.error('Swiper lib must be available to use this module.')
        return
      }
      const swiper = new window.Swiper(this.el.get(0), {
        slidesPerView: 1,
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev'
        },
        breakpoints: {
          768: {
            slidesPerView: 2,
            spaceBetween: 40
          },
          992: {
            slidesPerView: 3,
            spaceBetween: 40
          }
        }
      })
      // const trigger = document.getElementById(this.options.trigger)
      // const target = document.getElementById(this.options.target)
      // trigger.addEventListener('click', function() {
      //   target.classList.toggle('navbar-open')
      // })
    }
  }
})