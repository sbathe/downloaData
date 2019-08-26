#!/bin/bash
docker run -it --mount type=bind,source="$(pwd)/amfidata",target=/downloadData/amfidata --mount type=bind,source="$(pwd)/json_data",target=/downloadData/json_data  --env-file mongo_env datadownload
