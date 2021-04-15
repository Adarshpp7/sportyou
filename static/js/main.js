(function ($) {
    "use strict";
    
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 768) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });
    
    
    // Header slider
    $('.header-slider').slick({
        autoplay: true,
        dots: true,
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1
    });
    
    
    // Product Slider 4 Column
    $('.product-slider-4').slick({
        autoplay: true,
        infinite: true,
        dots: false,
        slidesToShow: 4,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 1200,
                settings: {
                    slidesToShow: 4,
                }
            },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 3,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2,
                }
            },
            {
                breakpoint: 576,
                settings: {
                    slidesToShow: 1,
                }
            },
        ]
    });
    
    
    // Product Slider 3 Column
    $('.product-slider-3').slick({
        autoplay: true,
        infinite: true,
        dots: false,
        slidesToShow: 3,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 3,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2,
                }
            },
            {
                breakpoint: 576,
                settings: {
                    slidesToShow: 1,
                }
            },
        ]
    });
    
    
    // Product Detail Slider
    $('.product-slider-single').slick({
        infinite: true,
        autoplay: true,
        dots: false,
        fade: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        asNavFor: '.product-slider-single-nav'
    });
    $('.product-slider-single-nav').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        dots: false,
        centerMode: true,
        focusOnSelect: true,
        asNavFor: '.product-slider-single'
    });
    
    
    // Brand Slider
    $('.brand-slider').slick({
        speed: 5000,
        autoplay: true,
        autoplaySpeed: 0,
        cssEase: 'linear',
        slidesToShow: 5,
        slidesToScroll: 1,
        infinite: true,
        swipeToSlide: true,
        centerMode: true,
        focusOnSelect: false,
        arrows: false,
        dots: false,
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 4,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 3,
                }
            },
            {
                breakpoint: 576,
                settings: {
                    slidesToShow: 2,
                }
            },
            {
                breakpoint: 300,
                settings: {
                    slidesToShow: 1,
                }
            }
        ]
    });
    
    
    // Review slider
    $('.review-slider').slick({
        autoplay: true,
        dots: false,
        infinite: true,
        slidesToShow: 2,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                }
            }
        ]
    });
    
    
    // Widget slider
    $('.sidebar-slider').slick({
        autoplay: true,
        dots: false,
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1
    });
    
    
    // Quantity
   
    // Shipping address show hide
    $('.checkout #shipto').change(function () {
        if($(this).is(':checked')) {
            $('.checkout .shipping-address').slideDown();
        } else {
            $('.checkout .shipping-address').slideUp();
        }
    });
    
    
    // Payment methods show hide
    $('.checkout .payment-method .custom-control-input').change(function () {
        if ($(this).prop('checked')) {
            var checkbox_id = $(this).attr('id');
            $('.checkout .payment-method .payment-content').slideUp();
            $('#' + checkbox_id + '-show').slideDown();
        }
    });
})(jQuery);


function plus(id){
    var val = document.getElementById("count"+id).value;
    var data = {
        'action':'plus'
    }
    $.ajax({
        url:'/count/'+ id +'/',
        method:'GET',
        data:data,
        dataType:'json',
        success:function(data){
            if(data=='true'){
                document.getElementById('count'+id).value = parseInt(val) + 1
                window.location.replace('/showcart/')

            }
        }
    })
    
}
function minus(id){
    var val = document.getElementById("count"+id).value;
    var data ={
        'action':'minus'
    }
    $.ajax({
        url:'/count/'+ id +'/',
        method:'GET',
        data:data,
        dataType:'json',
        success:function(data){
            if(data=='true'){
                if(document.getElementById('count'+id).value !== 1) {
                    document.getElementById('count'+id).value = parseInt(val) -1
                    window.location.replace('/showcart/')
                }
               
            }
        }
    })
    // document.getElementById('count'+id).value = parseInt(val) - 1
}

function addclick(id){
    // const CheckBox = document.getElementById('mycheck');
    //var text = document.getElementById('text').value;
   
    // var data ={
    //     'id':id
    // }
    // console.log(id)
    // console.log(CheckBox.checked)
    // if(CheckBox.checked == true){
    //    // text.style.display ="block";
        $.ajax({
            url:'/selectaddress/'+ id + '/',    
            method:'GET',
            // data:data,
            dataType:'json',
            success:function(data){
                alert("Address selected successfully");

                // window.location.replace()
            }
        })
    // }else {
    //     //text.style.display = "none";
    //  }
   
}
function clickadd(){
    var value=$("input[type='radio'][name='method']:checked").val();
    var tot=document.querySelector('.grandtotal').textContent;
    var coupon_code = document.getElementById('coupon_code').value;
    var total= parseInt(tot);
    var data = { 
        'v':value,
        'coupon_code':coupon_code,
        'total':total,
    }
    console.log(data);
    $.ajax({
        url:'/placeorder/' ,
        method: 'GET',
        data:data,
        datatype : 'json' ,
        success:function(data){
            if(data =='true'){
                window.location.replace('/cod/')
            }else if(data == 'true2'){
                window.location.replace('/paypalrazor/1/')
            }
            else if(data == 'true3'){
                window.location.replace('/paypalrazor/2/')
            }
        }


    })
    
}
function delclick(id){
     var f = confirm('do you realy want to proceed this deletion?')
     if (f == true){
        $.ajax({
            url:'/addressremove/'+ id +'/',
            method: 'GET',
            success:function(data){
                if (data=='true'){
                    window.location.replace('/userprofile/')
                   
                }

            }
        })
     }
       
}
function delclick1(id){
    var f = confirm('do you realy want to remove this item from your cart?')
    if (f== true){
        $.ajax({
            url:'/cartdelete/'+id+'/',
            method: 'GET',
            success:function(data){
                if (data='true'){
                    console.log('hoem')
                 window.location.replace('/showcart/')               
                }
            }
        })
    }
}
// function discountupdation(id){
//     var discount = document.getElementById('discount'+id).value;
//     var data = {
//         'csrfmiddlewaretoken':'{{csrf_token}}',
//         'discount':discount,
//     }
//     $.ajax({
//         url:'/discount/'+id+'/',
//         method : 'POST',
//         data : data, 
//         dataType :'json'


//     })
// }
// function edit(id){
//     console.log('helooo')
//     var fname = document.getElementById("fname").value;
//     var lname = document.getElementById("lname").value;
//     var email = document.getElementById("email").value;
//     var pnumber = document.getElementById("pnumber").value;
//     var data = {
//         'csrfmiddlewaretoken':'{{csrf_token}}',
//         'first_name':fname,
//         'last_name':lname,
//         'email':email,
//         'phone_number':pnumber,
//     }
//     $.ajax({
//         url:'/useredit/'+id+'/',
//         method :'POST',
//         data:data,
//         datatype:'json',
//         success:function(data){
//             if(data=='true'){
//                 alert('profile updated successfully')
//                 window.location.replace('/userprofile/')
//             }
//         }
//     })
// }
function search(){
    var search_input = document.getElementById('search_input').value;
    var data = {
        'input':search_input
    }
    $.ajax({
        url:'/product_search/',
        method:'GET',
        data:data,
        dataType:'json',
        success:function(data){
            if(data=='true'){
                console.log('hi')
                window.location.replace('/search_show/')
            }
        }
    })
}