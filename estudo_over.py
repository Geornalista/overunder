import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import unidecode

def limpa_e_calcula(liga):
    
    liga = unidecode.unidecode(liga.lower())

    links = {
            'alemanha': "https://www.football-data.co.uk/mmz4281/2122/D1.csv",
            'espanha': "https://www.football-data.co.uk/mmz4281/2122/SP1.csv",
            'franca': "https://www.football-data.co.uk/mmz4281/2122/F1.csv",
            'inglaterra': "https://www.football-data.co.uk/mmz4281/2122/E0.csv",
            'italia': "https://www.football-data.co.uk/mmz4281/2122/I1.csv",
            'belgica': "https://www.football-data.co.uk/mmz4281/2122/B1.csv",
            'holanda': "https://www.football-data.co.uk/mmz4281/2122/N1.csv",
            'portugal': "https://www.football-data.co.uk/mmz4281/2122/P1.csv",
            'turquia': "https://www.football-data.co.uk/mmz4281/2122/T1.csv",
            'escocia': "https://www.football-data.co.uk/mmz4281/2122/SC0.csv",
            'dinamarca': "https://www.football-data.co.uk/new/DNK.csv",
            'noruega': "https://www.football-data.co.uk/new/NOR.csv",
            'suica': "https://www.football-data.co.uk/new/SWZ.csv",
            'suecia': "https://www.football-data.co.uk/new/SWE.csv",
            'brasil': "https://www.football-data.co.uk/new/BRA.csv"
    }

    liga1 = ['alemanha','espanha','franca','inglaterra','italia','belgica','holanda','portugal','turquia','escocia']
  
    df = pd.read_csv(links[liga])

    if liga in liga1:
        df.drop(['Div','Time','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','BWH','BWD','BWA','IWH','IWD',
                    'IWA','PSH','PSD','PSA','WHH','WHD','WHA','VCH','VCD','VCA','MaxH','MaxD','MaxA','AvgH','AvgD','AvgA','P>2.5',
                    'P<2.5','Max>2.5','Max<2.5','Avg>2.5','Avg<2.5','AHh','B365AHH','B365AHA','PAHH','PAHA','MaxAHH','MaxAHA','AvgAHH',
                    'AvgAHA','B365CH','B365CD','B365CA','BWCH','BWCD','BWCA','IWCH','IWCD','IWCA','PSCH','PSCD','PSCA','WHCH','WHCD',
                    'WHCA','VCCH','VCCD','VCCA','MaxCH','MaxCD','MaxCA','AvgCH','AvgCD','AvgCA','B365C>2.5','B365C<2.5','PC>2.5',
                    'PC<2.5','MaxC>2.5','MaxC<2.5','AvgC>2.5','AvgC<2.5','AHCh','B365CAHH','B365CAHA','PCAHH','PCAHA','MaxCAHH',
                    'MaxCAHA','AvgCAHH','AvgCAHA','HTHG','HTAG','HTR','B365>2.5','B365<2.5'],axis=1,inplace=True)
        
        df.rename(columns={'HomeTeam':'Home','AwayTeam':'Away','FTHG': 'HG', 'FTAG': 'AG','FTR':'Res','B365H':'PH','B365D':'PD','B365A':'PA'}, inplace=True)
    
    else:
        if liga in ['dinamarca','suica']:
            df = df.query("Season == '2021/2022'")
        else:
            df = df.query("Season == 2021")

        df.drop(['Country','League','Season','Time','MaxH','MaxD','MaxA','AvgH','AvgD','AvgA'],axis=1,inplace=True)

    df['GOLS'] = df['HG'] + df['AG']
    
    def ambas(df):
        if (df['HG'] > 0) & (df['AG'] > 0):
            return 1
        else:
            return 0
    
    df['AMBAS'] = df.apply(ambas,axis=1)

    clubes = list(df.Home.unique())

    # JOGOS OVER 2.5
    df_O25 = df.query('GOLS > 2.5')
    # JOGOS OVER 1.5
    df_O15 = df.query('GOLS > 1.5')
    # JOGOS OVER 0.5
    df_O5 = df.query('GOLS > 0.5')
    # JOGOS AMBAS MARCAM
    df_ambas = df.query('AMBAS == 1')

    tabela = []

    for clube in clubes:
        if mando == 'CASA':
            texto1 = 'Home == "'+clube+'"'
        elif mando == 'FORA':
            texto1 = 'Away == "'+clube+'"'
        else:
            texto1 = 'Home == "'+clube+'" | Away == "'+clube+'"'

        if gols == 'Over 0.5':
            dfover = df_O5
        elif gols == 'Over 1.5':
            dfover = df_O15
        elif gols == 'Over 2.5':
            dfover = df_O25
        else:
            dfover = df_ambas

        taxa = 100 * (dfover.query(texto1).shape[0] / df.query(texto1).shape[0])

        tabela.append([clube,round(taxa,2)])

    tabela = pd.DataFrame(tabela, columns=['CLUBE','TAXA'])

    return tabela

def figura(df):
    fig, ax = plt.subplots(figsize=(3,5))
    fs = 20
    ls = 8

    df = df.sort_values('TAXA',ascending=True)

    ax.barh(df.CLUBE,df.TAXA,color='darkgreen')
    ax.set_title(dropdown+' - '+gols+' - '+mando+'\n',fontsize=fs)

    ax.set_xlim([0, 100])
    ax.set_xlabel('Aproveitamento %\n')
    ax.grid(axis='x',color='k',alpha=0.3)
    ax.tick_params(axis='y', which='major', labelsize=ls)
    ax.tick_params(axis='x', which='both', labelsize=ls)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    plt.xticks(np.arange(0, 110, 10))

    st.pyplot(fig)

ligas = ["Alemanha","Espanha","França","Inglaterra","Itália","Bélgica",
            "Holanda","Portugal","Turquia","Escócia","Dinamarca","Noruega",
            "Suiça","Suécia","Brasil"]


st.sidebar.title("Projeto Over / Under")

dropdown = st.selectbox('Escolha a liga', ligas)

mando = st.sidebar.radio('Escolha um item:',['CASA','FORA','TOTAL'])
gols = st.sidebar.radio('Escolha o limite de gols:',['Over 0.5','Over 1.5','Over 2.5','Ambas Marcam'])

figura(limpa_e_calcula(dropdown))

#st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
#st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
