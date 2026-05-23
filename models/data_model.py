import pandas as pd
import streamlit as st

@st.cache_data
def carregar_csv_em_cache(file_path):
    try:
        data = pd.read_csv(file_path, sep=';', encoding='utf-8', on_bad_lines='skip', low_memory=False)
        rename_map = {
            'abt_dt_abastecimento': 'Data',
            'fun_ds_funcionario': 'Frentista',
            'pro_ds_produto': 'Combustivel',
            'abt_vl_volume_abastecido': 'Litros',
            'abt_vl_abastecimento': 'Valor_Total'
        }
        data = data.rename(columns=rename_map)
        data['Frentista'] = data['Frentista'].fillna("Não Identificado")

        for col in ['Litros', 'Valor_Total']:
            if col in data.columns and not pd.api.types.is_numeric_dtype(data[col]):
                data[col] = data[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

        if 'Data' in data.columns:
            data['Data'] = pd.to_datetime(data['Data'], format='%d/%m/%Y', errors='coerce')

        colunas_utilizadas = ['Data', 'Frentista', 'Combustivel', 'Litros', 'Valor_Total']
        colunas_existentes = [c for c in colunas_utilizadas if c in data.columns]
        data = data[colunas_existentes]

        return data
    except Exception as e:
        st.error(f"Erro ao ler CSV: {e}")
        return pd.DataFrame()

class DataModel:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = carregar_csv_em_cache(self.file_path)

    def is_empty(self):
        return self.data.empty

    def get_dados_filtrados(self, frentista, combustiveis):
        if self.data.empty:
            return self.data

        dados_filtrados = self.data.copy()

        if frentista != "Todos":
            dados_filtrados = dados_filtrados[dados_filtrados["Frentista"] == frentista]

        if combustiveis:
            dados_filtrados = dados_filtrados[dados_filtrados["Combustivel"].isin(combustiveis)]

        return dados_filtrados

    def get_opcoes_frentistas(self):
        if self.data.empty:
            return ["Todos"]
        return ["Todos"] + sorted(list(self.data["Frentista"].dropna().unique()))

    def get_opcoes_combustiveis(self):
        if self.data.empty:
            return []
        return list(self.data["Combustivel"].unique())
