from flask import Flask, abort, render_template, current_app, request
import mysql.connector
import utils.maskPassword as maskPassword
import urllib.parse


def home_page():
    return render_template("home.html")

