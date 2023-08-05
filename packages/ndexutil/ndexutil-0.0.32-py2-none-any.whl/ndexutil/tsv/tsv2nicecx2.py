
import ndex2 # The ndex2 Python client
import ndex2.client as nc
import csv
import sys
import os
sys.path.insert(0, os.path.abspath('../../../ndex2_performance/ndex2-client'))

import json
from os import path
from jsonschema import validate
import pandas as pd
#import ndex2
from ndex2cx.NiceCXBuilder import NiceCXBuilder
import time
import re
import numpy as np
import types
import six
import gspread

version="0.1"

node_id_lookup = {}

#=====================
# NON-CLASS FUNCTIONS
#=====================
def convert_pandas_to_nice_cx_with_load_plan(pandas_dataframe, load_plan, max_rows=None,
                                            name=None, description=None,
                                            network_attributes=None, provenance=None):

    # open the schema first
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'loading_plan_schema.json')) as json_file:
        plan_schema = json.load(json_file)

    validate(load_plan, plan_schema)

    node_lookup = {}
    nice_cx_builder = NiceCXBuilder()
    row_count = 0
    t1 = int(time.time()*1000)
    #Add context if they are defined
    if load_plan.get('context'):
        nice_cx_builder.set_context(load_plan.get('context'))
        #self.ng_builder.addNamespaces(self.plan.context)

    total_row_count = pandas_dataframe.shape
    if len(total_row_count) > 1:
        total_row_count = str(total_row_count[0])
    for index, row in pandas_dataframe.iterrows():
        # As each row is processed, self.G_nx is updated
        process_row(nice_cx_builder, load_plan, row, node_lookup)
        row_count = row_count + 1
        if max_rows and row_count > max_rows + 2:
            break

        if row_count % 2500 == 0:
            print('processing %s out of %s edges' % (str(row_count), total_row_count))

    if network_attributes:
        for attribute in network_attributes:
            if attribute.get("n") == "name":
                nice_cx_builder.set_name(attribute.get("v"))
            else:
                nice_cx_builder.add_network_attribute(name=attribute.get('n'), values=attribute.get('v'),
                                                      type=attribute.get('d'))

    tsv_data_event = {
            "inputs": None,
            "startedAtTime": t1,
            "endedAtTime": int(time.time()*1000),
            "eventType": "TSV network generation",
            "properties": [{
                            "name": "TSV loader version",
                            "value": version
                        }]
        }

    # name and description take precedence over any prior values
    if name:
        nice_cx_builder.set_name(name)
    if description:
        nice_cx_builder.set_network_attribute(name='description', values=description)

    return nice_cx_builder.get_nice_cx()

#==================================
# Process Row USING NiceCX
# Added by Aaron G
#==================================
def process_row(nice_cx_builder, load_plan, row, node_lookup):
    # For each row, we create an edge + edge properties
    # For that edge, we may create elements if they are new
    # - source node + properties
    # - target node + properties
    # - predicate term
    skipped_edge = False

    source_node = create_node(row, load_plan.get('source_plan'), nice_cx_builder, node_lookup)
    target_node = create_node(row, load_plan.get('target_plan'), nice_cx_builder, node_lookup)

    if source_node is not None and target_node is not None:
        create_edge(nice_cx_builder, source_node, target_node, row, load_plan)

def create_node(row, node_plan, nice_cx_builder, node_lookup):
    use_name_as_id = False
    node_name_column = node_plan['node_name_column']
    node_name_type = None
    if '::' in node_name_column:
        node_name_split = node_name_column.split('::')
        node_plan['node_name_column'] = node_name_split[0]
        node_name_type = node_name_split[1]

    #=======================================
    # IF NO REP_COLUMN USE NODE NAME COLUMN
    #=======================================
    if not node_plan.get('rep_column'):
        node_plan['rep_column'] = node_plan['node_name_column']
        use_name_as_id = True

    if use_name_as_id and node_plan.get('rep_prefix'):
        raise RuntimeError("Id column needs to be defined if id_prefix is defined in your query plan.")

    node_name = row[node_plan['node_name_column']]
    ext_id = row[node_plan['rep_column']]

    if ext_id and node_plan.get('rep_prefix'):
        ext_id = node_plan['rep_prefix'] + ":" + str(ext_id)

    #========================================
    # NAME  |  EXT ID  | ACTION
    #----------------------------------------
    # VALID |  VALID   | NORMAL
    # VALID |  None    | SUB NAME FOR EXT ID
    # None  |  VALID   | SUB EXT ID FOR NAME
    # None  |  None    | SKIP ROW
    #========================================
    if node_name and not ext_id:
        ext_id = node_name
    elif not node_name and ext_id:
        node_name = ext_id
    elif not node_name and not ext_id:
        print('No node name or ext id.  Skipping this node (%s)' % node_plan['node_name_column'])
        return None

    node_id = nice_cx_builder.add_node(name=node_name, represents=ext_id, data_type=node_name_type)

    add_node_attributes(nice_cx_builder, node_id, node_plan, row)

    return node_id


def create_edge(nice_cx_builder, src_node_id, tgt_node_id, row, import_plan):
    predicate_str = None
    edge_plan = import_plan.get('edge_plan')
    if edge_plan.get('predicate_id_column'):
        predicate_str = row[edge_plan['predicate_id_column']]

    if not predicate_str and edge_plan.get('default_predicate'):
        predicate_str = edge_plan['default_predicate']

    if not predicate_str:
        raise RuntimeError("Value for predicate string is not found in this row.")

    if edge_plan.get("predicate_prefix"):
        predicate_str = edge_plan['predicate_prefix'] + ":" + predicate_str

    edge_id = nice_cx_builder.add_edge(source=src_node_id, target=tgt_node_id, interaction=predicate_str)

    add_edge_attributes(nice_cx_builder, edge_id, edge_plan, row)

    # Deal with citiations
    citation_id = None
    if edge_plan.get("citation_id_column"):
        citation_id = str(row[edge_plan['citation_id_column']])

    if citation_id is not None:
        citation_id = citation_id.replace(';', ',')
        citation_id = citation_id.replace('|', ',')
        if edge_plan.get("citation_id_prefix"):
            citation_id_temp = re.split('\s*,\s*', citation_id)
            citation_id = []
            for c in citation_id_temp:
                citation_id.append(edge_plan.get("citation_id_prefix") + ':' + c)
            #citation_id = edge_plan.get("citation_id_prefix") + ':' + citation_id
        else:
            citation_id = re.split('\s*,\s*', citation_id)

        nice_cx_builder.add_edge_attribute(property_of=edge_id, name='citation', values=citation_id, type='list_of_string')

    #if citation_id and edge_plan.get("citation_id_prefix"):
    #    newList = []
    #    for cid in citation_id:
    #        newList.append(edge_plan["citation_id_prefix"] + ":" + cid)
    #    citation_id = newList

    #if citation_id:
    #    nice_cx.set_edge_attribute(edge_id, 'citation', citation_id, type='list_of_string')
    #    #nice_cx.set_edge_attribute(edge_id, 'citation_ids', citation_id, type='list_of_string')


valid_cx_data_types = ['boolean', 'byte', 'char', 'double', 'float', 'integer', 'long', 'short', 'string', 'list_of_boolean',
 'list_of_byte', 'list_of_char', 'list_of_double', 'list_of_float', 'list_of_integer', 'list_of_long',
 'list_of_short','list_of_string']

def add_node_attributes(nice_cx_builder, node_element, load_plan, row):
    if load_plan.get('property_columns'):
        for column_raw_temp in load_plan['property_columns']:
            if isinstance(column_raw_temp, dict):
                column_raw = column_raw_temp
            else:
                if '::' in column_raw_temp:
                    column_split = column_raw_temp.split('::')
                    if len(column_split) > 1:
                        column_raw = {
                            'column_name': column_split[0],
                            'attribute_name': column_split[0],
                            'data_type': column_split[1]
                        }
                    else:
                        column_raw = {
                            'column_name': column_raw_temp,
                            'attribute_name': column_raw_temp
                        }
                else:
                    column_raw = {
                        'column_name': column_raw_temp,
                        'attribute_name': column_raw_temp
                    }

            type_temp = column_raw.get('data_type')
            value = None

            if column_raw.get('column_name'):
                value = row.get(column_raw['column_name'])

            if (value is None) and column_raw.get('default_value'):
                value = column_raw['default_value']

            if value:
                if column_raw.get('delimiter'):
                    if column_raw.get('data_type'):
                        if column_raw['data_type'] not in valid_cx_data_types:
                            raise Exception('data_type: ' + column_raw['data_type'] + ' is not valid')
                        value = value.split(column_raw.get('delimiter'))

                        value = data_to_type(value, column_raw['data_type'])
                        if not type_temp.startswith('list'):
                            type_temp = 'list_of_' + type_temp
                    else:
                        if not isinstance(value, str):
                            value = str(value)
                        value = value.split(column_raw.get('delimiter'))
                        type_temp = 'list_of_string'

                    if column_raw.get('value_prefix'):
                        value_list_temp = []
                        for value_item in value:
                            value_temp = column_raw.get('value_prefix') + ":" + str(value_item)
                            value_list_temp.append(value_temp)
                        value = value_list_temp
                else:
                    if column_raw.get('data_type'):
                        if column_raw['data_type'] not in valid_cx_data_types:
                            raise Exception('data_type: ' + column_raw['data_type'] + ' is not valid')

                        value = data_to_type(value, column_raw['data_type'])
                        if value is None:
                            return ''

                    if column_raw.get('value_prefix'):
                        value = column_raw.get('value_prefix') + ":" + str(value)

                if column_raw.get('attribute_name'):
                    nice_cx_builder.add_node_attribute(node_element, column_raw['attribute_name'], value, type=type_temp)
                else:
                    nice_cx_builder.add_node_attribute(node_element, column_raw['column_name'], value, type=type_temp)

def add_edge_attributes(nice_cx_builder, edge_id, load_plan, row):
    if load_plan.get('property_columns'):
        for column_raw_temp in load_plan['property_columns']:
            if isinstance(column_raw_temp, dict):
                column_raw = column_raw_temp
            else:
                if '::' in column_raw_temp:
                    column_split = column_raw_temp.split('::')
                    if len(column_split) > 1:
                        column_raw = {
                            'column_name': column_split[0],
                            'attribute_name': column_split[0],
                            'data_type': column_split[1]
                        }
                    else:
                        column_raw = {
                            'column_name': column_raw_temp,
                            'attribute_name': column_raw_temp
                        }
                else:
                    column_raw = {
                        'column_name': column_raw_temp,
                        'attribute_name': column_raw_temp
                    }

            type_temp = column_raw.get('data_type')

            value = None

            if column_raw.get('column_name'):
                value = row.get(column_raw['column_name'])

            if pd.isnull(value) or value == 'None':
                if column_raw.get('default_value'):
                    value = column_raw['default_value']
                else:
                    continue

            if value is not None and len(value) > 0:
                dt = None

                if column_raw.get('delimiter'):
                    if column_raw.get('data_type'):
                        dt = str(column_raw.get('data_type'))
                        if dt not in valid_cx_data_types:
                            raise Exception('data_type: ' + dt + ' is not valid')

                        value = value.split(column_raw.get('delimiter'))
                        value = data_to_type(value, dt)
                        if not type_temp.startswith('list'):
                            type_temp = 'list_of_' + type_temp
                    else:
                        value = value.split(column_raw.get('delimiter'))
                        type_temp = 'list_of_string'

                    if column_raw.get('value_prefix'):
                        value_list_temp = []
                        for value_item in value:
                            value_temp = column_raw.get('value_prefix') + ":" + str(value_item)
                            value_list_temp.append(value_temp)
                        value = value_list_temp
                else:
                    if column_raw.get('data_type'):
                        dt = str(column_raw.get('data_type'))
                        if dt not in valid_cx_data_types:
                            raise Exception('data_type: ' + dt + ' is not valid')

                        value = data_to_type(value, dt)

                    if column_raw.get('value_prefix'):
                        value = column_raw.get('value_prefix') + ":" + str(value)

                if column_raw.get('attribute_name'):
                    nice_cx_builder.add_edge_attribute(property_of=edge_id, name=column_raw['attribute_name'],
                                                       values=value, type=type_temp)
                else:
                    nice_cx_builder.add_edge_attribute(property_of=edge_id, name=column_raw['column_name'],
                                                       values=value, type=type_temp)


def data_to_type(data, data_type):
    return_data = None
    try:
        if(type(data) is str):
            data = data.replace('[', '').replace(']','')
            if('list_of' in data_type):
                data = data.split(',')

        if data_type == "boolean":
            if(type(data) is str):
                return_data = data.lower() == 'true'
            else:
                return_data = bool(data)
        elif data_type == "byte":
            return_data = str(data).encode()
        elif data_type == "char":
            return_data = str(data)
        elif data_type == "double":
            return_data = float(data)
        elif data_type == "float":
            return_data = float(data)
        elif data_type == "integer":
            return_data = int(data)
        elif data_type == "long":
            return_data = int(data)
        elif data_type == "short":
            return_data = int(data)
        elif data_type == "string":
            return_data = str(data)
        elif data_type == "list_of_boolean":
            # Assumption: if the first element is a string then so are the rest...
            if(type(data[0]) is str):
                return_data = [s.lower() == 'true' for s in data]
            else:
                return_data = [bool(s) for s in data]
        elif data_type == "list_of_byte":
            return_data = [bytes(s) for s in data]
        elif data_type == "list_of_char":
            return_data = [str(s) for s in data]
        elif data_type == "list_of_double":
            return_data = [float(s) for s in data]
        elif data_type == "list_of_float":
            return_data = [float(s) for s in data]
        elif data_type == "list_of_integer":
            return_data = [int(s) for s in data]
        elif data_type == "list_of_long":
            return_data = [int(s) for s in data]
        elif data_type == "list_of_short":
            return_data = [int(s) for s in data]
        elif data_type == "list_of_string":
            return_data = [str(s) for s in data]
        else:
            return_data = str(data)
    except Exception as err2:
        return_data = None

    return return_data

'''
def create_edge(src_node_id, tgt_node_id, row, plan, nice_cx):

    predicate_str = None
    if  plan.edge_plan.get('predicate_id_column'):
        predicate_str = row.get(plan.edge_plan['predicate_id_column'])

    if not predicate_str and plan.edge_plan.get('default_predicate'):
        predicate_str = plan.edge_plan['default_predicate']

    if not predicate_str :
        raise RuntimeError("Value for predicate string is not found this row.")

    if plan.edge_plan.get("predicate_prefix"):
        predicate_str = plan.edge_plan['predicate_prefix']+ ":"+ predicate_str

    edge_attr = create_attr_obj(plan.edge_plan, row)

    #Deal with citiations
    citation_id = None
    if  self.plan.edge_plan.get("citation_id_column"):
        citation_id = row.get(self.plan.edge_plan['citation_id_column'])

    if citation_id is not None:
        citation_id = citation_id.replace(';', ',')
        citation_id = citation_id.replace('|', ',')
        citation_id = re.split('\s*,\s*',citation_id)

    if citation_id and plan.edge_plan.get("citation_id_prefix"):
            newList = []
            for cid in citation_id:
                newList.append(plan.edge_plan["citation_id_prefix"] + ":" + cid)
            citation_id = newList

    if citation_id :
        edge_attr['citation_ids'] = citation_id

    ng_builder.addEdge(src_node_id,tgt_node_id,predicate_str, edge_attr)
'''

def find_or_create_node(nice_cx, name, represents, node_lookup):
    if node_lookup.get(represents):
        return nice_cx.nodes.get(node_lookup.get(represents))
    else:
        #new_node_id = nice_cx.create_node(node_name=name, node_represents=represents)
        new_node_id = nice_cx.create_node(node_name=name, node_represents=represents)

        node_lookup[represents] = new_node_id
        return nice_cx.nodes.get(new_node_id)

if __name__ == '__main__':
    print('made it')

