$(document).ready(function(){
var stripeFormModule = $('.stripe-payment-form')
var stripeModuleToken = stripeFormModule.attr('data-token')
var stripeModuleNextUrl = stripeFormModule.attr('data-next-url')
var stripeModuleBtnTitle = stripeFormModule.attr('data-btn-title')||"Add card"

var stripeTemplate = $.templates("#stripeTemplate")
var stripeTemplateDataContext = {
  publish_key : stripeModuleToken,
  next_url : stripeModuleNextUrl,
  btn_title : stripeModuleBtnTitle
}
var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
stripeFormModule.html(stripeTemplateHtml)


var paymentForm = $('.payment-form')

if (paymentForm.length >1) {
  alert('Only one payment form per page')
  paymentForm.css('display', 'none')
}
else if (paymentForm.length ==1) {
  var pubkey = paymentForm.attr('data-token')
  var nextUrl = paymentForm.attr('data-next-url')

  // Create a Stripe client.

  var stripe = Stripe(pubkey);

  // Create an instance of Elements.
  var elements = stripe.elements();

  // Custom styling can be passed to options when creating an Element.
  // (Note that this demo uses a wider set of styles than the guide below.)
  var style = {
    base: {
      color: '#32325d',
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: 'antialiased',
      fontSize: '16px',
      '::placeholder': {
        color: '#aab7c4'
      }
    },
    invalid: {
      color: '#fa755a',
      iconColor: '#fa755a'
    }
  };

  // Create an instance of the card Element.
  var card = elements.create('card', {style: style});

  // Add an instance of the card Element into the `card-element` <div>.
  card.mount('#card-element');

  // Handle real-time validation errors from the card Element.
  card.addEventListener('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
      displayError.textContent = event.error.message;
    } else {
      displayError.textContent = '';
    }
  });

  // Handle form submission.
  var form = $('#payment-form');
  var btnLoad = form.find(".btn-load")
  var btnLoadDefaultHtml = btnLoad.html()
  var btnLoadDefaultClasses = btnLoad.attr("class")
  form.on('submit', function(event) {
    event.preventDefault();
    var $this = $(this)
    btnLoad.blur()
    var loadTime = 1500
    var currentTimeout
    var errorHtml = "<i class='fa fa-warning'></i> Désolé, une erreur s'est produite."
    var errorClasses = "btn btn-danger disabled"
    var loadingHtml = "<i class='fa fa-spin fa-spinner'></i> Nous vérifions vos données."
    var loadingClasses = "btn btn-success disabled"
    stripe.createToken(card).then(function(result) {
      if (result.error) {
        // Inform the user if there was an error.
        var errorElement = $('#card-errors');
        errorElement.textContent = result.error.message;
        currentTimeout = displayBtnStatus(
                                    btnLoad,
                                    errorHtml,
                                    errorClasses,
                                    1000,
                                    currentTimeout
                        )
      } else {
        currentTimeout = displayBtnStatus(
                                    btnLoad,
                                    loadingHtml,
                                    loadingClasses,
                                    2000,
                                    currentTimeout
                        )
        // Send the token to your server.
        stripeTokenHandler(result.token, nextUrl);
      }
    });
  });

function displayBtnStatus(element, newHtml, newClasses, loadTime, timeout){
    if (!loadTime){
      loadTime = 1500
    }
    element.html(newHtml)
    element.removeClass(btnLoadDefaultClasses)
    element.addClass(newClasses)
    return setTimeout(function(){
        element.html(btnLoadDefaultHtml)
        element.removeClass(newClasses)
        element.addClass(btnLoadDefaultClasses)
    }, loadTime)
}

  function redirectToNext(nextPath, timeoffset){
      if (nextPath){
        setTimeout(function(){
          window.location.href = nextUrl
        }, timeoffset)
      }
  }

  // Submit the form with the token ID.
  function stripeTokenHandler(token, nextUrl) {
    console.log(token.id)
    var paymentMethodEndpoint = "/billing/payment-method/create/"
    data = {
      'token':token.id
    }
    $.ajax({
      data : data,
      url : paymentMethodEndpoint,
      method : 'POST',
      success : function(data){
        var successMsg = data.message || "Success ! ta carte a été ajoutée"
        card.clear()
        if (nextUrl){
          successMsg = successMsg + '<br/><br/><i class="fa fa-spin fa-spinner"></i>... Redirect'
        }
        if ($.alert){
          $.alert(successMsg)
        } else {
          alert(successMsg)
        }
        btnLoad.html(btnLoadDefaultHtml)
        btnLoad.attr('class', btnLoadDefaultClasses)
        redirectToNext(nextUrl,1500)
      },
        error: function(error){
            // console.log(error)
            $.alert({title: "An error occured", content:"Please try adding your card again."})
            btnLoad.html(btnLoadDefaultHtml)
            btnLoad.attr('class', btnLoadDefaultClasses)
        }
    })
    // Insert the token ID into the form so it gets submitted to the server
    // var form = document.getElementById('payment-form');
    // var hiddenInput = document.createElement('input');
    // hiddenInput.setAttribute('type', 'hidden');
    // hiddenInput.setAttribute('name', 'stripeToken');
    // hiddenInput.setAttribute('value', token.id);
    // form.appendChild(hiddenInput);

    // // Submit the form
    // form.submit();
  }
}

})

