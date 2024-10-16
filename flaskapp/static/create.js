function addStep() {
    const stepsList = document.getElementById('steps_list');
    const stepCount = stepsList.children.length + 1;

    const listItem = document.createElement('li');
    listItem.classList.add('step-item');

    const imagePreview = document.createElement('img');
    imagePreview.id = `preview_${stepCount}`;
    imagePreview.src = '/static/banner.png';
    imagePreview.classList.add('step-image');
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.style.display = 'none';

    imagePreview.addEventListener('click', function () {
        fileInput.click();
    });

    fileInput.addEventListener('change', function () {
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
    stepInput.classList.add('step_entry');
    stepInput.placeholder = 'Describe the step...';
    listItem.appendChild(stepInput);

    const toolsList = document.createElement('ul');
    toolsList.classList.add('tools-list');
    toolsList.style.listStyle = "none";

    const tools = Array.from(document.getElementsByClassName('tools_entry')).map(input => input.value); // Example tools

    tools.forEach(tool => {
        const toolItem = document.createElement('li');
        toolItem.classList.add('tool-item');

        const toolCheckbox = document.createElement('input');
        toolCheckbox.type = 'checkbox';
        toolCheckbox.name = `tool_${stepCount}`;
        toolCheckbox.value = tool;

        const toolLabel = document.createElement('label');
        toolLabel.textContent = tool;

        toolItem.appendChild(toolCheckbox);
        toolItem.appendChild(toolLabel);
        toolsList.appendChild(toolItem);
    });

    listItem.appendChild(toolsList);
    stepsList.appendChild(listItem);
}

function addTool() {
    const toolsList = document.getElementById('tools_list');
    const newTool = document.createElement('li');
    newTool.style.listStyleType = 'none';
    const toolInput = document.createElement('input');
    toolInput.type = 'text';
    toolInput.classList.add('tools_entry');
    toolInput.required = true;
    newTool.appendChild(toolInput);
    toolsList.appendChild(newTool);
}


async function submitProcedure() {
    console.log('Submitting procedure...');
    console.log('Procedure Name: ' + document.getElementById("procedure_name").value);
    current_step_data = {};
    // get img data and step_entry for each step
    const steps = Array.from(document.getElementsByClassName('step_entry')).map(input => input.value);
    console.log("IMAGES: ");
    console.log(document.getElementsByClassName('step-image'));
    const step_images = document.getElementsByClassName('step-image');

    for (let i = 0; i < step_images.length; i++) {
        console.log(step_images[i].
            src);
    }
    
    for (let i = 0; i < steps.length; i++) {
        current_step_data[i] = { "img": step_images[i].src, "step_description": steps[i], "tools_used": tool_usage[i] };
    }

    for (let step in current_step_data) {
        console.log(current_step_data[step]);
    }


    const formData = {
        procedure_name: document.getElementById('procedure_name').value,
        part: document.getElementById('part').value,
        toolsList: Array.from(document.getElementsByClassName('tools_entry')).map(input => input.value),
        item: document.getElementById('item').value,
        step_data: current_step_data
    };

    if (formData.part == "" || formData.step_data.length == 0, formData.item == "") {
        const errorPopup = document.createElement('div');
        errorPopup.textContent = "Please fill out all fields";
        errorPopup.id = 'error-popup';

        document.body.appendChild(errorPopup);

        setTimeout(() => {
            document.body.removeChild(errorPopup);
        }, 3000);
        return;
    }

    console.log("item: " + formData.item);

    console.log("Parts: " + formData.part);

    console.log("Tools:");
    for (let tool of formData.toolsList) {
        console.log(tool);
    }

    console.log(formData)
    const result = await fetch('/create_procedure', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });

    if (result.ok) {
        console.log('Procedure created successfully!');
    } else {
        console.error('Failed to create procedure');
    }
}

function setTools() {
    // make the tools uneditable
    const tools = Array.from(document.getElementsByClassName('tools_entry'));
    for (let tool of tools) {
        tool.readOnly = true;
        tool.style.border = "1px solid #ccc";
        tool.addEventListener('mouseover', function () {
            tool.style.border = "1px solid #000";
        });
        tool.addEventListener('mouseout', function () {
            tool.style.border = "1px solid #ccc";
        });
    }

    const newStepButton = document.getElementById('newStepButton');
    newStepButton.style.display = 'flex';

    const addToolButton = document.getElementsByClassName('tool_button');
    for (let button of addToolButton) {
        button.style.display = 'none';
    }

}