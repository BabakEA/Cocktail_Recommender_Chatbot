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



Ingrid_list_sample=list(Cocktail["Ingridiants"].keys())[:60]
#Name_list=random.sample(list(Cocktail["Ingridiants"].keys())[:60], 15)




class ActionAskFormCocktailIngrid(Action):#action_ask_form_cocktail_ingridiants_cocktail_ingrid

    def name(self) -> Text:
        return "action_ask_form_cocktail_ingridiants_cocktail_ingrid"
    async def run(
                self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
                ) -> List[Dict[Text, Any]]:

        cocktail_ingrid=tracker.get_slot("cocktail_ingrid")
        cocktail_ingrid_temp=tracker.get_slot("cocktail_ingrid_temp")
        
        logger.info(cocktail_ingrid_temp)


        if cocktail_ingrid_temp==None:
        
            #Name_list           =Movie_chatacter ### all the possible movies genres
            Name_list=random.sample(Ingrid_list_sample, 15)

        else:
            #sample_filter=20 if len(Account_check)>=20 else len(Account_check)
            Name_list           =[x for x in Ingrid_list_sample if x not in cocktail_ingrid_temp]
            Name_list=random.sample(Name_list, 15)
            Name_list.append("I am done")


        buttons             = list()
        for Name in Name_list :
            buttons.append({"title": Name, "payload": Name})
        

        dispatcher.utter_message(text="""
                                Please select the desired ingredients or select ' I am done ' to complete the analysis  """
                                ,buttons=buttons) 
        return []   

######################################################################################################################
class ValidatesFormMovieGenrR(FormValidationAction): # validate_form_movie_genr_r
    def name(self) -> Text:
        return "validate_form_cocktail_ingridiants"

    def validate_cocktail_ingrid(
                                self,
                                slot_value: Any,
                                dispatcher: CollectingDispatcher,
                                tracker: Tracker,
                                domain: DomainDict,
                                ) -> Dict[Text, Any]:

    
        cocktail_ingrid=tracker.get_slot("cocktail_ingrid")
        cocktail_ingrid_temp=tracker.get_slot("cocktail_ingrid_temp")

        if cocktail_ingrid_temp==None:
            cocktail_ingrid_temp=[]


        if cocktail_ingrid !="I am done":
            cocktail_ingrid_temp.append(cocktail_ingrid)
            return {"cocktail_ingrid":None,"cocktail_ingrid_temp":cocktail_ingrid_temp}
        else:
            logger.info(cocktail_ingrid_temp)


            Cocktail_List=Cocktail_features(cocktail_ingrid_temp)
            dispatcher.utter_message(text=f"""based on yoiur selections {cocktail_ingrid_temp} , I have found the following drinks for you. hope you like them :) . """
                                            )

            Cocktail_STR=""
            for key in Cocktail_List:
                #STR+="Cocktial :", key,"\n", "Ingridients: ",test_vector[key],"\n","*********" )
                Cocktail_STR+=f"""\n Cocktial : {key}\n Ingridients: {Cocktail_List[key]}\n 
 
                 """
                dispatcher.utter_message(text=f""" Cocktial : {key} Ingridients: {Cocktail_List[key]}""")



            logger.info(("Cocktail List: ", Cocktail_List))


            # dispatcher.utter_message(text=f""" {Cocktail_List} """
            #                                 )
            #dispatcher.utter_message(text=Cocktail_STR)
            
            return {"requested_slot":None,"cocktail_ingrid_temp":None,"cocktail_ingrid":None}



            














