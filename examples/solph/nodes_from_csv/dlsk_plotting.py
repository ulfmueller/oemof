# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm


# global plotting options
plt.rcParams.update(plt.rcParamsDefault)
matplotlib.style.use('ggplot')
plt.rcParams['lines.linewidth'] = 2.5
plt.rcParams['axes.facecolor'] = 'silver'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams.update({'font.size': 14})
plt.rcParams['image.cmap'] = 'RdYlBu'

# read file
file = ('results/'
        'scenario_nep_2035_ee_plus_25_2016-08-09 16:27:06.904477_DE.csv')

df_raw = pd.read_csv(file, parse_dates=[0], index_col=0, keep_date_col=True)
df_raw.head()
df_raw.columns


# %% plot fundamental and regression prices (1 year)

file_name = 'scenario_nep_2014_2016-08-04 12:04:42.180425_DE.csv'

df = pd.read_csv('results/' + file_name, parse_dates=[0],
                 index_col=0, keep_date_col=True)
df = df[['duals']]

price_real = pd.read_csv('price_eex_day_ahead_2014.csv')
price_real.index = df.index

df = pd.concat([price_real, df], axis=1)
df.columns = ['Real', 'Modell']

# line plot
df.plot(drawstyle='steps', cmap=cm.get_cmap('RdYlBu'))
plt.xlabel('Zeit in h')
plt.ylabel('Preis in EUR/MWh')
plt.tight_layout()
plt.show()


# scatter plot
df.plot(kind='scatter', x='Modell', y='Real')

# fit polynom of 3rd degree to price_real(res_load)
z = np.polyfit(df['Modell'], df['Real'], 3)
p = np.poly1d(z)
df['price_polynom'] = p(df['Modell'])
plt.plot(df['Modell'],
         (
          z[0] * df['Modell'] ** 3 +
          z[1] * df['Modell'] ** 2 +
          z[2] * df['Modell'] ** 1 +
          z[3]
          ), color='red')


plt.xlabel('Modellpreis')
plt.ylabel('Realpreis')
plt.tight_layout()
plt.show()

# duration curves for all scenarios
df_prices_duration = pd.concat(
    [df[col].sort_values(ascending=False).reset_index(drop=True)
     for col in df], axis=1)
df_prices_duration[['Real',
                   'Modell']].plot(legend='reverse',
                                   cmap=cm.get_cmap('RdYlBu'))
plt.xlabel('Stunden des Jahres')
plt.ylabel('Preis in EUR/MWh')
plt.tight_layout()
plt.show()

# %% plot fundamental and regression prices (8 weeks)

file_name = 'scenario_nep_2014_2016-08-04 12:04:42.180425_DE.csv'

df = pd.read_csv('results/' + file_name, parse_dates=[0],
                 index_col=0, keep_date_col=True)
df = df[['duals']]

price_real = pd.read_csv('price_eex_day_ahead_2014.csv')
price_real.index = df.index

df = pd.concat([price_real, df], axis=1)
df.columns = ['Real', 'Modell']

df[(24 * 7)*8:(24 * 7)*16].plot(drawstyle='steps', cmap=cm.get_cmap('RdYlBu'))
plt.xlabel('')
plt.ylabel('Preis in EUR/MWh')
plt.tight_layout()
plt.show()


# %% plot fundamental and regression prices (1 week)

file_name = 'scenario_nep_2014_2016-08-04 12:04:42.180425_DE.csv'

df = pd.read_csv('results/' + file_name, parse_dates=[0],
                 index_col=0, keep_date_col=True)
df = df[['duals']]

price_real = pd.read_csv('price_eex_day_ahead_2014.csv')
price_real.index = df.index

df = pd.concat([price_real, df], axis=1)
df.columns = ['Real', 'Modell']

df[(24 * 7)*21:(24 * 7)*22].plot(drawstyle='steps', cmap=cm.get_cmap('RdYlBu'))
plt.xlabel('')
plt.ylabel('Preis in EUR/MWh')
plt.tight_layout()
plt.show()

## %% polynom fitting: residual load
#
## prepare dataframe for fit
#residual_load = df_raw['DE_load'] + df_raw['AT_load'] + df_raw['LU_load'] - \
#                df_raw['DE_wind'] - df_raw['AT_wind'] - df_raw['LU_wind'] - \
#                df_raw['DE_solar'] - df_raw['AT_solar'] - df_raw['LU_solar']
#
## real prices
#price_real = pd.read_csv('price_eex_day_ahead_2014.csv')
#price_real.index = df_raw.index
#
#df = pd.concat([residual_load, price_real, df_raw['duals']], axis=1)
#df.columns = ['res_load', 'price_real', 'price_model']
#
## fit polynom of 3rd degree to price_real(res_load)
#z = np.polyfit(df['res_load'], df['price_real'], 3)
#p = np.poly1d(z)
#df['price_polynom_res_load'] = p(df['res_load'])
#
#df.plot.scatter(x='res_load', y='price_real')
#plt.plot(df['res_load'],
#         (
#          z[0] * df['res_load'] ** 3 +
#          z[1] * df['res_load'] ** 2 +
#          z[2] * df['res_load'] ** 1 +
#          z[3]
#          ), color='red')
#plt.xlabel('Residuallast in MW')
#plt.ylabel('Day-Ahead Preis in EUR/MWh')
#
#plt.show()


# %% dispatch plot: 2014
# (DE/LU/AT are one bidding area -> balance must not fit)

file_name = 'scenario_nep_2014_2016-08-04 12:04:42.180425_DE.csv'

df = pd.read_csv('results/' + file_name, parse_dates=[0],
                 index_col=0, keep_date_col=True)

df_dispatch = pd.DataFrame()

# country code
cc = ['DE', 'LU', 'AT']

# get fossil and renewable power plants
fuels = ['run_of_river', 'biomass', 'solar', 'wind', 'uranium', 'lignite',
         'hard_coal', 'gas', 'mixed_fuels', 'oil', 'load', 'excess',
         'shortage']
for f in fuels:
    cols = [c for c in df.columns
            if f in c and any(substring in c
                              for substring in cc)]
    df_dispatch[f] = df[cols].sum(axis=1)

# get imports and exports and aggregate columns
cols = [c for c in df.columns
        if 'powerline' in c and any(substring in c
                                    for substring in cc)]
powerlines = df[cols]
exports = powerlines[[c for c in powerlines.columns
                      if c.startswith('DE_')]]
imports = powerlines[[c for c in powerlines.columns
                      if ('_' + 'DE' + '_' in c)]]
df_dispatch['imports'] = imports.sum(axis=1)
df_dispatch['exports'] = exports.sum(axis=1)

# get phs in- and outputs
phs_in = df[[c for c in df.columns if 'phs_in' in c and
            any(substring in c for substring in cc)]]
phs_out = df[[c for c in df.columns if 'phs_out' in c and
             any(substring in c for substring in cc)]]
phs_level = df[[c for c in df.columns if 'phs_level' in c and
                any(substring in c for substring in cc)]]
df_dispatch['phs_in'] = phs_in.sum(axis=1)
df_dispatch['phs_out'] = phs_out.sum(axis=1)
df_dispatch['phs_level'] = phs_level.sum(axis=1)

# MW to GW
df_dispatch = df_dispatch.divide(1000)

# rename columns

en_de = {'run_of_river': 'Laufwasser',
         'biomass': 'Biomasse',
         'solar': 'Solar',
         'wind': 'Wind',
         'uranium': 'Kernenergie',
         'lignite': 'Braunkohle',
         'hard_coal': 'Steinkohle',
         'gas': 'Gas',
         'mixed_fuels': 'Sonstiges',
         'oil': 'Öl',
         'phs_in': 'Pumpspeicher (Laden)',
         'phs_out': 'Pumpspeicher (Entladen)',
         'imports': 'Import',
         'exports': 'Export',
         'load': 'Last',
         'shortage': 'Ungedeckte Nachfrage',
         'excess': 'Überschüssige Energie'}
df_dispatch = df_dispatch.rename(columns=en_de)

# area plot. gute woche: '2014-01-21':'2014-01-27'
cols = ['Biomasse', 'Laufwasser', 'Kernenergie', 'Braunkohle',
        'Steinkohle', 'Gas', 'Öl', 'Sonstiges', 'Solar', 'Wind',
        'Pumpspeicher (Entladen)', 'Import']
df_dispatch['2014-01-21':'2014-01-27'][cols] \
             .plot(kind='area', stacked=True,
                   cmap=cm.get_cmap('RdYlBu'), legend='reverse')
plt.xlabel('Datum')
plt.ylabel('Leistung in  GW')
plt.ylim(0, max(df_dispatch.sum(axis=1)) * 0.65)
plt.tight_layout()
plt.show()

# bar plot of annual production
cols = ['Biomasse', 'Laufwasser', 'Kernenergie', 'Braunkohle',
        'Steinkohle', 'Gas', 'Öl', 'Sonstiges', 'Solar', 'Wind']
annual_production = df_dispatch[cols].divide(1000).sum(axis=0).to_frame()
annual_production = annual_production.transpose()

# real production 2014
#http://www.bmwi.de/DE/Themen/Energie/Strommarkt-der-Zukunft/zahlen-fakten.html
DE2014 = pd.DataFrame([[36.8, 24.098, 91.799, 148.769, 114.824, 37.227, 1.434,
                        0.111, 34.961, 55.484]],
                      columns=annual_production.columns)

AT2014 = pd.DataFrame([[2.504, 40.902, 0, 0, 2.953, 5.161, 0.597, 4.52,
                        0.351, 3.640]],
                      columns=annual_production.columns)
LU2014 = pd.DataFrame([[0.05, 0.091, 0, 0, 0, 1.42, 0,
                        0, 0.79, 0.61]],
                      columns=annual_production.columns)

annual_production = annual_production.append([DE2014, AT2014, LU2014],
                                             ignore_index=True)
annual_production.index = ['DE/AT/LU (Modell)', 'DE (Real)', 'AT (Real)',
                           'LU (Real)']

annual_production = annual_production[
    ['Kernenergie', 'Braunkohle', 'Steinkohle', 'Gas', 'Öl', 'Sonstiges',
     'Solar', 'Wind', 'Biomasse', 'Laufwasser']]

annual_production.plot(kind='bar', legend=True, cmap=cm.get_cmap('RdYlBu'),
                       rot=0)
plt.xlabel('')
plt.ylabel('Energieproduktion in  TWh')
plt.tight_layout()
plt.show()

# duration curves for power plants
curves = pd.concat(
    [df_dispatch[col].sort_values(ascending=False).reset_index(drop=True)
     for col in df_dispatch], axis=1)
curves[['Kernenergie', 'Braunkohle', 'Steinkohle', 'Gas', 'Öl',
        'Sonstiges', 'Solar', 'Wind', 'Pumpspeicher (Entladen)',
        'Import', 'Export']].plot(cmap=cm.get_cmap('RdYlBu'))
plt.xlabel('Stunden des Jahres')
plt.ylabel('Leistung in GW')
plt.xlim(0, 10000)
plt.tight_layout()
plt.show()

# duration curves for all powerlines
pls = pd.concat(
    [powerlines[col].sort_values(ascending=False).reset_index(drop=True)
     for col in powerlines], axis=1)
pls.columns = [c.replace('_powerline', '') for c in pls.columns]
pls = pls[[
    'DE_AT', 'DE_CH', 'DE_CZ',
    'DE_DK', 'DE_FR', 'DE_LU',
    'DE_NL', 'DE_PL', 'DE_SE',
    'AT_DE', 'CH_DE', 'CZ_DE',
    'DK_DE', 'FR_DE', 'NL_DE',
    'PL_DE', 'SE_DE']]

pls.plot(cmap=cm.get_cmap('RdYlBu'))
plt.xlabel('Stunden des Jahres')
plt.ylabel('Leistung in GW')
plt.xlim(0, 10000)
plt.tight_layout()
plt.show()

# bar plot of powerlines (imports/exports)
pls_sum = pls.sum(axis=0).divide(10e6).to_frame().transpose()

exp = pls_sum[[c for c in pls.columns if c.startswith('DE_')]]
imp = pls_sum[[c for c in pls.columns if not c.startswith('DE_')]]
pls_sum_div = pd.concat([imp, exp], axis=0)
pls_sum_div.index = ['Import', 'Export']
pls_sum_div = pls_sum_div[[
    'DE_AT', 'DE_CH', 'DE_CZ',
    'DE_DK', 'DE_FR', 'DE_LU',
    'DE_NL', 'DE_PL', 'DE_SE',
    'AT_DE', 'CH_DE', 'CZ_DE',
    'DK_DE', 'FR_DE', 'NL_DE',
    'PL_DE', 'SE_DE']]

pls_sum_div.plot(kind='bar', stacked=True, cmap=cm.get_cmap('RdYlBu'), rot=0,
                 legend='reverse')
plt.xlabel('')
plt.ylabel('Energie in TWh')
plt.tight_layout()
plt.show()

# %% dispatch plot: 2025/2035
# (DE/LU/AT are one bidding area -> balance must not fit)

# ################## 2025 #####################################################

file_name = 'scenario_nep_2025_2016-08-16 14:52:22.118405_DE.csv'

df = pd.read_csv('results/' + file_name, parse_dates=[0],
                 index_col=0, keep_date_col=True)

df_dispatch = pd.DataFrame()

# country code
cc = ['DE', 'LU', 'AT']

# get fossil and renewable power plants
fuels = ['run_of_river', 'biomass', 'solar', 'wind', 'uranium', 'lignite',
         'hard_coal', 'gas', 'mixed_fuels', 'oil', 'load', 'excess',
         'shortage']
for f in fuels:
    cols = [c for c in df.columns
            if f in c and any(substring in c
                              for substring in cc)]
    df_dispatch[f] = df[cols].sum(axis=1)

# get imports and exports and aggregate columns
cols = [c for c in df.columns
        if 'powerline' in c and any(substring in c
                                    for substring in cc)]
powerlines = df[cols]
exports = powerlines[[c for c in powerlines.columns
                      if c.startswith('DE_')]]
imports = powerlines[[c for c in powerlines.columns
                      if ('_' + 'DE' + '_' in c)]]
df_dispatch['imports'] = imports.sum(axis=1)
df_dispatch['exports'] = exports.sum(axis=1)

# get phs in- and outputs
phs_in = df[[c for c in df.columns if 'phs_in' in c and
            any(substring in c for substring in cc)]]
phs_out = df[[c for c in df.columns if 'phs_out' in c and
             any(substring in c for substring in cc)]]
phs_level = df[[c for c in df.columns if 'phs_level' in c and
                any(substring in c for substring in cc)]]
df_dispatch['phs_in'] = phs_in.sum(axis=1)
df_dispatch['phs_out'] = phs_out.sum(axis=1)
df_dispatch['phs_level'] = phs_level.sum(axis=1)

# MW to GW
df_dispatch = df_dispatch.divide(1000)

# rename columns
en_de = {'run_of_river': 'Laufwasser',
         'biomass': 'Biomasse',
         'solar': 'Solar',
         'wind': 'Wind',
         'uranium': 'Kernenergie',
         'lignite': 'Braunkohle',
         'hard_coal': 'Steinkohle',
         'gas': 'Gas',
         'mixed_fuels': 'Sonstiges',
         'oil': 'Öl',
         'phs_in': 'Pumpspeicher (Laden)',
         'phs_out': 'Pumpspeicher (Entladen)',
         'imports': 'Import',
         'exports': 'Export',
         'load': 'Last',
         'shortage': 'Ungedeckte Nachfrage',
         'excess': 'Überschüssige Energie'}
df_dispatch = df_dispatch.rename(columns=en_de)


# bar plot of annual production
cols = ['Biomasse', 'Laufwasser', 'Kernenergie', 'Braunkohle',
        'Steinkohle', 'Gas', 'Öl', 'Sonstiges', 'Solar', 'Wind']
annual_production_2025 = df_dispatch[cols].divide(1000).sum(axis=0).to_frame()
annual_production_2025 = annual_production_2025.transpose()


# ################### 2035 ####################################################

file_name = 'scenario_nep_2035_2016-08-05 15:18:42.431986_DE.csv'

df = pd.read_csv('results/' + file_name, parse_dates=[0],
                 index_col=0, keep_date_col=True)

df_dispatch = pd.DataFrame()

# country code
cc = ['DE', 'LU', 'AT']

# get fossil and renewable power plants
fuels = ['run_of_river', 'biomass', 'solar', 'wind', 'uranium', 'lignite',
         'hard_coal', 'gas', 'mixed_fuels', 'oil', 'load', 'excess',
         'shortage']
for f in fuels:
    cols = [c for c in df.columns
            if f in c and any(substring in c
                              for substring in cc)]
    df_dispatch[f] = df[cols].sum(axis=1)

# get imports and exports and aggregate columns
cols = [c for c in df.columns
        if 'powerline' in c and any(substring in c
                                    for substring in cc)]
powerlines = df[cols]
exports = powerlines[[c for c in powerlines.columns
                      if c.startswith('DE_')]]
imports = powerlines[[c for c in powerlines.columns
                      if ('_' + 'DE' + '_' in c)]]
df_dispatch['imports'] = imports.sum(axis=1)
df_dispatch['exports'] = exports.sum(axis=1)

# get phs in- and outputs
phs_in = df[[c for c in df.columns if 'phs_in' in c and
            any(substring in c for substring in cc)]]
phs_out = df[[c for c in df.columns if 'phs_out' in c and
             any(substring in c for substring in cc)]]
phs_level = df[[c for c in df.columns if 'phs_level' in c and
                any(substring in c for substring in cc)]]
df_dispatch['phs_in'] = phs_in.sum(axis=1)
df_dispatch['phs_out'] = phs_out.sum(axis=1)
df_dispatch['phs_level'] = phs_level.sum(axis=1)

# MW to GW
df_dispatch = df_dispatch.divide(1000)

# rename columns
en_de = {'run_of_river': 'Laufwasser',
         'biomass': 'Biomasse',
         'solar': 'Solar',
         'wind': 'Wind',
         'uranium': 'Kernenergie',
         'lignite': 'Braunkohle',
         'hard_coal': 'Steinkohle',
         'gas': 'Gas',
         'mixed_fuels': 'Sonstiges',
         'oil': 'Öl',
         'phs_in': 'Pumpspeicher (Laden)',
         'phs_out': 'Pumpspeicher (Entladen)',
         'imports': 'Import',
         'exports': 'Export',
         'load': 'Last',
         'shortage': 'Ungedeckte Nachfrage',
         'excess': 'Überschüssige Energie'}
df_dispatch = df_dispatch.rename(columns=en_de)


# bar plot of annual production
cols = ['Biomasse', 'Laufwasser', 'Kernenergie', 'Braunkohle',
        'Steinkohle', 'Gas', 'Öl', 'Sonstiges', 'Solar', 'Wind']
annual_production_2035 = df_dispatch[cols].divide(1000).sum(axis=0).to_frame()
annual_production_2035 = annual_production_2035.transpose()

# ######################## Plot ###############################################

annual_production_2025 = \
    annual_production_2025.append(annual_production_2035, ignore_index=True)


annual_production_2025.index = ['NEP-2025', 'NEP-2035']

annual_production_2025 = annual_production_2025[
    ['Kernenergie', 'Braunkohle', 'Steinkohle', 'Gas', 'Öl', 'Sonstiges',
     'Solar', 'Wind', 'Biomasse', 'Laufwasser']]

annual_production_2025.plot(kind='bar', legend=True,
                            cmap=cm.get_cmap('RdYlBu'),
                            rot=0)
plt.xlabel('')
plt.ylabel('Energieproduktion in  TWh')
plt.tight_layout()
plt.show()

# %% import/export plot 2025
file_name = 'scenario_nep_2025_2016-08-16 14:52:22.118405_DE.csv'

df = pd.read_csv('results/' + file_name, parse_dates=[0],
                 index_col=0, keep_date_col=True)

df_dispatch = pd.DataFrame()

# country code
cc = ['DE', 'LU', 'AT']

# get fossil and renewable power plants
fuels = ['run_of_river', 'biomass', 'solar', 'wind', 'uranium', 'lignite',
         'hard_coal', 'gas', 'mixed_fuels', 'oil', 'load', 'excess',
         'shortage']
for f in fuels:
    cols = [c for c in df.columns
            if f in c and any(substring in c
                              for substring in cc)]
    df_dispatch[f] = df[cols].sum(axis=1)

# get imports and exports and aggregate columns
cols = [c for c in df.columns
        if 'powerline' in c and any(substring in c
                                    for substring in cc)]
powerlines = df[cols]
exports = powerlines[[c for c in powerlines.columns
                      if c.startswith('DE_')]]
imports = powerlines[[c for c in powerlines.columns
                      if ('_' + 'DE' + '_' in c)]]
df_dispatch['imports'] = imports.sum(axis=1)
df_dispatch['exports'] = exports.sum(axis=1)

# get phs in- and outputs
phs_in = df[[c for c in df.columns if 'phs_in' in c and
            any(substring in c for substring in cc)]]
phs_out = df[[c for c in df.columns if 'phs_out' in c and
             any(substring in c for substring in cc)]]
phs_level = df[[c for c in df.columns if 'phs_level' in c and
                any(substring in c for substring in cc)]]
df_dispatch['phs_in'] = phs_in.sum(axis=1)
df_dispatch['phs_out'] = phs_out.sum(axis=1)
df_dispatch['phs_level'] = phs_level.sum(axis=1)

# MW to GW
df_dispatch = df_dispatch.divide(1000)

# rename columns

en_de = {'run_of_river': 'Laufwasser',
         'biomass': 'Biomasse',
         'solar': 'Solar',
         'wind': 'Wind',
         'uranium': 'Kernenergie',
         'lignite': 'Braunkohle',
         'hard_coal': 'Steinkohle',
         'gas': 'Gas',
         'mixed_fuels': 'Sonstiges',
         'oil': 'Öl',
         'phs_in': 'Pumpspeicher (Laden)',
         'phs_out': 'Pumpspeicher (Entladen)',
         'imports': 'Import',
         'exports': 'Export',
         'load': 'Last',
         'shortage': 'Ungedeckte Nachfrage',
         'excess': 'Überschüssige Energie'}
df_dispatch = df_dispatch.rename(columns=en_de)

# duration curves for all powerlines
pls = pd.concat(
    [powerlines[col].sort_values(ascending=False).reset_index(drop=True)
     for col in powerlines], axis=1)
pls.columns = [c.replace('_powerline', '') for c in pls.columns]
pls = pls[[
    'DE_AT', 'DE_CH', 'DE_CZ',
    'DE_DK', 'DE_FR', 'DE_LU',
    'DE_NL', 'DE_NO', 'DE_PL', 'DE_SE',
    'AT_DE', 'CH_DE', 'CZ_DE',
    'DK_DE', 'FR_DE', 'NL_DE', 'NO_DE',
    'PL_DE', 'SE_DE']]

pls[['NO_DE', 'DE_NO']].plot(cmap=cm.get_cmap('RdYlBu'))
plt.xlabel('Stunden des Jahres')
plt.ylabel('Leistung in GW')
plt.xlim(0, 10000)
plt.ylim(0, 1500)
plt.tight_layout()
plt.show()

# bar plot of powerlines (imports/exports)
pls_sum = pls.sum(axis=0).divide(10e6).to_frame().transpose()

exp = pls_sum[[c for c in pls.columns if c.startswith('DE_')]]
imp = pls_sum[[c for c in pls.columns if not c.startswith('DE_')]]
pls_sum_div = pd.concat([imp, exp], axis=0)
pls_sum_div.index = ['Import', 'Export']
pls_sum_div = pls_sum_div[[
    'DE_AT', 'DE_CH', 'DE_CZ',
    'DE_DK', 'DE_FR', 'DE_LU',
    'DE_NL', 'DE_NO', 'DE_PL', 'DE_SE',
    'AT_DE', 'CH_DE', 'CZ_DE',
    'DK_DE', 'FR_DE', 'NL_DE', 'NO_DE',
    'PL_DE', 'SE_DE']]

pls_sum_div.plot(kind='bar', stacked=True, cmap=cm.get_cmap('Paired'), rot=0,
                 legend='reverse')
plt.xlabel('')
plt.ylabel('Energie in TWh')
plt.tight_layout()
plt.show()


# %% duraction curve for one cable e.g. NordLink cable

file_name = 'scenario_nep_2035_2016-08-05 15:18:42.431986_DE.csv'

df = pd.read_csv('results/' + file_name, parse_dates=[0],
                 index_col=0, keep_date_col=True)

cable = df[['DE_NO_powerline', 'NO_DE_powerline']]
cable = pd.concat(
    [cable[col].sort_values(ascending=False).reset_index(drop=True)
     for col in cable], axis=1)
cable = cable.rename(columns={'DE_NO_powerline': 'DE-NO',
                              'NO_DE_powerline': 'NO-DE'})
cable.plot(legend='reverse', cmap=cm.get_cmap('RdYlBu'))
plt.xlabel('Stunden des Jahres')
plt.ylabel('Leistung in GW')
plt.ylim(0, max(cable.sum(axis=1)) * 1.2)
plt.tight_layout()
plt.show()


# %% duraction curve for prices
file_name = 'scenario_nep_2014_2016-08-04 12:04:42.180425_DE.csv'

df = pd.read_csv('results/' + file_name, parse_dates=[0],
                 index_col=0, keep_date_col=True)

power_price_real = pd.read_csv('price_eex_day_ahead_2014.csv')
power_price_real.set_index(df.index, drop=True, inplace=True)
power_price = pd.concat([power_price_real,
                         df[['duals']]], axis=1)
power_price = pd.concat(
    [power_price[col].sort_values(ascending=False).reset_index(drop=True)
     for col in power_price], axis=1)
power_price.plot(legend='reverse', cmap=cm.get_cmap('RdYlBu'))
plt.xlabel('Stunden des Jahres')
plt.ylabel('Preis in EUR/MWh')
plt.tight_layout()
plt.show()


# %% boxplot for prices: monthly

file_name = 'scenario_nep_2014_2016-08-04 12:04:42.180425_DE.csv'

df = pd.read_csv('results/' + file_name, parse_dates=[0],
                 index_col=0, keep_date_col=True)

df = df[['duals']]
df['dates'] = df.index
df['month'] = df.index.month

df_box = df.pivot(index='dates', columns='month', values='duals')

bp = df_box.boxplot(showfliers=False, showmeans=True, return_type='dict')
plt.xlabel('Monat')
plt.ylabel('Preis in EUR/MWh')
plt.tick_params(axis='y')
plt.tick_params(axis='x')
plt.legend('')

[[item.set_color('k') for item in bp['boxes']]]
[[item.set_color('k') for item in bp['fliers']]]
[[item.set_color('k') for item in bp['medians']]]
[[item.set_color('k') for item in bp['whiskers']]]
[[item.set_color('k') for item in bp['caps']]]

[[item.set_markerfacecolor('k') for item in bp['means']]]

plt.show()

## %% spline interpolation
#
#file_name = 'scenario_nep_2014_2016-08-04 12:04:42.180425_DE.csv'
#
#df = pd.read_csv('results/' + file_name, parse_dates=[0],
#                 index_col=0, keep_date_col=True)
#
#df = df[['duals']]
#
#price_real = pd.read_csv('price_eex_day_ahead_2014.csv')
#price_real.index = df_raw.index
#
#df = pd.concat([price_real, df], axis=1)
#df.columns = ['price_real', 'price_model']
#
## detect tableus with a constand price
#tableaus = np.where(df['price_model'] == df['price_model'].shift(1))
#tableaus = tableaus[0].tolist()
#
## set the tableaus to NaN
#df.reset_index(drop=True, inplace=True)
#df['no_tableaus'] = df[~df.index.isin(tableaus)]['price_model']
#df.index = df_raw.index
#
## check different interpolation methods
#df['linear'] = df['no_tableaus'].interpolate(method='linear')
#df['cubic'] = df['no_tableaus'].interpolate(method='cubic')
#
## plot
#df[0:24 * 7 * 8].plot(drawstyle='steps', subplots=False, sharey=True,
#                      linewidth=2)
#plt.show()
#
## statistical parameters
#df.corr()
#df.describe()


# %% comparison of prices for sensitivities

files = {
    'NEP-2025':
        'scenario_nep_2025_2016-08-16 14:52:22.118405_DE.csv',
    'NEP-2035':
        'scenario_nep_2035_2016-08-05 15:18:42.431986_DE.csv',
    'NEP-2035-ee+25':
        'scenario_nep_2035_ee_plus_25_2016-08-09 16:27:06.904477_DE.csv',
    'NEP-2035-ee-25':
        'scenario_nep_2035_ee_minus_25_2016-08-09 16:45:40.295183_DE.csv',
    'NEP-2035-demand+25':
        'scenario_nep_2035_demand_plus_25_2016-08-10 09:38:10.628613_DE.csv',
    'NEP-2035-demand-25':
        'scenario_nep_2035_demand_minus_25_2016-08-10 09:50:48.953929_DE.csv',
    'NEP-2035-fuel+25':
        'scenario_nep_2035_fuel_plus_25_2016-08-10 12:10:08.246319_DE.csv',
    'NEP-2035-fuel-25':
        'scenario_nep_2035_fuel_minus_25_2016-08-10 12:20:30.690439_DE.csv',
    'NEP-2035-co2+25':
        'scenario_nep_2035_co2_plus_25_2016-08-10 12:37:36.981611_DE.csv',
    'NEP-2035-co2-25':
        'scenario_nep_2035_co2_minus_25_2016-08-10 12:49:50.740375_DE.csv',
    'NEP-2035-nordlink+25':
        'scenario_nep_2035_nordlink_plus_25_2016-08-10 13:00:08.919877_DE.csv',
    'NEP-2035-nordlink-25':
        'scenario_nep_2035_nordlink_minus_25_2016-08-10 13:10:34.528303_DE.csv'
}

file_name = 'scenario_nep_2035_2016-08-05 15:18:42.431986_DE.csv'

df = pd.read_csv('results/' + file_name, parse_dates=[0],
                 index_col=0, keep_date_col=True)

df_prices = pd.DataFrame(index=df.index)

for k, v in files.items():
    df = pd.read_csv('results/' + v, parse_dates=[0],
                     index_col=0, keep_date_col=True)
    df.index = df_prices.index
    df_prices[k] = df['duals']

# sort by column names
df_prices.sort_index(inplace=True, axis=1)

# save as csv
df_prices.to_csv('prices_all_scenarios_with_sensivities.csv')

# boxplot
df_prices.plot(kind='box', rot=90,
               color={'medians': 'k', 'boxes': 'k', 'whiskers': 'k',
                      'caps': 'k'})
plt.ylabel('Preis in EUR/MWh')
plt.tight_layout()
plt.show()

# histogram
df_prices \
    .plot(kind='hist', bins=25, normed=True, subplots=True, sharex=True,
          sharey=True, layout=(7, 2), cmap=cm.get_cmap('RdYlBu'))
[ax.legend(loc='upper right') for ax in plt.gcf().axes]
plt.suptitle('Preis in EUR/MWh (25 Bins)', size=20)
plt.show()

# duration curves for all scenarios
df_prices_duration = pd.concat(
    [df_prices[col].sort_values(ascending=False).reset_index(drop=True)
     for col in df_prices], axis=1)
df_prices_duration.plot(legend='reverse', cmap=cm.get_cmap('RdYlBu'))
plt.xlabel('Stunden des Jahres')
plt.ylabel('Preis in EUR/MWh')
plt.tight_layout()
plt.show()

# duration curves for base scenarios
df_prices_duration[['NEP-2025',
                    'NEP-2035']].plot(legend='reverse',
                                           cmap=cm.get_cmap('RdYlBu'))
plt.xlabel('Stunden des Jahres')
plt.ylabel('Preis in EUR/MWh')
plt.tight_layout()
plt.show()

#df_prices['2035-01':'2035-02'].plot(drawstyle='steps')
#plt.show()


# %% plot of annual production for scenarios

files = {
    'nep_2014_base':
        'scenario_nep_2014_2016-08-04 12:04:42.180425_DE.csv',
    'nep_2025_base':
        'scenario_nep_2025_2016-08-16 14:52:22.118405_DE.csv',
    'nep_2035_base':
        'scenario_nep_2035_2016-08-05 15:18:42.431986_DE.csv',
    'nep_2035_ee_plus_25':
        'scenario_nep_2035_ee_plus_25_2016-08-09 16:27:06.904477_DE.csv',
    'nep_2035_ee_minus_25':
        'scenario_nep_2035_ee_minus_25_2016-08-09 16:45:40.295183_DE.csv',
    'nep_2035_demand_plus_25':
        'scenario_nep_2035_demand_plus_25_2016-08-10 09:38:10.628613_DE.csv',
    'nep_2035_demand_minus_25':
        'scenario_nep_2035_demand_minus_25_2016-08-10 09:50:48.953929_DE.csv',
    'nep_2035_fuel_plus_25':
        'scenario_nep_2035_fuel_plus_25_2016-08-10 12:10:08.246319_DE.csv',
    'nep_2035_fuel_minus_25':
        'scenario_nep_2035_fuel_minus_25_2016-08-10 12:20:30.690439_DE.csv',
    'nep_2035_co2_plus_25':
        'scenario_nep_2035_co2_plus_25_2016-08-10 12:37:36.981611_DE.csv',
    'nep_2035_co2_minus_25':
        'scenario_nep_2035_co2_minus_25_2016-08-10 12:49:50.740375_DE.csv',
    'nep_2035_nordlink_plus_25':
        'scenario_nep_2035_nordlink_plus_25_2016-08-10 13:00:08.919877_DE.csv',
    'nep_2035_nordlink_minus_25':
        'scenario_nep_2035_nordlink_minus_25_2016-08-10 13:10:34.528303_DE.csv'
}

df_dispatch = pd.DataFrame()

for k, v in files.items():
    df = pd.read_csv('results/' + v, parse_dates=[0],
                     index_col=0, keep_date_col=True)

    df_tmp = pd.DataFrame()

    # country code
    cc = ['DE', 'LU', 'AT']

    # get fossil and renewable power plants
    fuels = ['run_of_river', 'biomass', 'solar', 'wind', 'uranium', 'lignite',
             'hard_coal', 'gas', 'mixed_fuels', 'oil', 'load', 'excess',
             'shortage']
    for f in fuels:
        cols = [c for c in df.columns
                if f in c and any(substring in c
                                  for substring in cc)]
        df_tmp[f] = df[cols].sum(axis=1)

    # get imports and exports and aggregate columns
    cols = [c for c in df.columns
            if 'powerline' in c and any(substring in c
                                        for substring in cc)]
    powerlines = df[cols]
    exports = powerlines[[c for c in powerlines.columns
                          if c.startswith('DE_')]]
    imports = powerlines[[c for c in powerlines.columns
                          if ('_' + 'DE' + '_' in c)]]
    df_tmp['imports'] = imports.sum(axis=1)
    df_tmp['exports'] = exports.sum(axis=1)

    # get phs in- and outputs
    phs_in = df[[c for c in df.columns if 'phs_in' in c and
                any(substring in c for substring in cc)]]
    phs_out = df[[c for c in df.columns if 'phs_out' in c and
                 any(substring in c for substring in cc)]]
    phs_level = df[[c for c in df.columns if 'phs_level' in c and
                    any(substring in c for substring in cc)]]
    df_tmp['phs_in'] = phs_in.sum(axis=1)
    df_tmp['phs_out'] = phs_out.sum(axis=1)
    df_tmp['phs_level'] = phs_level.sum(axis=1)

    # MW to TW
    df_tmp = df_tmp.divide(1000000)

    # Sum up data (TWh) and adjust index
    df_tmp = df_tmp.sum().to_frame().transpose()
    df_tmp.reset_index(drop=True, inplace=True)
    df_tmp.index = [k]

    # append row
    df_dispatch = df_dispatch.append(df_tmp)

# sort by row index
df_dispatch.sort_index(inplace=True)

df_dispatch.sum(axis=1)

# plot
df_dispatch['load'] = df_dispatch['load'].multiply(-1)
df_dispatch['phs_in'] = df_dispatch['phs_in'].multiply(-1)
df_dispatch['exports'] = df_dispatch['exports'].multiply(-1)
df_dispatch['excess'] = df_dispatch['excess'].multiply(-1)

# check if balance fits
df_dispatch.drop(['phs_level'], axis=1).sum(axis=1)

# rename columns
en_de = {'run_of_river': 'Laufwasser',
         'biomass': 'Biomasse',
         'solar': 'Solar',
         'wind': 'Wind',
         'uranium': 'Kernenergie',
         'lignite': 'Braunkohle',
         'hard_coal': 'Steinkohle',
         'gas': 'Gas',
         'mixed_fuels': 'Sonstiges',
         'oil': 'Öl',
         'phs_in': 'Pumpspeicher (Laden)',
         'phs_out': 'Pumpspeicher (Entladen)',
         'imports': 'Import',
         'exports': 'Export',
         'load': 'Last',
         'shortage': 'Ungedeckte Nachfrage',
         'excess': 'Überschüssige Energie'}

df_dispatch = df_dispatch.rename(columns=en_de)

cols = ['Biomasse', 'Laufwasser', 'Kernenergie', 'Braunkohle',
        'Steinkohle', 'Gas', 'Öl', 'Sonstiges', 'Solar', 'Wind',
        'Pumpspeicher (Entladen)', 'Import', 'Ungedeckte Nachfrage',
        'Last', 'Pumpspeicher (Laden)', 'Export', 'Überschüssige Energie']

df_dispatch[cols].plot(kind='bar', stacked=True, cmap=cm.get_cmap('RdYlBu'))
plt.title('Jährliche Stromproduktion nach Energieträgern')
plt.ylabel('TWh')
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.tight_layout()
plt.show()

# %% influence of norwegian hydro power plants

file_name = 'scenario_nep_2025_2016-08-16 14:52:22.118405_NO.csv'

df = pd.read_csv('results/' + file_name, parse_dates=[0],
                 index_col=0, keep_date_col=True)

df_dispatch = df

# MW to GW
df_dispatch = df_dispatch.divide(1000)

# rename columns
en_de = {'NO_run_of_river': 'Laufwasser',
         'NO_pp_biomass': 'Biomasse',
         'NO_solar': 'Solar',
         'NO_wind': 'Wind',
         'NO_pp_uranium': 'Kernenergie',
         'NO_pp_lignite': 'Braunkohle',
         'NO_pp_hard_coal': 'Steinkohle',
         'NO_pp_gas': 'Gas',
         'NO_pp_mixed_fuels': 'Sonstiges',
         'NO_pp_oil': 'Öl',
         'NO_storage_phs_in': 'Pumpspeicher (Laden)',
         'NO_storage_phs_out': 'Pumpspeicher (Entladen)',
         'NO_load': 'Last',
         'NO_shortage': 'Ungedeckte Nachfrage',
         'NO_excess': 'Überschüssige Energie',
         'DE_NO_powerline': 'DE-NO',
         'NO_DE_powerline': 'NO-DE'}
df_dispatch = df_dispatch.rename(columns=en_de)

# Plot
cols = ['Pumpspeicher (Entladen)', 'Pumpspeicher (Laden)',
        ]
df_dispatch['2025-01-13':'2025-01-14'][cols] \
             .plot(drawstyle='steps', cmap=cm.get_cmap('RdYlBu'))
plt.xlabel('')
plt.ylabel('Leistung in  GW')
plt.ylim(0, 1)

df_dispatch['2025-01-13':'2025-01-14']['NO_storage_phs_level'] \
             .plot(secondary_y=True, drawstyle='steps', linestyle='--',
                   color='k')
plt.xlabel('')
plt.ylabel('Füllstand in  GWh')
plt.ylim(0, 10)
plt.tight_layout()
plt.show()

# duration curves
cols = ['Laufwasser',
        'Pumpspeicher (Laden)',
        'Pumpspeicher (Entladen)',
        'DE-NO', 'NO-DE']
df_duration = pd.concat(
    [df_dispatch[col].sort_values(ascending=False).reset_index(drop=True)
     for col in df_dispatch[cols]], axis=1)
df_duration.plot(legend='reverse', cmap=cm.get_cmap('RdYlBu'))
plt.xlabel('Stunden des Jahres')
plt.xlim(0, 10000)
plt.ylim(0, 30)
plt.ylabel('GW')
plt.tight_layout()
plt.show()

## scatter plot
#df_dispatch[cols].plot(kind='scatter',
#                       x='Pumpspeicher (Entladen)',
#                       y='NO-DE')
#plt.show()
#
#
#df_dispatch[cols].plot(kind='scatter',
#                       x='Pumpspeicher (Laden)',
#                       y='DE-NO')
#plt.show()