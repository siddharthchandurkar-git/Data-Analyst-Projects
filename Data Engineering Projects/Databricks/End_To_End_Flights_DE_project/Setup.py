# Databricks notebook source
# MAGIC %sql
# MAGIC create volume flights_db.rawdata.rawvolume

# COMMAND ----------

dbutils.fs.mkdirs("/Volumes/flights_db/rawdata/rawvolume/raw_data/airports")

# COMMAND ----------

# MAGIC %sql
# MAGIC create schema flights_db.gold

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from delta.`/Volumes/flights_db/bronze/bronzevolume/flights/data/`