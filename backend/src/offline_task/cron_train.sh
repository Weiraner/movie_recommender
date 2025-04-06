#!/bin/bash

DATE=$(date +%F)
echo "[${DATE}] Running Spark ALS job..."

# Spark submit (example)
spark-submit ../model/train_als.py

# After training, you can export vectors to SQLite or Redis
