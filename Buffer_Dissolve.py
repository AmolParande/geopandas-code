import geopandas as gpd

data = gpd.read_file("C:\\Amol_Parande\\5_Souring\\2_Source\\For_Amol\\UTM_File_Udaypur.shp")

reproject_UTM = data.to_crs({'init':'epsg:32644'})

poly_to_line = reproject_UTM.boundary

line_Buffer = poly_to_line.unary_union.buffer(5)

Area_dissolved = gpd.GeoDataFrame({'geometry' : line_Buffer,'group': 1},crs={'init':'epsg:4326'}).dissolve(by='group')
Area_dissolved = Area_dissolved.to_crs(data.crs)

Area_dissolved.to_file("C:\\Amol_Parande\\5_Souring\\2_Source\\For_Amol\\New_Area_DissolveXXXcc.shp")


# Save to Geopkage
# Area_dissolved.to_file("C:\\Amol_Parande\\5_Souring\\2_Source\\For_Amol\\Expert.gpkg",layer='DissolvedXX', driver="GPKG")
