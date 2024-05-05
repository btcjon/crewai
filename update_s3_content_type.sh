#!/bin/bash

BUCKET="cashdaily1"
PREFIX="10KIn30DaysBlueprint/"

# List all files under the PREFIX and update their content type
aws s3 ls s3://$BUCKET/$PREFIX --recursive | while read -r line; do
    KEY=`echo $line | awk '{print $4}'`
    if [[ "$KEY" =~ \.jpg$|\.jpeg$ ]]; then
        CONTENT_TYPE="image/jpeg"
    elif [[ "$KEY" =~ \.png$ ]]; then
        CONTENT_TYPE="image/png"
    elif [[ "$KEY" =~ \.mp3$ ]]; then
        CONTENT_TYPE="audio/mpeg"
    else
        continue
    fi
    echo "Updating $KEY to $CONTENT_TYPE"
    aws s3 cp s3://$BUCKET/$KEY s3://$BUCKET/$KEY --metadata-directive REPLACE --content-type $CONTENT_TYPE
done
