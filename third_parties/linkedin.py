import os
import requests
import json

def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}

    # CORRECT CODE
    response = requests.get(
        api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic
    )

    # FOR DEVELOPMENT 
    # response = requests.get('https://gist.githubusercontent.com/toothyachy/8ef87890ccb7f7a6bf913bc4c311ecd9/raw/ba9a4afc6eb4f484855bd373288310e4def5f502/eden-marco.json')
    # response = requests.get('https://gist.githubusercontent.com/toothyachy/21e9a828d2bcc3a2d8e12461da6c2a2a/raw/5d04ab14f3d26258ad242a458fe1f5244e8287e9/mel-ow.json')

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k in ["profile_pic_url", "full_name", "occupation", "headline", "summary", "country_full_name", "experiences"]
        # and k in ["profile_pic_url", "full_name", "occupation", "headline", "summary", "country_full_name", "experiences", "certifications", "accomplishments_organisations"]
        # and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    print(data)
    return data
