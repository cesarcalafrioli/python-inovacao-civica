import requests
from zipfile import ZipFile
import pandas as pd

# Arquivo feito na aula 4.2 da semana 4

# fazendo o download do conteúdo do arquivo
url = f"http://www.camara.leg.br/cotas/Ano-2019.csv.zip"
r = requests.get(url)

# abrindo um arquivo no seu computador
file = open(f"Ano-2019.csv.zip", "wb")

# escrever o conteúdo
file.write(r.content)
file.close()

# outra forma de criar arquivos, e escrever conteúdo

# with open(f"Ano-{year}.csv.zip", "wb") as code:
#    code.write(r.content)


zip_file = ZipFile(f"Ano-2019.csv.zip", 'r')
zip_file.namelist()
zip_file.extract(member=f"Ano-2019.csv", path=f"reembolso-2019")

# caso a gente queira extrair todo o conteúdo do arquivo zip
# zip_file.extractall(path=f"reimbursements-{year}")

zip_file.close()

DTYPE = {
    "txNomeParlamentar": str,
    "ideCadastro": str,
    "nuCarteiraParlamentar": str,
    "nuLegislatura": str,
    "sgUF": str,
    "sgPartido": str,
    "codLegislatura": str,
    "numSubCota": str,
    "txtDescricao": str,
    "numEspecificacaoSubCota": str,
    "txtDescricaoEspecificacao": str,
    "txtFornecedor": str,
    "txtCNPJCPF": str,
    "txtNumero": str,
    "indTipoDocumento": str,
    "datEmissao": str,
    "vlrDocumento": float,
    "vlrGlosa": str,
    "vlrLiquido": float,
    "numMes": str,
    "numAno": str,
    "numParcela": str,
    "txtPassageiro": str,
    "txtTrecho": str,
    "numLote": str,
    "numRessarcimento": str,
    "nuDeputadoId": str,
    "ideDocumento": str,
}

# Lendo dados com pandas
print("Lendo csv reembolso...")
df_reembolso = pd.read_csv(
    "reembolso-2019/Ano-2019.csv",
    delimiter=";",
    dtype=DTYPE,
    low_memory=False
)

print("Converte to datetime...")
df_reembolso["datEmissao"] = pd.to_datetime(df_reembolso.datEmissao, format="%Y-%m-%d")


converters = {
    "0": "nota_fiscal",
    "1": "recibo",
    "2": "despesa_exterior",
    "4": None
}

df_reembolso.indTipoDocumento.replace(converters, inplace=True)

df_reembolso["txtCNPJCPF"] = df_reembolso["txtCNPJCPF"].str.replace(r"\D", "", regex=True)

DTYPE = {
    "cnpj": str,
}

df_empresas = pd.read_csv(
    "2019-11-19-companies.csv.xz",
    compression="xz",
    dtype=DTYPE,
)

df_final = df_reembolso.merge(df_empresas, how="left", left_on="txtCNPJCPF", right_on="cnpj")

df_final.to_csv("output.csv")