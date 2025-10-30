import os
import csv as csv
import unicodecsv
import StringIO as str_io

def dict2row(headers, rec):
    def false_to_blank(a):
        if a == False:
            return ''
        if a is None:
            return ''
        if a=='False':
            return ''
        return a
        #return '' if (a is False or str(a).upper == 'FALSE') else a
    return [false_to_blank(rec[p]) for p in headers]


def records2table(data, headers=None):
    if data and headers is None:
        headers = data[0].keys()
    return headers, [dict2row(headers, x) for x in data]


def load_data(env, records, model):
    """Transforms a list of dicts into a csv like table for odoo to import"""
    headers, data = records2table(records)
    return env[model].load(headers, data)


def load_csv(file_path, headers=None, delimiter=','):
    """Load a csv file from the local filesystem"""
    headers = headers or []
    data = None
    if os.path.isfile(file_path):
        if headers:
            fp = open(file_path, mode='r')
            data = [x for x in unicodecsv.DictReader(fp, fieldnames=headers, delimiter=delimiter)]
        else:
            try:
                fp = open(os.path.join(file_path), 'rb')
                data = [x for x in csv.DictReader(fp, delimiter=delimiter)]
            except Exception as e:
                fp = open(os.path.join(file_path), 'rb')
                data = [x for x in unicodecsv.DictReader(fp, delimiter=delimiter, encoding='utf-8-sig')]

        fp.close()
    return data


def save_csv(fn, data, headers=None):
    headers, out = records2table(data, headers=headers)
    fp = open(fn, 'wb')
    csv_writer = unicodecsv.writer(fp, encoding='utf-8', delimiter=',')
    csv_writer.writerows([headers] + out)
    fp.close()
def to_csv(data, headers=None):
    headers, out = records2table(data, headers=headers)
    #fp = open(fn, 'wb')
    fp = str_io.StringIO()
    csv_writer = unicodecsv.writer(fp, encoding='utf-8', delimiter=',')
    csv_writer.writerows([headers] + out)
    #fp.close()
    return fp.getvalue()

def save_csv_table(fn, data):
    #headers, out = records2table(data, headers=headers)
    fp = open(fn, 'wb')
    csv_writer = unicodecsv.writer(fp, encoding='utf-8', delimiter=',')
    csv_writer.writerows(data)
    fp.close()


def or_blank(a):
    return a or ''  # Absolutely no need for this function
