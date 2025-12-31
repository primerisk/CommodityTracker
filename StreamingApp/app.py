
import streamlit as st
from tmdb_client import TMDBClient
from utils import get_full_image_url, format_provider_data

# --- Configuration ---
st.set_page_config(page_title="StreamCheck", page_icon="🎬", layout="wide")

# Hardcoded API Key
API_KEY = "a750ef270fc15094c242c9719f90034c"

# --- Main App ---
st.title("🎬 Where is it Streaming?")
st.markdown("Find out where to watch your favorite movies and TV shows.")

client = TMDBClient(API_KEY)

# Search
query = st.text_input("Search for a movie or TV show...", placeholder="e.g. Inception, Breaking Bad")

if query:
    try:
        results = client.search_multi(query)
        
        # Filter mostly for movie and tv
        filtered_results = [r for r in results if r['media_type'] in ['movie', 'tv']]
        
        if not filtered_results:
            st.info("No results found.")
        else:
            # Display results
            st.subheader("Results")
            
            # Use a selectbox to pick the specific item
            # Creating a label that includes title and year
            options = {}
            for res in filtered_results:
                title = res.get('title') if res['media_type'] == 'movie' else res.get('name')
                date = res.get('release_date') if res['media_type'] == 'movie' else res.get('first_air_date')
                year = date.split('-')[0] if date else "N/A"
                label = f"{title} ({year}) [{res['media_type'].upper()}]"
                options[label] = res
            
            selected_label = st.selectbox("Select a title:", list(options.keys()))
            selected_item = options[selected_label]
            
            # Show details for selected item
            st.markdown("---")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                poster_path = selected_item.get('poster_path')
                st.image(get_full_image_url(poster_path), use_container_width=True)
                
            with col2:
                title = selected_item.get('title') if selected_item['media_type'] == 'movie' else selected_item.get('name')
                st.header(title)
                st.markdown(f"**Overview:** {selected_item.get('overview', 'No overview available.')}")
                
                # Fetch Providers
                with st.spinner("Checking streaming availability..."):
                    providers = client.get_watch_providers(selected_item['media_type'], selected_item['id'])
                    us_data = format_provider_data(providers, 'US')
                
                if not us_data:
                    st.warning("No streaming information available for the US.")
                else:
                    # Streaming (Flatrate)
                    st.subheader("Stream")
                    if us_data['flatrate']:
                        cols = st.columns(len(us_data['flatrate']))
                        # Wrap cols if too many
                        # Simplification: Just list names or show small logos if possible
                        # TMDB returns logo_path
                        
                        # Let's display logos in a flex-like grid
                        logo_cols = st.columns(8) # display up to 8 in a row
                        for i, prov in enumerate(us_data['flatrate']):
                            with logo_cols[i % 8]:
                                logo_url = get_full_image_url(prov['logo_path'])
                                st.image(logo_url, width=50, caption=prov['provider_name'])
                    else:
                        st.write("Not currently streaming on subscription services.")

                    # Rent
                    if us_data['rent']:
                        st.subheader("Rent")
                        rent_names = [p['provider_name'] for p in us_data['rent']]
                        st.write(", ".join(rent_names))
                        
                    # Buy
                    if us_data['buy']:
                        st.subheader("Buy")
                        buy_names = [p['provider_name'] for p in us_data['buy']]
                        st.write(", ".join(buy_names))
                    
                    st.markdown(f"[View on TMDB]({us_data['link']})")
                    st.caption("Streaming data provided by JustWatch via TMDB.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

