$(function() {
    let answerOptionsCount = 1;
    let data = {'questions': {}};

    // Add answer option
    $('#add-option').click(() => {
        // Clone of answer option
        $('ul').append($('template').html());
        // Assign answer option id
        $($('ul li:last-child').find('input:text')).attr('placeholder', `Enter answer option №${answerOptionsCount}`);
        // Assign unique id
        $($('ul li:last-child').find('input:text')).attr('id', 'title-option' + answerOptionsCount);
        answerOptionsCount++;
    });

    // Add question
    $('#add-question').click(() => {
        if (validateOptions() === true) {
            addQuestion();
            clearFields();
            console.log(data)
        }
    });

    // Create poll
    $('#create-poll').click(() => {
        if (validateOptions() === true) {
            addQuestion();
            clearFields();
            data['title'] = $('#title-input').val();

            $.ajax({
                url: "",
                type: "POST",
                data: JSON.stringify(data),
                contentType: 'application/json; charset=utf-8',
                dataType: "json",
                complete: (r) => {
                    alert(r.responseJSON['status'])
                    window.location.replace(window.location.origin);
                }
            });

        }
    });

    // Open settings modal
    $('#settings').click(() => {
        $('#settingsModal').modal('show');
        console.log(data)
    });


    $('#save-settings').click(() => {
       data['description'] =  $('#description').val();
       $('#settingsModal').modal('hide');
    });


    function addQuestion() {
        data['questions'][$('#title-question').val()] = getAnswerOptions();
    }

    function getAnswerOptions() {
        let options = [];
        $.each($('.answer-option'), (i, input) => {
            options.push(input.value)
        });
        return options
        }

    function clearFields() {
        $('.answer-item').remove();
        $('#title-question').val('');
        answerOptionsCount = 1;
    }

    function validateOptions() {
        let r = true;
        // Check question title
        r = $('#title-question').val().length > 5 && $('#title-question').val().length < 100;
        // Check poll title
        r = $('#title-input').val().length > 5 && $('#title-input').val().length < 70;
        // Check poll description
        r = $('#description').val().length < 70;

        // 5 Answer options max, 2 min
        if ($('.answer-option').length > 5) {
            alert('A question can have 5 answer options max');
            r = false;
        } else if ($('.answer-option').length < 2){
            alert('A question must have at least 2 answer options');
            r = false;
        }

        // Check each answer option
        $.each($('.answer-option'), (i, input) => {
            if (input.value.length <= 3) {
                alert('Please fill all information...')
                r = false;
                return false
            }
        });
        return r;
    }
});

