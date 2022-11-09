from learning_environment.its.base import Json5ParseException

class PictureDescription():
    """A single choice task."""

    template = 'learning_environment/partials/pic_des.html'

    @classmethod
    def check_json5(cls, task_json5, task_num=0):
        if "answer" not in task_json5:
            raise Json5ParseException(
                'Field "answer" is missing for short answer task task (task {})'.format(task_num))
        if "url" not in task_json5:
            raise Json5ParseException(
                'Field "url" is missing for short answer task task (task {})'.format(task_num))

    @classmethod
    def get_content_from_json5(cls, task_json5, task_num=0):
        return task_json5['answer'], task_json5['url']

    def __init__(self, task):
        self.task = task

    def analyze_solution(self, solution):
        context = {}
        analysis = {}

        given_answer = solution.get('answer', None)
        if self.task.content[0] == given_answer:
            analysis['solved'] = True
        else:
            analysis['solved'] = False

        context['mode'] = "result"  # display to try again
        return (analysis, context)

