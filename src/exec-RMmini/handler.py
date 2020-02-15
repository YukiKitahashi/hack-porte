################
# RMmini実動作部分Lambdaコード
# exec_RMmini
################

import json
import ir


def createResponse(statusCode, header, body):
    response = {
        "isBase64Encoded": False,
        "statusCode": statusCode,
        "header": header,
        "body": json.dumps(body)
    }
    return response

# このLambdaはトリガーを持たない：上位Lambdaからの呼び出し専用となる
def exec_RMmini(event, context):
    # この4つについては上位Lambdaから必ず渡される想定とする
    IP = event['queryStringParameters']['IP']
    MAC = event['queryStringParameters']['MAC']
    port_number = event['queryStringParameters']['port_num']
    signal = event['queryStringParameters']['signal']

    try:
        RM3Device = ir.RM3Mini(IP, MAC, port_number)
        RM3Device.sendIR(signal)

        body = {
            "message" : "complete sending signal!"
        }
        return createResponse(200, {}, body)

    except:
        body = {
            "message" : "Error occurred."
        }
        return createResponse(500, {}, body)