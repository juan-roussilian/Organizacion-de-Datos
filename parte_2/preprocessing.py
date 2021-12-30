import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import KNNImputer, IterativeImputer
from sklearn.manifold import TSNE, MDS
from sklearn.preprocessing import StandardScaler

features_continuas = ['id','horas_de_sol','humedad_tarde', 'humedad_temprano', 'mm_evaporados_agua', 'mm_lluvia_dia', 'nubosidad_tarde', 'nubosidad_temprano', 'presion_atmosferica_tarde', 'presion_atmosferica_temprano', 'rafaga_viento_max_velocidad','temp_max', 'temp_min', 'temperatura_tarde', 'temperatura_temprano',  'velocidad_viendo_tarde','velocidad_viendo_temprano']

def aplicar_dummy_variables_encoding(df, columnas):
    df_encodeado = pd.get_dummies(df, columns=columnas, dummy_na=True, drop_first=True)
    return df_encodeado

def aplicar_ordinal_encoding(df, columnas):
    oe = OrdinalEncoder(dtype='int')
    return oe.fit_transform(df[columnas])

def entrenar_normalizador_standard(df_train):
    df_a_normalizar = df_train.copy()
   
    scaler = StandardScaler()
    scaler.fit(df_a_normalizar)
    return scaler

def entrenar_normalizador_minmax(df_train):
    df_a_normalizar = df_train.copy()

    scaler = MinMaxScaler()
    scaler.fit(df_a_normalizar)
    return scaler

def normalizar_dataframe(df, scaler):
    df_normalizado = scaler.transform(df.copy())
    return df_normalizado

def limpiar_datos(df_a_limpiar):
    df = df_a_limpiar.copy(deep=True)
    df.fillna(np.nan, inplace = True)
    
    df['presion_atmosferica_tarde'].replace('.+\..+\..+', np.nan, inplace=True, regex=True)
    df.astype({'presion_atmosferica_tarde': 'float64'}).dtypes
    return df

    
def reduccion_TSNE(df):
    return TSNE(n_components=3).fit_transform(df)

def reduccion_MDS(df):
    return MDS(n_components=6).fit_transform(df)

def reduccion_PCA(df, dim_destino):
    return PCA(n_components=dim_destino).fit_transform(df)
    
def eliminar_features(df, columnas):
    df.drop(columnas, axis=1, inplace=True)
    df.reset_index()

def imputar_missings_KNN(df):
    imputer = KNNImputer(n_neighbors = 3, weights="uniform")
    imputer.fit_transform(df)
    
def entrenar_iterative_imputer(df_train):
    imputer = IterativeImputer()
    imputer.fit(df_train[FEATURES_CONTINUAS])
    return imputer
    
def imputar_missings_iterative(df, imputer_entrenado):
    array_imputeado = imputer_entrenado.transform(df[FEATURES_CONTINUAS])
    df_imputeado = pd.DataFrame(array_imputeado, columns=FEATURES_CONTINUAS)
    df_imputeado.set_index('id', inplace=True)
    df_imputeado = df_imputeado.sort_values(by=['id'], inplace=True, ascending=True) 
    return df_imputeado