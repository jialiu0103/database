#!/usr/local/Python-3.7/bin/python
import pymysql
import os,sys
import cgi
import matplotlib
import numpy as np
import pandas as pd
from io import BytesIO
import base64
import matplotlib.pyplot as plt

# print content-type


# retrieve form data, if any
form = cgi.FieldStorage()

# check if form data is returned
if form:

    # Connect to the database.
    connection = pymysql.connect(host='bioed.bu.edu', database='groupF', user='jiliu', password='jiliu', port=4253)
    cursor = connection.cursor()

    # check if submit button was clicked
    submit = form.getvalue("submit")
    if submit:
        # get the pathway

        vis_type = form.getvalue("vis_type")
        phylo_rank = form.getvalue("phylo_rank")
        mouse_type = form.getvalue("mouse_type")
        status = form.getvalue("status")
        labels = form.getvalue("labels")
        # specify the query for the interacting proteins
        query = ""

        if mouse_type == "All" and status == "All":
            query = """SELECT Abundance.value as value, mouse.name as mname, WTvsAD as type1, PurevsMix as type2, TaxonomicRank.name as tname FROM Abundance join mouse on Abundance.mid = mouse.mid join TaxonomicRank on Abundance.tid = TaxonomicRank.tid WHERE rank ='%s';""" % (
                phylo_rank)
        elif mouse_type == "All":
            query = """SELECT Abundance.value as value, mouse.name as mname, WTvsAD as type1, PurevsMix as type2,  TaxonomicRank.name as tname FROM Abundance join mouse on Abundance.mid = mouse.mid join TaxonomicRank on Abundance.tid = TaxonomicRank.tid WHERE rank ='%s' and WTvsAD = '%s';""" % (
                phylo_rank, status)
        elif status == "All":
            query = """SELECT Abundance.value as value, mouse.name as mname,  WTvsAD as type1, PurevsMix as type2, TaxonomicRank.name as tname FROM Abundance join mouse on Abundance.mid = mouse.mid join TaxonomicRank on Abundance.tid = TaxonomicRank.tid WHERE rank ='%s' and PurevsMix = '%s';""" % (
                phylo_rank, mouse_type)
        else:
            query = """SELECT Abundance.value as value, mouse.name as mname,  WTvsAD as type1, PurevsMix as type2, TaxonomicRank.name as tname FROM Abundance join mouse on Abundance.mid = mouse.mid join TaxonomicRank on Abundance.tid = TaxonomicRank.tid WHERE rank ='%s' and PurevsMix = '%s' and WTvsAD = '%s';""" % (
            phylo_rank, mouse_type, status)

        Abundance = []
        MName = []
        TName = []

        df = pd.read_sql(query, connection)
        if vis_type == "Heatmap":
            if labels == "Type":
                df['mname'] = df.apply(lambda row: row.mname+row.type1 + row.type2, axis=1)
                table = df.pivot(index='tname', columns='mname', values='value')
            else:
                table = df.pivot(index='tname', columns='mname', values='value')

            table= table.apply(lambda x: pow(10, x))
            fig, ax = plt.subplots()
            plt.xticks(rotation=90)
            ax.pcolor(table.values, vmin = pow(10,df['value'].min()), vmax = pow(10,df['value'].max()),cmap = 'bwr')
            ax.set_xticks(np.arange(table.shape[1] + 1) + 0.5, minor=False)
            ax.set_xticklabels(table.columns, minor=False)
            ax.set_yticks(np.arange(table.shape[0] + 1) + 0.5, minor=False)
            ax.set_yticklabels(table.index, minor=False)
            ax.set_xlim(0, table.shape[1])
            ax.set_ylim(0, table.shape[0])
            plt.colorbar(ax.pcolor(table.values, vmin=pow(10, df['value'].min()), vmax=pow(10, df['value'].max()), cmap='bwr'))
            #plt.show()
            #fig.colorbar(matplotlib.cm.ScalarMappable(cmap=plt.get_cmap('jet')), ax=ax)
            #doesn't work
            figdata = BytesIO()

            fig.savefig(figdata, format='png',bbox_inches='tight')
            image_base64 = base64.b64encode(figdata.getvalue()).decode('utf-8').replace('\n', '')
            figdata.close()

            print("Content-type: text/html\n")
            print("data:image/png;base64, %s" %(image_base64))


        # execute the query

        elif vis_type == "Stack Bar":
            if labels == "Type":
                df['mname'] = df.apply(lambda row: row.mname + row.type1 + row.type2, axis=1)
                pivot_df = df.pivot(index='mname', columns='tname', values='value')
            else:
                pivot_df = df.pivot(index='mname', columns='tname', values='value')
            pivot_df = pivot_df.apply(lambda x: pow(10, x))

            plot = pivot_df.plot.bar(stacked=True)
            fig, ax = plt.subplots()
            ax.set_xticks(np.arange(pivot_df.shape[1] + 1) + 0.5, minor=False)
            ax.set_xticklabels(pivot_df.columns, minor=False)
            ax.set_yticks(np.arange(pivot_df.shape[0] + 1) + 0.5, minor=False)
            ax.set_yticklabels(pivot_df.index, minor=False)
            ax.set_xlim(0, pivot_df.shape[1])
            ax.set_ylim(0, pivot_df.shape[0])
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.6, box.height])
            lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='xx-small')
            fig = plot.get_figure()
            figdata = BytesIO()
            fig.savefig(figdata, format='png',bbox_extra_artists=(lgd,),bbox_inches='tight')
            image_base64 = base64.b64encode(figdata.getvalue()).decode('utf-8').replace('\n', '')
            figdata.close()

            print("Content-type: text/html\n")
            print("data:image/png;base64, %s" %(image_base64))

else:
    # no form data, just print an empty http header
    print("Content-type: text/html\n")

