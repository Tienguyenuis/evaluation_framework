from flask import(
    Flask, render_template, Blueprint, url_for, request, current_app, flash, redirect
)
import sys, os

from tables import undirected_resultslp, undirected_data, directed_data, nc_data, all_methods, all_datasets, resultsnc, directed_resultslp, filter_methods, directed_restricted
from auto_docker import make_container_train, make_container_evaluate, install_requirements, execute_train, execute_evaluation
from make_scripts import maketrainlp, maketrainnc, makeevallp, makeevalnc

bp = Blueprint(
    'eval', __name__, url_prefix='/', template_folder='templates')

@bp.route("/", methods=['GET'])
def home():
   return render_template("index.html")


@bp.route("/hello/", methods=['GET'])
def hello():
    return("Hello World!")

@bp.route("evaluate", methods=['GET', 'POST'])
def evaluate():
    if request.method == 'POST':
        try:
            if request.form.get('confirmed') == 'confirmed':
                if not request.form.getlist('embedding_methods') and not request.form.getlist('embedding_datasets'):
                    flash("Methods and datasets have to be checked", category='danger')
                else:
                    flash("The methods and datasets have been selected. Please confirm if you would like to evaluate", category='warning')
                    checked_datasets = request.form.getlist('embedding_datasets')
                    checked_methods = request.form.getlist('embedding_methods')
                    print(checked_datasets, checked_methods)
                    return redirect(url_for('eval.confirm', checked_methods = checked_methods, checked_datasets = checked_datasets))
            else:
                flash("You need to check the confirmation box", category='danger')
        except:
            pass
    
    return render_template("evaluate.html", methods = all_methods, datasets = all_datasets)

@bp.route("/confirm/<checked_methods>/<checked_datasets>", methods=['GET', 'POST'])
def confirm(checked_methods, checked_datasets):
    checked_methods = checked_methods.strip('][').split(', ') 
    checked_datasets = checked_datasets.strip('][').split(', ') 
    if request.method == 'POST':
        print(checked_methods)
        for method in checked_methods:
            maketrainlp(method, checked_datasets)
            maketrainnc(method, checked_datasets)
            make_container_train()
            install_requirements(method)
            execute_train()
        
        make_container_evaluate()
        makeevallp(checked_methods, checked_datasets)
        makeevalnc(checked_methods, checked_datasets)
        execute_evaluation()
        flash("Evaluation finished", category='success')
        return redirect(url_for("eval.home"))
    
    return render_template("confirm.html", checked_methods = checked_methods, checked_datasets = checked_datasets)

