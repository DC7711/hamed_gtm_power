📄 README.md — Google Sheets - Lato Client
markdown
Copia
Modifica
# 📊 Google Sheets - Lato Client (GTM Template)

Questo tag personalizzato per **Google Tag Manager** permette di **inviare dati lato client a un Google Sheets** tramite uno script Apps Script distribuito come `web app`.

---

## 🔍 Descrizione del template

### 📌 Cosa fa questo tag?

Invia dinamicamente dati da GTM a un Google Sheets utilizzando un'URL personalizzata costruita da:
- ID del foglio (`spreadsheetId`)
- Nome del foglio (`sheetName`)
- ID del deployment di Google Apps Script

Il tag raccoglie coppie `campo: valore` da una tabella configurabile e li invia al Google Sheet tramite `sendPixel()` (compatibile con la sandbox GTM).

### 🧠 Quando e perché usarlo?

- Per **tracciare eventi o lead** senza usare un backend
- Per **salvare dati personalizzati** da moduli, click o eventi
- Quando vuoi inviare dati direttamente a Google Sheets **senza server**

---

## ⚙️ Istruzioni per l’uso

### 1. Importa il template in GTM
- Vai su **Templates > Nuovo > Importa**
- Carica il file `template.tpl`

### 2. Crea uno script Apps Script su Google
1. Vai su [Google Apps Script](https://script.google.com/)
2. Crea uno script vuoto e incolla questo codice:

```javascript
function doGet(e) {
  const ss = SpreadsheetApp.openById(e.parameter.spreadsheetId);
  const sheet = ss.getSheetByName(e.parameter.sheet || "Foglio1");
  const row = [];

  for (var key in e.parameter) {
    if (key !== "spreadsheetId" && key !== "sheet") {
      row.push(e.parameter[key]);
    }
  }

  sheet.appendRow(row);
  return ContentService.createTextOutput("OK");
}
Salva > Pubblica > Distribuisci come Web App

Seleziona “Chiunque, anche anonimi”

Copia l'Deployment ID

3. Crea il tag in GTM
Campo	Descrizione
spreadsheetUrl	L’URL completo del foglio (es. https://docs.google.com/spreadsheets/d/...)
deploymentId	L’ID di distribuzione dello script Apps Script
sheetName	Nome del foglio (es. LeadForm)
dataList	Una tabella con coppie nome campo e valore (es. "email" → {{Email}})

🧪 Esempio di configurazione
✅ Esempio di dataList
Noem campo	value
email	{{Form Email}}
nome	{{Form Name}}
evento	formSubmit

🔁 L’URL costruita sarà simile a:
perl
Copia
Modifica
https://script.google.com/macros/s/DEPLOYMENT_ID/exec?spreadsheetId=SPREADSHEET_ID&sheet=LeadForm&email=foo@bar.com&nome=Mario&evento=formSubmit
⚠️ Possibili errori comuni
Errore	Soluzione
❌ spreadsheetUrl non valido	Verifica che l'URL sia corretto e pubblico
❌ deploymentId non valido	Assicurati di usare l'ID di distribuzione e non lo scriptId
❌ simpleTable1 vuoto	Aggiungi almeno una coppia campo: valore nella tabella
Google Sheets non si aggiorna	Verifica che il foglio sia condiviso pubblicamente e accessibile

🧱 Requisiti tecnici
Requisito	Stato
✅ GTM Web Container	Sì
✅ Compatibile sandbox	Sì (usa sendPixel)
🌐 Browser moderni	Sì
🔐 GDPR	Nessun cookie gestito dal tag. I dati inviati devono essere legalmente trattati
⛔ Script esterni richiesti	No

🛟 Supporto
Per problemi o suggerimenti, apri una Issue su GitHub

📝 Licenza
Distribuito con licenza Apache 2.0.

yaml
Copia
Modifica

---

## 🔚 Prossimi passaggi consigliati

1. Inserisci questo contenuto in `README.md`
2. Assicurati che il file sia nella root del repository
3. Nel file `metadata.yaml`, usa il link al README:

```yaml
documentation: "https://github.com/neting/gtm-google-sheets-template#readme"
