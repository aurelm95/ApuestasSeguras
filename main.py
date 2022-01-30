import random, string
from flask import Flask, render_template, request, make_response
import json
import pandas as pd
import time
import random

from scripts.apuestas import Apuestas
from scripts.williamhill import Williamhill




if __name__=='__main__' and True:
    a=Apuestas()
    # a.buscar_partidos()
    a.cargar_partidos()
    a.comparar()
    a.buscar_apuestas_seguras()
    a.actualizar_json()
    # a.ordenar_eventos_alfabeticamente()
    # a.pretty_print()
    df=a.to_dataframe()
    print(df)
    seguras=df[df['Esperanza']>1]
    print("ApuestasSeguras:",seguras.values.shape[0])

# if __name__=='__main__':
#     w=Williamhill()
#     w.cargar_html()
