import json
from scrapegraphai.graphs import SmartScraperGraph
import streamlit as st
import nest_asyncio
nest_asyncio.apply()
import os
os.system('playwright install')
os.system('playwright install-deps')
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["SCRAPEGRAPH_API_KEY"] = st.secrets["SCRAPEGRAPH_API_KEY"]

graph_config_openai = {
    "llm": {
        "model": "gpt-4o-mini",
        "api_key": os.environ["OPENAI_API_KEY"],
    },
    "headless": True,
    "verbose": True,
}
st.title(":blue[Travel Guide]")
st.subheader("This guide will help you find the best things to do in a city.")
st.write("Enter the city or country you want to visit.")
city = st.text_input("City")

if st.button("Search") and city:
    city_url = f"https://www.thrillophilia.com/places-to-visit-in-{city}"
    with st.spinner("Please wait while we fetch Must Visits!"):
        try:
            
            prompt=f"""Extract all the Must Visit places in {city} from the webpage.
            For each place, extract the following information:
            1. name: The name of the place
            2. description: A one line description of the place
            3. image_link: URL to the image of the place. To fetch the image URL, use the following steps:
                1. Find the <img> tag of that place and inside that tag, copy the first link of the data-srcset attribute
                2. Use the link as the image_link
            Return the results as a JSON array of objects with the exact keys.""",
            smart_scraper_graph = SmartScraperGraph(
                prompt=prompt,
                source=city_url,
                config=graph_config_openai,
            )
            result = smart_scraper_graph.run()
            activities = []
            if isinstance(result, dict) and 'content' in result:
                if result['content'] != 'NA':
                    # Try to parse content as JSON if it's a string
                    if isinstance(result['content'], str):
                        try:
                            activities = json.loads(result['content'])
                        except Exception as e:
                            st.warning(f"Could not parse JSON content: {e}")
                    elif isinstance(result['content'], list):
                        activities = result['content']
            elif isinstance(result, list):
                activities = result
            if not activities:
                st.warning("No places found. Please check the city/country name or try again later.")
            else:
                st.success(f"Found {len(activities)} must visit places in {city}!")
                for item in activities:
                    # Get data with fallbacks
                    name = item.get('name', 'No Name')
                    desc = item.get('description', 'No Description')
                    img = item.get('image_link') or item.get('image', None)
                    with st.container():
                        cols = st.columns([1, 4])  # Creates a row with 2 columns in 1:4 ratio
                        if img:
                            cols[0].image(img, width=100)  # Display activity image in first column
                        else:
                            cols[0].write(":grey_question:")  # Show question mark if no image
                        cols[1].markdown(f"**{name}**")  # Display activity name in bold in second column
                        cols[1].write(desc)  # Display activity description below name
                        
        except Exception as e:
            st.error(f"An error occurred: {e}")
            import traceback
            st.code(traceback.format_exc())
