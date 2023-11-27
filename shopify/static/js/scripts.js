let updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++) {
   updateBtns[i].addEventListener('click', function() {
      let productId = this.dataset.product
      let action = this.dataset.action
      console.log('USER:', user)
      console.log('productId: ', productId, 'action: ', action)
      if(user === 'AnonymousUser'){
        addCookieItem(productId, action)
      }else{
        alert('Item added to cart successfully')
        updateUserOrder(productId,action)
      }
   })
    
}

function addCookieItem(productId, action) {
    console.log('Not logged in..')

    if(action == 'add'){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('item should be deleted..')
            delete cart[productId]
        }
    }

    console.log('cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain;path=/"
    location.reload()
}

function updateUserOrder(productId, action) {
    console.log('user is authenticated, sending data...')

    let url = '/updateItem/'
    // sending data to the updateitem view in the backend and the view will process the data
    fetch(url, {
        method :'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data: ', data)
        location.reload()
    });
}