import requests
import time
from deep_translator import GoogleTranslator

STRAPI_URL = "https://gezi-rehberi-backend-9nmq.onrender.com"
STRAPI_TOKEN = "e7e1fbc3ef414ab0992d663b4da0b8a01ddc34354213dd699df37ba92e1db0103bdacd0e43cae8420d4182a7427034d2a35017913675070e05f1d4d2cd012b67d33061e410745b1d825aef1f9eba935cdf49cf32820968ad69537fede31173706519bda42a11ea45d23c12bd6da68bb61c9c9484f9dc1d6c92674fc76fc303be" 

HEADERS = {
    "Authorization": f"Bearer {STRAPI_TOKEN}"
}

def fetch_travel_data():
    print("[1/5] Gezi verileri alınıyor...")
    return [
        {
            "city_name": "Istanbul",
            "city_country": "Turkiye",
            "city_info": "Asya ve Avrupa'yı birleştiren tarihi metropol.",
            "place_name": "Ayasofya Camii",
            "base_desc": "Tarihi yarımadada bulunan, dünya mimarlık tarihinin en önemli anıtlarından biri."
        },
        {
            "city_name": "Tokyo",
            "city_country": "Japonya",
            "city_info": "Geleneksel kültür ile ultra modern yaşamın harmanlandığı başkent.",
            "place_name": "Shibuya Kavsagi",
            "base_desc": "Dünyanın en yoğun yaya trafiğine sahip, Tokyo'nun modern yüzünü temsil eden neon ışıklı devasa kavşak."
        }
    ]

def enrich_and_translate_text(base_desc, place_name):
    print(f"[2/5] '{place_name}' için metin hazırlanıyor...")
    enriched_tr = f"{base_desc} Bu eşsiz mekan, her yıl milyonlarca yerli ve yabancı turisti ağırlamakta olup, şehrin kültürel dokusunu en iyi yansıtan noktalardan biridir."
    try:
        enriched_en = GoogleTranslator(source='tr', target='en').translate(enriched_tr)
    except Exception as e:
        print(f"  Çeviri hatası: {e}")
        enriched_en = "A wonderful place to visit with rich history and cultural importance."
    return enriched_tr, enriched_en

def generate_and_download_image(place_name):
    print(f"[3/5] '{place_name}' için görsel indiriliyor...")
    safe_prompt_name = place_name.replace('ı','i').replace('ğ','g').replace('ş','s').replace('ç','c').replace('ö','o').replace('ü','u')
    prompt = f"professional travel photography of {safe_prompt_name}, highly detailed, scenic, tourist destination"
    encoded_prompt = requests.utils.quote(prompt)
    
    pollinations_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=768"
    
    try:
        response = requests.get(pollinations_url, timeout=20)
        if response.status_code == 200 and len(response.content) > 1000:
            print("  Görsel başarıyla indirildi.")
            return response.content
        else:
            print(f"  Ana servis yanıtlamadı (Kod: {response.status_code}). Yedek kaynağa bağlanılıyor...")
            backup_url = f"https://images.unsplash.com/photo-1524230572899-a752b3835840?q=80&w=1024&auto=format&fit=crop"
            if "ayasofya" in safe_prompt_name.lower():
                backup_url = "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?q=80&w=1024&auto=format&fit=crop"
            elif "shibuya" in safe_prompt_name.lower():
                backup_url = "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?q=80&w=1024&auto=format&fit=crop"
                
            backup_res = requests.get(backup_url, timeout=20)
            if backup_res.status_code == 200:
                print("  Yedek kaynaktan görsel alındı.")
                return backup_res.content
    except Exception as e:
        print(f"  Görsel indirme hatası: {e}")
    return None

def upload_image_to_strapi(img_content, file_name):
    print(f"[4/5] '{file_name}' Strapi'ye yükleniyor...")
    upload_url = f"{STRAPI_URL}/api/upload"
    
    files = {
        'files': (file_name, img_content, 'image/jpeg')
    }
    
    try:
        res = requests.post(upload_url, headers=HEADERS, files=files, timeout=30)
        if res.status_code in [200, 201]:
            media_id = res.json()[0]['id']
            print(f"  Görsel yüklendi. Medya ID: {media_id}")
            return media_id
        else:
            print(f"  Yükleme hatası. Durum kodu: {res.status_code}")
    except Exception as e:
        print(f"  Bağlantı hatası: {e}")
    return None

def save_data_to_strapi(city_data, tr_desc, en_desc, media_id):
    print("[5/5] Veriler veritabanına kaydediliyor...")
    
    try:
        city_check_res = requests.get(f"{STRAPI_URL}/api/cities?filters[Ad][$eq]={city_data['city_name']}", headers=HEADERS)
        city_check = city_check_res.json()
        
        if city_check.get('data') and len(city_check['data']) > 0:
            city_id = city_check['data'][0]['id']
        else:
            city_payload = {"data": {"Ad": city_data["city_name"], "Ulke": city_data["city_country"], "Kisa_Bilgi": city_data["city_info"]}}
            city_res = requests.post(f"{STRAPI_URL}/api/cities", headers=HEADERS, json=city_payload)
            city_id = city_res.json()['data']['id']

        place_payload_tr = {
            "data": {
                "Mekan_Adi": city_data["place_name"],
                "Aciklama": tr_desc,
                "Puan": 4.9,
                "Kapak_Resmi": media_id,
                "city": city_id,
                "locale": "tr"
            }
        }
        place_res_tr = requests.post(f"{STRAPI_URL}/api/places", headers=HEADERS, json=place_payload_tr)
        
        if place_res_tr.status_code in [200, 201]:
            print(f"  '{city_data['place_name']}' (TR) kaydedildi.")
            
            place_payload_en = {
                "data": {
                    "Mekan_Adi": city_data["place_name"],
                    "Aciklama": en_desc,
                    "Puan": 4.9,
                    "Kapak_Resmi": media_id,
                    "city": city_id,
                    "locale": "en"
                }
            }
            place_res_en = requests.post(f"{STRAPI_URL}/api/places", headers=HEADERS, json=place_payload_en)
            
            if place_res_en.status_code in [200, 201]:
                print(f"  '{city_data['place_name']}' (EN) kaydedildi.")
            else:
                print(f"  EN kayıt hatası: {place_res_en.text}")
        else:
            print(f"  TR kayıt hatası: {place_res_tr.text}")
            
    except Exception as e:
        print(f"  Veritabanı hatası: {e}")

def main():
    raw_data = fetch_travel_data()
    
    for item in raw_data:
        print(f"\n--- {item['place_name']} ---")
        tr_desc, en_desc = enrich_and_translate_text(item["base_desc"], item["place_name"])
        img_content = generate_and_download_image(item["place_name"])
        
        if img_content:
            file_name = f"{item['place_name'].lower().replace(' ', '_')}.jpg"
            media_id = upload_image_to_strapi(img_content, file_name)
            
            if media_id:
                save_data_to_strapi(item, tr_desc, en_desc, media_id)
        else:
            print("  Görsel alınamadı, atlanıyor.")
            
        time.sleep(2)
    print("\nTamamlandı.")

if __name__ == "__main__":
    main()