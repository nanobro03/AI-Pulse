

import os
import pandas as pd
import plotly.express as px
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta
import numpy as np
import random
from PIL import Image 

# ------------------ CONFIG ------------------
st.set_page_config(page_title=" AI Pulse Dashboard", layout="wide")


# ------------------ IMAGE DISPLAY LOGIC (FIXED) ------------------ 
if 'view_photo' in st.query_params:
    incident_id_to_show = st.query_params['view_photo']
    
    st.title("📷 Incident Photo Viewer")

    photo_path_png = os.path.join('incident_photos', f"{incident_id_to_show}.png")
    photo_path_jpg = os.path.join('incident_photos', f"{incident_id_to_show}.jpg")
    photo_path_jpeg = os.path.join('incident_photos', f"{incident_id_to_show}.jpeg")

    photo_path = None
    if os.path.exists(photo_path_png):
        photo_path = photo_path_png
    elif os.path.exists(photo_path_jpg):
        photo_path = photo_path_jpg
    elif os.path.exists(photo_path_jpeg):
        photo_path = photo_path_jpeg

    if photo_path:
        try:
            image = Image.open(photo_path)
            # --- THIS IS THE FIX ---
            # Changed use_column_width to use_container_width
            st.image(image, caption=f"Photo for Incident ID: {incident_id_to_show}", use_container_width=True)
            # -----------------------
        except Exception as e:
            st.error(f"Error opening image file: {e}")
    else:
        st.warning(f"No photo found for Incident ID: {incident_id_to_show}")
        st.info("Ensure the image is in the 'incident_photos' folder and named correctly (e.g., '12.jpg').")

    st.markdown("### [← Click here to close and return to the dashboard](/)", unsafe_allow_html=True)

else:
    st.title("🚧 AI Pulse Dashboard")

    load_dotenv()
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("⚠️ Please set SUPABASE_URL and SUPABASE_KEY in a .env file.")
        st.stop()

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # ------------------ FETCH DATA ------------------
    try:
        response = supabase.table("incident_table") \
            .select("""
                *,
                analyze_result (
                    ai_priority,
                    assigned_department,
                    estimated_fix_time,
                    suggested_solution,
                    traffic_guidance,
                    map_update_json,
                    risk_level,
                    analysis_status
                )
            """).execute()

        if response.data:
            df = pd.json_normalize(response.data)
        else:
            df = pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        df = pd.DataFrame()

    # ------------------ CLEAN / DERIVE ------------------
    for col in ["reported_at", "updated_at"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    total_incidents = len(df)
    status_counts = df["status"].value_counts() if "status" in df.columns else pd.Series()

    # ------------------ METRICS ------------------
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Incidents", total_incidents)
    if not status_counts.empty:
        col2.metric("Open", status_counts.get("Open", 0))
        col3.metric("In Progress", status_counts.get("In Progress", 0))
        col4.metric("Closed", status_counts.get("Closed", 0))

    # ------------------ TABLE ------------------
    st.subheader("Incident Table")

    if not df.empty and 'id' in df.columns:
        df['photo_link'] = df['id'].apply(lambda id: f"?view_photo={id}")

        potential_cols = [
            "id", "reported_at", "incident_type", "location", "status", "priority",
            "analyze_result.risk_level", "analyze_result.assigned_department", "description",
            "photo_link"
        ]
        
        cols_to_show = [col for col in potential_cols if col in df.columns]
        
        display_df = df[cols_to_show].copy()
        display_df.rename(columns={
            'analyze_result.risk_level': 'Risk Level',
            'analyze_result.assigned_department': 'Assigned Dept.'
        }, inplace=True)

        st.dataframe(
            display_df.sort_values(by="reported_at", ascending=False),
            column_config={
                "photo_link": st.column_config.LinkColumn(
                    "Photo",
                    help="Click to view incident photo",
                    display_text="View Photo"
                )
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No incidents found in Supabase. Showing demo data only.")

    # ------------------ BARCHART: INCIDENTS BY LOCATION ------------------
    if not df.empty and "location" in df.columns:
        st.subheader("Incidents by Location")
        location_counts = df.groupby("location").size().reset_index(name="count")
        fig2 = px.bar(
            location_counts, x="location", y="count",
            title="Number of Incidents per Location",
            text_auto=True,
            color="count", color_continuous_scale="Reds"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ------------------ MAP ------------------
    st.subheader("📍 Incident Map (Cyberjaya)")

    map_rendered = False
    if not df.empty and "analyze_result.map_update_json.coordinates" in df.columns:
        coords = df["analyze_result.map_update_json.coordinates"].dropna()
        if not coords.empty:
            try:
                map_df = pd.DataFrame(coords.tolist(), columns=["latitude", "longitude"])
                if "incident_type" in df.columns: map_df["incident_type"] = df["incident_type"]
                if "analyze_result.assigned_department" in df.columns: map_df["assigned_department"] = df["analyze_result.assigned_department"]
                if "analyze_result.estimated_fix_time" in df.columns: map_df["estimated_fix_time"] = df["analyze_result.estimated_fix_time"]
                if "status" in df.columns: map_df["status"] = df["status"]

                status_colors = { "Open": "#FF3333", "In Progress": "#FFD700", "Closed": "#00AA55" }

                fig3 = px.scatter_mapbox(
                    map_df, lat="latitude", lon="longitude",
                    color="status" if "status" in map_df.columns else None,
                    hover_name="incident_type" if "incident_type" in map_df.columns else None,
                    hover_data=["assigned_department", "estimated_fix_time"] if "assigned_department" in map_df.columns else None,
                    zoom=13, height=500, color_discrete_map=status_colors
                )
                fig3.update_layout(mapbox_style="open-street-map")
                st.plotly_chart(fig3, use_container_width=True)
                map_rendered = True
            except Exception as e:
                st.error(f"⚠️ Could not render Supabase map: {e}")

    # ------------------ FALLBACK FAKE MAP ------------------
    if not map_rendered:
        roads = ["Persiaran Multimedia", "Jalan Cyber 8", "Persiaran APEC", "Jalan Teknokrat 3", "Persiaran Rimba Permai", "Jalan Cyber 6"]
        progress_states = ["Not Started", "Under Construction", "In Progress", "Done"]
        maintenance_teams = ["DBKL", "MBPJ", "Cyberjaya Maintenance", "Smart Selangor", "MRCB Infra"]
        center_lat, center_lon = 2.9220, 101.6550
        data = []
        for i in range(30):
            data.append({
                "road_name": random.choice(roads), "assigned_team": random.choice(maintenance_teams),
                "progress": random.choice(progress_states), "estimated_fix_time": round(np.random.uniform(1, 8), 1),
                "latitude": center_lat + np.random.randn() / 200, "longitude": center_lon + np.random.randn() / 200,
            })
        fake_df = pd.DataFrame(data)
        progress_colors = {"Not Started": "#FF3333", "Under Construction": "#FF8C00", "In Progress": "#FFD700", "Done": "#00AA55"}
        fig_fake = px.scatter_mapbox(
            fake_df, lat="latitude", lon="longitude", color="progress", hover_name="road_name",
            hover_data=["assigned_team", "estimated_fix_time"],
            zoom=13, height=500, color_discrete_map=progress_colors
        )
        fig_fake.update_layout(mapbox_style="open-street-map")

        st.plotly_chart(fig_fake, use_container_width=True)
