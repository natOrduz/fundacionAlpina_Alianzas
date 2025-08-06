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

def busqueda_alianza(fila, areasDeTrabajo, territoriosDeOp, tipoDeOrg):
    counter = 0

    # Area de trabajo de la organización
    areasDeTrabajo_aliado = [e.strip().lower() for e in str(fila["Areas de trabajo"]).split(",")]
    if areasDeTrabajo == "Todas" or areasDeTrabajo.strip().lower() in areasDeTrabajo_aliado:
        counter += 1

    # Territorios de operación de la organización
    territoriosDeOp_aliado = [u.strip().lower() for u in str(fila["Territorios de operación"]).split(",")]
    if territoriosDeOp == "Todas" or territoriosDeOp.strip().lower() in territoriosDeOp_aliado:
        counter += 1

    # Tipo de organización - ej. fundación
    tipoDeOrg_aliado = [u.strip().lower() for u in str(fila["Tipo de organización"]).split(",")]
    if tipoDeOrg == "Todas" or tipoDeOrg.strip().lower() in tipoDeOrg_aliado:
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
    st.subheader("***Buscar aliado por nombre***")
    busqueda = st.text_input("(opcional)")

    cantidad = 0
    resultados = pd.DataFrame()

    # Si hay texto en la barra, mostrar resultados - búsqueda específica
    if busqueda:
        resultados = df[df['Nombre de la organización'].astype(str).str.contains(busqueda, case=False, na=False)]
        cantidad = len(resultados)
        st.write(f"{cantidad} resultado(s) encontrado(s) para: **{busqueda}**")

    # Información/categorías que sale/se comunica al usuario tocar en el resultado de la búsqueda (el nombre)
    if cantidad == 1:
        aliado = resultados.iloc[0]
        st.markdown(f"✅ **{aliado['Nombre de la organización']}**")
        with st.expander("Más información"):
            st.markdown(f"**Areas de trabajo:** {aliado['Areas de trabajo']}")
            st.markdown(f"**Territorios de operación:** {aliado['Territorios de operación']}")
            st.markdown(f"**Tipo de organización:** {aliado['Tipo de organización']}")
            st.markdown(f"**Historial con la Fundación:** {aliado['Historial con la Fundación']}")
            st.markdown(f"**Última colaboración:** {aliado['Última colaboración']}")
            st.markdown(f"**Veces colaboradas con la Fundación:** {aliado['Veces colaboradas con la Fundación']}")
            st.markdown(f"**Persona de contacto:** {aliado['Persona de contacto']}")
            st.markdown(f"- **Cargo:** {aliado['Cargo de la persona de contacto']}")
            st.markdown(f"- **Correo:** {aliado['Correo']}")
            st.markdown(f"- **Número de contacto:** {aliado['Número de persona de contacto']}")
            st.markdown(f"**Origen del contacto:** {aliado['Origen del contacto']}")
            st.markdown(f"**Presupuesto acordado:** {aliado['Presupuesto acordado']}")
    
    elif cantidad > 1:
        opciones = resultados['Nombre de la organización'].unique().tolist()
        aliado_seleccionado = st.selectbox("Selecciona un aliado:", opciones)

        if aliado_seleccionado:
            aliado = resultados[resultados['Nombre de la organización'] == aliado_seleccionado].iloc[0]
            st.markdown(f"✅ **{aliado['Nombre de la organización']}**")
            with st.expander("Más información"):
                st.markdown(f"**Areas de trabajo:** {aliado['Areas de trabajo']}")
                st.markdown(f"**Territorios de operación:** {aliado['Territorios de operación']}")
                st.markdown(f"**Tipo de organización:** {aliado['Tipo de organización']}")
                st.markdown(f"**Historial con la Fundación:** {aliado['Historial con la Fundación']}")
                st.markdown(f"**Última colaboración:** {aliado['Última colaboración']}")
                st.markdown(f"**Veces colaboradas con la Fundación:** {aliado['Veces colaboradas con la Fundación']}")
                st.markdown(f"**Persona de contacto:** {aliado['Persona de contacto']}")
                st.markdown(f"- **Cargo de la persona de contacto:** {aliado['Cargo de la persona de contacto']}")
                st.markdown(f"- **Correo de la persona de contacto:** {aliado['Correo']}")
                st.markdown(f"- **Número de la persona de contacto:** {aliado['Número de persona de contacto']}")
                st.markdown(f"**Origen del contacto:** {aliado['Origen del contacto']}")
                st.markdown(f"**Presupuesto acordado:** {aliado['Presupuesto acordado']}")
    
    else:
        st.warning("No se encontraron aliados que coincidan.")

    st.subheader("***Búsqueda a base de filtros***")

    # Búsqueda a base de filtros
    areas = sorted(set(e.strip().lower() for lista in df["Areas de trabajo"].dropna() for e in str(lista).split(",")))
    territorios = sorted(set(u.strip().lower() for lista in df["Territorios de operación"].dropna() for u in str(lista).split(",")))
    tipo = sorted(df["Tipo de organización"].dropna().astype(str).unique().tolist())

    areas.insert(0, "Todas")
    territorios.insert(0, "Todas")
    tipo.insert(0, "Todas")

    busqueda_areas = st.selectbox("Areas de trabajo:", areas)
    busqueda_territorios = st.selectbox("Territorios de operación:", territorios)
    busqueda_tipo = st.selectbox("Tipo de organización:", tipo) 

    # Resultados de la búsqueda a base de filtros

    st.subheader("📋 Aliados disponibles:")

    resultados = []

    for _, fila in df.iterrows():
        if busqueda_alianza(fila, busqueda_areas, busqueda_territorios, busqueda_tipo):
            resultados.append(fila)

    if resultados:
        for aliado in resultados:
            st.markdown(f"✅ **{aliado['Nombre de la organización']}**")
            with st.expander("Más información"):
                st.markdown(f"**Historial con la Fundación:** {aliado['Historial con la Fundación']}")
                st.markdown(f"**Última colaboración:** {aliado['Última colaboración']}")
                st.markdown(f"**Veces colaboradas con la Fundación:** {aliado['Veces colaboradas con la Fundación']}")
                st.markdown(f"**Persona de contacto:** {aliado['Persona de contacto']}")
                st.markdown(f"- **Cargo:** {aliado['Cargo de la persona de contacto']}")
                st.markdown(f"- **Correo:** {aliado['Correo']}")
                st.markdown(f"- **Número de contacto:** {aliado['Número de persona de contacto']}")
                st.markdown(f"**Origen del contacto:** {aliado['Origen del contacto']}")
                st.markdown(f"**Presupuesto acordado:** {aliado['Presupuesto acordado']}")
    else:
        st.warning("No se encontraron aliados con esos criterios.")
else:
    st.error("Contraseña incorrecta. No hay acceso.")
