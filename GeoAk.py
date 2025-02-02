import geopandas as gpd
import pandas as pd
import numpy as np
import folium
import os

try:

    # File paths
    geojson_path = "C:/Users/Chidi/Downloads/4_5830242500287140859.geojson"  # Replace with your actual path
    excel_path = "C:/Users/Chidi/Desktop/akwaibom numbers.xlsx"       # Replace with your actual path
    output_geojson = "C:/Users/Chidi/Documents/geo py project/updated_filesl.geojson"

    if not os.path.exists(geojson_path):
        raise FileNotFoundError(f"GeoJSON file not found at {geojson_path}")
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Excel file not found at {excel_path}")

    # Load GeoJSON file
    gdf = gpd.read_file(geojson_path)

    # Load Excel file
    df = pd.read_excel(excel_path)

    # Ensure column names match exactly
    common_key = "admin2RefN"  # Replace with your actual key column name

    # Merge the Excel data into the GeoJSON
    merged_gdf = gdf.merge(df, on=common_key, how="left")

    # Define color mapping based on conditions
    def assign_color(row):
        if pd.isna(row["MU"]) and pd.isna(row["SHFs"]):
            return "red"  # Both MU & SHFs are null
        elif pd.isna(row["MU"]):
            return "yellow"  # Only MU is null
        else:
            return "blue"  # Default color

    # Apply color classification
    merged_gdf["color"] = merged_gdf.apply(assign_color, axis=1)

    # Remove the first row from the merged GeoDataFrame
    merged_gdf = merged_gdf.iloc[1:].reset_index(drop=True)

    # Convert MultiPolygons to individual Polygons for better visualization
    if "MultiPolygon" in merged_gdf.geom_type.values:
        merged_gdf = merged_gdf.explode(index_parts=False)

    # Save the updated GeoJSON file
    merged_gdf.to_file(output_geojson, driver="GeoJSON")

    print("Updated GeoJSON with color classification saved successfully!")

    merged_gdf = merged_gdf.set_crs("EPSG:4326")  # Use WGS84 (common for GeoJSON)

    # Create a base map centered around the dataset's centroid
    map_center = merged_gdf.geometry.centroid.iloc[0].coords[0][::-1]  # Reverse (lat, lon) format
    m = folium.Map(location=map_center, zoom_start=10)

    # Function to get color for each feature
    def style_function(feature):
        return {
            "fillColor": feature["properties"]["color"],
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.6
        }

    # Add GeoJSON layer with styling
    folium.GeoJson(
        merged_gdf,
        style_function=style_function
    ).add_to(m)

    # Save the map as an HTML file
    # Save the map as an HTML file
    map_output_path = "C:/Users/Chidi/Documents/geo py project/map_visualization.html"
    m.save(map_output_path)

    print(f"Map visualization saved successfully as {map_output_path}!")

    # Your script here
except Exception as e:
    print(f"An error occurred: {e}")