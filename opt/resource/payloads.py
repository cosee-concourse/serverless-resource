check_payload = ('{"source":{'
                 '"access_key_id":"apiKey123",'
                 '"secret_access_key":"secretKey321",'
                 '"region_name":"eu-west-1"'
                 '},'
                 '"version":{"stage":"release"}}')
in_payload = ('{"source":{'
              '"access_key_id":"apiKey123",'
              '"secret_access_key":"secretKey321",'
              '"region_name":"eu-west-1"'
              '},'
              '"version":{"stage":"release"}}')
out_deploy_payload = ('{"params":{'
               '"stage":"version-v1-dev",'
               '"deploy": true,'
               '"artifact_folder": "artifact/lambda",'
               '"serverless_file": "source/ci'
               '"},'
               '"source":{'
               '"access_key_id":"apiKey123",'
               '"secret_access_key":"secretKey321",'
               '"region_name":"eu-west-1'
               '"},'
               '"version":{"stage":"release"}}')
out_remove_payload = ('{"params":{'
               '"stage":"version-v1-dev",'
               '"remove": true,'
               '"artifact_folder": "artifact/lambda",'
               '"serverless_file": "source/ci'
               '"},'
               '"source":{'
               '"access_key_id":"apiKey123",'
               '"secret_access_key":"secretKey321",'
               '"region_name":"eu-west-1'
               '"},'
               '"version":{"stage":"release"}}')
