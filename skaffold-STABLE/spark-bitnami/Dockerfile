FROM bitnami/spark 
## muss noch angepasst werden
ENTRYPOINT spark-submit --verbose \
	--master local \
	--conf "spark.jars.ivy=${IVY_PACKAGE_DIR}" \
	--packages "${SPARK_KAFKA_DEPENDENCY}" \
	--py-files /app/dependencies.zip \
	/app/spark-app.py

CMD [""]