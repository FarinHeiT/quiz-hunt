def validate(data):
    """ Checks the structure of JSON data from front-end """

    if ('title' not in data.keys() or
        'questions' not in data.keys() or
        len(data['title']) <= 5 or
        len(data['questions']) < 1
    ): return False

    for question, answer_options in list(data['questions'].items()):
        if (len(question) <= 5 or
            len(answer_options) < 2 or
            len(answer_options) > 5
        ): return False

        for answer_option in answer_options:
            if len(answer_option) <= 2:
                return False
    return True
