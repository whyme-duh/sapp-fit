
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('search-input');
    const clientRows = document.querySelectorAll('.client-row');
    searchInput.addEventListener('input',function(e){
        const searchTerm= e.target.value.toLowerCase().trim();

        clientRows.forEach(row =>{
            const nameElement = row.querySelector('.client-name');

            if (nameElement){
                const clientName = nameElement.innerText.toLowerCase();
                if (clientName.includes(searchTerm)){
                    row.style.display = '';
                }else{
                    row.style.display = 'none';
                }
            }
        })

    })
});


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


function deleteModalFunction(option, button){
    const deleteOption = document.getElementById(`delete-option-${button.dataset.id}`);
    const actionOption = document.getElementById(`action-${button.dataset.id}`);
    if (deleteOption){
        deleteOption.style.display = "flex";
        actionOption.style.display = "none";
    }

    if (option == "closeModal"){
        actionOption.style.display = "flex";
        deleteOption.style.display = "none";
        console.log(actionOption, deleteOption);
    }

    
    
}
