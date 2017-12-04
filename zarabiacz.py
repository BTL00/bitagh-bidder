import requests
import hmac
import hashlib
import time
import json
import sys


def request_prepare(payload):
	tosign_ = ("&".join( [i + '=' + payload[i] for i in payload] )).encode('utf8')
	return hmac.new(secret_, tosign_, hashlib.sha512).hexdigest();

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj    


if (len(sys.argv) > 1):
	public_ = sys.argv[1].encode('utf8')
	secret_ = sys.argv[2].encode('utf8')



current_info = {}
old_info = {}


def main_loop():
	moment_ = int( time.time() )
	post_ = {'method': 'info', 'moment': str(moment_)}


	hash_ = request_prepare(post_);

	r = requests.post("https://bitbay.net/API/Trading/tradingApi.php", data=post_, headers = {'API-Key': public_, 'API-Hash': hash_})
	print(r.status_code, r.reason)
	return(r.text)


def main_ui(object_):
	parse_ui(object_) 


def parse_ui(object_):
	pp_json(object_)	

counter__ = 0
while True:
	counter__+=1
	time.sleep(0.5)
	if(counter__ % 5 == 0):
		current_info = main_loop()
	if(ordered(current_info) != ordered(old_info)): # nie dziala :(
		main_ui(current_info)


