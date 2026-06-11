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
                intro.style.top = "-200vh";
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




const modal = document.getElementById('modal-container');
const form = document.getElementById('clientForm');
const modalTitle = document.getElementById('modalTitle');
const submitBtn = document.querySelector('.modal-footer .btn-primary');

function openAddModal() {
    form.reset(); 
    modal.style.display = 'flex';
    // document.body.style.overflow = "hidden";
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
    // document.body.style.overflow = "";

}

window.onclick = function(event) {
    if (event.target == modal) {
        closeModal();
        
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const track = document.getElementById('testimonial-track');
    
    if (!track || track.children.length === 0) return;

    // check whether the testimonials is sliding automatically or not
    let isAutoPlaying = true; 

    setInterval(() => {
        // if cards don't overflow the container, or user is hovering, do nothing!
        if (track.scrollWidth <= track.clientWidth || !isAutoPlaying) return;

        const card = track.querySelector('.testinomial-card');
        const scrollAmount = card.offsetWidth + 16; 
        // checks if we have hit the very end of the scroll track
        // (Math.ceil fixes a bug where zoomed screens return fractional pixels)
        if (Math.ceil(track.scrollLeft + track.clientWidth) >= track.scrollWidth) {
            // Slide smoothly all the way back to the beginning
            track.scrollTo({ left: 0, behavior: 'smooth' }); 
        } else {
            // Slide to the next card
            track.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        }
    }, 10000); 

    // pausing when the mouse enters or leaves the testimonial cards
    // for desktop
    track.addEventListener('mouseenter', () => isAutoPlaying = false);
    track.addEventListener('mouseleave', () => isAutoPlaying = true);
    
    // For Mobile (Touch)
    track.addEventListener('touchstart', () => isAutoPlaying = false);
    track.addEventListener('touchend', () => {
        setTimeout(() => isAutoPlaying = true, 2000);
    });
});

// code below is for the custom service request page
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("plan-request-form");
    const loadingScreen = document.getElementById("ai-loading-screen");

    if (form) {
        form.addEventListener("submit", function(event) {
            const buttonClicked = event.submitter;

            if (buttonClicked && buttonClicked.value === "ai_preview") {
                // Show the overlay
                loadingScreen.style.display = "flex";
                
                buttonClicked.disabled = true;
            }
        });
    }
});
