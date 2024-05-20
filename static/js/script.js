$('.top-down-link').click(function(e) {
    window.scrollTo(0,0)
})

$(document).ready(function() {
  $('.add-to-cart-btn').click(function() {
      var productId = $(this).data('product-id');
      var productPrice = $(this).data('product-price');
      fetch(`/cart/quick_add/${productId}/`, {
          method: 'POST',
          headers: {
              'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
              'Content-Type': 'application/json',
              'Accept': 'application/json'
          },
          body: JSON.stringify({ product_id: productId })
      })
      .then(response => {
          if (!response.ok) {
              throw new Error('Failed to update product status');
          }
          return response.json();
      })
      .then(data => {
        const toastLive = document.getElementById('liveToast');
        const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLive);
        let successMessage = document.getElementById('toastcc');
        toastBootstrap.show()
        // Show message info
        successMessage.textContent = data.message;
        // Increases product count
        incrementProductCount();
        var ccss1 = document.getElementById('grand');
        ttd = parseInt(ccss1.textContent)
        incrementTotal(productPrice);
      })
      .catch(error => {
          console.error('Error updating product status:', error);
      });
  });
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to increment product count
function incrementProductCount() {
    var productCountElement = document.getElementById('prod');
    var currentCount = parseInt(productCountElement.textContent);
    if (!isNaN(currentCount)) {
        productCountElement.textContent = currentCount + 1;
    } else {
        productCountElement.textContent = 1;
    }
}


// Function to increment grandTotal
function incrementTotal(productPrice) {
    
    let grandTotal = document.getElementById('grand');
    let ccss = document.getElementById('grand');
    grandTotal = parseInt(grandTotal.textContent);
    let currentGrandTotal = parseInt(grandTotal.textContent);
    let productPrice2 = parseInt(productPrice);
    grandTotal.textContent = currentGrandTotal + productPrice;
    ccss.textContent = productPrice + ttd
}

$('#sort-selector').change(function() {
    var selector = $(this);
    var currentUrl = new URL(window.location);

    var selectedVal = selector.val();
    if(selectedVal != "reset"){
        var sort = selectedVal.split("_")[0];
        var direction = selectedVal.split("_")[1];

        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);

        window.location.replace(currentUrl);
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");

        window.location.replace(currentUrl);
    }
})