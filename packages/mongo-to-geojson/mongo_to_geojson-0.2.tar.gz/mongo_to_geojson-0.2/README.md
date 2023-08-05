# mongo_to_geojson

A tool to help you extract spatial data from Mongo and format into GeoJSON 

## Why Use It

 - Dump entire collections, use filters (with or without projections), and/or use aggregation framework
 - For geometries, the tool can use either standard geojson geometry objects, or construct point geometries from other document properties <sup>1</sup>
 - If you don't provide specific Mongo document properties to use for geometry, this tool attempts to infer geometry.   The tool will look for standard geojson geometry objects or other common coordinate naming conventions<sup>2</sup>
 - Since data is streamed to output json file, this tool won't run out of memory when writing very large geojson files

1.  As long as the underlying Mongo value can be converted to  a numeric value, this tool can use it.  For example, a string value for an x coordinate will be converted just fine (ex: "x":"-104.33")

2.  Common coordinate names this tool looks for below.  **Case doesn't matter.**
	 - x, lng, long, longitude
	 - y, lat, latitude

## Installation

    pip install mongo_to_geojson

## CLI
The command line utility mongo2geojson.py is installed along with the pip package

**Simplest use case:**  dump a collection to a properly formatted geojson file.  As long as the documents in the worldcities collection have either a standard geometry property or a lat/lng values in common formats, no more is needed of you
   

     mongo2geojson.py mongodb://localhost/gisdata worldcities worldcities.json

**Advanced use case:**  you have finally figured out an aggregate pipeline that answers all your questions.  The output of the aggregate does not have a geometry object, nor does it have "standard" lat/long properties.  Further complicating matters is that some of the output documents will have coordinates in fooX and fooY properties, and other documents in barX and barY properties.  And you really don't want to try to copy & paste the aggregate pipeline into the command line - so you save it a file. 

    mongo2geojson.py mongodb://localhost/gisdata worldcities results.json --agg_pipeline=awesome_aggregate.json  --x_possible_names=fooX,barX y_possible_names=fooY,barY

Using JSON strings as commandline parameters can be quite a boondoggle owing to string escaping.  For your own sanity, I'd suggest dumping query, projection, and/or agg_pipeline parameters to a file, and using those file paths as the cli parameters. Should you decide to use JSON strings, there are some subtle differences on how to do so between windows and unix.

unix:

`--query='{"POP": {"$gte": 100000}}'`

windows:

`--query="{\"POP\": {\"$gte\": 100000}}"`


## API
Integrate into your own workflows

    from mongo_to_geojson import mongo_to_geojson 
	
	mongo_uri = 'mongodb://localhost/gisdata'
	collection = 'worldcities'
	output_geojson =  'worldcities.json'
	query = {"POP": {"$gte": 100000}}
	projection = {"CITY_NAME": 1, "x": 1, "y": 1, "_id": 0}
	
    try:  
        mongo_to_geojson(mongo_uri,collection,output_geojson,query=query,projection=projection)  
    except:  
        print('mongo_to_geojson no worky'))