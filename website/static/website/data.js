const instapage = "https://www.instagram.com/sappfitwear/";

const template_products = [
    {
        "name" : "Sports Bra", 
        "price" : 2200,
        "image_url": "https://instagram.fktm20-1.fna.fbcdn.net/v/t51.82787-15/748194954_17945564322249237_7813366282811011335_n.jpg?stp=dst-jpg_e35_p1080x1080_tt6&_nc_cat=108&ig_cache_key=Mzk0MTE4NjIwOTk3NjI4NjI3Nw%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0ueHBpZHMuMzAyNC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=xaMZ5w9ynBkQ7kNvwGJKSgl&_nc_oc=AdrRqVDbspLlnaLPOMsOffmy7S52OV56ickmJmxaqpnxeOCkyMYCo288zZcrwsXJzHAU6wPokTd5c0SfMEOeBj31&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=instagram.fktm20-1.fna&_nc_gid=bsLLV8VEQO5fEpFsDTlu8g&_nc_ss=7a22e&oh=00_AQBuckfsL-RDINAws10jrHvzlphrcQCvs-9KVL3vd7mZRw&oe=6A6C06C1",
        "link": "https://www.instagram.com/p/Dax6KZBkxkH/?img_index=1"
    },
    {
        "name" : "Tops and Skirt", 
        "price" : 2500,
        "image_url" : "https://instagram.fktm20-1.fna.fbcdn.net/v/t51.82787-15/656288978_18085131119521658_9039585092772422620_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=103&ig_cache_key=MzQyMTE1OTg3OTM1NTMzODc5MQ%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0ueHBpZHMuMTQ0MC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=FSPWY68wxOMQ7kNvwG4Bwvg&_nc_oc=AdpqXmTlUlxj9FrKsVzI9d5WUvGAJDl2MFqeATj_jP2k8at-QUAVo-AYzesFy4GO_5NzUXitPOC_j3pkm04mOdkb&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=instagram.fktm20-1.fna&_nc_gid=7H6Udv7Itzoas04yzs7JIw&_nc_ss=7a22e&oh=00_AQCzZYtqgQ2FezsT8EcScb9m-TrlMtO9g8jL8HaOAfiXuw&oe=6A6C1348",
        "link": "https://www.instagram.com/p/C96ZsqnSTx7/?img_index=1"        
    },
    {
        "name" : "Leggins", 
        "price" : 2500,
        "image_url" : "https://instagram.fktm20-1.fna.fbcdn.net/v/t51.82787-15/655224885_18087275213184663_9131003065801918370_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=102&ig_cache_key=MzQwNzA0NzU0Mzk0NjM4OTY4Ng%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNBUk9VU0VMX0lURU0ueHBpZHMuMTQ0MC5zZHIucmVndWxhcl9waG90by5DMyJ9&_nc_ohc=yy18kIJTDgIQ7kNvwEzrKOJ&_nc_oc=Adr3SjGJ4V9HVy08bZeNtK6y6jFxy-i_r0Mu-7La-MmvkqKKi4yFkO1gp-mR2XqWXM0k2Bg5M03Ja0DX9MMYLhzj&_nc_ad=z-m&_nc_cid=0&_nc_zt=23&_nc_ht=instagram.fktm20-1.fna&_nc_gid=7H6Udv7Itzoas04yzs7JIw&_nc_ss=7a22e&oh=00_AQBcwXYPHs9WH-KZ5Ga_k2wNFjYkEaC-eSvZXts5HIvS3g&oe=6A6BEE25",
        "link": "https://www.instagram.com/p/C9IQ7IsSfu0/?img_index=1"
    }
]

async function loadDataFromMerch(){

    const isDebug = JSON.parse(document.getElementById('django-debug-mode').textContent);
    var url = "http://127.0.0.1:8001/";

    if (!isDebug){
        var url = "https://sappfitmerch.pythonanywhere.com/";

    }

    const container = document.getElementById('merch-list');
    const viewBtn = document.getElementById('visit-store');

    try{
        const response = await fetch(url + "featured/");
        console.log("response", response);
        if (!response.ok){
            throw new Error("Error occured as the server was unreachable.")
        }
        const data = await response.json();
        if (data.length > 0 || data.length <= 3){
            viewBtn.href = url + "products";
            container.innerHTML = data.map(product => `
            <a href="${product.product_url}" class="product-card"> 
                <img src="${product.image_url}" alt="${product.name}">
                <h3>${product.name}</h3>
                <strike>Rs. ${product.discount_price}</strike>
                <p>Rs. ${product.price}</p>
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
       
        <a href="${product.link}" class="product-card">
            <img src="${product.image_url}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>Rs. ${product.price}</p>
        </a>
        
    `).join('');
}