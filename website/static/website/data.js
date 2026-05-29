const instapage = "https://www.instagram.com/sappfitwear/";

const template_products = [
    {
        "name" : "Leggins", 
        "price" : 1200,
        "image_url" : "https://bandsam.com/cdn/shop/files/oasis-fitwear-set-stylish-outfit-beige-1.webp?v=1754558852&width=1946",
        "discount_price": null
    },
    {
        "name" : "Tops", 
        "price" : 1500,
        "image_url" : "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmo4IFq0gWX0WoscdxwzaTZnuiclrw85yF_g&s",
        "discount_price": null
        
    },
    {
        "name" : "Jacket", 
        "price" : 1200,
        "image_url" : "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRxPZSccu45BUrYNyJ6V8YAwpNeTSzi_KsBgA&s",
        "discount_price": null
    }
]

async function loadDataFromMerch(){

    const isDebug = JSON.parse(document.getElementById('django-debug-mode').textContent);
    var url = "http://127.0.0.1:8001/featured/";

    if (!isDebug){
        var url = "https://sappfitmerch.pythonanywhere.com/featured/";

    }

    const container = document.getElementById('merch-list');
    const viewBtn = document.getElementById('visit-store');

    try{
        const response = await fetch(url);
        console.log("response", response);
        if (!response.ok){
            throw new Error("Error occured as the server was unreachable.")
        }
        const data = await response.json();
        if (data.length > 0){
            viewBtn.href = url + "/products";
            container.innerHTML = data.map(product => `
            <a href="${product.product_url}" > 
            <div class="product-card">
                <img src="${product.image_url}" alt="${product.name}">
                <h3>${product.name}</h3>
                <strike>Rs. ${product.discount_price}</strike>
                <p>Rs. ${product.price}</p>
            </div>
            </a>
            `).join(""); 
        }else{
            renderProducts(container, template_products, viewBtn);
        }
           
    }catch(e){
        console.log("Error occured! The server might not be online.", e);
        renderProducts(container, template_products, viewBtn);
    }
}

loadDataFromMerch();

function renderProducts(container, data, viewBtn){
    const sloganEnd = document.getElementById('slogan');
    const notice = document.getElementById('notice');
    viewBtn.href = instapage;
    notice.innerText = "* Please note that price and products may vary from what is shown here! Thank you!"
    sloganEnd.innerHTML = "<p>Get your premium fit from Sappfit Wear <strong>@sappfitwear</strong></p>";
    container.innerHTML = data.map(product => `
       
        <div class="product-card">
            <img src="${product.image_url}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>Rs. ${product.price}</p>
        </div>
        
    `).join('');
}