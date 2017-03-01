# coding: utf-8
"""
#CloudWatchのログをS3に保存

##必要環境変数
*LOG_GROUP
*S3_BUCKET
*S3_FOLDER_PATH (空でもOK)

##sample
```
LOG_GROUP=/aws/lambda/lambda_1st_test
S3_BUCKET=logs
S3_FOLDER_PATH=exampleproject/stg/
```

## 注意点

* Lambda,CloudWatchが 同じタイムゾーンで動作していること  
* 一日１度回る事を想定しているので週１や月１であれば要修正


"""
import datetime
import time
import boto3
import os
import logging

log_group_name = os.environ['LOG_GROUP']
s3_bucket_name = os.environ['S3_BUCKET']
s3_prefix = os.environ['S3_FOLDER_PATH']  + '%s' % (datetime.date.today() - datetime.timedelta(days = 1))

def get_from_timestamp():
    """
    動作した前日０時を取得
    一日１回を想定しているので、週１等の場合は要修正
    
    """
    today = datetime.date.today()
    yesterday = datetime.datetime.combine(today - datetime.timedelta(days = 1), datetime.time(0, 0, 0))
    timestamp = time.mktime(yesterday.timetuple())
    return int(timestamp)

def get_to_timestamp(from_ts):
    """
    前日２４時を取得
    """
    return from_ts + (60 * 60 * 24) - 1

def lambda_handler(event, context):
    from_ts = get_from_timestamp()
    to_ts = get_to_timestamp(from_ts)
    print 'Timestamp: from_ts %s, to_ts %s' % (from_ts, to_ts)

    # logs をへの接続を設定
    client = boto3.client('logs')
    #create_export_task は CloudWatchLogs にある S3エクスポート機能
    
    response = client.create_export_task(
        logGroupName      = log_group_name,
        fromTime          = from_ts * 1000,
        to                = to_ts * 1000,
        destination       = s3_bucket_name,
        destinationPrefix = s3_prefix
    )
    return response
