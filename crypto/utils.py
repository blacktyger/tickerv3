from django.shortcuts import render
import json
import requests


def datex(value):
    value = str(value)
    new_value = value[0:10]+" "+value[11:16]
    return f"{new_value} UTC"

def btc(value):
    return f"₿ {value:.8f}"

def usd2(value):
    return f"$ {value:.2f}"

def usd3(value):
    return f"$ {value:.3f}"

def procent(value):
    return f"{value:.1f} %"
