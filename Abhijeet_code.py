import json
import requests
import geopandas as gpd
import numpy as np
import shapely.speedups
import pandas as pa
import matplotlib.pyplot as plt

# my_gdf.to_sql(name="test", con=engine, if_exists='append', index=False,
#               dtype={'geom': Geometry(geometry_type='POLYGON', srid=4326)})
def create_heirarchy(geo_data_frame, layers):
    filter = geo_data_frame["IndexOrder"] == layers[0]
    child_filter = geo_data_frame["IndexOrder"] == layers[1]
    parent_order = geo_data_frame[filter]
    child_order = geo_data_frame[child_filter]
    count = 0
    print("total parent ", parent_order.size)
    for row in parent_order.iterrows():
        count = count + 1
        print(count)
        ids = get_all_intersected_polygons(row[1].geometry, child_order)
        geo_data_frame.loc[geo_data_frame.unique_id.isin(ids), "parent_id"] = int(row[1].unique_id)
    geo_data_frame.to_file('/home/gulve/data-analysis/feature-comparator/data/complte_irl.gpkg', layer='index',
                           driver='GPKG')
    return geo_data_frame

def call_hierarchy(geo_data_frame, lowest_order):
    filter = geo_data_frame["IndexOrder"] == lowest_order
    geo_data_frame.unique_id.astype(str)
    # result_data_frame = gpd.GeoDataFrame(columns=["order10", "order9", "order8"])
    apts = gpd.read_file(
        "C:\\Amol_Parande\\8_MIS\Abhijeet\\contains_Python\\2_Geopakage\\Geo_Data.gpkg", layer="Points")
    for row in geo_data_frame[filter].iterrows():
        list = [row[1].unique_id]
        construct_hierarchy(geo_data_frame, row[1].parent_id, list)
        query = get_name_hierarchy_from_ids(geo_data_frame, list)
        # res = compare_pelias_hierarchy(geo_data_frame, query, list, {})
        print(query, ",", compare_with_apt(geo_data_frame, list, apts), percentage_match(None))

def percentage_match(ll):
    if ll == None:
        return 0
    count = 0
    for name in ll:
        if ll[name]:
            count = count + 1
    return count / len(ll)

api = "https://api.geocode.earth/v1/autocomplete?focus.point.lat=18.545351289248973&focus.point.lon=73.88522386550905&api_key=ge-8f137223ed5b405d&text="

def compare_pelias_hierarchy(geo_data_frame, query, hierarchy_ids, response_model_attribute):
    #     name  neighbourhood  locality
    resp = requests.get(api + query.strip())
    if resp.status_code != 200:
        raise Exception('GET /tasks/ {}'.format(resp.status_code))
    res_json = resp.json()
    if len(res_json["features"]) <= 0:
        return
    name_matching = res_json["features"][0]["properties"]
    # if "name" in name_matching and "neighbourhood" in name_matching and "locality" in name_matching:
    return json_value_math(name_matching, hierarchy_ids, geo_data_frame)

def json_value_math(json_obj, hierarchy_ids, geo_data_frame):
    json_obj = json.loads(json.dumps(json_obj))
    arr = {}
    for id in hierarchy_ids:
        name = get_area_name(geo_data_frame, id)
        if "County" not in name:
            temp = False
            for value in json_obj.values():
                temp |= name == value
            arr[name] = temp
        else:
            arr[name] = True
    return arr

def create_convex_hull_and_compare(apts_within_area, area):
    name_poly = check_for_same_name_poly_area(apts_within_area, area)
    if name_poly > 50:
        return name_poly
    group = apts_within_area.groupby("LOCALITY_NAME")
    for single_group in group:
        poly = single_group[1]["geometry"].unary_union.convex_hull
        intersection = poly.intersection(area[1].geometry)
        area[1].within(poly[1].geometry)

def check_for_same_name_poly_area(apts_within_area, area):
    fltr = apts_within_area[apts_within_area["LOCALITY_NAME"] == area[1].name]
    poly_with_area_name = fltr[1]["geometry"].unary_union.convex_hull
    intersection = poly_with_area_name.intersection(area[1].geometry)
    return (intersection.area / area.area) * 100

def compare_with_apt(geo_data_frame, hierarchical_ids, apts):
    global apt_group_by
    data_frame = geo_data_frame[geo_data_frame.unique_id.isin(hierarchical_ids[:2])]
    # data_frame = data_frame[not data_frame["name"].str.contains("County"
    for area in data_frame.iterrows():
        area_arr = []
        for touple in area.iteritems():
            area_arr.append(touple)
        gpd.GeoDataFrame(area_arr)
        apts_within_area = apts[apts.within(area[1].geometry)]
        group_by = apts_within_area.groupby("LOCALITY_NAME").aggregate("LOCALITY_NAME").count()
        arr = []
        for touple in group_by.iteritems():
            arr.append(touple)
        apt_group_by = pa.DataFrame(arr, columns=["LOCALITY_NAME", "count"])
        apt_group_by = remove_parent(apt_group_by, area, geo_data_frame)
        apt_group_by["perc"] = apt_group_by['count'] / (apt_group_by.sum()[1] / 100)
        apt_group_by = apt_group_by.sort_values(by="perc", ascending=False)
        aa = apt_group_by[apt_group_by["LOCALITY_NAME"] == area[1]["name"].upper()]
        if len(aa.perc.array) <= 0:
            return False
    return True

def filter_county_column_name(data_frame):
    for key in data_frame.keys():
        if "county" in key.lower():
            return key

def remove_parent(apt_group_by, area, geo_data_frame):
    list = []
    construct_hierarchy(geo_data_frame, area[1].parent_id, list)
    for id in list:
        row = geo_data_frame[geo_data_frame["unique_id"] == id]["name"].values[0].upper()
        apt_group_by = apt_group_by.drop(apt_group_by[apt_group_by["LOCALITY_NAME"] == row].index)
    return apt_group_by

def get_all_name_matching_poly(data_frame, poly):
    poly_list = poly[poly.LOCALITY_NAME.isin([x.upper() for x in data_frame.name.values])]
    return poly_list

def get_intersecting_polygons(poly_list, lowest_geo_data_frame):
    lowest_poly = poly_list[poly_list["LOCALITY_NAME"] == lowest_geo_data_frame.name.values[0].upper()]
    pip_mask = lowest_poly[lowest_poly.within(poly_list['geometry'])]
    for poly in poly_list.iterrows():
        poly[1].geometry

def get_area_name(geo_data_frame, id):
    return geo_data_frame.loc[geo_data_frame.unique_id == id].name.values[0]

def get_name_hierarchy_from_ids(geo_data_frame, list):
    string = ""
    for id in list:
        string += (geo_data_frame.loc[geo_data_frame.unique_id == id].name.values[0] + " ")
    return string

def construct_hierarchy(geo_data_frame, parent_id, list):
    if parent_id == '':
        return list
    list.append(np.int64(parent_id))
    construct_hierarchy(geo_data_frame,
                        geo_data_frame[geo_data_frame["unique_id"] == np.int64(parent_id)].parent_id.values[0],
                        list)

def get_all_intersected_polygons(parent_poly, child_data_frame):
    return child_data_frame[child_data_frame.within(parent_poly)].unique_id.array

def create_df_from_tuple(group_by, columns):
    arr = []
    index = []
    for touple in group_by.iteritems():
        arr.append(touple)
        index.append(touple)
    return pa.DataFrame(arr, columns=columns, index=index)

# df = gpd.read_file("/home/gulve/data-analysis/Geogesion/dublin.gpkg", driver="GPKG",
#                    layer="TTOM-Core::IndexArea")
df = gpd.read_file("/home/gulve/data-analysis/feature-comparator/data/complte_irl.gpkg",
                   driver="GPKG",
                   layer="index")
# df = df[df["IndexOrder"].notnull()]
# df['unique_id'] = df.name.map(hash)
# df['parent_id'] = ''
# create_heirarchy(df, ["Order9", "Order10"])

# df.loc[df["IndexOrder"] == "Order8", "parent_id"] = ''
call_hierarchy(df, "Order10")

def absolute_value(val):
    a = np.round(val, 0)
    return a
# csv = pa.read_csv("/home/gulve/data-analysis/hierarchy_res.csv")
# csv = csv.astype({"apt": str})
# both_matches_hierarchy = csv[csv["apt"] == csv["pelias"]]
#
# need_to_check = csv[csv["pelias"] == "None"]
# need_to_check = need_to_check[need_to_check["apt"] == "False"]
# print()
# not_matches = csv[csv["pelias"] != "None"]
# not_matches = not_matches[not_matches["apt"] != not_matches["pelias"]]
# print(need_to_check)
#
# pelias_distinct_values = create_df_from_tuple(csv.pelias.value_counts(), ["is_matches", "count"])
# pelias_distinct_values.plot.pie(y='count', autopct=absolute_value)
# apt = create_df_from_tuple(csv.apt.value_counts(), ["is_matches", "count"])
# apt = apt.astype({'count': np.int64})
# apt.plot.pie(y="count", x="apt", autopct=absolute_value)
# plt.show()
# df = gpd.read_file("/home/gulve/data-analysis/Geogesion/tt.gpkg", driver="GPKG",
#                    layer="TTOM-Core::IndexArea")
# create_convex_hull(df)