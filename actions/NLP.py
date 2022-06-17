try:
    from witcher_lib import *

except:
    from Setup.witcher_lib import *

from datetime import *
import spacy
from pprint import * 
from datetime import *
import pandas as pd
from matplotlib import pyplot as plt
nlp = spacy.load("en_core_web_sm")
#from spacy.tokenizer import Tokenizer
from spacy.lang.en.stop_words import STOP_WORDS
[STOP_WORDS.add(i) for i in ["-","\n","'",'"']]
from transformers import pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

#######
#######
class Text_summary:
    """
    input : report=Text_summary( 
    TEXT : STR > your string to analysis ,
    Limit:int >  hoowmant sentence would you like to have as a summary )
    output: 
    report.Summary > the sumeized text
    )
    """
    def __init__(self,TEXT:str,Limit:4,Requirments={"Labels":[],"Keywords":[]}):
        self.STR=TEXT
        self.Limit=Limit
        self.Labels=Requirments["Labels"]
        self.Keywords=self.__VIP_KEY(Requirments["Keywords"])
        
        ###### run process:
        self.__Token()
        self.__Word_to_dict()
        self.__Sentence_list()
        self.__Summary()
        self.__NER_analysis()
        Data=[]
        
        #for ents in self.Doc.ents:
        Data=[[ent.label_,ent,1] for ent in self.Doc.ents]
            
        df=pd.DataFrame(columns=(["Label","Entity","Flag"]),data=Data)
        plt.figure(dpi=150,figsize=(8,3))
        df.groupby("Label")["Flag"].sum().T.plot(kind="pie")
        plt.ylabel("")
        plt.xlabel('Entity diversity ')
        plt.grid()
        
        PLOT_NAME="./Setup/"+"Witcher_"+str(date.today())+".png"
        try:
            plt.savefig(PLOT_NAME, bbox_inches='tight')
        except:
            plt.savefig("PLOT_NAME", bbox_inches='tight')
        self.Plot=PLOT_NAME
        
        abstract = summarizer(self.STR, max_length=250, min_length=20)
        self.abstract=abstract
        
        
        
        
        
    def __Token(self):
        self.Doc=nlp(self.STR)
    
    
    def __Word_to_dict(self):
        self.word_dict = {}
        # loop through every sentence and give it a weight
        for word in self.Doc:
            if word.is_stop==False:
                word = word.text.lower()
                if word in self.word_dict:
                    self.word_dict[word] += 1
                else:
                    self.word_dict[word] = 1
            else:
                pass
        
    def __Sentence_list(self):
        # create a list of tuple (sentence text, score, index)
        self.sents = []
        # score sentences
        self.sent_score = {}
        
        for index, sent in enumerate(self.Doc.sents):
            sent_score=0
            for word in sent:
                if word.is_stop==False:                
                    word = word.text.lower()
                    sent_score += self.word_dict[word]
                else:
                    pass
                
            self.sent_score[index] ={
                                    "Sentece":sent.text.replace("\n", " "),
                                    "Score":sent_score,
                                    "Scor/Len_sentence":sent_score/len(sent)
                                    }
            
            self.sents.append((sent.text.replace("\n", " "), sent_score/len(sent), index))
    
    def __Summary(self):
        # sort sentence by word occurrences
        STR = sorted(self.sents, key=lambda x: -x[1])
        # return top 3
        STR = sorted(STR[:self.Limit], key=lambda x: x[2])
        self.Summary = ""
        for sent in STR:
            self.Summary += sent[0] + " "

        #print(summary_text)
    def __NER_analysis(self):
        self.ALL_ENT={}
        for i in nlp.get_pipe('ner').labels:
            self.ALL_ENT[i]=[]
        #for i in nlp(report.STR).ents:
        for i in self.Doc.ents:
            self.ALL_ENT[i.label_]+=[i]
    def __VIP_KEY(self,Requirments):
        #Requirments["Keywords"]
        STR=" ".join(Requirments)
        STR_token=nlp(STR)
        LEMA=[]
        for word in STR_token:
            LEMA.append(Word)
        Requirments+=LEMA
        return Requirments
              




    


##### form_news_analysis
##### news_titel
class ActionAskFormNLPsAnalysis(Action):#action_ask_form_nlp_analysis_str_articl

    def name(self) -> Text:
        return "action_ask_form_nlp_analysis_str_articl"
    async def run(
                self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
                ) -> List[Dict[Text, Any]]:
        logger.info("News_Picker activated")

        buttons             = [{"title": "I am done", "payload": "I am done"}]

        dispatcher.utter_message(text="""
                                Please enter the articel to analayze or plress '''I am done'''  to complete the analysis  """
                                ,buttons=buttons) 
        return []   

######################################################################################################################
class ValidatesFormNLPAnalysis(FormValidationAction): # validate_form_nlp_analysis#action_ask_form_nlp_analysis_str_articl
    def name(self) -> Text:
        return "validate_form_nlp_analysis"

    def validate_str_articl(
                                self,
                                slot_value: Any,
                                dispatcher: CollectingDispatcher,
                                tracker: Tracker,
                                domain: DomainDict,
                                ) -> Dict[Text, Any]:

    
        str_articl=tracker.get_slot("str_articl")



        if str_articl !="I am done":
            report=Text_summary(tr_articl)
            #Text_summary(article,6)


            Summary=report.Summary
            Abstract=report.abstract[0]["summary_text"]
            Figure=report.Plot
            ENtity=report.ALL_ENT



            dispatcher.utter_message(text=f""" Text analysis  ( abstract ) : {Abstract} """)

            dispatcher.utter_message(text=f""" Text analysis ( important sentences )) : {Summary} """)

            dispatcher.utter_message(image=Figure)
            logger.info(ENtity)

            return {"str_articl":None}
        else:
          
            return {"requested_slot":None,"str_articl":None}



            














