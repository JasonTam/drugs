import json
from os import listdir
from os.path import isfile, join
from itertools import chain
import pickle


def read_info(filepath):
    with open(filepath) as file:
        try:
            jsonDict = json.loads(file.read())
        except StopIteration as e:
            raise e
    _resultList = jsonDict.get('results', {})

    _reactionList = []
    _drug_nameList = []
    _drug_epcList = []

    for report in _resultList:
        patient = report.get('patient', {})
        _reaction = [r.get("reactionmeddrapt", [""]) for r in patient.get('reaction', [])]
        _reaction = {x.lower() for x in _reaction}
        _reactionList.append(_reaction)

        _drug_name = [r.get("openfda", {}).get('generic_name', []) for r in patient.get('drug', [])]
        _drug_name = {x.lower() for x in chain(*_drug_name)}
        _drug_nameList.append(_drug_name)

        _drug_epc = [r.get("openfda", {}).get('pharm_class_epc', []) for r in patient.get('drug', [])]
        _drug_epc = {x.lower() for x in chain(*_drug_epc)}
        _drug_epcList.append((_drug_epc))

    return _reactionList, _drug_nameList, _drug_epcList


if __name__ == "__main__":
    # Preparing data
    peopleHash = {}

    logs = []

    mypath = './json/'
    jsons = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    count = 0

    Obs = []

    for jFile in jsons:
        try:
            _reactionList, _drug_nameList, _drug_epcList = read_info(join(mypath, jFile))

            Obs.extend(zip(_reactionList, _drug_nameList, _drug_epcList))

            count += 1
            if count % 1000 == 0: print "%d files done..." % count

        except StopIteration as e1:
            logs.append((jFile, e1))
        except AttributeError as e2:
            logs.append((jFile, e2))

    Obs_new = []
    for o in Obs:
        for reaction in o[0]:
            Obs_new.append((reaction, o[1], o[2]))
    pickle.dump(Obs_new, open('Obs.txt', 'w'))
