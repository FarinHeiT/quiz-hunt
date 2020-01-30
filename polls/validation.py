from models import Poll


def validate_creation(data):
    """ Checks the structure of JSON data from front-end """

    if ('title' not in data.keys() or
            'questions' not in data.keys() or
            len(data['title']) <= 5 or
            len(data['title']) > 70 or
            len(data['questions']) < 1
    ): return False

    if 'description' in data:
        if len(data['description']) > 150:
            return False

    for question, answer_options in list(data['questions'].items()):
        if (len(question) <= 5 or
                len(answer_options) < 2 or
                len(answer_options) > 5
        ): return False

        for answer_option in answer_options:
            if len(answer_option) <= 2:
                return False

    return True


def validate_taking(data, sample):
    # Check count of question
    if len(data) != len(sample):
        return False

    for question, answer in data.items():
        # Check if the question is present
        if question not in sample:
            return False

        # Check if answer option if present
        if int(answer) not in [i[1] for i in sample[question]]:
            return False

    return True
