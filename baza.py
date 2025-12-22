import streamlit as st
from supabase import create_client, Client

# Konfiguracja połączenia z Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("📦 Zarządzanie Magazynem")

# Tworzymy zakładki dla lepszej przejrzystości
tab1, tab2 = st.tabs(["Dodaj Produkt", "Dodaj Kategorię"])

# --- ZAKŁADKA: DODAJ KATEGORIĘ ---
with tab2:
    st.header("Nowa Kategoria")
    with st.form("form_kategoria", clear_on_submit=True):
        kat_nazwa = st.text_input("Nazwa kategorii")
        kat_opis = st.text_area("Opis")
        
        submit_kat = st.form_submit_button("Zapisz kategorię")
        
        if submit_kat:
            if kat_nazwa:
                data = {"nazwa": kat_nazwa, "opis": kat_opis}
                response = supabase.table("Kategorie").insert(data).execute()
                st.success(f"Dodano kategorię: {kat_nazwa}")
            else:
                st.error("Nazwa kategorii jest wymagana!")

# --- ZAKŁADKA: DODAJ PRODUKT ---
with tab1:
    st.header("Nowy Produkt")
    
    # Pobieranie listy kategorii do selectboxa
    try:
        kategorie_res = supabase.table("Kategorie").select("id, nazwa").execute()
        kategorie_opcje = {k['nazwa']: k['id'] for k in kategorie_res.data}
    except Exception as e:
        st.error("Błąd podczas pobierania kategorii. Upewnij się, że tabela 'Kategorie' istnieje.")
        kategorie_opcje = {}

    with st.form("form_produkt", clear_on_submit=True):
        prod_nazwa = st.text_input("Nazwa produktu")
        prod_liczba = st.number_input("Liczba (sztuki)", min_value=0, step=1)
        prod_cena = st.number_input("Cena", min_value=0.0, format="%.2f")
        
        # Wybór kategorii z listy
        wybrana_kat_nazwa = st.selectbox("Kategoria", options=list(kategorie_opcje.keys()))
        
        submit_prod = st.form_submit_button("Dodaj produkt")
        
        if submit_prod:
            if prod_nazwa and wybrana_kat_nazwa:
                payload = {
                    "nazwa": prod_nazwa,
                    "liczba": prod_liczba,
                    "cena": prod_cena,
                    "Kategoria_id": kategorie_opcje[wybrana_kat_nazwa]
                }
                supabase.table("Produkty").insert(payload).execute()
                st.success(f"Produkt '{prod_nazwa}' został dodany!")
            else:
                st.error("Wypełnij wymagane pola!")

# Podgląd danych pod formularzami
st.divider()
if st.checkbox("Pokaż aktualną listę produktów"):
    res = supabase.table("Produkty").select("nazwa, liczba, cena, Kategorie(nazwa)").execute()
    st.table(res.data)
