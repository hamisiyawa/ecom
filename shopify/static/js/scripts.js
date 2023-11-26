let updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++) {
   updateBtns[i].addEventListener('click', function() {
      let productId = this.dataset.product
      let action = this.dataset.action
      console.log('USER:', user)
      console.log('productId: ', productId, 'action: ', action)
      if(user === 'AnonymousUser'){
        window.alert('user is not authenticated')
      }else{
        alert('Item added to cart successfully')
        updateUserOrder(productId,action)
      }
   })
    
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