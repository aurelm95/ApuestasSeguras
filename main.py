from scripts.apuestas import Apuestas






if __name__=='__main__':
    a=Apuestas()
    # a.buscar_partidos()
    a.cargar_partidos()
    a.comparar()
    a.actualizar_json()
    # a.ordenar_eventos_alfabeticamente()
    a.pretty_print()
    df=a.to_dataframe()