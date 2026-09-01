Estudos Over e Under Gols nas principais ligas de futebol.
Base de dados: https://www.football-data.co.uk/data.php

# Estatísticas Over / Under Gols

Aplicação estática para GitHub Pages.

## Estrutura

- `index.html` ou `estatisticas_over_under.html`: aplicação
- `.github/workflows/atualizar-dados.yml`: atualização automática
- `data/football-data/`: CSVs das ligas
- `data/australia/`: arquivo da A-League

## Publicação

1. Coloque o HTML como `index.html`.
2. Coloque o workflow em `.github/workflows/atualizar-dados.yml`.
3. Faça o primeiro push.
4. Execute manualmente o workflow uma vez em **Actions > Atualizar dados das ligas > Run workflow**.
5. Ative o GitHub Pages em **Settings > Pages**, usando a branch principal e a pasta `/ (root)`.

O workflow atualiza os dados a cada 6 horas.
