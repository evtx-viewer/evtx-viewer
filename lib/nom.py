from evtx import PyEvtxParser
import json
import datetime
import sys
import requests
from urllib3.exceptions import InsecureRequestWarning

# This file is parsing the evtx file and any default modules

# Example Standard Out Plugin
class stdout_nom():
    def __init__(self,config,parsing_config):
        self.name = "standard out JSON example"
        self.welm_map = load_welm_map(parsing_config['welm']['mapping_file'])
        self.welm_mode = parsing_config['welm']['enabled']
    def ingest_file(self,filename):
        print("Starting logging to log.txt on target {}".format(filename))
        log_filename = "log.txt"
        with open(log_filename, "w") as log_file:
            for event in nom_file(filename,self.welm_map):
                #print(json.dumps(event,indent=2))
                log_file.write(json.dumps(event,indent=2))
                #print("=" * 12)
                log_file.write("=" * 12)
            log_file.write("Finished Shouting")

# Get values form EVTX-RS json which may be attributes from XML land 
def get_value(item):
    if item != 0 and item == None:
        return None
    if isinstance(item,dict):
        output = {}
        # XML Peeps
        if '#text' in item:
            output = str(item['#text'])
        elif '#attributes' in item:
            for attr in item['#attributes']:
                output[attr.lower()] = item['#attributes'][attr]
            for thing in item:
                if thing != '#attributes':
                    output[thing.lower()] = item[thing]
        # Regular Object
        else:
            for thing in item:
                output[thing.lower()] = item[thing]
        if not item:
            output = None
        return output
    else:
        # just a variable strings for es as numbers dont make sense at the moment
        output = str(item)
    return output

# Fetch Whole JSON section
def get_section(item):
    output = {}
    for field in item:
        value = get_value(item[field])
        if value != None:
            output[field.lower()] = value
        if value == 0:
            output[field.lower()] = str(value)
    return output


# iterator from evtx-rs You can use this standalone if you want (ie for splunk)
def nom_file(filename,welm_map):
    parser = PyEvtxParser(filename)
    # Open Records
    for record in parser.records_json():
        data = json.loads(record['data'])
        try:
            # Event Log event
            event = {'recordid': str(record['event_record_id'])}
            event.update(get_section(data['Event']['System']))
            if data['Event'].get('EventData'):
                event['event_data'] = get_section(data['Event']['EventData'])
            if data['Event'].get('UserData'):
                #print(data['Event'].get('UserData'))
                if data['Event']['UserData'].get('EventXML'):
                    event['event_data'] = get_section(data['Event']['UserData']['EventXML'])
                else:
                    # not sure about what other namesspaces are here so for now just this loop
                    for ns in data['Event']['UserData']:
                        event['event_data'] = get_section(data['Event']['UserData'][ns])
            if isinstance(event['eventid'], dict):
                print(event['eventid'])
                print("#"*20)
                print(json.dumps(event,indent=3))
                print("#"*20)
                print(json.dumps(data,indent=3))
            key = make_key(
                event.get('channel') or '',
                event['provider']['name'],
                event['eventid']
                )
            if key in welm_map:
                if welm_map[key]['swap_mode'] and welm_map[key]['params'] != []:
                    if event.get('event_data') or False:
                        swap_target = 'event_data'
                    elif event.get('user_data') or False:
                        swap_target = 'user_data'
                    else:
                        swap_target = None
                        event['message'] = welm_map[key]['format_string']
                    if swap_target:
                        swap_values = ['bump']
                        for param in welm_map[key]['params']:
                            swap_values.append(event[swap_target].get(param) or "")
                    #print(key)
                    #print(welm_map[key]['format_string'])
                    #print(welm_map[key]['params'])
                    #print(swap_values)
                        try:
                            event['message'] = welm_map[key]['format_string'].format(*swap_values)
                        except:
                            event['message'] = welm_map[key]['format_string']
                else:
                    event['message'] = welm_map[key]['format_string']
            else:
                event['message'] = "{} | {} | {} | Unknown Message String".format(
                event['eventid'],
                event.get('channel') or '',
                event['provider']['name']
                )
            # Raw Document
            event['raw'] = record['data']
            yield event
        except KeyError as errormsg:
            print("Soemthing went wrong parsing this event")
            print(json.dumps(data,indent=4))
        

# make matching key
def make_key(channel,provider,event_id):
    key = channel + provider + event_id
    return key.lower()

# Load the Welm data
def load_welm_map(filename):
    with open(filename,'r') as in_file:
        data = json.load(in_file)
    # I think a flat dictionary is better for this sort of thing
    mapping_dict = {}
    for channel in data:
        for provider in data[channel]:
            for event_id in data[channel][provider]:
                mapping_dict[make_key(channel,provider,event_id)] =  data[channel][provider][event_id]
    return mapping_dict
    