const instapage = "https://www.instagram.com/sappfitwear/";

const template_products = [
    {
        "name" : "Leggins", 
        "price" : 1200,
        "image_url" : "/media/images/pics/finalized.png",
        "discount_price": null
    },
    {
        "name" : "Tops", 
        "price" : 1500,
        "image_url" : "/media/images/pics/finalized.png",
        "discount_price": null
        
    },
    {
        "name" : "Jacket", 
        "price" : 1200,
        "image_url" : "/media/images/pics/finalized.png",
        "discount_price": null
    }
]

async function loadDataFromMerch(){
    const container = document.getElementById('merch-list');
    const viewBtn = document.getElementById('visit-store');

    try{
        const url = "http://127.0.0.1:8001/";
        const response = await fetch(url+'featured/');
        if (!response.ok){
            throw new Error("Error occured as the server was unreachable.")
        }
        const data = await response.json();
        if (data.length > 0){
            viewBtn.href = url + "/products";
            container.innerHTML = data.map(product => `
            <a href="${product.product_url}"> 
            <div class="product-card">
                <img src="${product.image_url}" alt="${product.name}">
                <h3>${product.name}</h3>
                <strike>Rs. ${product.discount_price}</strike>
                <p>Rs. ${product.price}</p>
            </div>
            </a>
            `).join("")   ; 
        }else{
            renderProducts(container, template_products, viewBtn);
        }
           
    }catch(e){
        console.log("error occured", e);
        renderProducts(container, template_products, viewBtn);
    }
}

loadDataFromMerch();

function renderProducts(container, data, viewBtn){
    const sloganEnd = document.getElementById('slogan');
    const notice = document.getElementById('notice');
    viewBtn.href = instapage;
    notice.innerText = "* Please note that price and products may vary from what is shown here! Thank you!"
    sloganEnd.innerText = "Get your premium fit from Sappfit Wear @sappfitwear";
    container.innerHTML = data.map(product => `
        <a href="${product.product_url}"> 
        <div class="product-card">
            <img src="${product.image_url}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>Rs. ${product.price}</p>
        </div>
        </a>
    `).join('');
}