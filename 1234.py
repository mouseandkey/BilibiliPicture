import json

if __name__ == '__main__':
    aa = [{"uid": 194846269, 
           "uname": "秋风笑里有明哲_", 
           "dynamic_id": 0}
         ]
    with open(".//dynamic.json.", "w") as fp:
        json.dump(aa, fp)
