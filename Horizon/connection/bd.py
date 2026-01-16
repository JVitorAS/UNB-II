import mysql.connector
import matplotlib as mtb
import geobr
import pandas as pd

class config_bd():
    def __init__(self):
        self.host = '185.31.40.43'
        self.port = 3306
        self.user = 'horizon'
        self.password = 'bWCcHfU6Aanu6ab'
        self.db = 'horizon_space'

        self.conn = mysql.connector.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.db)

        self.cursor = self.conn.cursor()

    def view_uf(self, state):
        command = "SELECT * VIEW VW_ESTADOS_%s"
        self.cursor.execute(command,(state,))
        return self.cursor.fetchall()
        for uf in siglas:
            view_name = f"vw_estados__{uf}"
            try:
                self.cursor.execute(f"SELECT * FROM `{view_name}`;")
                self.resultados[uf] = self.cursor.fetchall()
            except mysql.connector.Error as e:
                self.resultados[uf] = f"Erro ao acessar a view: {e}"
        
        return self.resultados

    def comp_entre_uf(self):
        valor = self.result[]