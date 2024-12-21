function validateForm(event, pointValue) {
    const englishPattern = /^[A-Za-z\s]+$/;

    if (!englishPattern.test(pointValue)) {
        alert('Пожалуйста, используйте только английские буквы без чисел и других символов.');
        event.preventDefault();
        return false;
    }

    return true;
}

function validateAllForms(event) {
    event.preventDefault();

    const startPoint = document.getElementById('start_point').value.trim();
    const endPoint = document.getElementById('end_point').value.trim();

    let html = document.getElementsByClassName('point');
    let length = html.length;

    for (let i = 0; i < length; ++i) {
        let result = validateForm(event, html[i].value.trim());
        if (!result) {
            return false;
        }
    }

    if (startPoint === '' || endPoint === '') {
        alert('Пожалуйста, заполните оба поля.');
        event.preventDefault();
        return false;
    }

    if (startPoint === endPoint) {
        alert('Начальная и конечная точки не могут совпадать.');
        event.preventDefault();
        return false;
    }

    document.getElementById('requestForm').addEventListener('submit', function (event) {

        const formData = new FormData(this);


        const daysSelect = this.querySelector('#days');
        const daysValue = daysSelect.value;


        let values = {
            "points": [],
            "days": parseInt(daysValue)
        };

        const inputs = this.querySelectorAll('.point');

        inputs.forEach(input => {
            const value = input.value.trim();
            if (value) {
                values['points'].push(value);
            }
        });

        console.log(values.points);

        fetch('/eval', {
            method: 'POST',
            body: JSON.stringify(values),
            headers: {
                'Content-Type': 'application/json'
            },
        }).then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Network response was not ok');
        })
            .then(html => {
                document.open();
                document.write(html);
                document.close();
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });


    return false;
}


function addIntermediatePoint() {
    const container = document.getElementById('intermediate_points_container');
    const input = document.createElement('input');
    input.type = 'text';
    input.name = 'intermediate_point';
    input.className = 'point';
    input.placeholder = 'Введите промежуточную точку';
    input.required = true;
    input.pattern = '[A-Za-z\s]+';
    input.title = 'Пожалуйста, используйте только английские буквы.';
    container.appendChild(input);
}