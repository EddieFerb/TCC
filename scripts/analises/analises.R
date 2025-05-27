<<<<<<< HEAD
# Comandos para instalar as bibliotecas
# install.packages(c("tidyr", "dplyr", "plotly", "stringr"))

# Carregando Bibliotecas necessárias para o funcionamento do script
=======
# # Comandos para instalar as bibliotecas
# # install.packages(c("tidyr", "dplyr", "plotly", "stringr"))

# # Carregando Bibliotecas necessárias para o funcionamento do script
# library(tidyr)
# library(dplyr)
# library(plotly)
# library(stringr)

# palette <- c("green", "blue")

# # Processando as bases de dados

# ## Dados de ingressantes e concluíntes em universidades ao longo dos anos
# dados_cursos_tratado_2011  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2017.csv') |> dplyr::mutate(ano = 2011)
# dados_cursos_tratado_2012  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2017.csv') |> dplyr::mutate(ano = 2012)
# dados_cursos_tratado_2013  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2017.csv') |> dplyr::mutate(ano = 2013)
# dados_cursos_tratado_2014  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2017.csv') |> dplyr::mutate(ano = 2014)
# dados_cursos_tratado_2015  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2017.csv') |> dplyr::mutate(ano = 2015)
# dados_cursos_tratado_2016  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2017.csv') |> dplyr::mutate(ano = 2016)
# dados_cursos_tratado_2017  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2017.csv') |> dplyr::mutate(ano = 2017)
# dados_cursos_tratado_2018  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2018.csv') |> dplyr::mutate(ano = 2018)
# dados_cursos_tratado_2019  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2019.csv') |> dplyr::mutate(ano = 2019)
# dados_cursos_tratado_2020  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2020.csv') |> dplyr::mutate(ano = 2020)
# dados_cursos_tratado_2021  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2021.csv') |> dplyr::mutate(ano = 2021)
# dados_cursos_tratado_2022  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2022.csv') |> dplyr::mutate(ano = 2022)
# dados_cursos_tratado_2023  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2023.csv') |> dplyr::mutate(ano = 2023)

# ## Dados de universidades de modo geral
# dados_ies_tratado     <- read.csv2(file = 'informacao/dados/processado/dados_ies_tratado_2023.csv')


# ## Unindo os dados de cursos e universidades
# dados_cursos_tratado <- rbind(
#   dados_cursos_tratado_2011,
#   dados_cursos_tratado_2012,
#   dados_cursos_tratado_2013,
#   dados_cursos_tratado_2014,
#   dados_cursos_tratado_2015,
#   dados_cursos_tratado_2016,
#   dados_cursos_tratado_2017,
#   dados_cursos_tratado_2018,
#   dados_cursos_tratado_2019,
#   dados_cursos_tratado_2020,
#   dados_cursos_tratado_2021,
#   dados_cursos_tratado_2022,
#   dados_cursos_tratado_2023
# )

# ## Removendo bases que não serão mais utilizadas
# rm(
#   dados_cursos_tratado_2011,
#   dados_cursos_tratado_2012,
#   dados_cursos_tratado_2013,
#   dados_cursos_tratado_2014,
#   dados_cursos_tratado_2015,
#   dados_cursos_tratado_2016,
#   dados_cursos_tratado_2017,
#   dados_cursos_tratado_2018,
#   dados_cursos_tratado_2019,
#   dados_cursos_tratado_2020,
#   dados_cursos_tratado_2021,
#   dados_cursos_tratado_2022,
#   dados_cursos_tratado_2023
# )

# # Tratamento de dados

# ## Juntando informações sobre as universidades e os cursos ofertantes
# all_data <- dados_cursos_tratado |> 
#   dplyr::left_join(dados_ies_tratado, by = dplyr::join_by("id_ies")) |> 
#   dplyr::filter(numero_cursos > 0, !is.na(nome_ies)) |> 
#   dplyr::mutate_at(dplyr::vars(nome_curso, nome_ies), ~ toupper(.)) |>
#   dplyr::mutate_at(dplyr::vars(concluintes, ingressantes), ~ as.integer(.)) |>
#   dplyr::mutate(
#     tipo_rede = dplyr::case_when(
#       tipo_rede == "1" ~ "Pública",
#       tipo_rede == "2" ~ "Privada",
#       TRUE ~ "Outro"),
#     cat_adm = dplyr::case_when(
#       cat_adm == "1" ~ "Federal",
#       cat_adm == "2" ~ "Estadual",
#       TRUE ~ "Outro"),
#     modalidade_ensino = dplyr::case_when(
#       modalidade_ensino == "1" ~ "Presencial",
#       modalidade_ensino == "2" ~ "EAD",
#       TRUE ~ "Outro")
#   )

# # TODO
# '
# Agora que temos o ano de ingresso e ano de conclusão, calcular métricas e valores.
# Separar alguns cursos para análise. 

# Sugestão: 
#   * Engenharias: 5 Anos;
#   * Medicina: 6 Anos;
#   * Direito: 5 Anos;
#   * Administração: 4 Anos;

# Calcular a porcentagem de concluíntes em cima dos ingressantes para estes cursos.

# Fórmula adotada para evasão = 1 - (concluintes_{ano} / ingressantes_{ano - <duração do curso>})
# '

# ingress <- all_data |> 
#   dplyr::select(nome_curso, modalidade_ensino, ingressantes, ano, concluintes, tipo_rede) |> 
#   dplyr::group_by(
#     nome_curso, modalidade_ensino, ano, tipo_rede
#   ) |> 
#   dplyr::summarise(
#     ingressantes = sum(ingressantes),
#     concluintes = sum(concluintes)
#   ) |>
#   dplyr::ungroup() |> 
#   tidyr::pivot_wider(
#     names_from = ano,
#     values_from = c(ingressantes, concluintes),
#     names_glue = "{.value}_{ano}"
#   ) |> 
#   dplyr::filter(nome_curso %in% c("ENGENHARIA CIVIL", "MEDICINA", "DIREITO", "ADMINISTRAÇÃO"))


# # Taxa de conclusão por curso
# ## Fórmula adotada para evasão = 1 - (concluintes_{ano} / ingressantes_{ano - <duração do curso>})

# ### Engenharia Civil: 5 Anos ----
# eng_civil <- ingress |> 
#   dplyr::filter(
#     nome_curso == "ENGENHARIA CIVIL"
#   ) |> 
#   dplyr::mutate(
#     taxa_evasao_2023 = 1 - (concluintes_2023 / ingressantes_2018),
#     taxa_evasao_2022 = 1 - (concluintes_2022 / ingressantes_2017),
#     taxa_evasao_2021 = 1 - (concluintes_2021 / ingressantes_2016),
#     taxa_evasao_2020 = 1 - (concluintes_2020 / ingressantes_2015),
#     taxa_evasao_2019 = 1 - (concluintes_2019 / ingressantes_2014),
#     taxa_evasao_2018 = 1 - (concluintes_2018 / ingressantes_2013),
#     taxa_evasao_2017 = 1 - (concluintes_2017 / ingressantes_2012),
#     taxa_evasao_2016 = 1 - (concluintes_2016 / ingressantes_2011)
#   ) |> 
#   dplyr::select(
#     nome_curso, modalidade_ensino, tipo_rede, 
#     concluintes_2023, ingressantes_2018, taxa_evasao_2023, 
#     concluintes_2022, ingressantes_2017, taxa_evasao_2022,
#     concluintes_2021, ingressantes_2016, taxa_evasao_2021,
#     concluintes_2020, ingressantes_2015, taxa_evasao_2020,
#     concluintes_2019, ingressantes_2014, taxa_evasao_2019,
#     concluintes_2018, ingressantes_2013, taxa_evasao_2018,
#     concluintes_2017, ingressantes_2012, taxa_evasao_2017,
#     concluintes_2016, ingressantes_2011, taxa_evasao_2016
#   )

# #### Gráfico
# eng_civil <- eng_civil |> 
#   dplyr::select(
#     nome_curso, modalidade_ensino, tipo_rede, 
#     taxa_evasao_2016, taxa_evasao_2017, taxa_evasao_2018, 
#     taxa_evasao_2019, taxa_evasao_2020, taxa_evasao_2021, 
#     taxa_evasao_2022, taxa_evasao_2023
#   ) |>
#   tidyr::pivot_longer(
#     cols = starts_with("taxa_evasao_"),
#     names_to = "ano",
#     values_to = "taxa_evasao"
#   ) |> 
#   dplyr::mutate(
#     ano = stringr::str_extract(ano, "\\d{4}")
#   )

# plot_ly(eng_civil, x = ~ ano, y = ~ taxa_evasao,
#         type = 'scatter', mode = 'lines+markers', 
#         color = ~ tipo_rede,
#         colors = palette,
#         marker = list(size = 8),
#         line = list(width = 2)) %>%
#   layout(title = "Taxa de Evasão ao longo dos anos - Curso de Engenharia Civil",
#          xaxis = list(title = "Ano de Ingresso"),
#          yaxis = list(title = "Taxa de Evasão", tickformat = ".0%"),
#          legend = list(title = list(text = "Modalidade de Ensino")),
#          hovermode = "x unified")

# ### Direito: 5 Anos ----
# direito <- ingress |> 
#   dplyr::filter(
#     nome_curso == "DIREITO"
#   ) |> 
#   dplyr::mutate(
#     taxa_evasao_2023 = 1 - (concluintes_2023 / ingressantes_2018),
#     taxa_evasao_2022 = 1 - (concluintes_2022 / ingressantes_2017),
#     taxa_evasao_2021 = 1 - (concluintes_2021 / ingressantes_2016),
#     taxa_evasao_2020 = 1 - (concluintes_2020 / ingressantes_2015),
#     taxa_evasao_2019 = 1 - (concluintes_2019 / ingressantes_2014),
#     taxa_evasao_2018 = 1 - (concluintes_2018 / ingressantes_2013),
#     taxa_evasao_2017 = 1 - (concluintes_2017 / ingressantes_2012),
#     taxa_evasao_2016 = 1 - (concluintes_2016 / ingressantes_2011)
#   ) |> 
#   dplyr::select(
#     nome_curso, modalidade_ensino, tipo_rede, 
#     concluintes_2023, ingressantes_2018, taxa_evasao_2023, 
#     concluintes_2022, ingressantes_2017, taxa_evasao_2022,
#     concluintes_2021, ingressantes_2016, taxa_evasao_2021,
#     concluintes_2020, ingressantes_2015, taxa_evasao_2020,
#     concluintes_2019, ingressantes_2014, taxa_evasao_2019,
#     concluintes_2018, ingressantes_2013, taxa_evasao_2018,
#     concluintes_2017, ingressantes_2012, taxa_evasao_2017,
#     concluintes_2016, ingressantes_2011, taxa_evasao_2016
#   )

# #### Gráfico
# direito <- direito |> 
#   dplyr::select(
#     nome_curso, modalidade_ensino, tipo_rede, 
#     taxa_evasao_2016, taxa_evasao_2017, taxa_evasao_2018, 
#     taxa_evasao_2019, taxa_evasao_2020, taxa_evasao_2021, 
#     taxa_evasao_2022, taxa_evasao_2023
#   ) |>
#   tidyr::pivot_longer(
#     cols = starts_with("taxa_evasao_"),
#     names_to = "ano",
#     values_to = "taxa_evasao"
#   ) |> 
#   dplyr::mutate(
#     ano = stringr::str_extract(ano, "\\d{4}")
#   )

# plot_ly(direito, x = ~ ano, y = ~ taxa_evasao,
#         type = 'scatter', mode = 'lines+markers', 
#         color = ~ tipo_rede,
#         colors = palette,
#         marker = list(size = 8),
#         line = list(width = 2)) %>%
#   layout(title = "Taxa de Evasão ao longo dos anos - Curso de Direito",
#          xaxis = list(title = "Ano de Ingresso"),
#          yaxis = list(title = "Taxa de Evasão", tickformat = ".0%"),
#          legend = list(title = list(text = "Modalidade de Ensino")),
#          hovermode = "x unified")

# ### Medicina: 6 Anos ----
# medicina <- ingress |> 
#   dplyr::filter(
#     nome_curso == "MEDICINA"
#   ) |> 
#   dplyr::mutate(
#     taxa_evasao_2023 = 1 - (concluintes_2023 / ingressantes_2017),
#     taxa_evasao_2022 = 1 - (concluintes_2022 / ingressantes_2016),
#     taxa_evasao_2021 = 1 - (concluintes_2021 / ingressantes_2015),
#     taxa_evasao_2020 = 1 - (concluintes_2020 / ingressantes_2014),
#     taxa_evasao_2019 = 1 - (concluintes_2019 / ingressantes_2013),
#     taxa_evasao_2018 = 1 - (concluintes_2018 / ingressantes_2012),
#     taxa_evasao_2017 = 1 - (concluintes_2017 / ingressantes_2011),
#   ) |> 
#   dplyr::select(
#     nome_curso, modalidade_ensino, tipo_rede, 
#     concluintes_2023, ingressantes_2017, taxa_evasao_2023, 
#     concluintes_2022, ingressantes_2016, taxa_evasao_2022,
#     concluintes_2021, ingressantes_2015, taxa_evasao_2021,
#     concluintes_2020, ingressantes_2014, taxa_evasao_2020,
#     concluintes_2019, ingressantes_2013, taxa_evasao_2019,
#     concluintes_2018, ingressantes_2012, taxa_evasao_2018,
#     concluintes_2017, ingressantes_2011, taxa_evasao_2017,
#   )

# #### Gráfico
# medicina <- medicina |> 
#   dplyr::select(
#     nome_curso, modalidade_ensino, tipo_rede, 
#     taxa_evasao_2017, taxa_evasao_2018, 
#     taxa_evasao_2019, taxa_evasao_2020, taxa_evasao_2021, 
#     taxa_evasao_2022, taxa_evasao_2023
#   ) |>
#   tidyr::pivot_longer(
#     cols = starts_with("taxa_evasao_"),
#     names_to = "ano",
#     values_to = "taxa_evasao"
#   ) |> 
#   dplyr::mutate(
#     ano = stringr::str_extract(ano, "\\d{4}")
#   )

# plot_ly(medicina, x = ~ ano, y = ~ taxa_evasao,
#         type = 'scatter', mode = 'lines+markers', 
#         color = ~ tipo_rede,
#         colors = palette,
#         marker = list(size = 8),
#         line = list(width = 2)) %>%
#   layout(title = "Taxa de Evasão ao longo dos anos - Curso de Medicina",
#          xaxis = list(title = "Ano de Ingresso"),
#          yaxis = list(title = "Taxa de Evasão", tickformat = ".0%"),
#          legend = list(title = list(text = "Modalidade de Ensino")),
#          hovermode = "x unified")

# ### Administração: 4 Anos ----
# administracao <- ingress |> 
#   dplyr::filter(
#     nome_curso == "ADMINISTRAÇÃO"
#   ) |> 
#   dplyr::mutate(
#     taxa_evasao_2023 = 1 - (concluintes_2023 / ingressantes_2019),
#     taxa_evasao_2022 = 1 - (concluintes_2022 / ingressantes_2018),
#     taxa_evasao_2021 = 1 - (concluintes_2021 / ingressantes_2017),
#     taxa_evasao_2020 = 1 - (concluintes_2020 / ingressantes_2016),
#     taxa_evasao_2019 = 1 - (concluintes_2019 / ingressantes_2015),
#     taxa_evasao_2018 = 1 - (concluintes_2018 / ingressantes_2014),
#     taxa_evasao_2017 = 1 - (concluintes_2017 / ingressantes_2013),
#     taxa_evasao_2016 = 1 - (concluintes_2016 / ingressantes_2012),
#     taxa_evasao_2015 = 1 - (concluintes_2015 / ingressantes_2011)
#   ) |> 
#   dplyr::select(
#     nome_curso, modalidade_ensino, tipo_rede, 
#     concluintes_2023, ingressantes_2019, taxa_evasao_2023, 
#     concluintes_2022, ingressantes_2018, taxa_evasao_2022,
#     concluintes_2021, ingressantes_2017, taxa_evasao_2021,
#     concluintes_2020, ingressantes_2016, taxa_evasao_2020,
#     concluintes_2019, ingressantes_2015, taxa_evasao_2019,
#     concluintes_2018, ingressantes_2014, taxa_evasao_2018,
#     concluintes_2017, ingressantes_2013, taxa_evasao_2017,
#     concluintes_2016, ingressantes_2012, taxa_evasao_2016,
#     concluintes_2015, ingressantes_2011, taxa_evasao_2015
#   )

# #### Gráfico
# administracao <- administracao |> 
#   dplyr::select(
#     nome_curso, modalidade_ensino, tipo_rede, 
#     taxa_evasao_2016, taxa_evasao_2017, taxa_evasao_2018, 
#     taxa_evasao_2019, taxa_evasao_2020, taxa_evasao_2021, 
#     taxa_evasao_2022, taxa_evasao_2023
#   ) |>
#   tidyr::pivot_longer(
#     cols = starts_with("taxa_evasao_"),
#     names_to = "ano",
#     values_to = "taxa_evasao"
#   ) |> 
#   dplyr::mutate(
#     ano = stringr::str_extract(ano, "\\d{4}")
#   )

# plot_ly(administracao, x = ~ ano, y = ~ taxa_evasao,
#         type = 'scatter', mode = 'lines+markers', 
#         color = ~ tipo_rede,
#         colors = palette,
#         marker = list(size = 8),
#         line = list(width = 2)) %>%
#   layout(title = "Taxa de Evasão ao longo dos anos - Curso de Administração",
#          xaxis = list(title = "Ano de Ingresso"),
#          yaxis = list(title = "Taxa de Evasão", tickformat = ".0%"),
#          legend = list(title = list(text = "Modalidade de Ensino")),
#          hovermode = "x unified")

# # Export de dados ----

# ## Ingressantes
# write.csv(ingress, file = "informacao/dados/processado/final_ingressantes.csv", row.names = FALSE)

# ## Cursos
# write.csv(eng_civil, file = "informacao/dados/processado/final_eng_civil.csv", row.names = FALSE)
# write.csv(direito, file = "informacao/dados/processado/final_direito.csv", row.names = FALSE)
# write.csv(medicina, file = "informacao/dados/processado/final_medicina.csv", row.names = FALSE)
# write.csv(administracao, file = "informacao/dados/processado/final_administracao.csv", row.names = FALSE)

# Comandos para instalar as bibliotecas (se ainda não instaladas)
# install.packages(c("tidyr", "dplyr", "plotly", "stringr"))

# Carregando bibliotecas necessárias para o funcionamento do script
>>>>>>> testing_and_validation
library(tidyr)
library(dplyr)
library(plotly)
library(stringr)

palette <- c("green", "blue")

<<<<<<< HEAD
# Processando as bases de dados

## Dados de ingressantes e concluíntes em universidades ao longo dos anos
dados_cursos_tratado_2011  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2017.csv') |> dplyr::mutate(ano = 2011)
dados_cursos_tratado_2012  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2017.csv') |> dplyr::mutate(ano = 2012)
dados_cursos_tratado_2013  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2017.csv') |> dplyr::mutate(ano = 2013)
dados_cursos_tratado_2014  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2017.csv') |> dplyr::mutate(ano = 2014)
dados_cursos_tratado_2015  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2017.csv') |> dplyr::mutate(ano = 2015)
dados_cursos_tratado_2016  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2017.csv') |> dplyr::mutate(ano = 2016)
dados_cursos_tratado_2017  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2017.csv') |> dplyr::mutate(ano = 2017)
dados_cursos_tratado_2018  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2018.csv') |> dplyr::mutate(ano = 2018)
dados_cursos_tratado_2019  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2019.csv') |> dplyr::mutate(ano = 2019)
dados_cursos_tratado_2020  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2020.csv') |> dplyr::mutate(ano = 2020)
dados_cursos_tratado_2021  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2021.csv') |> dplyr::mutate(ano = 2021)
dados_cursos_tratado_2022  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2022.csv') |> dplyr::mutate(ano = 2022)
dados_cursos_tratado_2023  <- read.csv2(file = 'informacao/dados/processado/dados_cursos_tratado_2023.csv') |> dplyr::mutate(ano = 2023)

## Dados de universidades de modo geral
dados_ies_tratado     <- read.csv2(file = 'informacao/dados/processado/dados_ies_tratado_2023.csv')


## Unindo os dados de cursos e universidades
dados_cursos_tratado <- rbind(
  dados_cursos_tratado_2011,
  dados_cursos_tratado_2012,
  dados_cursos_tratado_2013,
  dados_cursos_tratado_2014,
  dados_cursos_tratado_2015,
  dados_cursos_tratado_2016,
  dados_cursos_tratado_2017,
  dados_cursos_tratado_2018,
  dados_cursos_tratado_2019,
  dados_cursos_tratado_2020,
  dados_cursos_tratado_2021,
  dados_cursos_tratado_2022,
  dados_cursos_tratado_2023
)

## Removendo bases que não serão mais utilizadas
rm(
  dados_cursos_tratado_2011,
  dados_cursos_tratado_2012,
  dados_cursos_tratado_2013,
  dados_cursos_tratado_2014,
  dados_cursos_tratado_2015,
  dados_cursos_tratado_2016,
  dados_cursos_tratado_2017,
  dados_cursos_tratado_2018,
  dados_cursos_tratado_2019,
  dados_cursos_tratado_2020,
  dados_cursos_tratado_2021,
  dados_cursos_tratado_2022,
  dados_cursos_tratado_2023
)

# Tratamento de dados

## Juntando informações sobre as universidades e os cursos ofertantes
all_data <- dados_cursos_tratado |> 
  dplyr::left_join(dados_ies_tratado, by = dplyr::join_by("id_ies")) |> 
  dplyr::filter(numero_cursos > 0, !is.na(nome_ies)) |> 
  dplyr::mutate_at(dplyr::vars(nome_curso, nome_ies), ~ toupper(.)) |>
  dplyr::mutate_at(dplyr::vars(concluintes, ingressantes), ~ as.integer(.)) |>
  dplyr::mutate(
    tipo_rede = dplyr::case_when(
      tipo_rede == "1" ~ "Pública",
      tipo_rede == "2" ~ "Privada",
      TRUE ~ "Outro"),
    cat_adm = dplyr::case_when(
      cat_adm == "1" ~ "Federal",
      cat_adm == "2" ~ "Estadual",
      TRUE ~ "Outro"),
    modalidade_ensino = dplyr::case_when(
      modalidade_ensino == "1" ~ "Presencial",
      modalidade_ensino == "2" ~ "EAD",
      TRUE ~ "Outro")
  )

# TODO
'
Agora que temos o ano de ingresso e ano de conclusão, calcular métricas e valores.
Separar alguns cursos para análise. 

Sugestão: 
  * Engenharias: 5 Anos;
  * Medicina: 6 Anos;
  * Direito: 5 Anos;
  * Administração: 4 Anos;

Calcular a porcentagem de concluíntes em cima dos ingressantes para estes cursos.

Fórmula adotada para evasão = 1 - (concluintes_{ano} / ingressantes_{ano - <duração do curso>})
'

ingress <- all_data |> 
  dplyr::select(nome_curso, modalidade_ensino, ingressantes, ano, concluintes, tipo_rede) |> 
  dplyr::group_by(
    nome_curso, modalidade_ensino, ano, tipo_rede
  ) |> 
  dplyr::summarise(
    ingressantes = sum(ingressantes),
    concluintes = sum(concluintes)
  ) |>
  dplyr::ungroup() |> 
  tidyr::pivot_wider(
    names_from = ano,
    values_from = c(ingressantes, concluintes),
    names_glue = "{.value}_{ano}"
  ) |> 
  dplyr::filter(nome_curso %in% c("ENGENHARIA CIVIL", "MEDICINA", "DIREITO", "ADMINISTRAÇÃO"))


# Taxa de conclusão por curso
## Fórmula adotada para evasão = 1 - (concluintes_{ano} / ingressantes_{ano - <duração do curso>})

### Engenharia Civil: 5 Anos ----
eng_civil <- ingress |> 
  dplyr::filter(
    nome_curso == "ENGENHARIA CIVIL"
  ) |> 
  dplyr::mutate(
=======
# =============================================================================
# Leitura dos dados de cursos para os anos de 2009 a 2023
# =============================================================================
anos <- 2009:2023

lista_cursos <- lapply(anos, function(ano) {
  caminho <- paste0("dados/processado/dados_cursos_tratado_", ano, ".csv")
  df <- read.csv2(file = caminho, stringsAsFactors = FALSE)
  
  # Lista de colunas que devem ser numéricas (adicionamos "inscritos_totais")
  numeric_cols <- c("numero_cursos", "vagas_totais", "ingressantes", "concluintes", "inscritos_totais")
  
  # Se as colunas existirem, converter para numérico
  for(col in numeric_cols) {
    if(col %in% names(df)) {
      # Converter utilizando as.character para evitar problemas com fatores ou strings
      df[[col]] <- as.numeric(as.character(df[[col]]))
    }
  }
  
  df <- df %>% mutate(ano = ano)
  return(df)
})

dados_cursos_tratado <- bind_rows(lista_cursos)

# =============================================================================
# Leitura dos dados de universidades (IES) – Mantendo a base de 2023
# =============================================================================
dados_ies_tratado <- read.csv2(file = "informacao/dados/processado/dados_ies_tratado_2023.csv", 
                               stringsAsFactors = FALSE)

# =============================================================================
# Unindo os dados de cursos e universidades
# =============================================================================
all_data <- dados_cursos_tratado %>% 
  left_join(dados_ies_tratado, by = "id_ies") %>% 
  filter(numero_cursos > 0, !is.na(nome_ies)) %>% 
  mutate_at(vars(nome_curso, nome_ies), ~ toupper(.)) %>%
  mutate_at(vars(concluintes, ingressantes, inscritos_totais, vagas_totais), ~ as.integer(.)) %>%
  mutate(
    tipo_rede = case_when(
      tipo_rede == "1" ~ "Pública",
      tipo_rede == "2" ~ "Privada",
      TRUE ~ "Outro"
    ),
    cat_adm = case_when(
      cat_adm == "1" ~ "Federal",
      cat_adm == "2" ~ "Estadual",
      TRUE ~ "Outro"
    ),
    modalidade_ensino = case_when(
      modalidade_ensino == "1" ~ "Presencial",
      modalidade_ensino == "2" ~ "EAD",
      TRUE ~ "Outro"
    )
  )

# =============================================================================
# TODO - Cálculo das métricas de evasão
#
# Agora que temos os anos de ingresso e de conclusão, iremos calcular a taxa de evasão 
# para os cursos:
#   * Engenharias (Ex.: Engenharia Civil): 5 anos;
#   * Medicina: 6 anos;
#   * Direito: 5 anos;
#   * Administração: 4 anos.
#
# A fórmula adotada é:
#   taxa_evasao = 1 - (concluintes_{ano} / ingressantes_{ano - <duração do curso>})
# =============================================================================

ingress <- all_data %>% 
  select(nome_curso, modalidade_ensino, ingressantes, ano, concluintes, tipo_rede) %>% 
  group_by(
    nome_curso, modalidade_ensino, ano, tipo_rede
  ) %>% 
  summarise(
    ingressantes = sum(ingressantes, na.rm = TRUE),
    concluintes  = sum(concluintes, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  ungroup() %>% 
  pivot_wider(
    names_from = ano,
    values_from = c(ingressantes, concluintes),
    names_glue = "{.value}_{ano}"
  ) %>% 
  filter(nome_curso %in% c("ENGENHARIA CIVIL", "MEDICINA", "DIREITO", "ADMINISTRAÇÃO"))

# --- Engenharia Civil: 5 Anos ---
eng_civil <- ingress %>% 
  filter(nome_curso == "ENGENHARIA CIVIL") %>% 
  mutate(
>>>>>>> testing_and_validation
    taxa_evasao_2023 = 1 - (concluintes_2023 / ingressantes_2018),
    taxa_evasao_2022 = 1 - (concluintes_2022 / ingressantes_2017),
    taxa_evasao_2021 = 1 - (concluintes_2021 / ingressantes_2016),
    taxa_evasao_2020 = 1 - (concluintes_2020 / ingressantes_2015),
    taxa_evasao_2019 = 1 - (concluintes_2019 / ingressantes_2014),
    taxa_evasao_2018 = 1 - (concluintes_2018 / ingressantes_2013),
    taxa_evasao_2017 = 1 - (concluintes_2017 / ingressantes_2012),
    taxa_evasao_2016 = 1 - (concluintes_2016 / ingressantes_2011)
<<<<<<< HEAD
  ) |> 
  dplyr::select(
=======
  ) %>% 
  select(
>>>>>>> testing_and_validation
    nome_curso, modalidade_ensino, tipo_rede, 
    concluintes_2023, ingressantes_2018, taxa_evasao_2023, 
    concluintes_2022, ingressantes_2017, taxa_evasao_2022,
    concluintes_2021, ingressantes_2016, taxa_evasao_2021,
    concluintes_2020, ingressantes_2015, taxa_evasao_2020,
    concluintes_2019, ingressantes_2014, taxa_evasao_2019,
    concluintes_2018, ingressantes_2013, taxa_evasao_2018,
    concluintes_2017, ingressantes_2012, taxa_evasao_2017,
    concluintes_2016, ingressantes_2011, taxa_evasao_2016
  )

<<<<<<< HEAD
#### Gráfico
eng_civil <- eng_civil |> 
  dplyr::select(
    nome_curso, modalidade_ensino, tipo_rede, 
    taxa_evasao_2016, taxa_evasao_2017, taxa_evasao_2018, 
    taxa_evasao_2019, taxa_evasao_2020, taxa_evasao_2021, 
    taxa_evasao_2022, taxa_evasao_2023
  ) |>
  tidyr::pivot_longer(
    cols = starts_with("taxa_evasao_"),
    names_to = "ano",
    values_to = "taxa_evasao"
  ) |> 
  dplyr::mutate(
    ano = stringr::str_extract(ano, "\\d{4}")
  )

plot_ly(eng_civil, x = ~ ano, y = ~ taxa_evasao,
        type = 'scatter', mode = 'lines+markers', 
        color = ~ tipo_rede,
=======
eng_civil_long <- eng_civil %>% 
  select(nome_curso, modalidade_ensino, tipo_rede, starts_with("taxa_evasao_")) %>%
  pivot_longer(
    cols = starts_with("taxa_evasao_"),
    names_to = "ano",
    values_to = "taxa_evasao"
  ) %>% 
  mutate(ano = str_extract(ano, "\\d{4}"))

plot_ly(eng_civil_long, x = ~ano, y = ~taxa_evasao,
        type = 'scatter', mode = 'lines+markers', 
        color = ~tipo_rede,
>>>>>>> testing_and_validation
        colors = palette,
        marker = list(size = 8),
        line = list(width = 2)) %>%
  layout(title = "Taxa de Evasão ao longo dos anos - Curso de Engenharia Civil",
         xaxis = list(title = "Ano de Ingresso"),
         yaxis = list(title = "Taxa de Evasão", tickformat = ".0%"),
         legend = list(title = list(text = "Modalidade de Ensino")),
         hovermode = "x unified")

<<<<<<< HEAD
### Direito: 5 Anos ----
direito <- ingress |> 
  dplyr::filter(
    nome_curso == "DIREITO"
  ) |> 
  dplyr::mutate(
=======
# --- Direito: 5 Anos ---
direito <- ingress %>% 
  filter(nome_curso == "DIREITO") %>% 
  mutate(
>>>>>>> testing_and_validation
    taxa_evasao_2023 = 1 - (concluintes_2023 / ingressantes_2018),
    taxa_evasao_2022 = 1 - (concluintes_2022 / ingressantes_2017),
    taxa_evasao_2021 = 1 - (concluintes_2021 / ingressantes_2016),
    taxa_evasao_2020 = 1 - (concluintes_2020 / ingressantes_2015),
    taxa_evasao_2019 = 1 - (concluintes_2019 / ingressantes_2014),
    taxa_evasao_2018 = 1 - (concluintes_2018 / ingressantes_2013),
    taxa_evasao_2017 = 1 - (concluintes_2017 / ingressantes_2012),
    taxa_evasao_2016 = 1 - (concluintes_2016 / ingressantes_2011)
<<<<<<< HEAD
  ) |> 
  dplyr::select(
=======
  ) %>% 
  select(
>>>>>>> testing_and_validation
    nome_curso, modalidade_ensino, tipo_rede, 
    concluintes_2023, ingressantes_2018, taxa_evasao_2023, 
    concluintes_2022, ingressantes_2017, taxa_evasao_2022,
    concluintes_2021, ingressantes_2016, taxa_evasao_2021,
    concluintes_2020, ingressantes_2015, taxa_evasao_2020,
    concluintes_2019, ingressantes_2014, taxa_evasao_2019,
    concluintes_2018, ingressantes_2013, taxa_evasao_2018,
    concluintes_2017, ingressantes_2012, taxa_evasao_2017,
    concluintes_2016, ingressantes_2011, taxa_evasao_2016
  )

<<<<<<< HEAD
#### Gráfico
direito <- direito |> 
  dplyr::select(
    nome_curso, modalidade_ensino, tipo_rede, 
    taxa_evasao_2016, taxa_evasao_2017, taxa_evasao_2018, 
    taxa_evasao_2019, taxa_evasao_2020, taxa_evasao_2021, 
    taxa_evasao_2022, taxa_evasao_2023
  ) |>
  tidyr::pivot_longer(
    cols = starts_with("taxa_evasao_"),
    names_to = "ano",
    values_to = "taxa_evasao"
  ) |> 
  dplyr::mutate(
    ano = stringr::str_extract(ano, "\\d{4}")
  )

plot_ly(direito, x = ~ ano, y = ~ taxa_evasao,
        type = 'scatter', mode = 'lines+markers', 
        color = ~ tipo_rede,
=======
direito_long <- direito %>% 
  select(nome_curso, modalidade_ensino, tipo_rede, starts_with("taxa_evasao_")) %>%
  pivot_longer(
    cols = starts_with("taxa_evasao_"),
    names_to = "ano",
    values_to = "taxa_evasao"
  ) %>% 
  mutate(ano = str_extract(ano, "\\d{4}"))

plot_ly(direito_long, x = ~ano, y = ~taxa_evasao,
        type = 'scatter', mode = 'lines+markers', 
        color = ~tipo_rede,
>>>>>>> testing_and_validation
        colors = palette,
        marker = list(size = 8),
        line = list(width = 2)) %>%
  layout(title = "Taxa de Evasão ao longo dos anos - Curso de Direito",
         xaxis = list(title = "Ano de Ingresso"),
         yaxis = list(title = "Taxa de Evasão", tickformat = ".0%"),
         legend = list(title = list(text = "Modalidade de Ensino")),
         hovermode = "x unified")

<<<<<<< HEAD
### Medicina: 6 Anos ----
medicina <- ingress |> 
  dplyr::filter(
    nome_curso == "MEDICINA"
  ) |> 
  dplyr::mutate(
=======
# --- Medicina: 6 Anos ---
medicina <- ingress %>% 
  filter(nome_curso == "MEDICINA") %>% 
  mutate(
>>>>>>> testing_and_validation
    taxa_evasao_2023 = 1 - (concluintes_2023 / ingressantes_2017),
    taxa_evasao_2022 = 1 - (concluintes_2022 / ingressantes_2016),
    taxa_evasao_2021 = 1 - (concluintes_2021 / ingressantes_2015),
    taxa_evasao_2020 = 1 - (concluintes_2020 / ingressantes_2014),
    taxa_evasao_2019 = 1 - (concluintes_2019 / ingressantes_2013),
    taxa_evasao_2018 = 1 - (concluintes_2018 / ingressantes_2012),
<<<<<<< HEAD
    taxa_evasao_2017 = 1 - (concluintes_2017 / ingressantes_2011),
  ) |> 
  dplyr::select(
=======
    taxa_evasao_2017 = 1 - (concluintes_2017 / ingressantes_2011)
  ) %>% 
  select(
>>>>>>> testing_and_validation
    nome_curso, modalidade_ensino, tipo_rede, 
    concluintes_2023, ingressantes_2017, taxa_evasao_2023, 
    concluintes_2022, ingressantes_2016, taxa_evasao_2022,
    concluintes_2021, ingressantes_2015, taxa_evasao_2021,
    concluintes_2020, ingressantes_2014, taxa_evasao_2020,
    concluintes_2019, ingressantes_2013, taxa_evasao_2019,
    concluintes_2018, ingressantes_2012, taxa_evasao_2018,
<<<<<<< HEAD
    concluintes_2017, ingressantes_2011, taxa_evasao_2017,
  )

#### Gráfico
medicina <- medicina |> 
  dplyr::select(
    nome_curso, modalidade_ensino, tipo_rede, 
    taxa_evasao_2017, taxa_evasao_2018, 
    taxa_evasao_2019, taxa_evasao_2020, taxa_evasao_2021, 
    taxa_evasao_2022, taxa_evasao_2023
  ) |>
  tidyr::pivot_longer(
    cols = starts_with("taxa_evasao_"),
    names_to = "ano",
    values_to = "taxa_evasao"
  ) |> 
  dplyr::mutate(
    ano = stringr::str_extract(ano, "\\d{4}")
  )

plot_ly(medicina, x = ~ ano, y = ~ taxa_evasao,
        type = 'scatter', mode = 'lines+markers', 
        color = ~ tipo_rede,
=======
    concluintes_2017, ingressantes_2011, taxa_evasao_2017
  )

medicina_long <- medicina %>% 
  select(nome_curso, modalidade_ensino, tipo_rede, starts_with("taxa_evasao_")) %>%
  pivot_longer(
    cols = starts_with("taxa_evasao_"),
    names_to = "ano",
    values_to = "taxa_evasao"
  ) %>% 
  mutate(ano = str_extract(ano, "\\d{4}"))

plot_ly(medicina_long, x = ~ano, y = ~taxa_evasao,
        type = 'scatter', mode = 'lines+markers', 
        color = ~tipo_rede,
>>>>>>> testing_and_validation
        colors = palette,
        marker = list(size = 8),
        line = list(width = 2)) %>%
  layout(title = "Taxa de Evasão ao longo dos anos - Curso de Medicina",
         xaxis = list(title = "Ano de Ingresso"),
         yaxis = list(title = "Taxa de Evasão", tickformat = ".0%"),
         legend = list(title = list(text = "Modalidade de Ensino")),
         hovermode = "x unified")

<<<<<<< HEAD
### Administração: 4 Anos ----
administracao <- ingress |> 
  dplyr::filter(
    nome_curso == "ADMINISTRAÇÃO"
  ) |> 
  dplyr::mutate(
=======
# --- Administração: 4 Anos ---
administracao <- ingress %>% 
  filter(nome_curso == "ADMINISTRAÇÃO") %>% 
  mutate(
>>>>>>> testing_and_validation
    taxa_evasao_2023 = 1 - (concluintes_2023 / ingressantes_2019),
    taxa_evasao_2022 = 1 - (concluintes_2022 / ingressantes_2018),
    taxa_evasao_2021 = 1 - (concluintes_2021 / ingressantes_2017),
    taxa_evasao_2020 = 1 - (concluintes_2020 / ingressantes_2016),
    taxa_evasao_2019 = 1 - (concluintes_2019 / ingressantes_2015),
    taxa_evasao_2018 = 1 - (concluintes_2018 / ingressantes_2014),
    taxa_evasao_2017 = 1 - (concluintes_2017 / ingressantes_2013),
    taxa_evasao_2016 = 1 - (concluintes_2016 / ingressantes_2012),
    taxa_evasao_2015 = 1 - (concluintes_2015 / ingressantes_2011)
<<<<<<< HEAD
  ) |> 
  dplyr::select(
=======
  ) %>% 
  select(
>>>>>>> testing_and_validation
    nome_curso, modalidade_ensino, tipo_rede, 
    concluintes_2023, ingressantes_2019, taxa_evasao_2023, 
    concluintes_2022, ingressantes_2018, taxa_evasao_2022,
    concluintes_2021, ingressantes_2017, taxa_evasao_2021,
    concluintes_2020, ingressantes_2016, taxa_evasao_2020,
    concluintes_2019, ingressantes_2015, taxa_evasao_2019,
    concluintes_2018, ingressantes_2014, taxa_evasao_2018,
    concluintes_2017, ingressantes_2013, taxa_evasao_2017,
    concluintes_2016, ingressantes_2012, taxa_evasao_2016,
    concluintes_2015, ingressantes_2011, taxa_evasao_2015
  )

<<<<<<< HEAD
#### Gráfico
administracao <- administracao |> 
  dplyr::select(
    nome_curso, modalidade_ensino, tipo_rede, 
    taxa_evasao_2016, taxa_evasao_2017, taxa_evasao_2018, 
    taxa_evasao_2019, taxa_evasao_2020, taxa_evasao_2021, 
    taxa_evasao_2022, taxa_evasao_2023
  ) |>
  tidyr::pivot_longer(
    cols = starts_with("taxa_evasao_"),
    names_to = "ano",
    values_to = "taxa_evasao"
  ) |> 
  dplyr::mutate(
    ano = stringr::str_extract(ano, "\\d{4}")
  )

plot_ly(administracao, x = ~ ano, y = ~ taxa_evasao,
        type = 'scatter', mode = 'lines+markers', 
        color = ~ tipo_rede,
=======
administracao_long <- administracao %>% 
  select(nome_curso, modalidade_ensino, tipo_rede, starts_with("taxa_evasao_")) %>%
  pivot_longer(
    cols = starts_with("taxa_evasao_"),
    names_to = "ano",
    values_to = "taxa_evasao"
  ) %>% 
  mutate(ano = str_extract(ano, "\\d{4}"))

plot_ly(administracao_long, x = ~ano, y = ~taxa_evasao,
        type = 'scatter', mode = 'lines+markers', 
        color = ~tipo_rede,
>>>>>>> testing_and_validation
        colors = palette,
        marker = list(size = 8),
        line = list(width = 2)) %>%
  layout(title = "Taxa de Evasão ao longo dos anos - Curso de Administração",
         xaxis = list(title = "Ano de Ingresso"),
         yaxis = list(title = "Taxa de Evasão", tickformat = ".0%"),
         legend = list(title = list(text = "Modalidade de Ensino")),
         hovermode = "x unified")

<<<<<<< HEAD
# Export de dados ----
=======
# =============================================================================
# Exportação dos dados processados
# =============================================================================
>>>>>>> testing_and_validation

## Ingressantes
write.csv(ingress, file = "informacao/dados/processado/final_ingressantes.csv", row.names = FALSE)

<<<<<<< HEAD
## Cursos
write.csv(eng_civil, file = "informacao/dados/processado/final_eng_civil.csv", row.names = FALSE)
write.csv(direito, file = "informacao/dados/processado/final_direito.csv", row.names = FALSE)
write.csv(medicina, file = "informacao/dados/processado/final_medicina.csv", row.names = FALSE)
write.csv(administracao, file = "informacao/dados/processado/final_administracao.csv", row.names = FALSE)

=======
## Exportação dos dados de cada curso (usados para os gráficos)
write.csv(eng_civil, file = "informacao/dados/processado/final_eng_civil.csv", row.names = FALSE)
write.csv(direito, file = "informacao/dados/processado/final_direito.csv", row.names = FALSE)
write.csv(medicina, file = "informacao/dados/processado/final_medicina.csv", row.names = FALSE)
write.csv(administracao, file = "informacao/dados/processado/final_administracao.csv", row.names = FALSE)
>>>>>>> testing_and_validation
