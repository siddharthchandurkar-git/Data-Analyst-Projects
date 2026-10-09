import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

@dlt.table(
    name = "stage_bookings"
)
def stage_bookings():
    # Reading from an external path with Spark is correct here
    df = spark.readStream.format("delta")\
        .load("/Volumes/flights_db/bronze/bronzevolume/bookings/data")
    
    return df

@dlt.view(
    name = "trans_bookings"
)
def trans_bookings():
    # FIX: Use dlt.read_stream to read from the DLT table defined above
    df = dlt.read_stream("stage_bookings")
    
    df = df.withColumn("amount", col("amount").cast(DoubleType()))\
            .withColumn("modifiedDate", current_timestamp())\
            .withColumn("booking_date", to_date(col("booking_date")))\
            .drop("_rescued_data")
    return df

rules = {
    "rule1": "booking_id IS NOT NULL",
    "rule2": "passenger_id IS NOT NULL"
}

@dlt.table (
    name = "silver_bookings"  # FIX: Added quotation marks here
)
@dlt.expect_all_or_drop(rules)
def silver_bookings():
    # FIX: Use dlt.read_stream to read from the DLT view defined above
    df = dlt.read_stream("trans_bookings")
    return df


#######################################################
### 2 -dim Flights - #####

import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *


@dlt.view(
    name = "trans_flights"
)
def trans_flights():
    # 1. Must use readStream for DLT CDC pipelines
    df = spark.readStream.format("delta")\
                .load("/Volumes/flights_db/bronze/bronzevolume/flights/data/")

    # 2. Apply your transformations
    df = df.withColumn("flight_date", to_date(col("flight_date")))\
           .drop("_rescued_data")\
           .withColumn("F_modifiedDate", current_timestamp())
    
    # 3. Return the dataframe (do not use display() in DLT)
    return df


dlt.create_streaming_table("silver_flights")

dlt.create_auto_cdc_flow(
  target = "silver_flights",
  source = "trans_flights",
  keys = ["flight_id"],
  sequence_by = col("F_modifiedDate"),
  stored_as_scd_type = 1
)

##################################################################
### 3 - dim passengers data
@dlt.view(
    name = "trans_passengers"
)

def trans_passengers():
    df = spark.readStream.format("delta")\
                .load("/Volumes/flights_db/bronze/bronzevolume/customers/data/")
    
    df = df.withColumn("P_modifiedDate", current_timestamp())\
           .drop("_rescued_data")

    
    return df

dlt.create_streaming_table("silver_passengers")

dlt.create_auto_cdc_flow(
  target = "silver_passengers",
  source = "trans_passengers",
  keys = ["passenger_id"],
  sequence_by= col("P_modifiedDate"),
  stored_as_scd_type = 1
)

##################################################################
### 4 - dim airports data
@dlt.view(
    name = "trans_airports"
)

def trans_airports():
    df = spark.readStream.format("delta")\
                .load("/Volumes/flights_db/bronze/bronzevolume/airports/data/")
    
    df = df.withColumn("A_modifiedDate", current_timestamp())\
           .drop("_rescued_data")

    
    return df

dlt.create_streaming_table("silver_airports")

dlt.create_auto_cdc_flow(
  target = "silver_airports",
  source = "trans_airports",
  keys = ["airport_id"],
  sequence_by= col("A_modifiedDate"),
  stored_as_scd_type = 1
)

#########################################
## Silver Business View

@dlt.table(
    name = "silver_business"
)
def silver_business():
    df = dlt.readStream("silver_bookings")\
            .join(dlt.readStream("silver_flights"), ["flight_id"])\
            .join(dlt.readStream("silver_passengers"), ["passenger_id"])\
            .join(dlt.readStream("silver_airports"), ["airport_id"])
    return df
