import json

if __name__ == '__main__':
    aa = {'544270456': "空响不是空想"
         }
    with open(".//aa.json", "w") as fp:
        json.dump(aa, fp)
