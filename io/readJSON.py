import json
from os import listdir
from os.path import isfile, join, dirname
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
        _drug_epcList.append(_drug_epc)

    return _reactionList, _drug_nameList, _drug_epcList


if __name__ == "__main__":
    cur_path = dirname(__file__)

    # Preparing data
    peopleHash = {}

    logs = []

    data_path = join(cur_path, '../data')
    json_path = join(data_path, 'json')
    jsons = [f for f in listdir(json_path) if isfile(join(json_path, f))]

    obs = []

    for count, jFile in enumerate(jsons):
        try:
            _reactionList, _drug_nameList, _drug_epcList = read_info(join(json_path, jFile))

            x = zip(_drug_nameList, _drug_epcList)
            y = _reactionList
            obs.extend(zip(x, y))

            if count % 1000 == 0:
                print "%d files done..." % count

        except StopIteration as e1:
            logs.append((jFile, e1))
        except AttributeError as e2:
            logs.append((jFile, e2))

    obs_new = []
    for xs, ys in obs:
        for y in ys:
            # Purge empty drugs
            # todo: are these due to program bug or is the data actually empty?
            if len(xs[0]) > 0:
                obs_new.append((xs, y))

    pickle.dump(obs_new, open(
        join(data_path, 'obs.p'), 'wb'))
