document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("aiForm");
    const formContainer = document.querySelector(".request-container"); 
    const skeletonLoader = document.getElementById("skeleton-loader"); 

    if (form) {
        form.addEventListener("submit", function(event) {
            if (event.submitter && event.submitter.value === "ai_preview") {
                // this stops the normal form submission
                event.preventDefault(); 
                
                
                formContainer.style.display = "none";
                skeletonLoader.style.display = "block";
                
                //package the form data
                const formData = new FormData(form);
                formData.append('action', 'ai_preview'); 

                // sends the information to backend in background
                fetch(window.location.href, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest' // telling django that it is the ajax request
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        window.location.href = data.redirect_url;
                    } else {
                        window.location.href = data.error_redirect_url;
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    window.location.reload();

                });
            }
        });
    }

    const officialPlanBtn = document.getElementById('official-plan');
    const aiPlanBtn = document.getElementById('ai-plan')


    officialPlanBtn.addEventListener('click', function (){
        const officialPlanForm = document.getElementById('official-plan-form');
        const aiPlanForm = document.getElementById('ai-preview-form');
        officialPlanForm.style.display = "flex";
        aiPlanForm.style.display = "none";
        this.disabled = true;
        aiPlanBtn.disabled = false;
    })

    aiPlanBtn.addEventListener('click', function(){

        const officialPlanForm = document.getElementById('official-plan-form');
        const aiPlanForm = document.getElementById('ai-preview-form');
        officialPlanForm.style.display = "none";
        aiPlanForm.style.display = "flex";
        this.disabled = true;
        officialPlanBtn.disabled = false;
    })
});



