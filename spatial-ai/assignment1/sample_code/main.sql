-- create postgis extension
CREATE EXTENSION postgis;

-- create a table for locations
-- you might want to create two tables for the two location sets, same for the following code
DROP TABLE IF EXISTS sample_locations;
CREATE TABLE sample_locations(
  sensor_id INTEGER PRIMARY KEY,
  lon DOUBLE PRECISION NOT NULL,
  lat DOUBLE PRECISION NOT NULL);

-- create a table for buffers
DROP TABLE IF EXISTS sample_location_buffers;
CREATE TABLE sample_location_buffers(
	gid BIGSERIAL PRIMARY KEY,
	sensor_id INTEGER,
	lon DOUBLE PRECISION NOT NULL,
	lat DOUBLE PRECISION NOT NULL,
	buffer_size INTEGER NOT NULL,
	buffer geometry(Polygon,4326) NOT NULL);
CREATE INDEX "sample_location_buffers_buffer_idx" ON sample_location_buffers USING gist(buffer);

-- insert buffers into the buffer table
INSERT INTO sample_location_buffers
-- # code block # --

CREATE INDEX "line_features_wkb_geometry_geom_idx" ON line_features USING gist(wkb_geometry);
CREATE INDEX "point_features_wkb_geometry_geom_idx" ON point_features USING gist(wkb_geometry);
CREATE INDEX "polygon_features_wkb_geometry_geom_idx" ON polygon_features USING gist(wkb_geometry);

-- create a table for geographic features
DROP TABLE IF EXISTS geographic_features;
CREATE TABLE geographic_features(
	gid BIGSERIAL PRIMARY KEY,
	sensor_id INTEGER NOT NULL,
	geom_type TEXT NOT NULL,
	geo_feature TEXT NOT NULL,
	feature_type TEXT NOT NULL,
	buffer_size INTEGER NOT NULL,
	value  DOUBLE PRECISION);

-- insert geographic features into the geographic_features table
INSERT INTO geographic_features
-- # code block # --