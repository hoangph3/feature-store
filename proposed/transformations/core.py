from dataclasses import dataclass

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, from_json, to_json, struct
from pyspark.sql.types import StructType, StructField, ArrayType, FloatType, IntegerType

import settings
from schemas import get_entity_name, get_featuregroup_name, get_spark_schema


@dataclass
class FeatureGroup:
    name: str
    key: str
    input_entity: str
    output_entity: str

    def transform(self, df: DataFrame) -> DataFrame:
        pass


# TODO: register schema on the registry before sending to kafka
class FeatureGroupJob:
    def __init__(self, spark: SparkSession, definition: FeatureGroup):
        self.spark = spark
        self.feature_group = get_featuregroup_name(definition.name)
        self.feature_group_key = definition.key
        self.input_entity = get_entity_name(definition.input_entity)
        self.definition = definition

    def subscribe(self) -> DataFrame:
        return (
            self.spark
            .readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", settings.KAFKA_BROKER)
            .option("subscribe", self.input_entity)
            .load()
        )

    def from_kafka(self, df: DataFrame, full_schema: str) -> DataFrame:
        """Convert kafka value to a dataframe with flattened fields"""
        return (
            df
            # .selectExpr("CAST(key as STRING)", "CAST(value AS STRING)")
            .selectExpr("CAST(value AS STRING)")
            .withColumn(
                "record",
                from_json(col("value"), get_spark_schema(full_schema))
            )
            .select("record.*")
        )

    def to_kafka(self, df: DataFrame, key_field: str) -> DataFrame:
        """Convert dataframe to kafka format with key and value fields"""
        return df.select(
            # col(key_field).alias("key"),
            to_json(struct([df[x] for x in df.columns])).alias("value")
        )

    def foreach_batch(self, batch_df: DataFrame, batch_id: int):
        (
            batch_df
            # .selectExpr("CAST(key as STRING)", "CAST(value AS STRING) as record")
            # .selectExpr("CAST(value AS STRING) as record")
            .write
            .format("mongo")
            .mode("append")
            .option("database", settings.MONGO_DATABASE)
            .option("collection", self.feature_group)
            .save()
        )

    def start_query(self, df: DataFrame):
        return (
            df
            .writeStream
            .queryName(self.feature_group)
            .outputMode("append")
            .foreachBatch(self.foreach_batch)
            .start()
        )

    def run(self):
        # Subscribe to input entity kafka topic
        df = self.subscribe()

        # Convert kafka value to dataframe
        df = self.from_kafka(df, self.input_entity)

        # Apply the user defined transformation
        df = self.definition.transform(df)

        # Start running the query
        return self.start_query(df)
