async function loadDataFromMerch(){
    try{
        const response = await fetch('http://127.0.0.1:8001/featured/');
        const data = await response.json();
        const container = document.getElementById('merch-list');
        container.innerHTML = data.map(product => `
            <a href="${product.product_url}"> 
            <div class="product-card">
                <img src="${product.image_url}" alt="${product.name}">
                <h3>${product.name}</h3>
                <strike>Rs. ${product.price}</strike>
                <p>Rs. ${product.discount_price}</p>
                
            </div>
            </a>

        `)
    }catch(e){
        console.log("error occured", e);
    }
    
}

loadDataFromMerch();