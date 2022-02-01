import argparse
import time
import pandas as pd
from pyspark import SparkConf
from pyspark.sql import SparkSession

from sedona.register.geo_registrator import SedonaRegistrator
from pyspark.sql.types import StructType, IntegerType, DoubleType
from sedona.utils import KryoSerializer, SedonaKryoRegistrator

from sample_code.common_db import engine


schema_point = StructType() \
    .add("sensor_id", IntegerType(), False) \
    .add("lon", DoubleType(), False) \
    .add("lat", DoubleType(), False)


def gen_buffers(input_file, buffer_sizes):

    point_df = spark.read.option("header", True).schema(schema_point).csv(input_file)
    point_df.createOrReplaceTempView("points")

    """ complete the function to generate buffers """
    buffer_df = [Code Block]

    buffer_df.createOrReplaceTempView("buffers")
    buffer_df.show()


def gen_geographic_features(osm_table, out_path):

    osm_df = pd.read_sql(f"select geo_feature, feature_type, wkb_geometry from {osm_table}", engine)
    osm_df = spark.createDataFrame(osm_df).persist()
    osm_df.createOrReplaceTempView("osm")
    # print(osm_df.rdd.getNumPartitions())

    """ compute geographic features for different geom """
    if osm_table == 'polygon_features':
        geographic_feature_df = [Code Block]

    elif osm_table == 'line_features':
        geographic_feature_df = [Code Block]

    elif osm_table == "point_features":
        geographic_feature_df = [Code Block]

    else:
        raise NotImplementedError

    start_time = time.time()
    geographic_feature_df.coalesce(1).write.csv(f'{out_path}/{osm_table}_{int(time.time()/1000)}',
                                                header=True, sep=',')
    print(time.time() - start_time)
    # print(geographic_feature_df)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default='data/ca_purple_air_locations_subset.csv',
                        help='The path to the location file.')
    parser.add_argument('--osm_table', type=str, default='polygon_features',
                        help='The OSM table to query.')
    parser.add_argument('--out_path', type=str, default='./results',
                        help='The output folder path.')
    args = parser.parse_args()

    conf = SparkConf(). \
        setMaster("local[*]"). \
        set("spark.executor.memory", '4g'). \
        set("spark.driver.memory", '16g')

    spark = SparkSession. \
        builder. \
        appName("hw1"). \
        config(conf=conf). \
        config("spark.serializer", KryoSerializer.getName). \
        config("spark.kryo.registrator", SedonaKryoRegistrator.getName). \
        getOrCreate()

    SedonaRegistrator.registerAll(spark)

    gen_buffers(args.input_file, buffer_sizes=[100, 500, 1000])
    gen_geographic_features(osm_table=args.osm_table, out_path=args.out_path)

    spark.stop()

