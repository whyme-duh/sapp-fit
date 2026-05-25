let intro = document.querySelector('.intro');
let introheader = document.querySelector('.intro-header');
let logos = document.querySelectorAll('.logo');

window.addEventListener("DOMContentLoaded", ()=>{   
    let splashScreenCount = parseInt(localStorage.getItem('splashScreenCount')) || 0;

    if (splashScreenCount == 1){
        intro.style.display = "none";
    } 
    else{
        localStorage.setItem('splashScreenCount', splashScreenCount + 1);
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
    }
})



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


const quotesContainer = document.querySelector('.quotes-container');


const modal = document.getElementById('modal-container');
const form = document.getElementById('clientForm');
const modalTitle = document.getElementById('modalTitle');
const submitBtn = document.querySelector('.modal-footer .btn-primary');

function openAddModal() {
    form.reset(); 
    modal.style.display = 'flex';
}

function openEditModal(button) {
    const data = button.dataset;

    document.getElementById('id_name').value = data.name;
    document.getElementById('id_age').value = data.age;
    document.getElementById('id_gender').value = data.gender;
    document.getElementById('id_started_training_from').value = data.date;
    document.getElementById('id_services').value = data.service;
    document.getElementById('id_status').value = data.status;
    document.getElementById('id_any_problem').value = data.problem;

    form.action = `/clients/${data.id}/edit/`; 
    
    modalTitle.innerText = "Edit Client Details";
    submitBtn.innerText = "Update Details";
    
    modal.style.display = 'flex';
}

function closeModal() {
    modal.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == modal) {
        closeModal();
    }
}