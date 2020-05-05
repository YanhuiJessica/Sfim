from flask import Blueprint, render_template, flash, redirect, request

start = Blueprint('start', __name__)

@start.route('')
def index():
    return render_template('start.html')