# Databricks notebook source
dbutils.widgets.text("src","")

# COMMAND ----------

src_value = dbutils.widgets.get("src")
src_value

# COMMAND ----------

# MAGIC %md
# MAGIC ## data ingestion increamental
# MAGIC

# COMMAND ----------

df = spark.readStream.format("cloudFiles") \
  .option("cloudFiles.format", "csv") \
  .option("cloudFiles.schemaLocation", f"/Volumes/flights_db/bronze/bronzevolume/{src_value}/checkpoint") \
  .option("cloudFiles.schemaEvolutionMode", "rescue") \
  .load(f"/Volumes/flights_db/rawdata/rawvolume/raw_data/{src_value}/")

# COMMAND ----------

df.writeStream.format("delta")\
    .outputMode("append")\
    .trigger(once=True)\
    .option("checkpointLocation",f"/Volumes/flights_db/bronze/bronzevolume/{src_value}/checkpoint")\
    .option("path",f"/Volumes/flights_db/bronze/bronzevolume/{src_value}/data")\
    .start()  

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from delta.`/Volumes/flights_db/bronze/bronzevolume/customers/data/`

# COMMAND ----------

