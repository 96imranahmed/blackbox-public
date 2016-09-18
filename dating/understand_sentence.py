
import json
try:
    from urllib import urlopen
    from urllib import quote
except ImportError: # For Python 3
    from urllib.request import urlopen
    from urllib.parse import quote

def get_NLP(msg):
    data = load_json(msg)
    return get_intent(data)

def create_url(sentence):
    params = quote(sentence)
    url = \
    'https://api.projectoxford.ai/luis/v1/application?id=4bfeb1ef-2c16-4990-a35d-d7beb009fa67&subscription-key=7228827ba793462ca04c48b723deccac&q=' + params
    return url


def load_json(sentence):
    url = create_url(sentence)
    response = urlopen(url)
    data = json.loads(response.read().decode("utf-8"))
    return data

def get_intent(data):
    flag_empty = False
    most_likely = data['intents'][0]
    second_most_likely = data['intents'][1]
    output = {}
    if most_likely['score'] > 0.1:
        intent = most_likely['intent']
        print(intent)
        output["intent"] = intent
        if(intent == "None"):
            pass
        elif(intent == "DateInfo"):
            pass
        elif(intent == "Accept"):
            pass
        elif(intent=="Pickup"):
            pass
        elif(intent == "Name"):
            actions = most_likely['actions']
            parameters = actions[0]['parameters'][0]
            value = parameters['value']
            if value is None:
                output["values"] = value
            else:
                output["values"] = value[0]['entity']
        elif(intent=="Recommend"):
            actions = most_likely['actions']
            parameters = actions[0]['parameters'][0]
            value = parameters['value']
            if value is None:
                output["values"] = value
            else:
                output["values"] = value[0]['entity']
        elif(intent=="SetDate"):
            actions = most_likely['actions']
            parameters = actions[0]['parameters'][0]
            value = parameters['value']
            if value is None:
                output["values"] = value
            else:
                values = []
                for x in value:
                    values.append(x['entity'])
                output["values"] = values
        elif(intent=="Like"):
            actions = most_likely['actions']
            parameters = actions[0]['parameters'][0]
            value = parameters['value']
            if value is None:
                output["values"] = value
            else:
                output["values"] = value[0]['entity']
        elif(intent=="Dislike"):
            actions = most_likely['actions']
            parameters = actions[0]['parameters'][0]
            value = parameters['value']
            if value is None:
                output["values"] = value
            else:
                output["values"] = value[0]['entity']
        elif(intent=="More"):
            pass
        elif(intent=="Decline"):
            pass
        extras={}
        for x in data['entities']:
            extras[x['type']] = x['entity']
        output["extras"] = extras
        if len(extras) == 0:
            flag_empty = True
    else:
        output["intent"] = "Confused"
    return output, flag_empty



if __name__ == '__main__':
    data = load_json('her name? Mary')
    print(get_intent(data))
