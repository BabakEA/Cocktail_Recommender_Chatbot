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
    recommended_ID=Config["KNN_Model"].kneighbors(Movie_features)[1][0].tolist()
    Recommended_movies=[Config["Movies_characteristics"]["movie title"].tolist()[x] for x in recommended_ID]
    
    return Recommended_movies
    
def Cor_Recommandation(Movie_name):
  
    Member_list    = {x:new_similarity_check(x.lower(),Movie_name.lower()) for x in Config["movies_list"]
                  if new_similarity_check(x.lower(),Movie_name.lower())>=0.9}

    Member_list= dict(sorted(Member_list.items(), key=lambda item: item[1],reverse=True))
    
    if len(Member_list)>=1 :
        Movie_name=list(Member_list.keys())[0]
    
    
    Movie_id=__Movie_Name_to_ID(Movie_name)

    ### create a correlation matrix 

    corr_Movie = Config["corr_mat"][Movie_id]

    return_dict={
                    Config["movies_list"][list(corr_Movie).index(x)]:x.round(3) for x in list(corr_Movie)
                    if x >=0.91 and Config["movies_list"][list(corr_Movie).index(x)]!=Movie_name
                }
    return_dict= dict(sorted(return_dict.items(), key=lambda item: item[1],reverse=True))
    
    return return_dict   


# def __Movie_features(Features:list):
#     return [1 if x in Features else 0 for x in Config["Movie_chatacter"]]


def Movie_features(Features:list):
    Feature_list=[1 if x in Features else 0 for x in Movie_chatacter]
    recommended_ID=Config["KNN_Model"].kneighbors([Feature_list])[1][0].tolist()
    Recommended_movies=[Config["Movies_characteristics"]["movie title"].tolist()[x] for x in recommended_ID]
    
    return Recommended_movies
    
    

###3 test genre: 
# __Movie_features(Features=["Documentary","War","Western"])

# ['Koyaanisqatsi (1983)',
#  'Great Day in Harlem, A (1994)',
#  'Hoop Dreams (1994)',
#  'Thirty-Two Short Films About Glenn Gould (1993)',
#  'Celluloid Closet, The (1995)']

Movie_chatacter=Config["Movies_characteristics"].columns.tolist()[1:]
class ActionAskFormMovieGenrR(Action):#action_ask_form_movie_genr_r_movie_genre

    def name(self) -> Text:
        return "action_ask_form_movie_genr_r_movie_genre"
    async def run(
                self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
                ) -> List[Dict[Text, Any]]:

        movie_genre=tracker.get_slot("movie_genre")
        movie_genre_temp=tracker.get_slot("movie_genre_temp")
        
        logger.info(movie_genre_temp)


        if movie_genre_temp==None:
        
            Name_list           =Movie_chatacter ### all the possible movies genres

        else:
            #sample_filter=20 if len(Account_check)>=20 else len(Account_check)
            Name_list           =[x for x in Movie_chatacter if x not in movie_genre_temp]
            Name_list.append("I am done")


        buttons             = list()
        for Name in Name_list :
            buttons.append({"title": Name, "payload": Name})
        

        dispatcher.utter_message(text="""
                                Please select the movie genre or select ' I am done ' to complete the analysis  """
                                ,buttons=buttons) 
        return []   

######################################################################################################################
class ValidatesFormMovieGenrR(FormValidationAction): # validate_form_movie_genr_r
    def name(self) -> Text:
        return "validate_form_movie_genr_r"

    def validate_movie_genre(
                                self,
                                slot_value: Any,
                                dispatcher: CollectingDispatcher,
                                tracker: Tracker,
                                domain: DomainDict,
                                ) -> Dict[Text, Any]:

    
        movie_genre=tracker.get_slot("movie_genre")
        movie_genre_temp=tracker.get_slot("movie_genre_temp")

        if movie_genre_temp==None:
            movie_genre_temp=[]


        if movie_genre !="I am done":
            movie_genre_temp.append(movie_genre.lower())
            return {"movie_genre":None,"movie_genre_temp":movie_genre_temp}
        else:
            logger.info(movie_genre_temp)

            movie_list=Movie_features(Features=movie_genre_temp)
            logger.info(("movie list: ", movie_list))

            dispatcher.utter_message(text=f"""based on yoiur selections {movie_genre_temp} , I have found the following movies. hope you like them :) . """
                                            )
            dispatcher.utter_message(text=f""" {movie_list} """
                                            )
            
            return {"requested_slot":None,"movie_genre_temp":None,"movie_genre":None}



            














