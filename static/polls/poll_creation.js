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
        }
    });

    // Create poll
    $('#create-poll').click(() => {
        if (validateOptions() === true) {
            addQuestion();
            data['title'] = $('#title-input').val();

            $.ajax({
                url: "",
                type: "POST",
                data: JSON.stringify(data),
                contentType: 'application/json; charset=utf-8',
                dataType: "json",
                complete: (r) => {
                    if (r.responseJSON["status"] === 'Success') {
                        window.location.replace(window.location.origin);
                    } else if (r.responseJSON["status"] === 'TitleAlreadyExists') {
                        alert('Poll with given name already exists...')
                    } else if (r.responseJSON['status'] === "ValidationError") {
                        alert('There is an validation error - please check your input.')
                    }


                }
            });

        }
    });

    // Open settings modal
    $('#settings').click(() => {
        $('#settingsModal').modal('show');
    });


    $('#save-settings').click(() => {
       data['description'] =  $('#description').val();
       $('#settingsModal').modal('hide');
    });

    $('#upload_image').click( () => {
        const fd = new FormData();
        const files = $('#file')[0].files[0];
        fd.append('file',files);

        $.ajax({
            url: "image_upload",
            type: "POST",
            data: fd,
            contentType: false,
            processData: false,
            statusCode: {
                413: (r) => {
                    alert('Image size should me less than 5mb');
                }
            },
            complete: (r) => {
                if (r.responseJSON["status"] === 'Success') {
                    let elem = `<img width="320" height="180" src='${location.origin}/files/${r.responseJSON["filename"]}'>`
                    if ($('.modal-body > img').length === 0) {
                        $('.modal-body').append(elem)
                    } else {
                        $('.modal-body > img').attr('src', `${location.origin}/files/${r.responseJSON["filename"]}`)
                    }
                    data['filename'] = r.responseJSON["filename"];
                    $('#upload_image').attr('disabled', '')
                    // // Wait 5 sec before loading another image
                    // setTimeout(() => $('#upload_image').removeAttr('disabled'), 5000)
                }
            }
        });
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

