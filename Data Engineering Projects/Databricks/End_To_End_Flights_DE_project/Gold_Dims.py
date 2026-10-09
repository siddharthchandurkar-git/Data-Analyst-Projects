# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from flights_db.silver.silver_passengers

# COMMAND ----------

# MAGIC %md
# MAGIC ## parameters
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### **Fetching Parameters & Creating Variables**

# COMMAND ----------

catalog = "flights_db"
key_cols = "['flight_id']"
key_cols_list = eval(key_cols)

cdc_col = "f_modifiedDate"

backdated_refresh = ""

source_object = "silver_flights"

source_schema = "silver"

target_schema = "gold"

target_object = "Dimflights"

#surrogate Key
surrogate_key = "DimFlightsKey"

# COMMAND ----------

# catalog = "flights_db"
# key_cols = "['airport_id']"
# key_cols_list = eval(key_cols)

# cdc_col = "A_modifiedDate"

# backdated_refresh = ""

# source_object = "silver_airports"

# source_schema = "silver"

# target_schema = "gold"

# target_object = "DimAirports"

# #surrogate Key
# surrogate_key = "DimAirportsKey"

# COMMAND ----------

# catalog = "flights_db"
# key_cols = "['passenger_id']"
# key_cols_list = eval(key_cols)

# cdc_col = "P_modifiedDate"

# backdated_refresh = ""

# source_object = "silver_passengers"

# source_schema = "silver"

# target_schema = "gold"

# target_object = "DimPassengers"

# #surrogate Key
# surrogate_key = "DimPassengersKey"

# COMMAND ----------

key_cols_list

# COMMAND ----------

# MAGIC %md
# MAGIC ### **DATA INGSTION INCREMENTAL**

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC #### last load date

# COMMAND ----------

#No backdated refresh
if len(backdated_refresh) == 0:
    # if table exists in the destination
    if  spark.catalog.tableExists(f"flights_db.{target_schema}.{target_object}"):

        last_load = spark.sql(f"select max({cdc_col}) from {catalog}.{target_schema}.{target_object}").collect()[0][0]

    else:
        last_load = "1900-01-01 00:00:00"
        #Yes Back dated refresh
else:
    last_load = backdated_refresh


# COMMAND ----------

last_load

# COMMAND ----------

df_src =  spark.sql(f"select * from flights_db.{source_schema}.{source_object} where {cdc_col} >= '{last_load}'")
df_src.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Old vs New Records

# COMMAND ----------



# COMMAND ----------

if spark.catalog.tableExists(f"{catalog}.{target_schema}.{target_object}"):
    #Key cols string for incremental
    key_cols_string_incremental = ", ".join(key_cols_list)
    df_trg = spark.sql(f"select {key_cols_string_incremental},{surrogate_key},create_date,update_date from {catalog}.{target_schema}.{target_object}")
else:

    # Key Columns String for initial
    key_cols_string_init = [f"'' AS {i}" for i in key_cols_list]
    key_cols_string_init = ", ".join(key_cols_string_init)
    
    df_trg = spark.sql(f"select {key_cols_string_init},cast('0' AS int) as {surrogate_key},cast('1900-01-01 00:00:00' as timestamp) as create_date,cast('1900-01-01 00:00:00'as timestamp) as update_date where 1=0") #from {catalog}.{target_schema}.{target_object}")


# COMMAND ----------


df_trg.display()

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC join condition

# COMMAND ----------

join_condition = ' AND '.join([f"src.{i} = trg.{i}" for i in key_cols_list])
# df_trg.createOrReplaceTempView("trg")
#'

# COMMAND ----------

df_src.createOrReplaceTempView("src")
df_trg.createOrReplaceTempView("trg")

df_join = spark.sql(f"""
                        select src.*,
                                trg.{surrogate_key},
                                trg.create_date,
                                trg.update_date
                        from src
                        left join trg
                        on {join_condition}
                        """)

#

# COMMAND ----------

df_join.display()

# COMMAND ----------

df_old = df_join.filter(col(f'{surrogate_key}').isNotNull())

df_new = df_join.filter(col(f'{surrogate_key}').isNull())

# COMMAND ----------

df_old.display()


# COMMAND ----------

# MAGIC %md
# MAGIC #### preparing df old
# MAGIC

# COMMAND ----------

df_old_enr = df_old.withColumn('update_date',(current_timestamp()))

# COMMAND ----------

# MAGIC %md
# MAGIC #### Preparing Df new

# COMMAND ----------

if spark.catalog.tableExists(f"{catalog}.{target_schema}.{target_object}"):
    max_surrogate_key = spark.sql(f"""
                                  select max ({surrogate_key}) from {catalog}.{target_schema}.{target_object}
                                  """).collect()[0][0]
    df_new_enr = df_new.withColumn(f'{surrogate_key }',lit(max_surrogate_key)+lit(1)+monotonically_increasing_id())\
                    .withColumn('create_date',current_timestamp())\
                    .withColumn('update_date',current_timestamp())
    
else:
    max_surrogate_key = 0
    df_new_enr = df_new.withColumn(f'{surrogate_key }',lit(max_surrogate_key)+lit(1)+monotonically_increasing_id())\
                    .withColumn('create_date',current_timestamp())\
                    .withColumn('update_date',current_timestamp())
    

# COMMAND ----------

df_old_enr.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #### establishing an union between old and new records

# COMMAND ----------

df_union = df_old_enr.unionByName(df_new_enr)



# COMMAND ----------

df_union.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #### implementing upsert logic

# COMMAND ----------

from delta.tables import DeltaTable


# COMMAND ----------

if spark.catalog.tableExists(f'{catalog}.{target_schema}.{target_object}'):
    
    dlt_obj = DeltaTable.forName(spark, f'{catalog}.{target_schema}.{target_object}')
    dlt_obj.alias("trg").merge(df_union.alias("src"), f"trg.{surrogate_key} = src.{surrogate_key}")\
                        .whenMatchedUpdateAll(condition = f'src.{cdc_col} >= trg.{cdc_col}')\
                        .whenNotMatchedInsertAll()\
                        .execute()
        
 

else:

    df_union.write.format("delta")\
        .mode("append")\
        .saveAsTable(f'{catalog}.{target_schema}.{target_object}')

    

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from flights_db.gold.dimpassengers where passenger_id = 'P0049'