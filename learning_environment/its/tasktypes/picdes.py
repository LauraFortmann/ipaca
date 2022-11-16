from learning_environment.its.base import Json5ParseException
import spacy


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
        
        #get labels
        labels = self.task.content[0]
        labels = str(labels).split(",")
        labels_remove_white=[]
        for label in labels:
            labels_remove_white.append(label.replace(" ", ""))
        print("labels", labels_remove_white)

        #get answer and extract the nouns
        given_answer = solution.get('answer', None)
        nlp = spacy.load("en_core_web_sm")
        answer_parsed = nlp(given_answer)
        print(answer_parsed)
        
        answer_only_nouns = []
        for noun in answer_parsed.noun_chunks:
           # answer_only_nouns.append(noun.split(" ")[-1])
            answer_only_nouns.append(noun)
        
        print(answer_only_nouns)
        extracted_nouns = []
        for noun_phrases in answer_only_nouns:
            extracted_nouns.append(str(noun_phrases).split(" ")[-1])

        print(extracted_nouns)
        mentioned_nouns = []
        for noun in extracted_nouns:
            for l in labels_remove_white:
                print("noun: ", noun, type(noun), "label: ", l, type(l))
                print(noun == l)
                if noun == l:
                    if noun not in mentioned_nouns:
                        mentioned_nouns.append(noun)

        print("Nouns mentioned: ", mentioned_nouns)
        context = {}
        analysis = {}

        
        if len(mentioned_nouns)>=4:
            analysis['solved'] = True
        else:
            analysis['solved'] = False

        context['mode'] = "result"  # display to try again
        context['mentioned']=len(mentioned_nouns)
        context['labels']=labels
        return (analysis, context)

