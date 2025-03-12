___TERMS_OF_SERVICE___

By creating or modifying this file you agree to Google Tag Manager's Community
Template Gallery Developer Terms of Service available at
https://developers.google.com/tag-manager/gallery-tos (or such other URL as
Google may provide), as modified from time to time.


___INFO___

{
  "type": "TAG",
  "id": "cvt_temp_public_id",
  "version": 1,
  "securityGroups": [],
  "displayName": "Google Sheets - Lato Client",
  "brand": {
    "id": "brand_dummy",
    "displayName": "Modello personalizzato"
  },
  "description": "Invia dati da GTM a Fogli di Google",
  "containerContexts": [
    "WEB"
  ]
}


___TEMPLATE_PARAMETERS___

[
  {
    "type": "TEXT",
    "name": "spreadsheetUrl",
    "displayName": "spreadsheetUrl",
    "simpleValueType": true
  },
  {
    "type": "TEXT",
    "name": "Nome del foglio",
    "displayName": "sheetName",
    "simpleValueType": true
  },
  {
    "type": "TEXT",
    "name": "deploymentId",
    "displayName": "deploymentId",
    "simpleValueType": true
  },
  {
    "type": "GROUP",
    "name": "Dati da inviare",
    "displayName": "dataList",
    "groupStyle": "ZIPPY_CLOSED",
    "subParams": [
      {
        "type": "SIMPLE_TABLE",
        "name": "simpleTable1",
        "displayName": "",
        "simpleTableColumns": [
          {
            "defaultValue": "",
            "displayName": "Noem campo",
            "name": "column1",
            "type": "TEXT"
          },
          {
            "defaultValue": "",
            "displayName": "value",
            "name": "column2",
            "type": "TEXT"
          }
        ]
      }
    ]
  }
]


___SANDBOXED_JS_FOR_WEB_TEMPLATE___

const logToConsole = require('logToConsole');
const encodeUriComponent = require('encodeUriComponent');
const sendPixel = require('sendPixel'); // Metodo compatibile con GTM sandbox

const spreadsheetUrl = data.spreadsheetUrl || ""; // URL del foglio Google
const deploymentId = data.deploymentId || ""; // Deployment ID di Apps Script
const sheetName = data.sheetName || "Foglio1"; // Nome del foglio predefinito
const isLoggingEnabled = data.enableLogging;

// **Verifica se spreadsheetUrl è valido prima di usarlo**
let spreadsheetId = "";

if (spreadsheetUrl) {
    spreadsheetId = spreadsheetUrl.replace("https://docs.google.com/spreadsheets/d/", "").split("/")[0];
} else {
    logToConsole("❌ Errore: `spreadsheetUrl` non valido.");
    data.gtmOnFailure();
}

// **Se manca lo Spreadsheet ID o il Deployment ID, logga l'errore e fallisce il tag**
if (!spreadsheetId || !deploymentId) {
    logToConsole("❌ Errore: `spreadsheetId` o `deploymentId` non validi.");
    data.gtmOnFailure();
} else {
    // **Costruisce l'URL per inviare i dati**
    const postUrl = getUrl();

    if (isLoggingEnabled) {
        logToConsole("✅ Invio dati a: " + postUrl);
    }

    // **Usa sendPixel() per inviare i dati senza problemi di sandbox**
    sendPixel(postUrl);

    data.gtmOnSuccess(); // Indica il successo del tag
}

// **Funzione per costruire l'URL con i dati**
function getUrl() {
    var columnNames = [];
    var dataList = [];

    // **Recupera i dati dalla tabella simpleTable1**
    if (data.simpleTable1 && typeof data.simpleTable1 === "object" && data.simpleTable1.length) {
        for (var i = 0; i < data.simpleTable1.length; i++) {
            columnNames.push(data.simpleTable1[i].column1); // Nome colonna
            dataList.push(data.simpleTable1[i].column2);   // Valore corrispondente
        }
    } else {
        logToConsole("❌ Errore: `simpleTable1` è vuoto o non è un array.");
    }

    var queryString = "";
    for (var j = 0; j < columnNames.length; j++) {
        queryString += encodeUriComponent(columnNames[j]) + "=" + encodeUriComponent(dataList[j] || "N/A") + "&";
    }

    return "https://script.google.com/macros/s/" + encodeUriComponent(deploymentId) +
        "/exec?spreadsheetId=" + encodeUriComponent(spreadsheetId) + 
        "&sheet=" + encodeUriComponent(sheetName) + "&" + queryString;
}


___WEB_PERMISSIONS___

[
  {
    "instance": {
      "key": {
        "publicId": "logging",
        "versionId": "1"
      },
      "param": [
        {
          "key": "environments",
          "value": {
            "type": 1,
            "string": "debug"
          }
        }
      ]
    },
    "clientAnnotations": {
      "isEditedByUser": true
    },
    "isRequired": true
  },
  {
    "instance": {
      "key": {
        "publicId": "send_pixel",
        "versionId": "1"
      },
      "param": [
        {
          "key": "allowedUrls",
          "value": {
            "type": 1,
            "string": "any"
          }
        }
      ]
    },
    "clientAnnotations": {
      "isEditedByUser": true
    },
    "isRequired": true
  }
]


___TESTS___

scenarios: []


___NOTES___

Created on 12/03/2025, 12:47:26


