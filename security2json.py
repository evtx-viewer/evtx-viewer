from lib import nom
import json
import argparse
import os
import sys

def process_json_file(input_file, output_file):
    with open(input_file, 'r') as file:
        data = file.read() 
        records = data.split('============')
        
        result = []
        for record in records:
            # Игнорирование пустых записей
            if not record.strip():
                continue
            
            try:
                # json parsing
                json_data = json.loads(record)
                
                # JSON-object checker
                if isinstance(json_data, dict):
                    # 'message' and 'raw' keys deletion
                    if 'message' in json_data:
                        del json_data['message']
                    if 'raw' in json_data:
                        del json_data['raw']
                    
                    # formatting json to single string
                    result.append(json.dumps(json_data))
            
            except json.JSONDecodeError:
                print("Invalid record:\n", record)
                continue
        
    # write output file
    with open(output_file, 'w') as file:
        file.write('\n'.join(result))

parser = argparse.ArgumentParser(description='Ingest EVTX files into Elasticsearch and more')
parser.add_argument("-f","--file", help="Input .evtx file. Default: Security.evtx", default="Security.evtx")
parser.add_argument("-o","--output", help="Output .json file. Default: Security.json", default="Security.json")
parser.add_argument("-c","--config", help="Config File Defaults to config.json", default="config.json")
args = parser.parse_args()

print("Getting Ready to convertation")
# Open Config File
with open(args.config,'r') as conf_file:
    config = json.load(conf_file)

# Grab All the files from input and from directory from config file
target_list = [args.file]
for path in config['inputs']['directory']['paths']:
    for root,d_names,f_names in os.walk(path):
        for f in f_names:
            if f.endswith('.evtx'):
                target_list.append(os.path.join(root, f))

print("found {} source files".format(len(target_list)))
print("=" * 24)
# Open Plugins
for output_plugin in config['outputs']:
    output = config['outputs'][output_plugin]
    if output['enabled']:
        #es output
        try:
            print("Trying '{}' Plugin".format(output['name']))
            nom_plugin = getattr(nom, output['name'])
            actioner = nom_plugin(output,config['parsing'])
        except AttributeError as errormsg:
            print("Cannot load module '{}' have you messed up the spelling???".format(output['name']))
            print(errormsg)
            sys.exit()
        # Ingest Files
        print("Ingesting files")
        for target in target_list:
            actioner.ingest_file(target)
        print("=" * 24)

process_json_file('log.txt', args.output)