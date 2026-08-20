# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *
from typing import List
from pyspark.sql import DataFrame
from pyspark.sql.window import Window


# COMMAND ----------

import os
import sys

# COMMAND ----------

current_dir = os.getcwd()
sys.path.append(current_dir)

# COMMAND ----------

df_cust= spark.read.table("pysparkdbt.bronze.customers")
display(df_cust)

# COMMAND ----------

df_cust = df_cust.withColumn("domain",split(col('email'),'@')[1])
display(df_cust)

# COMMAND ----------

df_cust = df_cust.withColumn("phone_number",regexp_replace(col("phone_number"),r"[^0-9]",""))

# COMMAND ----------

display(df_cust)

# COMMAND ----------

df_cust = df_cust.withColumn("full_name",concat_ws(" ",col("first_name"),col("last_name")))
df_cust = df_cust.drop("first_name","last_name")
display(df_cust)

# COMMAND ----------

from utils.custom_utils import transformations

# COMMAND ----------

# DBTITLE 1,Cell 10
import importlib
from utils import custom_utils
importlib.reload(custom_utils)
from utils.custom_utils import transformations

cust_obj = transformations()
cust_df_trans = cust_obj.dedup(df_cust,['customer_id'],'last_updated_timestamp')
display(cust_df_trans)

# COMMAND ----------

# DBTITLE 1,Cell 11
# Import current_timestamp and inject it into custom_utils module
from pyspark.sql.functions import current_timestamp
import utils.custom_utils
utils.custom_utils.current_timestamp = current_timestamp

df_cust = cust_obj.process_timestamp(cust_df_trans)
display(df_cust)

# COMMAND ----------

# DBTITLE 1,Cell 12
from delta.tables import DeltaTable

if not spark.catalog.tableExists("pysparkdbt.silver.customers"):
    # Table doesn't exist - create it
    df_cust.write.format("delta")\
            .mode("overwrite")\
            .saveAsTable("pysparkdbt.silver.customers")
else:
    # Table exists - perform upsert/merge
    merge_condition = "src.customer_id = trg.customer_id"
    dlt_obj = DeltaTable.forName(spark, "pysparkdbt.silver.customers")
    dlt_obj.alias("trg").merge(df_cust.alias("src"), merge_condition)\
                        .whenMatchedUpdateAll(condition="src.last_updated_timestamp >= trg.last_updated_timestamp")\
                        .whenNotMatchedInsertAll()\
                        .execute()

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from pysparkdbt.silver.customers

# COMMAND ----------

# MAGIC %md
# MAGIC #### **Drivers**

# COMMAND ----------

df_driver = spark.read.table("pysparkdbt.bronze.drivers")
display(df_driver)

# COMMAND ----------

df_driver = df_driver.withColumn("phone_number",regexp_replace(col("phone_number"),r"[^0-9]",""))

# COMMAND ----------

df_driver = df_driver.withColumn("full_name",concat_ws(" ",col("first_name"),col("last_name")))
df_driver = df_driver.drop("first_name","last_name")
display(df_driver)

# COMMAND ----------

driver_obj = transformations()


# COMMAND ----------

df_driver = driver_obj.dedup(df_driver,['driver_id'],'last_updated_timestamp')

# COMMAND ----------

df_driver = driver_obj.process_timestamp(df_driver)

# COMMAND ----------

# DBTITLE 1,Cell 21
from delta.tables import DeltaTable

if not spark.catalog.tableExists("pysparkdbt.silver.drivers"):
    # Table doesn't exist - create it
    df_driver.write.format("delta")\
            .mode("overwrite")\
            .saveAsTable("pysparkdbt.silver.drivers")
else:
    # Table exists - perform upsert/merge
    merge_condition = "src.driver_id = trg.driver_id"
    dlt_obj = DeltaTable.forName(spark, "pysparkdbt.silver.drivers")
    dlt_obj.alias("trg").merge(df_driver.alias("src"), merge_condition)\
                        .whenMatchedUpdateAll(condition="src.last_updated_timestamp >= trg.last_updated_timestamp")\
                        .whenNotMatchedInsertAll()\
                        .execute()

# COMMAND ----------

# MAGIC %md
# MAGIC #### **locations**

# COMMAND ----------

df_loc = spark.read.table("pysparkdbt.bronze.locations")
display(df_loc)

# COMMAND ----------

loc_obj = transformations()


# COMMAND ----------

df_loc = loc_obj.dedup(df_loc,['location_id'],'last_updated_timestamp')
df_loc = loc_obj.process_timestamp(df_loc)

# COMMAND ----------

# DBTITLE 1,Cell 26
from delta.tables import DeltaTable

if not spark.catalog.tableExists("pysparkdbt.silver.locations"):
    # Table doesn't exist - create it
    df_loc.write.format("delta")\
            .mode("overwrite")\
            .saveAsTable("pysparkdbt.silver.locations")
else:
    # Table exists - perform upsert/merge
    merge_condition = "src.location_id = trg.location_id"
    dlt_obj = DeltaTable.forName(spark, "pysparkdbt.silver.locations")
    dlt_obj.alias("trg").merge(df_loc.alias("src"), merge_condition)\
                        .whenMatchedUpdateAll(condition="src.last_updated_timestamp >= trg.last_updated_timestamp")\
                        .whenNotMatchedInsertAll()\
                        .execute()

# COMMAND ----------

# MAGIC %md
# MAGIC #### **payments**

# COMMAND ----------

df_pay = spark.read.table("pysparkdbt.bronze.payments")
display(df_pay)

# COMMAND ----------

df_pay = df_pay.withColumn("online_payment_status",
                           when( ((col('payment_method')=='Card') & (col('payment_status')=='Success') ),
                                "online Success")
                           .when( ((col('payment_method')=='Card') & (col('payment_status')=='Failed') ),
                                "online failed")
                           .when( ((col('payment_method')=='Card') & (col('payment_status')=='Pending') ),
                                "online Pending")
                           .otherwise("offline"))


display(df_pay)

# COMMAND ----------

# DBTITLE 1,Cell 30
payment_obj = transformations()
df_pay = payment_obj.dedup(df_pay,['payment_id'],'last_updated_timestamp')
df_pay = payment_obj.process_timestamp(df_pay)
from delta.tables import DeltaTable

if not spark.catalog.tableExists("pysparkdbt.silver.payments"):
    # Table doesn't exist - create it
    df_pay.write.format("delta")\
            .mode("overwrite")\
            .saveAsTable("pysparkdbt.silver.payments")
else:
    # Table exists - perform upsert/merge
    merge_condition = "src.payment_id = trg.payment_id"
    dlt_obj = DeltaTable.forName(spark, "pysparkdbt.silver.payments")
    dlt_obj.alias("trg").merge(df_pay.alias("src"), merge_condition)\
                        .whenMatchedUpdateAll(condition="src.last_updated_timestamp >= trg.last_updated_timestamp")\
                        .whenNotMatchedInsertAll()\
                        .execute()
    

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from pysparkdbt.silver.payments

# COMMAND ----------

# MAGIC %md
# MAGIC #### **VEHICLES**

# COMMAND ----------

df_veh = spark.read.table("pysparkdbt.bronze.vehicles")
display(df_veh)


# COMMAND ----------

from pyspark.sql.functions import upper, col

df_veh = df_veh.withColumn("make",upper(col("make")))
display(df_veh)

# COMMAND ----------

vehicle_obj = transformations()
df_veh = vehicle_obj.dedup(df_veh,['vehicle_id'],'last_updated_timestamp')
df_veh = vehicle_obj.process_timestamp(df_veh)
from delta.tables import DeltaTable



# COMMAND ----------

if not spark.catalog.tableExists("pysparkdbt.silver.vehicles"):
    # Table doesn't exist - create it
    df_veh.write.format("delta")\
            .mode("overwrite")\
            .saveAsTable("pysparkdbt.silver.vehicles")
else:
    # Table exists - perform upsert/merge
    merge_condition = "src.vehicle_id = trg.vehicle_id"
    dlt_obj = DeltaTable.forName(spark, "pysparkdbt.silver.vehicles")
    dlt_obj.alias("trg").merge(df_veh.alias("src"), merge_condition)\
                        .whenMatchedUpdateAll(condition="src.last_updated_timestamp >= trg.last_updated_timestamp")\
                        .whenNotMatchedInsertAll()\
                        .execute()

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from pysparkdbt.silver.vehicles