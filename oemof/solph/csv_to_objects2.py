# -*- coding: utf-8 -*-

import sys
import pandas as pd
import oemof.network as on
from oemof.network import Bus
from oemof.solph import Flow, Storage, LinearTransformer, Sink, Source


bel = Bus(label='el_balance')
bcoal = Bus(label='coalbus')

# %% new core interface

so = Source(label='coalsource', outputs={bcoal: Flow()})

wind = Source(label='wind',
              outputs={bel: Flow(actual_value=[1, 1, 2], nominal_value=2,
                                 fixed_costs=25)})
si = Sink(label='sink', inputs={bel: Flow(max=[0.1, 0.2, 0.9],
                                          nominal_value=10,
                                          fixed=True, actual_value=[1, 2, 3])})

trsf = LinearTransformer(label='trsf', inputs={bcoal: Flow()},
                         outputs={bel: Flow(nominal_value=10,
                                            fixed_costs=5,
                                            variable_costs=10,
                                            summed_max=4,
                                            summed_min=2)},
                         conversion_factors={bel: 0.4})

stor = Storage(label='stor', inputs={bel: Flow()}, outputs={bel: Flow()},
               nominal_capacity=50, inflow_conversion_factor=0.9,
               outflow_conversion_factor=0.8, initial_capacity=0.5,
               capacity_loss=0.001)

# %% approach to create objects by iterating over dataframe

nodes_flows = pd.read_csv('nodes_flows.csv', sep=',')
nodes_flows_seq = pd.read_csv('nodes_flows_seq.csv', sep=',', header=None)
nodes_flows_seq.drop(0, axis=1, inplace=True)
nodes_flows_seq = nodes_flows_seq.transpose()


def str_to_class(str):
    return getattr(sys.modules[__name__], str)

for idx, row in nodes_flows.iterrows():
    # print(idx, row['label'])
    attributes_set = dict(zip(row.index, row.values))
#    print(str_to_class(attributes_set['class']))
    eval(attributes_set['class'])
    # first create an object of each class that only contains a label
