import random, string
from flask import Flask, render_template, request, make_response
import json
import pandas as pd
import time
import random

from scripts.apuestas import Apuestas

a=Apuestas()
# a.buscar_partidos()
a.cargar_partidos()
a.comparar()
a.actualizar_json()
# a.ordenar_eventos_alfabeticamente()
# a.pretty_print()


if __name__=='__main__':
    a=Apuestas()
    a.buscar_partidos()
    # a.cargar_partidos()
    a.comparar()
    a.buscar_apuestas_seguras()
    # a.actualizar_json()
    # a.ordenar_eventos_alfabeticamente()
    # a.pretty_print()
    df=a.to_dataframe()
    seguras=df[df['Esperanza']>1]
    print("ApuestasSeguras:\n",seguras)
