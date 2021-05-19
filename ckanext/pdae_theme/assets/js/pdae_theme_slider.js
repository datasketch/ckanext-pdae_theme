'use strict';

ckan.module('pdae_theme_slider', function ($) {
  return {
    initialize: function () {
      if (!window.Swiper) {
        console.error('Swiper lib must be available to use this module.')
        return
      }
      const container = this.el.find('.swiper-container')
      const nextEl = this.el.find('.slider-next')
      const prevEl = this.el.find('.slider-prev')
      
      const swiper = new window.Swiper(container.get(0), {
        slidesPerView: 1,
        spaceBetween: 32,
        navigation: {
          nextEl: nextEl.get(0),
          prevEl: prevEl.get(0)
        },
        breakpoints: {
          768: {
            slidesPerView: 2,
            spaceBetween: 32
          },
          992: {
            slidesPerView: 3,
            spaceBetween: 32
          }
        }
      })
    }
  }
})