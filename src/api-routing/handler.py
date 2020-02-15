################
# 動作指示のAPIリクエスト用Lambda
# exec_home_control
# 
# この関数ではAPIへのGETリクエストをトリガーとする想定で
# 　①認証情報の確認 <TBD Cognitoオーソライザーによってはいらない可能性あり>
# 　②DB接続＆情報取得
# 　③各コンポーネント毎の実動作Lambdaを呼び出し実行
# を行うとする。
################

import sys
import json
from packages import boto3 

def createResponse(statusCode, header, body):
    response = {
        "isBase64Encoded": False,
        "statusCode": statusCode,
        "header": header,
        "body": json.dumps(body)
    }
    return response



def exec_home_control(event, context):
    client = boto3.client('lambda')

    # 認証用の情報を取得
    # ここは一回Cognitoのオーソライザー通ってきているはずだからその情報？？要調査


    # DB接続　
    # pathParam&queryParamからユーザ情報と動作させたい設備＆動作内容を取得
    # <TBD> ここで使われる機器によってDBから取得するべき情報が分かれる？上記クエリ情報はDB名と対応づくように出来ると良い
    # DBに検索投げて結果(RMminiで言うIP, MAC, port_num, signal)を取得する


    # Lambda呼び出し
    query = {
        "parent": "hello",
        "message": "hello test2!"
    }
    try:
        response = client.invoke(
            FunctionName='hack-porte-dev-test2', # ここは変数で渡せるようにする
            InvocationType='RequestResponse', # APIGatewayと同様のReq&Resにするにはこれを指定する
            LogType='Tail',
            Payload= json.dumps(query)
        )
    except: # 何のエラーが起こり得るか調査要
        body = {
            "message": "Component invoke error"
        }
        return createResponse(500, {}, body)

    # 正常実動作完了時
    body = {}
    if response['StatusCode'] == 200:
        payload =  json.loads(response['Payload'].read().decode('utf-8'))
        body = {
            "message": payload
        }

    return createResponse(200, {}, body)


