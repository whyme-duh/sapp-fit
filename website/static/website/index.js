// responsive navbar

function navFunction() {
    var x = document.getElementById("responsive");
    if (x.className === "right-side") {
        x.className += " right-side-responsive";
    } else {
        x.className = "right-side";
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


document.addEventListener("DOMContentLoaded", function() {
    const track = document.getElementById('testimonial-track');
    const gap = parseFloat(getComputedStyle(track).gap) || 0;
    
    if (!track || track.children.length === 0) return;

    // check whether the testimonials is sliding automatically or not
    let isAutoPlaying = true; 

    setInterval(() => {
        // if cards don't overflow the container, or user is hovering, do nothing!
        if (track.scrollWidth <= track.clientWidth || !isAutoPlaying) return;

        const card = track.querySelector('.testinomial-card');
        const scrollAmount = card.offsetWidth + gap; 
        // checks if we have hit the very end of the scroll track
        // (Math.ceil fixes a bug where zoomed screens return fractional pixels)
        if (Math.ceil(track.scrollLeft + track.clientWidth) >= track.scrollWidth) {
            // Slide smoothly all the way back to the beginning
            track.scrollTo({ left: 0, behavior: 'smooth' }); 
        } else {
            // Slide to the next card
            track.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        }
    }, 5000); 

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


// this is for stats counter
document.addEventListener("DOMContentLoaded", function () {
    const statsSection = document.querySelector('.stats-container');
    const counters = document.querySelectorAll('.counter');
    let animated = false;

    const runCounters = () => {
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            let count = 0;
            const increment = target / 50; 

            const updateCount = () => {
                count += increment;
                if (count < target) {
                    counter.innerText = Math.ceil(count);
                    setTimeout(updateCount, 30);
                } else {
                    counter.innerText = target;
                }
            };
            updateCount();
        });
    };

    const observerOptions = {
        root: null,
        threshold: 0.3 // Triggers when 30% of the container is visible
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !animated) {
                // Fade in all stat elements
                document.querySelectorAll('.reveal').forEach(el => el.classList.add('active'));
                // Run the numbers up
                runCounters();
                animated = true;
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    if (statsSection) {
        observer.observe(statsSection);
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const observerOptions = {
        root: null,
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                // Also trigger child elements if it's the about-content wrapper
                if(entry.target.classList.contains('text-reveal-right')) {
                    entry.target.classList.add('active');
                }
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all directional animation elements
    const animatedElements = document.querySelectorAll('.reveal-top-init, .reveal-down-init, .reveal-side-init, .text-reveal-right, .about');
    animatedElements.forEach(el => observer.observe(el));
});