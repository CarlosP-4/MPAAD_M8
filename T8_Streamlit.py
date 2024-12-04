import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import pandas as pd
import plotly.express as px

# Definición de los colores
PRIMARY_BLUE = "#000C64"  # Azul primario
LIGHT_BLUE = "#003C8C"    # Azul más claro

# Función para aplicar los estilos globales
def apply_styles():
    st.markdown(f"""
    <style>
        /* Cambiar color de fondo de la barra lateral */
        .css-1d391kg {{background-color: {PRIMARY_BLUE};}}  
        
        /* Cambiar color del menú de opciones */
        .css-1v3fvcr {{background-color: {PRIMARY_BLUE};}}  
        
        /* Cambiar color de los iconos del menú */
        .css-1p72jhv {{color: white;}}  
        
        /* Cambiar color de los enlaces del menú */
        .css-16g7i8b {{color: white;}}  
        
        /* Cambiar color de los botones */
        .css-1l0w9k7 {{color: white;}}  
        
        /* Cambiar color de los textos de las tablas */
        .css-1xl4yxx {{color: white;}}  
        
        /* Estilo para títulos de nivel h1, h2, etc. */
        h1, h2, h3, h4, h5, h6 {{
            color: {LIGHT_BLUE}; 
            font-family: 'Arial'; 
            font-weight: bold;
        }}
        
        /* Personalizar los botones */
        button {{
            background-color: {PRIMARY_BLUE};
            color: white;
            border-radius: 5px;
            padding: 10px;
            font-weight: bold;
        }}
        
        button:hover {{
            background-color: {LIGHT_BLUE};
        }}
        
        /* Estilo para las tablas */
        .dataframe {{
            border-collapse: collapse;
            width: 100%;
        }}
        
        .dataframe th, .dataframe td {{
            border: 1px solid {PRIMARY_BLUE};
            padding: 8px;
            text-align: left;
        }}
        
        .dataframe th {{
            background-color: {LIGHT_BLUE};
            color: white;
        }}
    </style>
    """, unsafe_allow_html=True)

# Función para cargar datos de SQLite
def load_sqlite_data():
    conn = sqlite3.connect('data/liga_espanyola_gps.db')
    query = 'SELECT * FROM jugadores_gps'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Función para cargar los datos de Sergio Ramos desde el archivo Excel
def load_fbref_data():
    file_path = 'data/sergio_ramos_stats.xlsx'  # Ajusta la ruta del archivo
    df = pd.read_excel(file_path, header=[0, 1])  # Usamos dos niveles de encabezado
    return df

# Página de Login (Usuario y Contraseña)
def login_page():
    st.markdown("""
    <style>         
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 30px;
        background-color: rgba(0, 12, 100, 0.05);
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .login-title {
        text-align: center;
        color: #000C64;
        margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%;
        background-color: #000C64;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #003C8C;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #000C64;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    
    
    # Title with icon
    st.markdown('<h1 class="login-title"><i class="fas fa-lock"></i> Inicio de Sesión</h1>', unsafe_allow_html=True)
    
    # User input fields
    username = st.text_input(
        "Usuario", 
        placeholder="Ingrese su nombre de usuario",
        help="Nombre de usuario registrado"
    )
    
    password = st.text_input(
        "Contraseña", 
        type="password", 
        placeholder="Ingrese su contraseña",
        help="Contraseña de acceso"
    )
    
    # Remember me checkbox
    remember_me = st.checkbox("Recordar mi sesión")
    
    # Login button with spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Login button
    if st.button("Iniciar Sesión"):
        if username == "admin" and password == "admin":
            # Cambiar directamente el estado de la sesión para mostrar el menú principal
            st.session_state['logged_in'] = True
            
            # Usar rerun() para recargar la página y mostrar el menú
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
    
    # Forgot password and signup links
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <a href="#" style="color: #000C64; margin-right: 15px; text-decoration: none;">¿Olvidaste tu contraseña?</a>
        <a href="#" style="color: #003C8C; text-decoration: none;">Registrarse</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Página de Datos Globales
def global_data_page():
    st.title("Datos Globales")
    st.write("Aquí mostramos los datos obtenidos de la base de datos SQLite.")

    try:
        df_sqlite = load_sqlite_data()
        
        # Columnas numéricas para selección (excluyendo ID)
        columnas_numericas = df_sqlite.select_dtypes(include=['float64', 'int64']).columns.tolist()
        columnas_numericas = [col for col in columnas_numericas if col != 'id']
        
        # Mejorar la visualización de la tabla
        st.markdown("### Tabla de Datos Globales")
        st.dataframe(
            df_sqlite, 
            use_container_width=True,
            hide_index=True
        )
        
        # Separador visual con color primer gráfico
        st.markdown("<hr style='border: 2px solid #000C64; margin: 20px 0;'>", unsafe_allow_html=True)
         
        
        # Crear columnas para los selectores con información adicional
        col1, col2 = st.columns(2)
        
        with col1:
            columna_x = st.selectbox(
                "Selecciona la columna para el eje X", 
                options=["nombre"] + columnas_numericas,
                help="Elige la variable para el eje horizontal del gráfico"
            )
        
        with col2:
            columna_y = st.selectbox(
                "Selecciona la columna para el eje Y", 
                options=columnas_numericas,
                help="Elige la variable para el eje vertical del gráfico"
            )
        
    except Exception as e:
        st.error(f"Error al cargar los datos de SQLite: {e}")
    
    if not df_sqlite.empty:
        # Gráfico de barras dinámico con mejoras
        fig = px.bar(
            df_sqlite, 
            x=columna_x, 
            y=columna_y, 
            title=f"Análisis de {columna_y} por {columna_x}",
            labels={columna_x: columna_x.replace('_', ' ').title(), 
                    columna_y: columna_y.replace('_', ' ').title()}
        )
        
        # Personalización avanzada del gráfico
        fig.update_traces(
            marker_color=PRIMARY_BLUE,
            marker_line_color='#000C64',  # Línea de contorno más oscura
            marker_line_width=1.5,
            opacity=0.8,
            texttemplate='%{y:.2f}', 
            textposition='outside',
            textfont=dict(color='black', size=12)  # Texto más grande
        )
        
        fig.update_layout(
            title_font=dict(size=20, color=PRIMARY_BLUE, family='Arial Black'),
            xaxis_title_font=dict(size=14, color='#000C64', family='Arial'),
            yaxis_title_font=dict(size=14, color='#000C64', family='Arial'),
            xaxis=dict(
                showgrid=True, 
                gridcolor='#A0A0A0',  # Líneas de grid más visibles
                tickangle=45,
                tickfont=dict(size=12)  # Etiquetas más grandes
            ),
            yaxis=dict(
                showgrid=True, 
                gridcolor='#A0A0A0',
                tickfont=dict(size=12)  # Etiquetas más grandes
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
                font_family="Arial"
            ),
            plot_bgcolor='rgba(0,0,0,0)',  # Fondo transparente
            paper_bgcolor='rgba(0,0,0,0)'  # Fondo del papel transparente
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Separador visual para la sección de correlación
        st.markdown("<hr style='border: 2px solid #000C64; margin: 20px 0;'>", unsafe_allow_html=True)

        # Gráfico de Dispersión con estilos actualizados
        st.markdown("### Análisis de Correlación")
        col3, col4 = st.columns(2)

        with col3:
            x_corr = st.selectbox(
                "Selecciona Eje X", 
                options=columnas_numericas
            )
        
        with col4:
            y_corr = st.selectbox(
                "Selecciona Eje Y", 
                options=[col for col in columnas_numericas if col != x_corr]
            )
        
        fig_scatter = px.scatter(
            df_sqlite, 
            x=x_corr, 
            y=y_corr,
            title=f"Correlación entre {x_corr} y {y_corr}",
            labels={x_corr: x_corr.replace('_', ' ').title(), 
                    y_corr: y_corr.replace('_', ' ').title()}
        )
        
        fig_scatter.update_traces(
            marker_color=PRIMARY_BLUE,
            marker_size=10,
            marker_line_width=1.5,
            marker_line_color='#000C64',
            textfont=dict(color='black', size=10)
        )
        
        fig_scatter.update_layout(
            title_font=dict(size=20, color=PRIMARY_BLUE, family='Arial Black'),
            xaxis_title_font=dict(size=14, color='#000C64', family='Arial'),
            yaxis_title_font=dict(size=14, color='#000C64', family='Arial'),
            xaxis=dict(
                showgrid=True, 
                gridcolor='#A0A0A0',
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                showgrid=True, 
                gridcolor='#A0A0A0',
                tickfont=dict(size=10)
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=PRIMARY_BLUE)
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
         
# Página de Análisis de Sergio Ramos
# Función para cargar los datos de Sergio Ramos desde el archivo Excel
def load_fbref_data():
    file_path = 'data/sergio_ramos_stats.xlsx'  # Ajusta la ruta del archivo
    df = pd.read_excel(file_path, sheet_name=None, header=[0, 1])  # Cargar todas las hojas con dos niveles de encabezado
    return df

# Página de Análisis de Sergio Ramos
def sergio_ramos_page():
    st.title("Análisis de Sergio Ramos")
    st.write("Aquí mostramos los datos extraídos desde FBref.")
    
    # Cargar los datos
    df_api = load_fbref_data()

    # Inicializar df_standard para evitar el error
    df_standard = pd.DataFrame()  # Inicializar el DataFrame vacío
    
    # Buscar la hoja que contiene los datos de temporada y partidos jugados
    for sheet_name, sheet_data in df_api.items():
        st.write(f"Tabla de Datos: {sheet_name}")
        st.write(sheet_data.head())  # Muestra las primeras filas de la hoja
        
        # Verificar si la columna 'Temporada' está presente y tiene los datos de temporada
        if 'Temporada' in sheet_data.columns.get_level_values(0):
            # Acceder a las columnas correctamente con el nivel jerárquico
            df_standard = sheet_data.droplevel(1, axis=1)  # Eliminar el segundo nivel del índice de columnas
            
            # Asegurarse de que las columnas necesarias estén presentes
            required_columns = ['Temporada', 'Partidos Jugados', 'Goles+Asistencias']
            
            if all(col in df_standard.columns for col in required_columns):
                # Filtrar y preparar los datos
                df_standard = df_standard.dropna(subset=["Partidos Jugados"])  # Eliminar filas sin partidos jugados

                # Separador visual para la sección de correlación
                st.markdown("<hr style='border: 2px solid #000C64; margin: 20px 0;'>", unsafe_allow_html=True)

                # Crear gráfico de partidos jugados por temporada (gráfico de líneas)
                fig1 = px.line(df_standard, x="Temporada", y="Partidos Jugados", title="Evolución de Partidos Jugados de Sergio Ramos",
                               labels={"Partidos Jugados": 'Partidos Jugados', 'Temporada': 'Temporada'},
                               line_shape='linear', markers=True)
                # Personalización de colores
                fig1.update_traces(line_color=PRIMARY_BLUE, text=df_standard["Partidos Jugados"], textposition="top center")
                fig1.update_layout(
                    title_font=dict(size=20, color=PRIMARY_BLUE),
                    xaxis_title_font=dict(size=12, color=PRIMARY_BLUE),
                    yaxis_title_font=dict(size=12, color=PRIMARY_BLUE),
                    xaxis=dict(showgrid=True, gridcolor='#DDDDDD'),
                    yaxis=dict(showgrid=True, gridcolor='#DDDDDD'),
                    font=dict(color=PRIMARY_BLUE)
                )
                st.plotly_chart(fig1)

                # Separador visual para la sección de correlación
                st.markdown("<hr style='border: 2px solid #000C64; margin: 20px 0;'>", unsafe_allow_html=True)

                # Crear gráfico de Goles+Asistencias por temporada (gráfico de barras)
                fig2 = px.bar(df_standard, x="Temporada", y="Goles+Asistencias", title="Evolución de Goles + Asistencias de Sergio Ramos",
                              labels={"Goles+Asistencias": 'Goles + Asistencias', 'Temporada': 'Temporada'})
                # Personalización de colores
                fig2.update_traces(marker_color=LIGHT_BLUE, text=df_standard["Goles+Asistencias"], textposition="inside")
                fig2.update_layout(
                    title_font=dict(size=20, color=PRIMARY_BLUE),
                    xaxis_title_font=dict(size=12, color=PRIMARY_BLUE),
                    yaxis_title_font=dict(size=12, color=PRIMARY_BLUE),
                    xaxis=dict(showgrid=True, gridcolor='#DDDDDD'),
                    yaxis=dict(showgrid=True, gridcolor='#DDDDDD'),
                    font=dict(color=PRIMARY_BLUE)
                )
                st.plotly_chart(fig2)
                
                break  # Una vez encontrado, terminamos el ciclo para no seguir buscando más hojas
    
    # Si no se encuentran los datos, mostrar un mensaje
    if df_standard.empty:
        st.error("No se encontraron los datos de temporada o partidos jugados en el archivo.")

# Función principal
def main():
    sergio_ramos_page()

# Menú principal con tres pestañas
# Renderizar la página seleccionada
def main():
    apply_styles()
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if not st.session_state['logged_in']:
        login_page()
    else:
        menu = option_menu("Menú", ["Datos Globales", "Análisis Individual"],
                           icons=["bar-chart", "person"],
                           menu_icon="cast", default_index=0)
        if menu == "Datos Globales":
            global_data_page()
        elif menu == "Análisis Individual":
            sergio_ramos_page()

# Ejecutar la aplicación
if __name__ == "__main__":
    main()

