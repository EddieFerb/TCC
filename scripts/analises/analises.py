# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# # Definindo a paleta de cores
# palette = ["green", "blue"]

# # Carregando os dados
# years = range(1995, 2024)
# dfs = []

# for year in years:
#     df = pd.read_csv(f'dados/processado/dados_cursos_tratado_{year}.csv', sep=';')
#     df['ano'] = year
#     dfs.append(df)

# dados_cursos_tratado = pd.concat(dfs, ignore_index=True)

# dados_ies_tratado = pd.read_csv('dados/processado/dados_ies_tratado_2023.csv', sep=';')

# # Juntando as informações das universidades e cursos
# df = dados_cursos_tratado.merge(dados_ies_tratado, on='id_ies', how='left')
# df = df[(df['numero_cursos'] > 0) & (df['nome_ies'].notna())]
# df[['nome_curso', 'nome_ies']] = df[['nome_curso', 'nome_ies']].apply(lambda x: x.str.upper())
# df[['concluintes', 'ingressantes']] = df[['concluintes', 'ingressantes']].astype(int)

# df['tipo_rede'] = df['tipo_rede'].replace({'1': 'Pública', '2': 'Privada'}).fillna('Outro')
# df['cat_adm'] = df['cat_adm'].replace({'1': 'Federal', '2': 'Estadual'}).fillna('Outro')
# df['modalidade_ensino'] = df['modalidade_ensino'].replace({'1': 'Presencial', '2': 'EAD'}).fillna('Outro')

# # Filtrando cursos específicos e calculando taxa de evasão
# cursos_selecionados = {'ENGENHARIA CIVIL': 5, 'MEDICINA': 6, 'DIREITO': 5, 'ADMINISTRAÇÃO': 4}

# df_grouped = df.groupby(['nome_curso', 'modalidade_ensino', 'ano', 'tipo_rede'])[['ingressantes', 'concluintes']].sum().reset_index()
# df_pivot = df_grouped.pivot(index=['nome_curso', 'modalidade_ensino', 'tipo_rede'], columns='ano', values=['ingressantes', 'concluintes']).reset_index()

# df_pivot.columns = ['_'.join(map(str, col)).strip('_') for col in df_pivot.columns]
# df_pivot = df_pivot[df_pivot['nome_curso'].isin(cursos_selecionados.keys())]

# for curso, duracao in cursos_selecionados.items():
#     curso_df = df_pivot[df_pivot['nome_curso'] == curso].copy()
#     for ano in range(1995 + duracao, 2024):
#         curso_df[f'taxa_evasao_{ano}'] = 1 - (curso_df[f'concluintes_{ano}'] / curso_df.get(f'ingressantes_{ano-duracao}', np.nan))
#     curso_df = curso_df.melt(id_vars=['nome_curso', 'modalidade_ensino', 'tipo_rede'], value_vars=[f'taxa_evasao_{ano}' for ano in range(1995 + duracao, 2024)], var_name='ano', value_name='taxa_evasao')
#     curso_df['ano'] = curso_df['ano'].str.extract(r'(\d{4})').astype(int)
    
#     # Plotando os gráficos
#     plt.figure(figsize=(10, 5))
#     for tipo_rede in curso_df['tipo_rede'].unique():
#         subset = curso_df[curso_df['tipo_rede'] == tipo_rede]
#         plt.plot(subset['ano'], subset['taxa_evasao'], marker='o', label=tipo_rede)
    
#     plt.title(f'Taxa de Evasão ao longo dos anos - {curso}')
#     plt.xlabel('Ano de Ingresso')
#     plt.ylabel('Taxa de Evasão')
#     plt.legend(title='Modalidade de Ensino')
#     plt.grid(True)
#     plt.show()

# # Exportando os dados
# df_pivot.to_csv('dados/processado/final_ingressantes_py.csv', index=False)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Definindo a paleta de cores
palette = ["green", "blue"]

# Carregando os dados
years = range(2009, 2024)
dfs = []

for year in years:
    df = pd.read_csv(f'dados/processado/dados_cursos_tratado_{year}.csv', sep=';')
    df['ano'] = year
    dfs.append(df)

dados_cursos_tratado = pd.concat(dfs, ignore_index=True)

dados_ies_tratado = pd.read_csv('dados/processado/dados_ies_tratado_2023.csv', sep=';')

# Juntando as informações das universidades e cursos
df = dados_cursos_tratado.merge(dados_ies_tratado, on='id_ies', how='left')
df = df[(df['numero_cursos'] > 0) & (df['nome_ies'].notna())]
df[['nome_curso', 'nome_ies']] = df[['nome_curso', 'nome_ies']].apply(lambda x: x.str.upper())
df[['concluintes', 'ingressantes']] = df[['concluintes', 'ingressantes']].astype(int)

# A linha abaixo era responsável por ajustar o tipo de rede, mas estamos desconsiderando essa variável.
# df['tipo_rede'] = df['tipo_rede'].replace({'1': 'Pública', '2': 'Privada'}).fillna('Outro')

df['cat_adm'] = df['cat_adm'].replace({'1': 'Federal', '2': 'Estadual'}).fillna('Outro')
df['modalidade_ensino'] = df['modalidade_ensino'].replace({'1': 'Presencial', '2': 'EAD'}).fillna('Outro')

# Filtrando cursos específicos e calculando taxa de evasão
cursos_selecionados = {'ENGENHARIA CIVIL': 5, 'MEDICINA': 6, 'DIREITO': 5, 'ADMINISTRAÇÃO': 4}

# Agrupamos apenas por 'nome_curso', 'modalidade_ensino' e 'ano', desconsiderando o 'tipo_rede'
df_grouped = df.groupby(['nome_curso', 'modalidade_ensino', 'ano'])[['ingressantes', 'concluintes']].sum().reset_index()

# Pivotamos os dados sem o 'tipo_rede'
df_pivot = df_grouped.pivot(index=['nome_curso', 'modalidade_ensino'], columns='ano', values=['ingressantes', 'concluintes']).reset_index()

df_pivot.columns = ['_'.join(map(str, col)).strip('_') for col in df_pivot.columns]
df_pivot = df_pivot[df_pivot['nome_curso'].isin(cursos_selecionados.keys())]

# No cálculo de taxas, não consideramos mais a variável tipo_rede.
for curso, duracao in cursos_selecionados.items():
    curso_df = df_pivot[df_pivot['nome_curso'] == curso].copy()
    for ano in range(2009 + duracao, 2024):
        # Cálculo da taxa de evasão: 1 - (concluintes / ingressantes do ano de ingresso)
        curso_df[f'taxa_evasao_{ano}'] = 1 - (
            curso_df.get(f'concluintes_{ano}', np.nan) / curso_df.get(f'ingressantes_{ano - duracao}', np.nan)
        )
    # Remodelamos o DataFrame para plotagem
    curso_df = curso_df.melt(id_vars=['nome_curso', 'modalidade_ensino'], 
                              value_vars=[f'taxa_evasao_{ano}' for ano in range(2009 + duracao, 2024)], 
                              var_name='ano', value_name='taxa_evasao')
    curso_df['ano'] = curso_df['ano'].str.extract(r'(\d{4})').astype(int)
    
    # Plotando os gráficos (agora sem distinção por tipo de rede)
    plt.figure(figsize=(10, 5))
    plt.plot(curso_df['ano'], curso_df['taxa_evasao'], marker='o', label='Taxa de Evasão')
    plt.title(f'Taxa de Evasão ao longo dos anos - {curso}')
    plt.xlabel('Ano de Ingresso')
    plt.ylabel('Taxa de Evasão')
    plt.legend(title='Modalidade de Ensino')
    plt.grid(True)
    plt.show()

# Exportando os dados
df_pivot.to_csv('dados/processado/final_ingressantes_py.csv', index=False)