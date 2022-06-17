try:
    from witcher_lib import *

except:
    from Setup.witcher_lib import *

from GoogleNews import GoogleNews
#googlenews = GoogleNews()
googlenews = GoogleNews(lang='en', region='CA')

def Google_News(keyword=str ,Period="7"):
    Period=str(Period)+"d"
    
    googlenews = GoogleNews(period=Period)
    googlenews = GoogleNews(encode='utf-8')
    googlenews.search(keyword)
    STR=f""" here are your results \n """
    for i in googlenews.results():
        STR+=f"""{i["date"]} :: [{i["title"]}]({i["link"]})"""+"\n"

    return STR
    


##### form_news_analysis
##### news_titel
class ActionAskFormNewsAnalysis(Action):#action_ask_form_news_analysis_news_titel

    def name(self) -> Text:
        return "action_ask_form_news_analysis_news_titel"
    async def run(
                self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
                ) -> List[Dict[Text, Any]]:
        logger.info("News_Picker activated")

        buttons             = [{"title": "I am done", "payload": "I am done"}]

        dispatcher.utter_message(text="""
                                Please enter the topic to search ' I am done ' to complete the analysis  """
                                ,buttons=buttons) 
        return []   

######################################################################################################################
class ValidatesFormNewsAnalysis(FormValidationAction): # validate_form_news_analysis
    def name(self) -> Text:
        return "validate_form_news_analysis"

    def validate_news_titel(
                                self,
                                slot_value: Any,
                                dispatcher: CollectingDispatcher,
                                tracker: Tracker,
                                domain: DomainDict,
                                ) -> Dict[Text, Any]:

    
        news_titel=tracker.get_slot("news_titel")



        if news_titel !="I am done":
            News_list=Google_News(keyword=news_titel)

            dispatcher.utter_message(text=f"""based on yoiur selections {news_titel} , I have found the following resources. hope you like them :) . """
                                            )
            dispatcher.utter_message(text=News_list)

            return {"news_titel":None}
        else:
          
            return {"requested_slot":None,"news_titel":None}



            














