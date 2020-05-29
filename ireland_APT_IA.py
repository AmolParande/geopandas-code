import geopandas as gpd

# admin_area = gpd.read_file("C:\\Amol_Parande\\8_MIS\Abhijeet\\contains_Python\\1_Example\\AA_Area.shp")
# apt_point = gpd.read_file("C:\\Amol_Parande\\8_MIS\Abhijeet\\contains_Python\\1_Example\\Points.shp")

admin_area = gpd.read_file("C:\\Amol_Parande\\8_MIS\\Abhijeet\\contains_Python\\2_Geopakage\\Geo_Data.gpkg", layer='Order10')
apt_point = gpd.read_file("C:\\Amol_Parande\\8_MIS\\Abhijeet\\contains_Python\\2_Geopakage\\Geo_Data.gpkg", layer='Points')


attibutes_aa = ['name','unique_id','parent_id','IndexOrder', 'geometry']

admin_area = admin_area[attibutes_aa]

##### SELECT BY ATTRIBUTE #######

# for index, row in apt_point.iterrows():
#     # print("This is a ROW:", row)
#     if row["LOCALITY_N"]== 'LACKABEG':
#         print(row["LOCALITY_N"])
#     # print(row["LOCALITY_N"]== 'LACKABEG')

join = gpd.sjoin(apt_point, admin_area, how="inner", op="within")

# writing to ESRI sheapfile

# join.to_file("C:\\Amol_Parande\\8_MIS\Abhijeet\\contains_Python\\1_Example\\intersects_area.shp")

# writing to Geopakage
join.to_file("C:\\Amol_Parande\\8_MIS\Abhijeet\\contains_Python\\1_Example\\with_in_1.gpkg",layer='With_in_1', driver="GPKG")

