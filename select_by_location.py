import geopandas as gpd
Area = gpd.read_file("C:\\Amol_Parande\\8_MIS\Abhijeet\\contains_Python\\1_Example\\Example\\AA_Area.shp")
Point = gpd.read_file("C:\\Amol_Parande\\8_MIS\Abhijeet\\contains_Python\\1_Example\\Example\\Points.shp")

pop = gpd.read_file("Vaestotietoruudukko_2015_1.shp")
addresses  = gpd.read_file("addresses_epsg3879_1.shp")

# Check the crs of address points & Check the crs of population layer Do they match?
# print(addresses.crs==pop.crs)
# print(addresses.crs)
# print(pop.crs)
# rename columns name
pop = pop.rename(columns={'ASUKKAITA': 'pop15'})

# Columns that will be select
selected_cols = ['pop15', 'geometry']

pop = pop[selected_cols]

# Spatila Join
# join = gpd.sjoin(addresses, pop, how= "inner", op= 'within')

# 1.Intersection
# intersects = gpd.sjoin(addresses, pop, how="inner", op="intersects")

# 2.Within
# within = gpd.sjoin(addresses, pop, how="inner", op="within")

# 3.Contains
# contains = gpd.sjoin(addresses, pop, how="inner", op="contains")

### WRITING TO SHAPEFILE

# intersects.to_file("intersects.shp")
# within.to_file("within.shp")

# you can not use "contains" operations for point in area need to use "within"
# contains.to_file("contains.shp")












