#!/usr/bin/env python

from collections import OrderedDict
import copy
import json
import math
import io
import yaml
import os
import progressbar
import warnings

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
warnings.filterwarnings("ignore", message="Polyfit may be poorly conditioned")

import pandas
from panoptes_aggregation import extractors
from panoptes_aggregation.csv_utils import flatten_data, order_columns
from panoptes_aggregation.extractors.utilities import annotation_by_task


def get_file_instance(file):
    if not isinstance(file, io.IOBase):
        file = open(file, 'r', encoding='utf-8')
    return file


def get_major_version(s):
    return s.split('.')[0]


def extract_csv(classification_csv, config, output='extractions', order=False):
    config = get_file_instance(config)
    with config as config_in:
        config_yaml = yaml.load(config_in)

    extractor_config = config_yaml['extractor_config']
    workflow_id = config_yaml['workflow_id']
    version = config_yaml['workflow_version']

    blank_extracted_data = OrderedDict([
        ('classification_id', []),
        ('user_name', []),
        ('user_id', []),
        ('workflow_id', []),
        ('task', []),
        ('created_at', []),
        ('subject_id', []),
        ('extractor', []),
        ('data', [])
    ])

    extracted_data = {}

    classification_csv = get_file_instance(classification_csv)
    with classification_csv as classification_csv_in:
        classifications = pandas.read_csv(classification_csv_in, encoding='utf-8', dtype={'workflow_version': str})

    wdx = classifications.workflow_id == workflow_id
    assert (wdx.sum() > 0), 'There are no classifications matching the configured workflow ID'
    if '.' in version:
        vdx = classifications.workflow_version == version
    else:
        vdx = classifications.workflow_version.apply(get_major_version) == version

    assert (vdx.sum() > 0), 'There are no classificaitons matching the configured version number'
    assert ((vdx & wdx).sum() > 0), 'There are no classifications matching the combined workflow ID and version number'

    widgets = [
        'Extracting: ',
        progressbar.Percentage(),
        ' ', progressbar.Bar(),
        ' ', progressbar.ETA()
    ]
    pbar = progressbar.ProgressBar(widgets=widgets, max_value=(wdx & vdx).sum())
    counter = 0
    pbar.start()
    for cdx, classification in classifications[wdx & vdx].iterrows():
        classification_by_task = annotation_by_task({'annotations': json.loads(classification.annotations)})
        for extractor_name, keywords in extractor_config.items():
            for keyword in keywords:
                if extractor_name in extractors.extractors:
                    try:
                        extract = extractors.extractors[extractor_name](copy.deepcopy(classification_by_task), **keyword)
                    except:
                        print()
                        print('Incorrectly formatted annotation')
                        print(classification)
                        continue
                    if isinstance(extract, list):
                        for e in extract:
                            extracted_data.setdefault(extractor_name, copy.deepcopy(blank_extracted_data))
                            extracted_data[extractor_name]['classification_id'].append(classification.classification_id)
                            extracted_data[extractor_name]['user_name'].append(classification.user_name)
                            extracted_data[extractor_name]['user_id'].append(classification.user_id)
                            extracted_data[extractor_name]['workflow_id'].append(classification.workflow_id)
                            extracted_data[extractor_name]['task'].append(keyword['task'])
                            extracted_data[extractor_name]['created_at'].append(classification.created_at)
                            extracted_data[extractor_name]['subject_id'].append(classification.subject_ids)
                            extracted_data[extractor_name]['extractor'].append(extractor_name)
                            extracted_data[extractor_name]['data'].append(e)
                    else:
                        extracted_data.setdefault(extractor_name, copy.deepcopy(blank_extracted_data))
                        extracted_data[extractor_name]['classification_id'].append(classification.classification_id)
                        extracted_data[extractor_name]['user_name'].append(classification.user_name)
                        extracted_data[extractor_name]['user_id'].append(classification.user_id)
                        extracted_data[extractor_name]['workflow_id'].append(classification.workflow_id)
                        extracted_data[extractor_name]['task'].append(keyword['task'])
                        extracted_data[extractor_name]['created_at'].append(classification.created_at)
                        extracted_data[extractor_name]['subject_id'].append(classification.subject_ids)
                        extracted_data[extractor_name]['extractor'].append(extractor_name)
                        extracted_data[extractor_name]['data'].append(extract)
        counter += 1
        pbar.update(counter)
    pbar.finish()

    # create one flat csv file for each extractor used
    output_path, output_base = os.path.split(output)
    output_base_name, output_ext = os.path.splitext(output_base)
    output_files = []
    for extractor_name, data in extracted_data.items():
        if len(data['data']) == 0:
            warnings.warn('No data extracted with {0}'.format(extractor_name))
        output_name = os.path.join(output_path, '{0}_{1}.csv'.format(extractor_name, output_base_name))
        output_files.append(output_name)
        flat_extract = flatten_data(data)
        if order:
            flat_extract = order_columns(flat_extract, front=['choice'])
        flat_extract.to_csv(output_name, index=False, encoding='utf-8')
    return output_files


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="extract data from panoptes classifications based on the workflow"
    )
    parser.add_argument(
        "classification_csv",
        help="the classification csv file containing the panoptes data dump",
        type=argparse.FileType('r', encoding='utf-8')
    )
    parser.add_argument(
        'extractor_config',
        help="the extractor configuration yaml file produced by `config_workflow_panoptes`",
        type=argparse.FileType('r', encoding='utf-8')
    )
    parser.add_argument(
        "-O",
        "--order",
        help="arrange the data columns in alphabetical order before saving",
        action="store_true"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="the base name for output csv file to store the annotation extractions (one file will be created for each extractor used)",
        type=str,
        default="extractions"
    )
    args = parser.parse_args()

    extract_csv(
        args.classification_csv,
        args.extractor_config,
        output=args.output,
        order=args.order
    )


if __name__ == "__main__":
    main()
