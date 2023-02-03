from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import requests
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


#connexion aux models

models.Base.metadata.create_all(bind=engine)

# Creation de L'application 

origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#configurer les import de routes 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#@app.get("/")
def root():   
    return {"message": "Hello world"}

#get avec SQLalchemy

""" @app.get("/sqlalchemy")
def test_posts(db: Session= Depends(get_db)):

    posts =db.query(models.Post).all()
    return  posts
 """


# Début Test sur les données GBFS de lime

""" @app.get("/lime/bike_infos")
def get_general_infos():
    response = requests.get("https://data.lime.bike/api/partners/v2/gbfs/paris/gbfs.json")
    if response.status_code == 200:
        return response.json()
    else:
        return {"message": "Oh noo, something went wrong :() "}  """


""" @app.get("/lime/feeds")
def get_general_infos():
    response = requests.get("https://data.lime.bike/api/partners/v2/gbfs/paris/gbfs.json")
    if response.status_code == 200:
        ret = response.json()
        print(ret)
        data = ret["data"]["en"]["feeds"]
        return data
    else:
        return {"message": "Oh noo, something went wrong :() "} """

#system information

@app.get("/API_GBFS/system_information")
def get_general_infos():
    response1 = requests.get("https://data.lime.bike/api/partners/v2/gbfs/paris/gbfs.json")
    response3 = requests.get("https://transport.data.gouv.fr/gbfs/cergy-pontoise/gbfs.json")
    response5 = requests.get("https://transport.data.gouv.fr/gbfs/creteil/gbfs.json")
    if response1.status_code == 200 & response3.status_code == 200 & response5.status_code == 200:
        ret1 = response1.json()
        #print(ret1)
        data1 = ret1["data"]["en"]["feeds"]
        url1 = data1[0]["url"]

        ret3 = response3.json()
        #print(ret3)
        data3 = ret3["data"]["fr"]["feeds"]
        url3 = data3[0]["url"]
        
        ret5 = response5.json()
        #print(ret3)
        data5 = ret5["data"]["fr"]["feeds"]
        url5 = data5[0]["url"]


        response2 = requests.get(url1)
        response4 = requests.get(url3)
        response6 = requests.get(url5)
        if response2.status_code == 200 & response4.status_code == 200 & response6.status_code == 200:
            ret2 = response2.json()
            ret4 = response4.json()
            ret6 = response6.json()
            all_data = {"Lime": ret2,"Velo2": ret4}
            #print( all_data )
            #return all_data
           
            New_data = {
                "last_updated": all_data["Lime"]["last_updated"],
                "ttl": all_data["Lime"]["ttl"],
                "version": all_data["Lime"]["version"],
                "data": {}
            }

            for company, info in all_data.items():
                for key, value in info["data"].items():
                    new_key = f"{key}_{company.lower()}"
                    New_data["data"][new_key] = value

            return New_data
        else:
            return {"message": "Oh noo, something went wrong :() "}
    else:
        return {"message": "Oh noo, something went wrong :() "}


#station information

@app.get("/API_GBFS/station_information")
def get_general_infos():
    response1 = requests.get("https://data.lime.bike/api/partners/v2/gbfs/paris/gbfs.json")
    response3 = requests.get("https://transport.data.gouv.fr/gbfs/cergy-pontoise/gbfs.json")
    response5 = requests.get("https://transport.data.gouv.fr/gbfs/creteil/gbfs.json")
    if response1.status_code == 200 & response3.status_code == 200 & response5.status_code == 200:
        ret1 = response1.json()
        #print(ret1)
        data1 = ret1["data"]["en"]["feeds"]
        url1 = data1[1]["url"]

        ret3 = response3.json()
        #print(ret3)
        data3 = ret3["data"]["fr"]["feeds"]
        url3 = data3[1]["url"]
        
        ret5 = response5.json()
        #print(ret3)
        data5 = ret5["data"]["fr"]["feeds"]
        url5 = data5[1]["url"]


        response2 = requests.get(url1)
        response4 = requests.get(url3)
        response6 = requests.get(url5)
        if response2.status_code == 200 & response4.status_code == 200 & response6.status_code == 200:
            ret2 = response2.json()
            ret4 = response4.json()
            ret6 = response6.json()
            all_data = {"Lime": ret2,"Velo2": ret4}
            #print( all_data )


            new_structure = {
                "last_updated": all_data["Lime"]["last_updated"],
                "ttl": all_data["Lime"]["ttl"],
                "version": all_data["Lime"]["version"],
                "data": {"stations": []}
            }

            for company, info in all_data.items():
                for station in info["data"]["stations"]:
                    new_station = {}
                    for key, value in station.items():
                        new_key = f"{key}_{station['station_id']}"
                        new_station[new_key] = value
                    new_structure["data"]["stations"].append(new_station)

            
            return new_structure
        else:
            return {"message": "Oh noo, something went wrong :() "}
    else:
        return {"message": "Oh noo, something went wrong :() "}

#station_status

@app.get("/API_GBFS/station_status")
def get_general_infos():
    response1 = requests.get("https://data.lime.bike/api/partners/v2/gbfs/paris/gbfs.json")
    response3 = requests.get("https://transport.data.gouv.fr/gbfs/cergy-pontoise/gbfs.json")
    response5 = requests.get("https://transport.data.gouv.fr/gbfs/creteil/gbfs.json")
    if response1.status_code == 200 & response3.status_code == 200 & response5.status_code == 200:
        ret1 = response1.json()
        #print(ret1)
        data1 = ret1["data"]["en"]["feeds"]
        url1 = data1[2]["url"]

        ret3 = response3.json()
        #print(ret3)
        data3 = ret3["data"]["fr"]["feeds"]
        url3 = data3[2]["url"]
        
        ret5 = response5.json()
        #print(ret3)
        data5 = ret5["data"]["fr"]["feeds"]
        url5 = data5[2]["url"]


        response2 = requests.get(url1)
        response4 = requests.get(url3)
        response6 = requests.get(url5)
        if response2.status_code == 200 & response4.status_code == 200 & response6.status_code == 200:
            ret2 = response2.json()
            ret4 = response4.json()
            ret6 = response6.json()
            all_data = {"Lime": ret2,"Velo2": ret4,"Cristolib": ret6}
            #print( all_data )
            return all_data
        else:
            return {"message": "Oh noo, something went wrong :() "}
    else:
        return {"message": "Oh noo, something went wrong :() "}

#lime vehicule type
@app.get("/API_GBFS/Lime/vehicle_types")
def get_general_infos():
    response1 = requests.get("https://data.lime.bike/api/partners/v2/gbfs/paris/gbfs.json")
    if response1.status_code == 200:
        ret1 = response1.json()
        print(ret1)
        data1 = ret1["data"]["en"]["feeds"]
        url1 = data1[4]["url"]

        response2 = requests.get(url1)
        if response2.status_code == 200:
            ret2 = response2.json()
            return ret2
        else:
            return {"message": "Oh noo, something went wrong :() "}
    else:
        return {"message": "Oh noo, something went wrong :() "}

#lime free_bike_status

""" @app.get("/API_GBFS/Lime/system_information")
def get_general_infos():
    response1 = requests.get("https://data.lime.bike/api/partners/v2/gbfs/paris/gbfs.json")
    if response1.status_code == 200:
        ret1 = response1.json()
        #print(ret1)
        data1 = ret1["data"]["en"]["feeds"]
        url1 = data1[0]["url"]


        response2 = requests.get(url1)
        
        if response2.status_code == 200:
            ret2 = response2.json()
            
            all_data = {"Lime": ret2}
            #print( all_data )
            return all_data
        else:
            return {"message": "Oh noo, something went wrong :() "}
    else:
        return {"message": "Oh noo, something went wrong :() "} """


@app.get("/API_GBFS/Lime/free_bike_status")
def get_general_infos():
    response1 = requests.get("https://data.lime.bike/api/partners/v2/gbfs/paris/gbfs.json")
    if response1.status_code == 200:
        ret1 = response1.json()
        print(ret1)
        data1 = ret1["data"]["en"]["feeds"]
        url1 = data1[3]["url"]

        response2 = requests.get(url1)
        if response2.status_code == 200:
            ret2 = response2.json()
            return ret2
        else:
            return {"message": "Oh noo, something went wrong :() "}
    else:
        return {"message": "Oh noo, something went wrong :() "}

#Fin test lime 




