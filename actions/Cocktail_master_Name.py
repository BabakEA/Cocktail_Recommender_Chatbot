try:
    from witcher_lib import *

except:
    from Setup.witcher_lib import *

import pandas as pd
import numpy as np
import pickle
import collections
import sklearn
from sklearn.decomposition import TruncatedSVD
from difflib import *
import sklearn
from sklearn.neighbors import NearestNeighbors 
import random


with open('./Setup/Witcher_cocktail_master.pickle', 'rb') as handle:
    Cocktail = pickle.load(handle)
################################ Movie functions ###############
def Cocktail_Name_to_ID(Cocktail_name):
    """ import movie Cocktail_name, 
        export : Cocktail ID
    """
    try:
        return Cocktail["Cocktail_list"].index(Cocktail_name)
    except:
        return(len(Cocktail["Cocktail_list"]))

def new_similarity_check(a,b):
    return (SequenceMatcher(None,a,b).ratio())

def Ingridiants_Extraction(C_name):
    Ingrid=Cocktail["Cocktail_charactristic"][Cocktail["Cocktail_charactristic"]["Cocktail Name"]==C_name]["Ingredients"]
    return list(Ingrid.values)

def Cocktail_KNN_model(Cocktail_name):
    Cocktail_list    = {x:new_similarity_check(x.lower(),Cocktail_name.lower()) for x in Cocktail["Cocktail_list"]
                  if new_similarity_check(x.lower(),Cocktail_name.lower())>=0.9}

    Cocktail_list= dict(sorted(Cocktail_list.items(), key=lambda item: item[1],reverse=True))
    
    if len(Cocktail_list)>=1 :
        Cocktail_list=list(Cocktail_list.keys())[0]
    #print(Cocktail_list)

    C_features=Cocktail["Cocktail_charactristic"][Cocktail["Cocktail_charactristic"]["Cocktail Name"]==Cocktail_list].values[:,3:].tolist()
    #print(C_features)
    #C_features=Cocktail["Cocktail_charactristic"][Cocktail["Cocktail_charactristic"]["Cocktail Name"]==Cocktail_list].values[:,2:].tolist()
    Ingrid=Cocktail["Cocktail_charactristic"][Cocktail["Cocktail_charactristic"]["Cocktail Name"]==Cocktail_list]["Ingredients"]
    #print(Ingrid)
    try:
        recommended_ID=Cocktail["KNN_Cocktail"].kneighbors(C_features)[1][0].tolist()
        Recommended_C=[Cocktail["Cocktail_list"][x] for x in recommended_ID]
        #print(recommended_ID)

        Ingrid={x:Ingridiants_Extraction(x) for x in Recommended_C}
        return Ingrid
    except:
        return []
    
def Cocktail_features(Features:list):
    Feature_list=Cocktail_Features(Features)
    recommended_ID=Cocktail["KNN_Cocktail"].kneighbors([Feature_list])[1][0].tolist()
    Recommended_C=Recommended_C=[Cocktail["Cocktail_list"][x] for x in recommended_ID]
    Ingrid={x:Ingridiants_Extraction(x) for x in Recommended_C}
    
    return Ingrid

def Cocktail_Features(Features:list):
    #return [1 if x in list(Ingridiants.keys()) else 0 x in Features]
    return [1 if x in Features else 0 for x in list(Cocktail["Ingridiants"].keys())]
            

######################################################################3
class ActionAskFormCocktailName(Action):#action_ask_form_cocktail_name_cocktail_name
    def name(self) -> Text:
        return "action_ask_form_cocktail_name_cocktail_name"
    async def run(
                self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
                ) -> List[Dict[Text, Any]]:
        

        logger.info("action_ask_form_cocktail_name_cocktail_name")


        #buttons             = ({"title": "I am done", "payload": "I am done"})
        #buttons             = [{"title": "I am done", "payload": "I am done"}]
        Name_list=random.sample(Cocktail["Cocktail_list"], 15)

        


        buttons=[]
        for Name in Name_list :
            buttons.append({"title": Name, "payload": Name})
        buttons.append({"title": "I am done", "payload": "I am done"})
        

        dispatcher.utter_message(text="""
                                Please enter your favorite drink or select ' I am done ' to complete the analysis  """
                                ,buttons=buttons) 
        return []   

######################################################################################################################
class ValidatesFormMovieGenrR(FormValidationAction): # validate_form_movie_genr_r
    def name(self) -> Text:
        return "validate_form_cocktail_name"

    def validate_cocktail_name(
                                self,
                                slot_value: Any,
                                dispatcher: CollectingDispatcher,
                                tracker: Tracker,
                                domain: DomainDict,
                                ) -> Dict[Text, Any]:

    

        cocktail_name=tracker.get_slot("cocktail_name")
        #movie_genre_temp=tracker.get_slot("movie_genre_temp")
        
        logger.info(cocktail_name)


        if cocktail_name =="I am done":
            
            return {"requested_slot":None,"cocktail_name":None}
        else:
            logger.info(cocktail_name)


            #popularity=Cor_Recommandation(movie_name)
            Cocktail_list=Cocktail_KNN_model(cocktail_name)
            dispatcher.utter_message(text=f"""Based on the selected drink :
            {cocktail_name} I have the following options to offer """)

            Cocktail_STR=""
            for key in Cocktail_list:
                Cocktail_STR+=f""" \n Cocktial : {key}\n Ingridients: {Cocktail_list[key]}\n """
                dispatcher.utter_message(text=f""" Cocktial : {key} Ingridients: {Cocktail_list[key]}""")


            # dispatcher.utter_message(text=f"""Recommendation based on the selected drink :
            # {Cocktail_list} """)
            # dispatcher.utter_message(text=f"""Recommendation based on the selected drink :
            # {Cocktail_STR} """)


            
            return {"cocktail_name":None}



            














