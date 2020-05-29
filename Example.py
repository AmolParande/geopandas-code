import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString
# from matplotlib import pylab as plt
data = gpd.read_file("C:\\Amol_Parande\\5_Souring\\2_Source\\For_Amol\\UTM_File_Udaypur.shp")
#print(data.head(1000))

# select by attribute
# print(data[data['Dist_Code'].apply(int) > 120]  )

# print(data[data['Dist_Code'].isin (['Rajsamand', 'Udaipur'])])

#  Indexing by row
# print(data[12:50])

# Select by Attribute String
# print(data[data['District'] == 'Rajsamand' ])
# print(data['Dist_Code'])

# Reproject to UTM 44N
repriject = data.to_crs({'init':'epsg:32644'})

# Attribute to be expose
# new = repriject[['Name','Dist_Code']]


# convert polygon to polyline
polygon = repriject.boundary

polygon_buff = polygon.buffer(5)

#  Data export to geopakage
# polygon_buff.to_file("C:\\Amol_Parande\\5_Souring\\2_Source\\For_Amol\\Udaipur.gpkg", layer = 'Buffer', driver = 'GPKG')


# new.to_file("C:\\Amol_Parande\\5_Souring\\2_Source\\For_Amol\\Buffer_dissolve1.shp")

# Buffer
# buffer_vila = polygon.buffer(5)

# create new geodataframe
# GF_Buffer = gpd.GeoDataFrame(buffer_vila)

# buffer_vila.to_file("C:\\Amol_Parande\\5_Souring\\2_Source\\For_Amol\\Udaipur_Village_line_BufferXXXXX.shp")

# Dissolve

new = gpd.GeoDataFrame({'geometry': polygon_buff.unary_union, 'group': 1}).dissolve(by='group')

# Dissolve_Buf = GF_Buffer.dissolve()

# Dissolve_Buf.to_file("C:\\Amol_Parande\\5_Souring\\2_Source\\For_Amol\\Udaipur_Village_Poly_Dissolve.shp")

















