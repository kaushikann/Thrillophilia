import json
from scrapegraphai.graphs import SmartScraperGraph
import streamlit as st
import nest_asyncio
nest_asyncio.apply()
import os
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.system('playwright install')
os.system('playwright install-deps')

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
    city_url = f"https://www.thrillophilia.com/countries/{city}/things-to-do"
    with st.spinner("Scraping, please wait..."):
        try:
            smart_scraper_graph = SmartScraperGraph(
                prompt=f"List all the Things to do in {city} and a one line description of each with a link to image.",
                source=city_url,
                config=graph_config_openai,
            )
            result = smart_scraper_graph.run()
            if not result:
                st.warning("No results found. Please check the city name or try again later.")
            else:
                st.success(f"Found {len(result)} things to do in {city}!")
                for item in result:
                    # Expecting item to have 'name', 'description', 'image', 'link' keys
                    name = item['name']
                    desc = item['description']
                    img = item['image_link']
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







