import os

from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from secret import openai_key


os.environ['OPENAI_API_KEY'] = openai_key





def getPlaces(country):
    llm = OpenAI(temperature=0.6)
    print(country)
    prompt_template_name = PromptTemplate (
    input_variables= ['country',"reviews"],
    template = """Can you suggest a top city to visit in {country} based on reviews? print only one city name alone please"""
    )

    llm_name_chain =  LLMChain (llm = llm , prompt=prompt_template_name, output_key = "city_name")


    prompt_template_iternary = PromptTemplate (
        input_variables= ['city_name'],
        template = """can you suggest 5 places to visit in {city_name}?"""
    )
    llm_city_chain =  LLMChain (llm = llm , prompt=prompt_template_iternary, output_key = "places")

    sequential_chain = SequentialChain ( chains = [llm_name_chain,llm_city_chain],
                                    input_variables=["country"],
                                    output_variables=["city_name" , "places"])

    places = sequential_chain({"country" : country})

    return places


if __name__ ==  "__main__":
    places = getPlaces("India")
    print(places)
    print(places['country'])
    all_places=places['places'].split("\n")
    for place in all_places:
        print(place)