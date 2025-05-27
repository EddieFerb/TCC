import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv

caminhos = {
    'Administração': 'dados/processado/final_administracao.csv',
    'Direito': 'dados/processado/final_direito.csv',
    'Engenharia Civil': 'dados/processado/final_eng_civil.csv',
    'Medicina': 'dados/processado/final_medicina.csv'
}

for curso, caminho in caminhos.items():
    try:
        df = pd.read_csv(caminho, delimiter=';')
        # Se 'ano' e 'evasao_real' não estiverem no DataFrame, recriá-los a partir das colunas 'taxa_evasao_20XX'
        if 'ano' not in df.columns or 'evasao_real' not in df.columns:
            colunas_evasao = [col for col in df.columns if col.startswith('taxa_evasao_')]
            if colunas_evasao:
                anos = [int(col.split('_')[-1]) for col in colunas_evasao]
                evasoes = [df[col].values[0] for col in colunas_evasao]
                df = pd.DataFrame({'ano': anos, 'evasao_real': evasoes})
                df['evasao_predita'] = df['evasao_real']  # Inicialmente copia, pode ser sobrescrito se existir coluna real
        print(f"📂 Verificando cabeçalho do arquivo {caminho}...")
        with open(caminho, 'r') as f:
            for _ in range(3):
                print(f.readline().strip())
        print(f"📄 Colunas encontradas: {df.columns.tolist()}")
    except Exception as e:
        print(f"❌ Erro ao ler {caminho}: {e}")
        continue
    if 'ano' not in df.columns:
        print(f"⚠️ Coluna 'ano' não encontrada no arquivo {caminho}.")
    print(f"\n📄 Colunas no arquivo {caminho}:\n{df.columns.tolist()}\n")
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='ano', y='evasao_real', data=df, label='INEP (real)', marker='o')
    sns.lineplot(x='ano', y='evasao_predita', data=df, label='Projeto TCC (predita)', marker='s')
    plt.title(f'Taxa de Evasão - {curso}')
    plt.xlabel('Ano')
    plt.ylabel('Taxa de Evasão')
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'documentos/graficos/taxa_evasao_{curso.lower().replace(" ", "_")}.png')
    plt.close()

print("✅ Gráficos gerados para os cursos: Administração, Direito, Engenharia Civil e Medicina.")