import json
from clean import clean_xml

# open
with open('keyword-database-export.json') as file:
    content = file.read()
whole_json = json.loads(content)

# process
for entry in whole_json.values():
    if 'definition' in entry:
        entry['definition'] = clean_xml(entry['definition'])

# save
json_text = json.dumps(whole_json, indent=2)
with open("keyword-database-cleaned.json", "w") as outfile:
    outfile.write(json_text)
