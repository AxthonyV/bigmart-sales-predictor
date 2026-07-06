# BigMart Sales Predictor

Este proyecto académico tiene como objetivo estimar las ventas de productos en una cadena de supermercados mediante aprendizaje estadístico. Se utiliza un modelo de regresión basado en Random Forest Regressor para predecir Item_Outlet_Sales a partir de variables relacionadas con producto, tienda y visibilidad.

## Descripción del problema de negocio

BigMart requiere una herramienta de apoyo para estimar el volumen de ventas esperado de un artículo en un punto de venta. La predicción considera factores como precio, peso del producto, antigüedad de la tienda, visibilidad de exhibición y características categóricas del producto y del canal de venta.

## Metodología

El sistema carga un modelo preentrenado serializado en modelo_bigmart.pkl junto con la estructura esperada de columnas en columnas.pkl. La inferencia realiza un preprocesamiento basado en variables dummy para las características categóricas y alinea la entrada con las columnas utilizadas durante el entrenamiento.

### Variables predictoras

- Numéricas: Item_Weight, Item_MRP, Outlet_Age, Item_Visibility_MeanRatio
- Categóricas transformadas a variables dummy: Item_Fat_Content, Item_Type, Outlet_Size, Outlet_Location_Type, Outlet_Type

### Modelo utilizado

- Random Forest Regressor con 100 árboles
- Implementado con scikit-learn

## Métricas del Modelo

| Métrica | Valor |
| --- | ---: |
| Correlación | 0.7396 |
| MAE | 809.17 |
| RMSE | 1,150.87 |

## Instalación y Uso

1. Crear y activar un entorno virtual, si se desea.
2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:

```bash
streamlit run app.py
```

## Estructura del Proyecto

```text
bigmart-sales-predictor/
├── app.py
├── modelo_bigmart.pkl
├── columnas.pkl
├── Train_limpio.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Créditos

Proyecto académico desarrollado para el curso de Aprendizaje Estadístico de la Universidad Privada Antenor Orrego (UPAO).

## Nota de implementación

En la aplicación actual, la inferencia construye variables dummy sobre un único registro y luego aplica una reindexación con las columnas esperadas por el modelo. Este procedimiento depende de que la estructura de entrada sea consistente con la utilizada durante el entrenamiento; si aparecen nuevas categorías o cambios en el esquema de datos, la predicción puede requerir un ajuste adicional.
