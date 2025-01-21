import google.generativeai as genai
from dotenv import load_dotenv
import os
import PIL
from PIL import Image
import pandas as pd
import streamlit as st

def create_med_plan_from_img(patient_name, image_file):
    prompt = """Sei un assistente medico virtuale che data una o più immagini in allegato 
    che contiene i dati testuali della terapia farmacologica da assumere di un paziente, 

    Devi estrarre dati con questa tipologia e struttura seguendo l'esempio, che devi applicare
    per tutti i farmaci, impilando la loro somministrazione in una tabella strutturata dalle seguenti colonne:

    Orario: Orario di somministrazione farmaco.
    Nome Farmaco: Il nome del farmaco da somministrare.
    Tipo Farmaco: La tipologia del farmaco da somministrare.
    Dosaggio: Il dosaggio del farmaco da somministrare.
    Dettagli: I dettagli della terapia scritti dal medico che possono includere le variazioni nel tempo
    del piano, dosaggi e tempistiche di somministrazione.

    ---Caso Esempio---:
    Orario: 7:00.
    Nome Farmaco: Paracetamolo.
    Tipo Farmaco: Analgesico.
    Dosaggio: 1000 mg.
    Dettagli: 2 compressa al giorno per 7 giorni e poi 1 per i restanti 10 giorno.
    ------------------------------------------------------------------------------

    # Quindi, ora, ritorna un testo formattato in righe e colonne, accuratamente strutturato e che contiene 
    # tutti i dettagli dei farmaci in maniera esaustiva:

    Orario, Nome Farmaco, Tipo Farmaco, Dosaggio, Dettagli.

    Nota bene: 
    - non ritornare altro testo a parte la tabella dei farmaci da somministrare.
    - se ci sono dei campi vuoti, inserisci "Mancante".
    - non tralasciare nessun dettaglio della colonna "Dettagli", devono esserci tutti i dettagli testuali
    senza omissioni. 
    """
    
    model = genai.GenerativeModel('gemini-1.5-pro')
    result = model.generate_content([prompt, PIL.Image.open(image_file)])
    
    pharma_list = []
    pharma_list.append(result.text.split('\n'))
    
    headers = ["Orario", "Nome Farmaco", "Tipo Farmaco", "Dosaggio", "Dettagli"]
    rows = [line.split(',') for line in pharma_list[0] if line]

    processed_rows = [line[:5] + [''] if len(line) < 5 else line[:5] for line in rows]  
    processed_rows = processed_rows[1:]

    for row in processed_rows:
        row.append(patient_name)

    df = pd.DataFrame(processed_rows, columns=headers + ["Nome Paziente"])
    
    df["Orario"] = pd.to_datetime(df["Orario"], errors="coerce", format="%H:%M")
    df = df.sort_values("Orario").reset_index(drop=True)
    df["Orario"] = df["Orario"].dt.strftime('%H:%M')
    df.fillna("Mancante", inplace=True)
    
    title = f"Terapia {patient_name}"
    
    excel_filename = f"terapia_{patient_name.replace(' ', '_')}.xlsx"
    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=title)
        
    return df, excel_filename

if __name__=='__main__':
    load_dotenv(".env")
    # google_api_key = os.getenv("GOOGLE_API_KEY")
    google_api_key = st.secrets["google"]["api_key"]
    genai.configure(api_key=google_api_key)
    
    st.set_page_config(page_title="Generatore Calendario Farmacologico", page_icon="🩺")
    st.title("Generatore Calendario Farmacologico")
    st.image("https://img.freepik.com/foto-premium/farmaci-e-calendario-della-medicina-dei-cartoni-animati-sullo-sfondo-arancione-rendering-3d-disegno-digitale_778569-4112.jpg", use_container_width=True)  
    
    patient_name = st.text_input("Nome del paziente:")
    image_file = st.file_uploader("Carica l'immagine della terapia", type=["png", "jpg", "jpeg"])
    if image_file is not None:
        image = Image.open(image_file)
        st.image(image, caption="Immagine caricata", use_container_width=True)
    
    if 'calendar_generated' not in st.session_state:
        st.session_state['calendar_generated'] = False

    if patient_name and image_file and not st.session_state['calendar_generated']:
        with st.spinner("Caricamento del Calendario Farmacologico..."):
            df, excel_filename = create_med_plan_from_img(patient_name, image_file)
            st.session_state['calendar_generated'] = True
            st.session_state['df'] = df
            st.session_state['excel_filename'] = excel_filename

    if st.session_state['calendar_generated']:
        st.success(f"Il Calendario Farmacologico per {patient_name} è stato generato con successo!")
        st.write(f"Dettagli della terapia per {patient_name}:")
        st.dataframe(st.session_state['df'])

        st.download_button(
            label="Scarica il Calendario Farmacologico",
            data=open(st.session_state['excel_filename'], "rb").read(),
            file_name=st.session_state['excel_filename'],
            mime="application/vnd.ms-excel"
        )

