#!/bin/bash
docker run -it --mount type=bind,source="$(pwd)/amfidata",target=/downloadData/amfidata --mount type=bind,source="$(pwd)/jsondata",target=/downloadData/jsondata  --env-file mongo_env datadownload
