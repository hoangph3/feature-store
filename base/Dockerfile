FROM hoangph3/spark-py:3.1.2

# Cache Spark packages described above.
ENV APP_PACKAGES="--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,com.redislabs:spark-redis_2.12:2.6.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1"
ENV PYSPARK_SUBMIT_ARGS="$APP_PACKAGES pyspark-shell"
RUN spark-submit run-example $APP_PACKAGES example-class | true
