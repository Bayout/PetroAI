#!/bin/bash

# Comando curl para obter o token de acesso
curl -X POST 'https://ims-na1.adobelogin.com/ims/token/v3' -H 'Content-Type: application/x-www-form-urlencoded' -d 'grant_type=client_credentials&client_id=08f35b1008af4a8091ccb4c55dc44c30&client_secret=p8e-KSWjsdJ139KfBDr-Jq0xVzs15iiN2bLN&scope=openid,AdobeID,DCAPI'

# Definir as variáveis de ambiente
export PDF_SERVICES_CLIENT_SECRET="p8e-KSWjsdJ139KfBDr-Jq0xVzs15iiN2bLN..."
export PDF_SERVICES_CLIENT_ID="08f35b1008af4a8091ccb4c55dc44c30"

# Executar o comando do seu aplicativo Python (substitua pelo seu comando real)
python src/extractpdf/extract_txt_from_pdf.py
