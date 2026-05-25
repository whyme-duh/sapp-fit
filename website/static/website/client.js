
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