/*--------loader script-----------*/
$(function(){
    let questionNo = 0;
    let keys = Object.keys(questions);
    let data = {};
    
    renderNextQuestion();

    $(document.body).on('click',"label.element-animation",function (e) {
    //ripple start
        var parent, ink, d, x, y;    
        

        parent = $(this);

        if(parent.find(".ink").length === 0)
            parent.prepend("<span class='ink'></span>");
            
        ink = parent.find(".ink");
        ink.removeClass("animate");
        
        if(!ink.height() && !ink.width())
        {
            d = Math.max(parent.outerWidth(), parent.outerHeight());
            ink.css({height: "100px", width: "100px"});
        }
        
         x = e.pageX - parent.offset().left - ink.width()/2;
        y = e.pageY - parent.offset().top - ink.height()/2;
        
        ink.css({top: y+'px', left: x+'px'}).addClass("animate");
    //ripple end

        // Store the answer
        data[keys[questionNo]] = $(this).parent().find('input:radio').val();

        setTimeout(function(){
            $('#quiz').fadeOut();
            questionNo++;
            if((questionNo) + 1 > keys.length){

                $.ajax({
                    url: "",
                    type: "POST",
                    data: JSON.stringify(data),
                    contentType: 'application/json; charset=utf-8',
                    dataType: "json",
                    complete: () => {
                        alert('Poll completed');
                        window.location.replace(window.location.origin);
                    }
                });



                $('label.element-animation').unbind('click');
            } else {
                $('#qid').html(questionNo + 1);
                $('input:radio').prop('checked', false);
                setTimeout(function(){
                    $('#quiz').show();
                    // Delete previous answer options
                    $('ul li').remove();

                    // Render the next question
                    renderNextQuestion();
                }, 1500);
            }
        }, 1000);

    })

    function renderNextQuestion() {
        // First question pre-loading
        $('#question').html(keys[questionNo]);
        $.each(questions[keys[questionNo]], (i, data) => {
            // Clone of answer option
            $('ul').append(document.querySelector('template').content.cloneNode(true));
            // Assign value to answer option
            $($('ul li:last-child').find('label')).html(data[0]);
            // Assign answer option id
            $($('ul li:last-child').find('input:radio')).attr('value', data[1]);
            // Assign unique id
            $($('ul li:last-child').find('input:radio')).attr('id', 'question' + i);
            $($('ul li:last-child').find('label')).attr('for', 'question' + i);
        });
    }
});

