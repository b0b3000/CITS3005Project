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
    current_step_data = {};
    // get img data and step_entry for each step
    const steps = Array.from(document.getElementsByClassName('step_entry')).map(input => input.value);

    const step_images = document.getElementsByClassName('step-image');

    const tools_lists = document.getElementsByClassName("tools-list")
    tool_usage = {};
    console.log(tools_lists);
    console.log("Getting used tools");
    for (let i = 0; i < tools_lists.length; i++) {
        let tool_list_items = tools_lists[i].getElementsByClassName("tool-item");
        let tools_used = [];
        console.log(tool_list_items);
        for (let tool_item of tool_list_items) {
            let checkbox = tool_item.getElementsByTagName("input")[0];
            console.log(checkbox.value);
            if (checkbox.checked) {
                console.log("Adding used tool: " + checkbox.value);
                tools_used.push(checkbox.value);
            }
        }
        console.log(tools_used)
        tool_usage[i] = tools_used
        console.log("Tool usage: " + tool_usage);
    }

    const ancestorDropdown = document.getElementById('ancestor_dropdown');
    const selectedAncestor = ancestorDropdown ? ancestorDropdown.value : "";

    console.log("Selected ancestor: " + selectedAncestor);

    for (let i = 0; i < steps.length; i++) {
        current_step_data[i] = { "img": step_images[i].src, "step_description": steps[i], "tools_used": tool_usage[i] };
    }

    for (let step in current_step_data) {
        console.log(current_step_data[step]);
    }


    const formData = {
        procedure_name: document.getElementById('procedure_name').value,
        part: document.getElementById('part').value,
        toolbox: Array.from(document.getElementsByClassName('tools_entry')).map(input => input.value),
        item: document.getElementById('item').value,
        step_data: current_step_data,
        ancestor: selectedAncestor
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

    console.log(formData)
    const result = await fetch('/edit_procedure', {
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
    const stepItems = document.getElementsByClassName('step-item');
    for (let item of stepItems) {
        item.style.display = 'flex';
    }
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

async function getPossibleAncestors() {
    const itemValue = document.getElementById('item').value;
    const result = await fetch('/get_ancestors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(itemValue)
    }).then(response => response.json())
        .then(data => {
            const ancestorButton = document.getElementById('ancestor_button');
            const dropdown = document.getElementById('ancestor_dropdown');
            if (!dropdown) {
                dropdown = document.createElement('select');
                dropdown.id = 'ancestor_dropdown';
                ancestorButton.parentNode.insertBefore(dropdown, ancestorButton.nextSibling);
            }
            dropdown.innerHTML = '';
            data.forEach(ancestor => {
                const option = document.createElement('option');
                option.value = ancestor;
                option.textContent = ancestor;
                dropdown.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching ancestors:', error));
}