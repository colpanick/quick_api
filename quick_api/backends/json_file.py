import json
from pathlib import Path

from .base import Base


def _sorted_records(records, key, order):
    records = records.copy()
    if order in ["dsc", "desc"]:
        rev = True
    else:
        rev = False

    records.sort(key=lambda x: x[key], reverse=rev)

    return records


def _record_by_id(records, record_id):
    record_id = int(record_id)
    for record in records:
        if record["id"] == record_id:
            return record


class JsonFile(Base):

    def __init__(self, json_file):
        self.json_file = Path(json_file)
        self.indent = 2
        self.json_data = None

        if not self.json_file.is_file():
            self.json_data = {}
            self.write_json_data()
        else:
            self.update_json_data()

    def update_json_data(self):
        with open(self.json_file, "r") as jf:
            self.json_data = json.load(jf)

    def write_json_data(self):
        with open(self.json_file, "w") as jf:
            json.dump(self.json_data, jf, indent=self.indent)

    def datasets(self):
        return self.json_data.keys()

    def dataset_records(self, dataset):
        try:
            records = self.json_data[dataset]
        except KeyError:
            raise KeyError(f"Invalid dataset: {dataset}")

        return records

    def get_all(self, dataset, sort=None, order=None):
        records = self.dataset_records(dataset)

        if sort:
            records = _sorted_records(records, sort, order)

        return json.dumps(records, indent=self.indent)

    def get_record(self, dataset, record_id):
        record_id = int(record_id)
        records = self.dataset_records(dataset)
        record = [r for r in records if r["id"] == record_id]
        if record:
            record = record[0]
        else:
            raise KeyError(f"id:{record_id} not found in {dataset}")
        return json.dumps(record, indent=self.indent)

    def post(self, dataset, data):
        records = self.dataset_records(dataset)
        new_id = max([record["id"] for record in records]) + 1
        data["id"] = new_id
        records.append(data)
        self.write_json_data()
        return json.dumps(data, indent=self.indent)

    def _put_patch(self, dataset, record_id, data, is_put):
        records = self.dataset_records(dataset)
        record = _record_by_id(records, record_id)
        if not record:
            raise KeyError(f"id:{record_id} not found in {dataset}")
        if is_put:
            record.clear()
        record.update(data)
        record["id"] = record_id
        self.write_json_data()
        return json.dumps(record, indent=self.indent)

    def put(self, dataset, record_id, data):
        return self._put_patch(dataset, record_id, data, True)

    def patch(self, dataset, record_id, data):
        return self._put_patch(dataset, record_id, data, False)

    def delete(self, dataset, record_id):
        records = self.dataset_records(dataset)
        record_id = int(record_id)
        new_records = [record for record in records if record["id"] != record_id]
        records.clear()
        records.extend(new_records)
        self.write_json_data()
        return json.dumps({})
