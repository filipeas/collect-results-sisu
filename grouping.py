import os
import pandas as pd

# Lista das colunas mais importantes
colunas_importantes = [
    "CO_IES", "NO_IES", "SG_IES", "SG_UF_IES", "NO_CAMPUS", "CO_IES_CURSO",
    "NO_CURSO", "DS_TURNO", "QT_VAGAS_CONCORRENCIA",
    "NO_INSCRITO", "NU_NOTA_CANDIDATO", "NU_NOTACORTE_CONCORRIDA", "NU_CLASSIFICACAO"
]

# Colunas a serem garantidas como numéricas
colunas_numericas = [
    "NU_NOTA_CANDIDATO", "NU_NOTACORTE_CONCORRIDA", "NU_CLASSIFICACAO",
    "CO_IES", "QT_VAGAS_CONCORRENCIA", "CO_IES_CURSO"
]

# Caminho para a pasta 'downloads' onde os arquivos .csv estão armazenados
pasta_downloads = 'downloads'

# Lista os arquivos .csv na pasta
arquivos_csv = [f for f in os.listdir(pasta_downloads) if f.endswith('.csv')]

# DataFrame vazio para armazenar os dados combinados
df_combinado = pd.DataFrame()

for arquivo in arquivos_csv:
    # Lê o arquivo .csv com header especificado
    caminho_arquivo = os.path.join(pasta_downloads, arquivo)
    try:
        df = pd.read_csv(caminho_arquivo, sep=';', header=0, quotechar='"')  # Usando ponto e vírgula e tratando aspas

        # Verificar se as colunas existem no arquivo
        colunas_faltando = [col for col in colunas_importantes if col not in df.columns]
        if colunas_faltando:
            print(f"Aviso: As colunas {colunas_faltando} não foram encontradas no arquivo {arquivo}.")
        
        # Filtra apenas as colunas de interesse
        df_filtrado = df[colunas_importantes].copy()  # Usar .copy() para evitar o SettingWithCopyWarning

        # Substituir vírgula por ponto nas colunas numéricas
        for col in colunas_numericas:
            if df_filtrado[col].dtype == 'object':  # Verifica se a coluna é de tipo 'object' (string)
                df_filtrado[col] = df_filtrado[col].str.replace(',', '.', regex=False)  # Substitui vírgula por ponto

            # Converte para numérico, tratando erros e substituindo valores não numéricos por NaN
            df_filtrado.loc[:, col] = pd.to_numeric(df_filtrado[col], errors='coerce')

        # Concatena o DataFrame atual com o combinado
        df_combinado = pd.concat([df_combinado, df_filtrado], ignore_index=True)
    
    except Exception as e:
        print(f"Erro ao processar o arquivo {arquivo}: {e}")

# Caminho para salvar o arquivo combinado
caminho_saida = 'arquivo_combinado.csv'

# Salva o DataFrame combinado em um único arquivo CSV
df_combinado.to_csv(caminho_saida, index=False, sep=';')

print(f'Arquivo combinado salvo em: {caminho_saida}')
