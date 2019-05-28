from flask import(
    Flask, render_template, Blueprint, url_for, request, current_app, flash, redirect
)
import sys, os

from tables import undirected_resultslp, undirected_data, directed_data, nc_data, all_methods, all_datasets, resultsnc, directed_resultslp, filter_methods, directed_restricted
from results import listlp_to_json, listnc_to_json

bp = Blueprint('stats', __name__, url_prefix='/', template_folder='templates')



@bp.route("statistics", methods=['GET'])
def statistics():
    listlp_to_json()
    listnc_to_json()
    undirected_score = undirected_resultslp()
    nc_score = resultsnc()
    directed_score = directed_resultslp()

    return render_template("statistics.html", undirected_datas = undirected_data, undirected_score = undirected_score,
    directed_methods = filter_methods(directed_restricted), directed_datas = directed_data, directed_score = directed_score,
    nc_datas = nc_data, nc_score = nc_score)
