import streamlit as st
import requests

# --- YAPILANDIRMA ---
STRAPI_URL = "https://gezi-rehberi-backend-9nmq.onrender.com"

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="🌍 Gezi Rehberi",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ÖZEL CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@700;800;900&display=swap');
    
    /* ===== GENEL ===== */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: #0a0a14;
    }
    .block-container {
        padding-top: 2rem !important;
    }
    
    /* ===== HERO ===== */
    .hero-container {
        text-align: center;
        padding: 3rem 1rem 2rem;
        position: relative;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50px;
        left: 50%;
        transform: translateX(-50%);
        width: 600px;
        height: 400px;
        background: radial-gradient(ellipse, rgba(102,126,234,0.15) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(102,126,234,0.1);
        border: 1px solid rgba(102,126,234,0.25);
        padding: 0.45rem 1.2rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #a5b4fc;
        margin-bottom: 1.25rem;
        letter-spacing: 0.5px;
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #c7d2fe 0%, #a78bfa 40%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.15;
        position: relative;
        z-index: 1;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #64748b;
        margin-top: 0.75rem;
        font-weight: 400;
        letter-spacing: 0.3px;
        position: relative;
        z-index: 1;
    }
    
    /* ===== BÖLÜM BAŞLIKLARI ===== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2.5rem 0 1.5rem;
    }
    .section-icon {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(102,126,234,0.2));
        border: 1px solid rgba(124,58,237,0.2);
    }
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 0;
    }
    .section-count {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 500;
        background: rgba(255,255,255,0.05);
        padding: 0.2rem 0.7rem;
        border-radius: 50px;
        margin-left: auto;
    }
    
    /* ===== ŞEHİR BİLGİ KARTI ===== */
    .city-banner {
        background: linear-gradient(135deg, rgba(124,58,237,0.12) 0%, rgba(59,130,246,0.08) 100%);
        border: 1px solid rgba(124,58,237,0.18);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0 2rem;
        position: relative;
        overflow: hidden;
    }
    .city-banner::after {
        content: '';
        position: absolute;
        top: -30px;
        right: -30px;
        width: 120px;
        height: 120px;
        background: radial-gradient(circle, rgba(124,58,237,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .city-banner-name {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 800;
        color: #e2e8f0;
        margin-bottom: 0.3rem;
    }
    .city-banner-country {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.85rem;
        color: #a78bfa;
        font-weight: 600;
        margin-bottom: 1rem;
        background: rgba(167,139,250,0.1);
        padding: 0.3rem 0.8rem;
        border-radius: 50px;
    }
    .city-banner-info {
        font-size: 0.95rem;
        color: #94a3b8;
        line-height: 1.7;
        max-width: 600px;
    }
    
    /* ===== MEKAN KARTLARI ===== */
    .place-card {
        background: #111827;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1.5rem;
        position: relative;
    }
    .place-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 25px 60px rgba(124,58,237,0.15), 0 0 0 1px rgba(124,58,237,0.2);
    }
    
    .place-img-wrapper {
        position: relative;
        overflow: hidden;
    }
    .place-img-wrapper img {
        width: 100%;
        height: 240px;
        object-fit: cover;
        transition: transform 0.5s ease;
    }
    .place-card:hover .place-img-wrapper img {
        transform: scale(1.05);
    }
    .place-img-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 100px;
        background: linear-gradient(transparent, #111827);
    }
    
    .place-body {
        padding: 1.25rem 1.5rem 1.5rem;
    }
    .place-top-row {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        margin-bottom: 0.75rem;
    }
    .place-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        font-weight: 800;
        color: #f1f5f9;
        line-height: 1.3;
        flex: 1;
        margin-right: 0.75rem;
    }
    
    /* Puan Rozeti */
    .rating {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        color: #1a1a2e;
        font-weight: 800;
        font-size: 0.85rem;
        padding: 0.4rem 0.85rem;
        border-radius: 50px;
        white-space: nowrap;
        box-shadow: 0 4px 12px rgba(251,191,36,0.3);
    }
    
    .place-desc {
        font-size: 0.9rem;
        color: #94a3b8;
        line-height: 1.75;
        margin-top: 0.5rem;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    .place-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 1.25rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.06);
    }
    .place-city-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.78rem;
        color: #64748b;
        font-weight: 500;
    }
    .place-lang-tags {
        display: flex;
        gap: 0.4rem;
    }
    .lang-tag {
        font-size: 0.7rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        letter-spacing: 0.5px;
    }
    .lang-tr {
        background: rgba(239,68,68,0.12);
        color: #f87171;
        border: 1px solid rgba(239,68,68,0.2);
    }
    .lang-en {
        background: rgba(59,130,246,0.12);
        color: #60a5fa;
        border: 1px solid rgba(59,130,246,0.2);
    }
    
    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d1a 0%, #0a0a14 100%) !important;
        border-right: 1px solid rgba(124,58,237,0.12) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #c7d2fe !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar Logo */
    .sidebar-logo {
        text-align: center;
        padding: 1rem 0 1.5rem;
    }
    .sidebar-logo-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .sidebar-logo-text {
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #c7d2fe, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Stat Cards */
    .stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
        margin-top: 0.5rem;
    }
    .stat-card {
        background: rgba(124,58,237,0.06);
        border: 1px solid rgba(124,58,237,0.12);
        border-radius: 14px;
        padding: 1rem 0.75rem;
        text-align: center;
    }
    .stat-number {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #a78bfa, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 0.4rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* ===== DİVİDER ===== */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(124,58,237,0.25), transparent);
        margin: 1.75rem 0;
    }
    
    /* ===== BOŞ DURUM ===== */
    .empty-state {
        text-align: center;
        padding: 5rem 2rem;
    }
    .empty-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
    .empty-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        color: #475569;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .empty-text {
        color: #334155;
        font-size: 0.95rem;
    }
    
    /* ===== FOOTER ===== */
    .app-footer {
        text-align: center;
        padding: 2.5rem 1rem;
        margin-top: 4rem;
        border-top: 1px solid rgba(255,255,255,0.04);
    }
    .footer-brand {
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #334155;
        margin-bottom: 0.5rem;
    }
    .footer-sub {
        font-size: 0.8rem;
        color: #1e293b;
    }
    .footer-link {
        color: #7c3aed;
        text-decoration: none;
        font-weight: 600;
    }
    .footer-link:hover {
        color: #a78bfa;
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.2rem; }
        .city-banner { padding: 1.25rem; }
        .city-banner-name { font-size: 1.5rem; }
    }
    
    /* Streamlit element overrides */
    div[data-testid="stImage"] {
        border-radius: 16px 16px 0 0;
        overflow: hidden;
    }
    .stRadio > div {
        gap: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)


# --- VERİ ÇEKME ---
@st.cache_data(ttl=300)
def get_cities():
    try:
        res = requests.get(f"{STRAPI_URL}/api/cities?populate=*", timeout=60)
        if res.status_code == 200:
            return res.json().get("data", [])
    except Exception as e:
        st.error(f"Şehir verileri alınamadı: {e}")
    return []

@st.cache_data(ttl=300)
def get_places(city_id=None):
    try:
        url = f"{STRAPI_URL}/api/places?populate=*"
        if city_id:
            url += f"&filters[city][id][$eq]={city_id}"
        res = requests.get(url, timeout=60)
        if res.status_code == 200:
            return res.json().get("data", [])
    except Exception as e:
        st.error(f"Mekan verileri alınamadı: {e}")
    return []


# --- YARDIMCI ---
def get_image_url(place):
    try:
        kapak = place.get("Kapak_Resmi")
        if kapak:
            img_url = kapak.get("url", "")
            if img_url.startswith("/"):
                return f"{STRAPI_URL}{img_url}"
            return img_url
    except:
        pass
    return None

def extract_text(field):
    if not field:
        return ""
    if isinstance(field, str):
        return field
    if isinstance(field, list):
        texts = []
        for block in field:
            if isinstance(block, dict):
                for child in block.get("children", []):
                    if isinstance(child, dict):
                        texts.append(child.get("text", ""))
        return " ".join(texts)
    return ""

def get_city_name_for_place(place, cities):
    """Mekanın bağlı olduğu şehri bulur."""
    city_data = place.get("city")
    if city_data:
        return city_data.get("Ad", "")
    return ""


# --- ANA UYGULAMA ---
def main():
    cities = get_cities()
    all_places = get_places()
    
    # ===== SIDEBAR =====
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <div class="sidebar-logo-icon">🗺️</div>
            <div class="sidebar-logo-text">Gezi Rehberi</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Dil Seçimi
        st.markdown("### 🌐 Dil")
        lang = st.radio(
            "Dil seçin",
            ["🇹🇷 Türkçe", "🇬🇧 English"],
            index=0,
            horizontal=True,
            label_visibility="collapsed"
        )
        is_turkish = "Türkçe" in lang
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Şehir Filtresi
        st.markdown("### 🏙️ " + ("Şehir Filtresi" if is_turkish else "City Filter"))
        
        all_label = "Tüm Şehirler" if is_turkish else "All Cities"
        city_options = [all_label]
        city_map = {}
        for c in cities:
            name = c.get("Ad", "Bilinmeyen")
            country = c.get("Ulke", "")
            label = f"{name}, {country}" if country else name
            city_options.append(label)
            city_map[label] = c.get("id") if "id" in c else c.get("documentId")
        
        selected = st.selectbox(
            "Şehir seçin" if is_turkish else "Select a city",
            city_options,
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # İstatistikler
        st.markdown("### 📊 " + ("İstatistikler" if is_turkish else "Statistics"))
        st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{len(cities)}</div>
                <div class="stat-label">{"Şehir" if is_turkish else "Cities"}</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(all_places)}</div>
                <div class="stat-label">{"Mekan" if is_turkish else "Places"}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align:center;padding:1rem 0;">
            <div style="font-size:0.7rem;color:#334155;text-transform:uppercase;letter-spacing:2px;font-weight:600;">
                BIP210 • İçerik Yönetimi
            </div>
            <div style="font-size:0.65rem;color:#1e293b;margin-top:0.3rem;">
                Final Projesi — 2026
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== ANA İÇERİK =====
    
    # Hero
    st.markdown(f"""
    <div class="hero-container">
        <div class="hero-badge">✨ {"YZ Destekli • Çok Dilli • Dinamik" if is_turkish else "AI-Powered • Multi-Language • Dynamic"}</div>
        <h1 class="hero-title">{"Gezi Rehberi" if is_turkish else "Travel Guide"}</h1>
        <p class="hero-subtitle">{"Dünyanın en güzel şehirlerini ve mekanlarını keşfedin" if is_turkish else "Discover the most beautiful cities and places around the world"}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtreleme
    selected_city_id = None
    if selected and selected not in ["Tüm Şehirler", "All Cities"]:
        selected_city_id = city_map.get(selected)
    
    # Seçili Şehir Bannerı
    if selected_city_id:
        for c in cities:
            cid = c.get("id") if "id" in c else c.get("documentId")
            if cid == selected_city_id:
                city_info = extract_text(c.get("Kisa_Bilgi"))
                st.markdown(f"""
                <div class="city-banner">
                    <div class="city-banner-name">📍 {c.get("Ad", "")}</div>
                    <div class="city-banner-country">🌍 {c.get("Ulke", "")}</div>
                    <div class="city-banner-info">{city_info}</div>
                </div>
                """, unsafe_allow_html=True)
                break
    
    # Mekanları getir
    places = get_places(selected_city_id) if selected_city_id else all_places
    
    # Bölüm Başlığı
    place_count = len(places)
    st.markdown(f"""
    <div class="section-header">
        <div class="section-icon">🏛️</div>
        <h2 class="section-title">{"Keşfedilecek Mekanlar" if is_turkish else "Places to Discover"}</h2>
        <div class="section-count">{place_count} {"mekan" if is_turkish else "places"}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mekan Kartları
    if not places:
        st.markdown(f"""
        <div class="empty-state">
            <div class="empty-icon">🔍</div>
            <div class="empty-title">{"Henüz mekan bulunamadı" if is_turkish else "No places found"}</div>
            <div class="empty-text">{"Bu şehir için kayıtlı mekan bulunmuyor." if is_turkish else "No places registered for this city."}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(2, gap="large")
        for idx, place in enumerate(places):
            with cols[idx % 2]:
                img_url = get_image_url(place)
                desc = extract_text(place.get("Aciklama"))
                name = place.get("Mekan_Adi", "Bilinmeyen Mekan")
                puan = place.get("Puan", 0)
                city_name = get_city_name_for_place(place, cities)
                
                # Görsel
                if img_url:
                    st.image(img_url, width="stretch")
                
                # Kart İçeriği
                st.markdown(f"""
                <div class="place-body">
                    <div class="place-top-row">
                        <div class="place-name">{name}</div>
                        <div class="rating">⭐ {puan}</div>
                    </div>
                    <div class="place-desc">{desc if desc else ("Açıklama mevcut değil." if is_turkish else "No description available.")}</div>
                    <div class="place-footer">
                        <div class="place-city-tag">📍 {city_name}</div>
                        <div class="place-lang-tags">
                            <span class="lang-tag lang-tr">TR</span>
                            <span class="lang-tag lang-en">EN</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("")
    
    # Footer
    st.markdown(f"""
    <div class="app-footer">
        <div class="footer-brand">🌍 {"Gezi Rehberi Sistemi" if is_turkish else "Travel Guide System"}</div>
        <div class="footer-sub">
            {"YZ Destekli, Çok Dilli ve Dinamik Gezi Rehberi" if is_turkish else "AI-Powered, Multi-Language and Dynamic Travel Guide"}
            <br>
            BIP210 İçerik Yönetimi — Final Projesi
            <br>
            <a href="{STRAPI_URL}/admin" target="_blank" class="footer-link">Strapi Admin Panel</a>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
