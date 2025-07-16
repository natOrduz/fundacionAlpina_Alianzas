import streamlit as st
import pandas as pd

# -------------------------
# FUNCIONES PRINCIPALES
# -------------------------

def login():
    st.write("Ingreso de operativos de la Fundación Alpina")
    usuario_login = st.text_input("Contraseña:", type="password")
    contraseña = 'fundacionAliados80'
    return usuario_login == contraseña

@st.cache_data
def cargar_datos():
    sheet_id = "1jHx7DyT3GBiRVJIyjF-622ANE0Rmjmhi9qPodCmtaSM"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()  # Quita espacios invisibles
    return df

def busqueda_alianza(fila, enfoque, ubicacion, accion):
    counter = 0

    enfoques_aliado = [e.strip().lower() for e in str(fila["Enfoque"]).split(",")]
    if enfoque == "Todas" or enfoque.strip().lower() in enfoques_aliado:
        counter += 1

    ubicaciones_aliado = [u.strip().lower() for u in str(fila["Ubicación"]).split(",")]
    if ubicacion == "Todas" or ubicacion.strip().lower() in ubicaciones_aliado:
        counter += 1

    if accion == "Todas" or str(fila["Nivel de acción"]).strip() == str(accion).strip():
        counter += 1

    return counter == 3

# -------------------------
# CUERPO PRINCIPAL
# -------------------------

st.title("Buscador de Aliados - Fundación Alpina")

if login():
    st.success("Acceso permitido ✅")

    df = cargar_datos()

    # Barra de búsqueda opcional
    busqueda = st.text_input("Buscar aliado por nombre (opcional):")

    # Si hay texto en la barra, mostrar resultados
    if busqueda:
    resultados = df[df['Aliados'].astype(str).str.contains(busqueda, case=False, na=False)]
    st.write(f"{len(resultados)} resultado(s) encontrado(s) para: **{busqueda}**")
    st.dataframe(resultados)

    enfoques = sorted(set(e.strip().lower() for lista in df["Enfoque"].dropna() for e in str(lista).split(",")))
    ubicaciones = sorted(set(u.strip().lower() for lista in df["Ubicación"].dropna() for u in str(lista).split(",")))
    acciones = sorted(df["Nivel de acción"].dropna().astype(str).unique().tolist())

    enfoques.insert(0, "Todas")
    ubicaciones.insert(0, "Todas")
    acciones.insert(0, "Todas")

    busqueda_enfoque = st.selectbox("Enfoque:", enfoques)
    busqueda_ubicacion = st.selectbox("Ubicación:", ubicaciones)
    busqueda_accion = st.selectbox("Nivel de acción:", acciones)

    st.subheader("📋 Aliados disponibles:")

    resultados = []

    for _, fila in df.iterrows():
        if busqueda_alianza(fila, busqueda_enfoque, busqueda_ubicacion, busqueda_accion):
            resultados.append(fila)

    if resultados:
        for aliado in resultados:
            st.markdown(f"✅ **{aliado['Aliado']}**")
            with st.expander("Más información"):
                st.markdown(f"- **Encargado/a:** {aliado['Encargado/a']}")
                st.markdown(f"- **Historial con la Fundación:** {aliado['Historial con la Fundación']}")
                st.markdown(f"- **Última colaboración:** {aliado['Última colaboración']}")
                st.markdown(f"- **Veces colaboradas con la Fundación:** {aliado['Veces colaboradas con la Fundación']}")
    else:
        st.warning("No se encontraron aliados con esos criterios.")
else:
    st.error("Contraseña incorrecta. No hay acceso.")
