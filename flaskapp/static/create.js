function addStep() {
    const stepsList = document.getElementById('steps_list');
    const stepCount = stepsList.children.length + 1;

    const listItem = document.createElement('li');
    listItem.classList.add('step-item');

    const imagePreview = document.createElement('img');
    imagePreview.id = `preview_${stepCount}`;
    imagePreview.src = '/static/banner.png';
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.style.display = 'none';

    imagePreview.addEventListener('click', function() {
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        if (fileInput.files && fileInput.files[0]) {
            imagePreview.src = URL.createObjectURL(fileInput.files[0]);
        }
    });

    listItem.appendChild(fileInput);
    listItem.appendChild(imagePreview);

    const stepLabel = document.createElement('label');
    stepLabel.textContent = `Step ${stepCount}:`;
    listItem.appendChild(stepLabel);

    const stepInput = document.createElement('input');
    stepInput.type = 'text';
    stepInput.name = `step_${stepCount}`;
    stepInput.placeholder = 'Describe the step...';
    listItem.appendChild(stepInput);

    stepsList.appendChild(listItem);
}


function submitProcedure() {
    
}