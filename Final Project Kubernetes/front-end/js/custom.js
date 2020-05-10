


jQuery(function($){


    jQuery(window).scroll(function(){
      if ($(this).scrollTop() > 300) {
        $('.scrollToTop').fadeIn();
      } else {
        $('.scrollToTop').fadeOut();
      }
    });
     
   
    jQuery('.scrollToTop').click(function(){
      $('html, body').animate({scrollTop : 0},800);
      return false;
    });

    jQuery(window).load(function() {   
      jQuery('#wpf-loader-two').delay(200).fadeOut('slow'); 
    })


});

