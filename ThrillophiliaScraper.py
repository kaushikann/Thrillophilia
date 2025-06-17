import json
from scrapegraphai.graphs import SmartScraperGraph
import streamlit as st
import nest_asyncio
nest_asyncio.apply()
import os
os.system('playwright install')
os.system('playwright install-deps')
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

graph_config_openai = {
    "llm": {
        "model": "gpt-4o-mini",
        "api_key": os.environ["OPENAI_API_KEY"],
    },
    "headless": True,
    "verbose": True,
}
st.title("Thrillophilia Scraper")
st.subheader("This is a scraper for the Thrillophilia website.")
st.write("Enter the city you want to visit.")
city = st.text_input("City")

if st.button("Search") and city:
    city_url = f"https://www.thrillophilia.com/cities/{city}/things-to-do"
    with st.spinner("Scraping, please wait..."):
        try:
            smart_scraper_graph = SmartScraperGraph(
                prompt=f"""Extract all the things to do in {city} from the webpage.
                For each activity, extract the following information:
                - name: The name of the activity
                - description: A one line description of the activity
                - image_link: URL to the image of the activity
                - link: The link to the thing to do
                Return the results as a JSON array of objects with the exact keys.""",
                source=city_url,
                config=graph_config_openai,
            )
            result = smart_scraper_graph.run()
            activities = []
            if isinstance(result, dict) and 'content' in result:
                if result['content'] != 'NA':
                    if isinstance(result['content'], str):
                        try:
                            activities = json.loads(result['content'])
                            st.write(activities)
                        except Exception as e:
                            st.warning(f"Could not parse JSON content: {e}")
            if not result:
                st.warning("No results found. Please check the city name or try again later.")
            else:
                st.success(f"Found {len(result)} things to do in {city}!")
                for item in result:
                    # Expecting item to have 'name', 'description', 'image', 'link' keys
                    name = item['name'] if isinstance(item, dict) else str(item)
                    desc = item['description'] if isinstance(item, dict) else 'No Description'
                    img = item['image_link'] if isinstance(item, dict) else None
                    with st.container():
                        cols = st.columns([1, 4])
                        if img:
                            cols[0].image(img, width=100)
                        else:
                            cols[0].write(":grey_question:")
                        cols[1].markdown(f"**{name}**")
                        cols[1].write(desc)
                        
        except Exception as e:
            st.error(f"An error occurred: {e}")







