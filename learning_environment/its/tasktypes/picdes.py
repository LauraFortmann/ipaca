from learning_environment.its.base import Json5ParseException
import spacy
import nltk
from nltk.corpus import wordnet
import string
from textblob import Word


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
        penalties = 0
        error_tense=0
        error_spelling = 0
        wrong_tense = []
        #extract verb tense
        words = nltk.word_tokenize(solution.get('answer', None))
        words1 = nltk.pos_tag(words)
        pos=[]
        for w in words1:
            pos.append(w[1])
        print(pos)
        for w in words1:
            if w[1] == 'VBD' or w[1] =='VBN':
                penalties += -0.5
                error_tense += 1
                wrong_tense.append(w[0])

        #penalities for spelling mistakes
        
        #for each spelling mistake -0.5
        given_answer = solution.get('answer', None)
        given_answer_single = given_answer.split(" ")
        given_answer_without_punctuation =[]
        for ans in given_answer_single:
            given_answer_without_punctuation.append(ans.translate(str.maketrans('', '', string.punctuation)))
        
        corrected =[]
        false_words=[]
        corrected_words=[]
        print("before",given_answer_without_punctuation)
        for answe in given_answer_without_punctuation:
            word = Word(answe)
            result = word.spellcheck()
            if result[0][0] !=answe:
                false_words.append(answe)
                error_spelling +=1
                corrected_words.append(result[0][0])
                penalties -= 0.5
                # if noun is not too far away from real word we correct it 
                if result[0][1] >=0.95:
                    corrected.append(result[0][0])
            else: corrected.append(answe)
            print(answe, result[0][0])
        print(penalties)
        print("after:", corrected)
        

        nltk.download("wordnet")
        #get labels
        labels = self.task.content[0]
        labels = str(labels).split(",")
        labels_remove_white=[]
        for label in labels:
            labels_remove_white.append(label.replace(" ", ""))
        print("labels", labels_remove_white)


        synonyms = {}
        # #synonym first label:
        for sing_label in labels_remove_white:
            synonyms_single=[]
            for syn in wordnet.synsets(sing_label):
                for lemm in syn.lemmas():
                    synonyms_single.append(lemm.name())
            synonyms[sing_label]=synonyms_single 
      
        given_answer = ' '.join(str(e) for e in corrected)
        print("given",given_answer)
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
        not_mentioned_nouns = []
        mentioned_labels=[]

        for noun in extracted_nouns:
            for l in labels_remove_white:
               
                if noun == l or noun in synonyms.get(l):

                    if noun not in mentioned_nouns:
                        mentioned_nouns.append(noun)
                        mentioned_labels.append(l)
        
        for l in labels_remove_white:
            if l not in mentioned_labels:
                not_mentioned_nouns.append(l)
       

        context = {}
        analysis = {}

        
        if len(mentioned_nouns)>=4:
            analysis['solved'] = True
        else:
            analysis['solved'] = False

        context['mode'] = "result"  # display to try again
        context['mentioned']=len(mentioned_nouns)
        context['not_mentioned_nouns'] = not_mentioned_nouns
        context['mentioned_nouns'] = mentioned_nouns
        context['labels']=labels
        context['false_words']= false_words
        context['corrected_words']= corrected_words
        context['error_tense']= error_tense
        context['error_spelling']= error_spelling
        context['spelling_wrong'] = error_spelling >0
        context['wrong_tense'] = wrong_tense
        context['answer'] = given_answer
        return (analysis, context)

