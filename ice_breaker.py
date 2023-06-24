from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
# https://ice-break-7ca9ef5bb14e.herokuapp.com/

from typing import Tuple

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties.linkedin import scrape_linkedin_profile
from output_parsers import person_intel_parser, PersonIntel

def ice_break(name:str)->Tuple[PersonIntel, str]:
    
    # CORRECT CODE
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)
    
    # FOR DEVELOPMENT
    # linkedin_profile_url = "https://www.linkedin.com/in/karenannleong"
    # linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)
    
    
    summary_template = """
         given the Linkedin information {linkedin_information} about a person from I want you to create:
         1. A short summary
         2. 3 interesting facts about them
         3. Topics that may interest them
         4. 2 creative ice breakers to open a conversation with them
         \n{format_instructions}
     """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information"],
        template=summary_template,
        partial_variables={"format_instructions": person_intel_parser.get_format_instructions}
    )

    llm = ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    result=chain.run(linkedin_information=linkedin_data)    
    print(result)
    
    person_info = person_intel_parser.parse(result)
    picture_url = linkedin_data.get("profile_pic_url")
    
    print(person_info, picture_url)
    return person_info, picture_url


# if __name__ == "__main__":
#     print("Hello LangChain!")
#     ice_break(name="Harrison Chase")

