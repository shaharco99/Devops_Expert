# Helm
command to start :
"helm lint helm_test/"
test template :
"helm template helm_test/" 
to check with values file add : "-f helm_test/airflow.values.yaml"
to deploy:
"helm upgrade --install {{RELEASE_NAME}}"
if not using file helm uses default values (jenkins)
to deploy with values file add : "-f helm_test/airflow.values.yaml"
