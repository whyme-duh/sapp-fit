let intro = document.querySelector('.intro');
let introheader = document.querySelector('.intro-header');
let logos = document.querySelectorAll('.logo');

window.addEventListener("DOMContentLoaded", ()=>{
    logos.forEach((logo, index) => {
        setTimeout(()=>{
            setTimeout(()=>{
                logo.classList.add('add');
                
            }, (index+1) * 400)
        })
        setTimeout(()=>{
            logos.forEach((logo, index)=>{
                setTimeout(()=>{
                    logo.classList.remove('add');
                    logo.classList.add('fade');
                }, (index+1) * 50)
            })
        }, 2000)

        setTimeout(() =>{
            intro.style.top = "-100vh";
        }, 2300)
    })
})


// changing the background of the navbar

const header = document.querySelector('.header');

window.onscroll = () =>{
    if(window.scrollY>100){
        header.style.background ="#CCB288";
    }
    else{
        header.style.background = "transparent";
    }
}

// responsive navbar

const responsiveNav = document.getElementById('responsive');

function navFunction(){
    if(responsiveNav.classList == "right-side"){
        responsiveNav.className = "right-side-responsive";
    }
    else{
        responsiveNav.className = "right-side";
    }
}


const hiddenClass = document.querySelectorAll('.hidden');
const childElemets = document.querySelectorAll('.child');

const observer = new IntersectionObserver((entries)=>{
    entries.forEach((e) =>{
        if(e.isIntersecting){
            e.target.classList.add('show');
            e.target.classList.add('showChild');
        }
    })
})

hiddenClass.forEach((el)=> observer.observe(el));
childElemets.forEach((el)=> observer.observe(el));


