try:
    from witcher_lib import *

except:
    from Setup.witcher_lib import *

import numpy as np
import pandas as pd
import sklearn
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors
from difflib import *

import pickle 


with open('./Setup/Witcher_recommender.pickle', 'rb') as handle:
    Config = pickle.load(handle)
################################ Movie functions ###############


def Movie_Name_to_ID(Movie_name):
    """ import movie Movie_name, 
        export : movie ID
    """
    return Config["movies_list"].index(Movie_name)

def new_similarity_check(a,b):
    return (SequenceMatcher(None,a,b).ratio())


def KNN_model(Movie_name):
    Member_list    = {x:new_similarity_check(x.lower(),Movie_name.lower()) for x in Config["movies_list"]
                  if new_similarity_check(x.lower(),Movie_name.lower())>=0.9}

    Member_list= dict(sorted(Member_list.items(), key=lambda item: item[1],reverse=True))
    
    if len(Member_list)>=1 :
        Movie_name=list(Member_list.keys())[0]

    Movie_features=Config["Movies_characteristics"][Config["Movies_characteristics"]["movie title"]==Movie_name].values[:,1:].tolist()
    try:
        recommended_ID=Config["KNN_Model"].kneighbors(Movie_features)[1][0].tolist()
        Recommended_movies=[Config["Movies_characteristics"]["movie title"].tolist()[x] for x in recommended_ID]
        return Recommended_movies
    except:
        return []
    
def Cor_Recommandation(Movie_name):
  
    Member_list    = {x:new_similarity_check(x.lower(),Movie_name.lower()) for x in Config["movies_list"]
                  if new_similarity_check(x.lower(),Movie_name.lower())>=0.9}

    Member_list= dict(sorted(Member_list.items(), key=lambda item: item[1],reverse=True))
    
    if len(Member_list)>=1 :
        Movie_name=list(Member_list.keys())[0]
    
    
    Movie_id=Movie_Name_to_ID(Movie_name)

    ### create a correlation matrix 

    corr_Movie = Config["corr_mat"][Movie_id]

    return_dict={
                    Config["movies_list"][list(corr_Movie).index(x)]:x.round(3) for x in list(corr_Movie)
                    if x >=0.91 and Config["movies_list"][list(corr_Movie).index(x)]!=Movie_name
                }
    return_dict= dict(sorted(return_dict.items(), key=lambda item: item[1],reverse=True))
    
    return return_dict   


def Movie_features(Features:list):
    Feature_list=[1 if x in Features else 0 for x in Movie_chatacter]
    recommended_ID=Config["KNN_Model"].kneighbors([Feature_list])[1][0].tolist()
    Recommended_movies=[Config["Movies_characteristics"]["movie title"].tolist()[x] for x in recommended_ID]
    
    return Recommended_movies
    

Movie_chatacter=Config["Movies_characteristics"].columns.tolist()[1:]



class ActionAskFormMovieNameR(Action):#action_ask_form_movie_name_r_movie_name
    def name(self) -> Text:
        return "action_ask_form_movie_name_r_movie_name"
    async def run(
                self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
                ) -> List[Dict[Text, Any]]:
        

        logger.info("movie_recommender_using_name_similarities")


        #buttons             = ({"title": "I am done", "payload": "I am done"})
        buttons             = [{"title": "I am done", "payload": "I am done"}]

        # for Name in Name_list :
        #     buttons.append({"title": Name, "payload": Name})
        

        dispatcher.utter_message(text="""
                                Please enter your favorite movie or select ' I am done ' to complete the analysis  """
                                ,buttons=buttons) 
        return []   

######################################################################################################################
class ValidatesFormMovieGenrR(FormValidationAction): # validate_form_movie_genr_r
    def name(self) -> Text:
        return "validate_form_movie_name_r"

    def validate_movie_name(
                                self,
                                slot_value: Any,
                                dispatcher: CollectingDispatcher,
                                tracker: Tracker,
                                domain: DomainDict,
                                ) -> Dict[Text, Any]:

    

        movie_name=tracker.get_slot("movie_name")
        #movie_genre_temp=tracker.get_slot("movie_genre_temp")
        
        logger.info(movie_name)


        if movie_name =="I am done":
            
            return {"requested_slot":None,"movie_name":None}
        else:
            logger.info(movie_name)


            popularity=Cor_Recommandation(movie_name)
            characteristics=KNN_model(movie_name)


            dispatcher.utter_message(text=f"""Recommendation based on the popularity and IMDB ranking : 
            
            {popularity}
            
             """
                                            )
            dispatcher.utter_message(text=f"""Recommendation based on the movie characteristics :
            {characteristics} """
                                            )
            
            return {"movie_name":None}



            














