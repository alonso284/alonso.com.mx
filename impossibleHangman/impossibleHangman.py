from flask import Flask, render_template, request, redirect, url_for, jsonify, Markup, session, Blueprint
import requests
import os
import json
from dotenv import load_dotenv
import base64
import psycopg2
from urllib.parse import urlparse



impossibleHangman = Blueprint('impossibleHangman', __name__,
                          static_folder='static', template_folder='templates')

@impossibleHangman.route('/')
def main():
    return "Hello World"