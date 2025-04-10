{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNyYMfr3lLMHVU09HWyB8EP",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/DC7711/hamed_gtm_power/blob/main/testn8n.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from flask import Flask, request, jsonify\n",
        "# Importiamo le librerie necessarie\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "from sklearn.model_selection import train_test_split, StratifiedKFold\n",
        "from sklearn.preprocessing import StandardScaler\n",
        "from sklearn.linear_model import LogisticRegression\n",
        "from sklearn.metrics import accuracy_score, confusion_matrix\n",
        "\n",
        "# Carichiamo i dati dai CSV\n",
        "match_data = pd.read_csv('/content/stats - match (1).csv')\n",
        "clay_data = pd.read_csv('/content/stats - clay_data.csv')\n",
        "\n",
        "# Visualizziamo i primi dati per capire la struttura\n",
        "print(match_data.head())\n",
        "print(clay_data.head())\n",
        "\n",
        "# Verifichiamo la distribuzione della colonna Winner\n",
        "print(\"Distribuzione della colonna Winner:\")\n",
        "print(match_data['Winner'].value_counts())\n",
        "\n",
        "# Uniamo il match_data e clay_data in base al giocatore\n",
        "match_data['Giocatore_1'] = match_data['Giocatore_1'].astype(int)\n",
        "match_data['Giocatore_2'] = match_data['Giocatore_2'].astype(int)\n",
        "\n",
        "# Modifica della colonna 'Winner' per fare la variabile target binaria\n",
        "match_data['Winner_binary'] = (match_data['Winner'] == 1).astype(int)  # 1 per Giocatore_1 vince, 0 per Giocatore_2\n",
        "\n",
        "# Verifichiamo che abbiamo effettivamente due classi nella colonna Winner_binary\n",
        "print(\"Distribuzione della colonna Winner_binary:\")\n",
        "print(match_data['Winner_binary'].value_counts())\n",
        "\n",
        "# Se tutti i valori sono 1, dobbiamo generare alcuni esempi con valore 0\n",
        "if len(match_data['Winner_binary'].unique()) == 1:\n",
        "    print(\"ATTENZIONE: Tutti i match sono stati vinti dal giocatore 1!\")\n",
        "    print(\"Creiamo artificialmente alcuni esempi dove vince il giocatore 2...\")\n",
        "\n",
        "    # Invertiamo alcuni esempi (scambiando i giocatori e impostando Winner_binary = 0)\n",
        "    num_to_flip = min(5, len(match_data) // 2)\n",
        "    indices_to_flip = np.random.choice(match_data.index, num_to_flip, replace=False)\n",
        "\n",
        "    for idx in indices_to_flip:\n",
        "        # Scambiamo i giocatori\n",
        "        temp_g1 = match_data.loc[idx, 'Giocatore_1']\n",
        "        temp_sets_g1 = match_data.loc[idx, 'Set Vinti']\n",
        "\n",
        "        match_data.loc[idx, 'Giocatore_1'] = match_data.loc[idx, 'Giocatore_2']\n",
        "        match_data.loc[idx, 'Set Vinti'] = match_data.loc[idx, 'Set Vinti.1']\n",
        "\n",
        "        match_data.loc[idx, 'Giocatore_2'] = temp_g1\n",
        "        match_data.loc[idx, 'Set Vinti.1'] = temp_sets_g1\n",
        "\n",
        "        # Impostiamo Winner e Winner_binary\n",
        "        match_data.loc[idx, 'Winner'] = 2\n",
        "        match_data.loc[idx, 'Winner_binary'] = 0\n",
        "\n",
        "    print(\"Nuova distribuzione della colonna Winner_binary:\")\n",
        "    print(match_data['Winner_binary'].value_counts())\n",
        "\n",
        "# Uniamo il dataset con clay_data per entrambi i giocatori\n",
        "# Per il giocatore 1\n",
        "player1_features = match_data.merge(clay_data, left_on='Giocatore_1', right_on='Giocatore', how='left')\n",
        "player1_features = player1_features.add_suffix('_1').reset_index()\n",
        "\n",
        "# Per il giocatore 2\n",
        "player2_features = match_data.merge(clay_data, left_on='Giocatore_2', right_on='Giocatore', how='left')\n",
        "player2_features = player2_features.add_suffix('_2').reset_index()\n",
        "\n",
        "# Uniamo i due dataframe per indice\n",
        "final_data = pd.DataFrame()\n",
        "for col in player1_features.columns:\n",
        "    if col.startswith('index'):\n",
        "        continue\n",
        "    if not (col.startswith('Giocatore_') or col.startswith('Set Vinti') or col.startswith('Winner')):\n",
        "        final_data[col] = player1_features[col]\n",
        "\n",
        "for col in player2_features.columns:\n",
        "    if col.startswith('index'):\n",
        "        continue\n",
        "    if not (col.startswith('Giocatore_') or col.startswith('Set Vinti') or col.startswith('Winner')):\n",
        "        final_data[col] = player2_features[col]\n",
        "\n",
        "# Aggiungiamo la colonna target (solo Winner_binary_1 che contiene la nostra classe binaria)\n",
        "final_data['Winner'] = player1_features['Winner_binary_1']\n",
        "\n",
        "# Verifichiamo le classi nella colonna Winner\n",
        "print(\"Classi nella colonna Winner del final_data:\")\n",
        "print(final_data['Winner'].value_counts())\n",
        "\n",
        "# Eliminiamo colonne non necessarie o che potrebbero causare problemi\n",
        "cols_to_drop = ['index_1', 'index_2', 'superfice_1', 'superfice_2']\n",
        "for col in cols_to_drop:\n",
        "    if col in final_data.columns:\n",
        "        final_data = final_data.drop(col, axis=1)\n",
        "\n",
        "# Eliminiamo righe con valori NaN\n",
        "final_data = final_data.dropna()\n",
        "\n",
        "# Variabili indipendenti - tutte le colonne tranne Winner\n",
        "X = final_data.drop('Winner', axis=1)\n",
        "\n",
        "# La variabile dipendente (target)\n",
        "y = final_data['Winner'].values\n",
        "\n",
        "# Verifica la forma di y e la distribuzione delle classi\n",
        "print(f\"Shape di y: {y.shape}\")\n",
        "print(f\"Valori unici in y: {np.unique(y, return_counts=True)}\")\n",
        "\n",
        "# Usiamo StratifiedKFold per mantenere la distribuzione delle classi\n",
        "skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n",
        "\n",
        "# Prendiamo un solo fold per il training e test\n",
        "for train_index, test_index in skf.split(X, y):\n",
        "    X_train, X_test = X.iloc[train_index], X.iloc[test_index]\n",
        "    y_train, y_test = y[train_index], y[test_index]\n",
        "    break  # Prendiamo solo il primo fold\n",
        "\n",
        "# Verifichiamo che entrambe le classi siano presenti in entrambi i set\n",
        "print(f\"Valori unici in y_train: {np.unique(y_train, return_counts=True)}\")\n",
        "print(f\"Valori unici in y_test: {np.unique(y_test, return_counts=True)}\")\n",
        "\n",
        "# Standardizziamo i dati\n",
        "scaler = StandardScaler()\n",
        "X_train_scaled = scaler.fit_transform(X_train)\n",
        "X_test_scaled = scaler.transform(X_test)\n",
        "\n",
        "# Creiamo il modello di regressione logistica\n",
        "model = LogisticRegression(max_iter=1000)\n",
        "model.fit(X_train_scaled, y_train)\n",
        "\n",
        "# Prediciamo i valori sul set di test\n",
        "y_pred = model.predict(X_test_scaled)\n",
        "\n",
        "# Valutiamo il modello\n",
        "accuracy = accuracy_score(y_test, y_pred)\n",
        "cm = confusion_matrix(y_test, y_pred)\n",
        "\n",
        "# Stampa i risultati\n",
        "print(f\"Accuracy: {accuracy}\")\n",
        "print(f\"Confusion Matrix:\\n{cm}\")\n",
        "\n",
        "# Analizziamo i coefficienti del modello\n",
        "coefficients = pd.DataFrame({\n",
        "    'Feature': X.columns,\n",
        "    'Coefficient': model.coef_[0]\n",
        "})\n",
        "print(\"Top 10 features by importance:\")\n",
        "print(coefficients.reindex(coefficients['Coefficient'].abs().sort_values(ascending=False).index))\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "mu-NUeynH0rV",
        "outputId": "5f651da1-f9b5-4733-830b-b401c4450a6f"
      },
      "execution_count": 8,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "   Giocatore_1  Giocatore_2  Winner\n",
            "0           55           24       1\n",
            "1           69           47       2\n",
            "2           36           27       1\n",
            "3           21           31       1\n",
            "4           59           56       1\n",
            "   Giocatore  Serve_Rating  1st_Serve  1st_Serve_Points_Won  \\\n",
            "0          1         261.2       70.5                  62.8   \n",
            "1          2         261.1       61.4                  71.3   \n",
            "2          3         254.5       53.8                  68.6   \n",
            "3          4         243.0       69.8                  60.9   \n",
            "4          5         243.2       58.9                  69.0   \n",
            "\n",
            "   2st_Serve_Points_Won  Service_Games_Won  Avg_Aces/Match  \\\n",
            "0                  53.9               73.2             3.1   \n",
            "1                  46.8               78.8             5.0   \n",
            "2                  56.1               76.3             2.6   \n",
            "3                  48.6               63.8             2.4   \n",
            "4                  44.1               70.8             7.6   \n",
            "\n",
            "   Avg_Double_Faults/Match  Return_Rating  1st_Serve_Return_Points_Won  \\\n",
            "0                      2.3          145.3                         33.6   \n",
            "1                      2.2          139.6                         28.4   \n",
            "2                      2.9          179.5                         37.5   \n",
            "3                      2.5          147.4                         32.9   \n",
            "4                      7.2          152.1                         31.4   \n",
            "\n",
            "   2nd_Serve_Return_PointsWon  Return_Games_Won  Break_Points_Converted  \\\n",
            "0                        48.6              25.0                    38.1   \n",
            "1                        49.7              20.9                    40.6   \n",
            "2                        54.1              37.9                    50.0   \n",
            "3                        47.0              23.4                    44.1   \n",
            "4                        44.4              23.5                    52.8   \n",
            "\n",
            "  superfice  \n",
            "0      clay  \n",
            "1      clay  \n",
            "2      clay  \n",
            "3      clay  \n",
            "4      clay  \n",
            "Distribuzione della colonna Winner:\n",
            "Winner\n",
            "1    22\n",
            "2     6\n",
            "Name: count, dtype: int64\n",
            "Distribuzione della colonna Winner_binary:\n",
            "Winner_binary\n",
            "1    22\n",
            "0     6\n",
            "Name: count, dtype: int64\n",
            "Classi nella colonna Winner del final_data:\n",
            "Winner\n",
            "1    22\n",
            "0     6\n",
            "Name: count, dtype: int64\n",
            "Shape di y: (28,)\n",
            "Valori unici in y: (array([0, 1]), array([ 6, 22]))\n",
            "Valori unici in y_train: (array([0, 1]), array([ 5, 17]))\n",
            "Valori unici in y_test: (array([0, 1]), array([1, 5]))\n",
            "Accuracy: 0.8333333333333334\n",
            "Confusion Matrix:\n",
            "[[1 0]\n",
            " [1 4]]\n",
            "Top 10 features by importance:\n",
            "                          Feature  Coefficient\n",
            "15         2st_Serve_Points_Won_2    -0.924387\n",
            "3          2st_Serve_Points_Won_1     0.744953\n",
            "6       Avg_Double_Faults/Match_1     0.743383\n",
            "21   2nd_Serve_Return_PointsWon_2    -0.622145\n",
            "5                Avg_Aces/Match_1    -0.491505\n",
            "23       Break_Points_Converted_2     0.444613\n",
            "11       Break_Points_Converted_1     0.418096\n",
            "13                    1st_Serve_2    -0.349476\n",
            "20  1st_Serve_Return_Points_Won_2     0.337550\n",
            "18      Avg_Double_Faults/Match_2    -0.307647\n",
            "12                 Serve_Rating_2    -0.259311\n",
            "7                 Return_Rating_1     0.244916\n",
            "2          1st_Serve_Points_Won_1    -0.241826\n",
            "10             Return_Games_Won_1     0.181726\n",
            "16            Service_Games_Won_2    -0.167200\n",
            "22             Return_Games_Won_2    -0.158954\n",
            "1                     1st_Serve_1    -0.151502\n",
            "17               Avg_Aces/Match_2     0.143074\n",
            "0                  Serve_Rating_1    -0.124386\n",
            "4             Service_Games_Won_1    -0.122806\n",
            "9    2nd_Serve_Return_PointsWon_1     0.095880\n",
            "8   1st_Serve_Return_Points_Won_1    -0.065077\n",
            "19                Return_Rating_2     0.040578\n",
            "14         1st_Serve_Points_Won_2    -0.006233\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "Xaz9O7jw3XAd"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}