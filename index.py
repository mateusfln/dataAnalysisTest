import pandas as pd

data = pd.read_csv('impact-report.csv')

data['Sub Id 3'] = data['Sub Id 3'].fillna('N/A')

faturamento_total = data.groupby(['Sub Id 1', 'Sub Id 2', 'Sub Id 3'])['Action Earnings'].sum().reset_index()
print("Faturamento Atual Total:")
print('---------------------------------------------------------------')
print(faturamento_total.head())
print('---------------------------------------------------------------')

# valores ficticios da comissão
valor_free_trial_mes_cheio = 29
valor_paid_trial_mes_cheio = 79

free_trial_count = data[data['Event Type'] == 'Free Trial API'].groupby(['Sub Id 1', 'Sub Id 2', 'Sub Id 3']).size().reset_index(name='Free Trial Count')
paid_trial_count = data[data['Event Type'] == 'Paid Trial API'].groupby(['Sub Id 1', 'Sub Id 2', 'Sub Id 3']).size().reset_index(name='Paid Trial Count')

print("Contagem de Free Trial:")
print('---------------------------------------------------------------')
print(free_trial_count.head())
print('---------------------------------------------------------------')
print("Contagem de Paid Trial:")
print('---------------------------------------------------------------')
print(paid_trial_count.head())
print('---------------------------------------------------------------')

faturamento_previsao = pd.merge(free_trial_count, paid_trial_count, on=['Sub Id 1', 'Sub Id 2', 'Sub Id 3'], how='outer').fillna(0)

print("Faturamento Previsão:")
print('---------------------------------------------------------------')
print(faturamento_previsao.head())
print('---------------------------------------------------------------')

faturamento_previsao['Free Trial Revenue'] = faturamento_previsao['Free Trial Count'] * valor_free_trial_mes_cheio
faturamento_previsao['Paid Trial Revenue'] = faturamento_previsao['Paid Trial Count'] * valor_paid_trial_mes_cheio

relatorio = pd.merge(faturamento_total, faturamento_previsao, on=['Sub Id 1', 'Sub Id 2', 'Sub Id 3'], how='outer').fillna(0)

relatorio = relatorio.fillna(0)

relatorio['Total Projected Revenue'] = relatorio['Action Earnings'] + relatorio['Free Trial Revenue'] + relatorio['Paid Trial Revenue']

print("Relatório Final:")
print('---------------------------------------------------------------')
print(relatorio)
print('---------------------------------------------------------------')
