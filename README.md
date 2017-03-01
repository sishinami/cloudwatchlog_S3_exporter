# LambdaのログをS3に保存する

printでCloudWatchに出力されたログを一日一回 S3に回す時に使うソース

## 環境変数
* LOG_GROUP
* S3_BUCKET
* S3_FOLDER_PATH (空でもOK)

##sample
```
LOG_GROUP=/aws/lambda/lambda_1st_test
S3_BUCKET=logs
S3_FOLDER_PATH=exampleproject/stg/
```


ところでバケットってプロジェクト単位で作ってる？  
それとも LOG_BUCKETってでかい単位で作って 中のフォルダでプロジェクト分けてる？  
バケット上限あるし数増えると管理めんどくさいし、どうするのがベストなんかね  


## トリガーは CloudWatchScheduler

cron 書式が 僕らのLinuxとはなんか違うので適当にググってください。


