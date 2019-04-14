import json

with open ('mappable.json') as data_file:
    data = json.load(data_file)

med_list ={}
#hashtable

def update_med_list(meds, med_list, geotag, time):
        for med in meds:
            result = med_list.get(med)
            if result:
                result['count'] += 1
                result['geo'].append(geotag)
                result['time'].append(time)
                med_list[med] = result
            else:
                med_list[med]={
                    'count': 1,
                    'geo': geotag,
                    'time':[time]
                }
            return med_list

def medicine_list(data, med_list):
    for twit in data:
                lista = update_med_list(twit['medicines'], med_list, twit['locations'],twit['tweet_date'])
    return lista

a = medicine_list(data, med_list)
print(a)
with open('Medicines.json','w') as outfile:
    json.dump(a,outfile)
