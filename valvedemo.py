import time
import pandas as pd
import cloudscraper
from bs4 import BeautifulSoup
from tkinter import filedialog, messagebox
import tkinter as tk
import threading

# Global değişkenler
is_running = False
products = []

def show_info_message(title, message):
    messagebox.showinfo(title, message)

def show_error_message(title, message):
    messagebox.showerror(title, message)

def start_automation():
    global is_running
    if is_running:
        messagebox.showinfo("Bilgi", "Otomasyon zaten çalışıyor.")
        print("Otomasyon zaten çalışıyor.")
        return
    is_running = True
    print("Otomasyon başlatılıyor...")
    threading.Thread(target=scrape_data).start()

def stop_automation():
    global is_running
    if is_running:
        is_running = False
        messagebox.showinfo("Bilgi", "Otomasyon durduruldu.")
        print("Otomasyon durduruldu.")
    else:
        messagebox.showinfo("Bilgi", "Otomasyon çalışmıyor.")
        print("Otomasyon çalışmıyor.")

def scrape_data():
    global is_running
    global products
    products = []
    print("Veri çekme işlemi başladı...")

    # cloudscraper örneği oluştur
    scraper = cloudscraper.create_scraper()

    url = "https://store.steampowered.com/search/?supportedlang=turkish&os=win&specials=1&hidef2p=1&filter=topsellers&ndl=1"
    response = scraper.get(url)
    print(f"URL '{url}' adresine istek gönderildi. Status code: {response.status_code}")

    if response.status_code != 200:
        root.after(0, show_error_message, "Error", "Failed to retrieve data from Steam.")
        print("Hata: Steam'den veri alınamadı.")
        is_running = False
        return

    soup = BeautifulSoup(response.content, 'lxml')
    print("HTML içeriği başarıyla alındı ve parse edildi.")

    # <a> etiketlerindeki verileri işleyelim
    game_links = soup.select('a.search_result_row')
    print(f"{len(game_links)} adet oyun bulundu.")
    for idx, a_tag in enumerate(game_links):
        if not is_running:
            print("Otomasyon durduruldu. Veri çekme işlemi sonlandırılıyor...")
            break

        # Oyun adı
        name_span = a_tag.select_one("div.responsive_search_name_combined > div.col.search_name.ellipsis > span.title")
        game_name = name_span.text.strip() if name_span else 'N/A'

        # Fiyat bilgisi
        price_container = a_tag.select_one("div.discount_block.search_discount_block")
        if price_container:
            discount_final = price_container.select_one('div.discount_final_price')
            discount_original = price_container.select_one('div.discount_original_price')
            discount_pct = price_container.select_one('div.discount_pct')

            final_price = discount_final.text.strip() if discount_final else 'N/A'
            original_price = discount_original.text.strip() if discount_original else 'N/A'
            discount_percentage = discount_pct.text.strip() if discount_pct else 'N/A'
        else:
            # Eğer indirim yoksa final fiyat normal fiyattır
            final_price_element = a_tag.select_one("div.col.search_price_discount_combined.responsive_secondrow")
            final_price = final_price_element.text.strip() if final_price_element else 'N/A'
            original_price = 'N/A'
            discount_percentage = 'N/A'

        # Oyun resmi
        img_tag = a_tag.select_one("div.search_capsule img")
        img_src = img_tag['src'] if img_tag and 'src' in img_tag.attrs else 'N/A'

        # Oyun linki
        game_url = a_tag['href']
        print(f"Oyun {idx+1}: {game_name}, URL: {game_url}")

        # Oyun sayfasından video linkini alalım
        game_response = scraper.get(game_url)
        print(f"Oyun sayfası '{game_url}' adresine istek gönderildi. Status code: {game_response.status_code}")

        if game_response.status_code != 200:
            print(f"Hata: '{game_name}' oyun sayfasından veri alınamadı.")
            product_video = 'N/A'
        else:
            game_soup = BeautifulSoup(game_response.content, 'lxml')
            highlight_div = game_soup.find('div', class_='highlight_movie')
            if highlight_div and highlight_div.has_attr('data-webm-source'):
                product_video = highlight_div['data-webm-source']
                print(f"Video linki bulundu: {product_video}")
            else:
                print(f"Video linki bulunamadı: {game_name}")
                product_video = 'N/A'

        # Oyun bilgilerini log olarak yazdır
        print(f"Game: {game_name}, Final Price: {final_price}, Original Price: {original_price}, Discount: {discount_percentage}")

        # Veriyi listeye ekleyelim
        product = {
            "product_Name": game_name,
            "product_Img": img_src,
            "product_downsale": discount_percentage,
            "old_price": original_price,
            "new_price": final_price,
            "product_video": product_video
        }
        products.append(product)
        print(f"Ürün {idx+1} işlendi.\n")

    if is_running:
        is_running = False
        root.after(0, show_info_message, "Başarılı", "Veriler başarıyla çekildi.")
        print("Veriler başarıyla çekildi.")
    else:
        root.after(0, show_info_message, "Bilgi", "Otomasyon durduruldu.")
        print("Otomasyon durduruldu.")

def get_data():
    if is_running:
        messagebox.showinfo("Bilgi", "Lütfen verilerin çekilmesi tamamlanana kadar bekleyin.")
        print("Verilerin çekilmesi tamamlanana kadar bekleyin.")
        return
    if not products:
        messagebox.showinfo("Bilgi", "Kaydedilecek veri yok.")
        print("Kaydedilecek veri yok.")
        return
    # Kullanıcıdan dosya adı al
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        print(f"Veriler '{file_path}' dosyasına kaydediliyor...")
        with open(file_path, 'w', encoding='utf-8') as f:
            for idx, product in enumerate(products):
                line = f'Steam\'de "{product["product_Name"]}", "{product["product_downsale"]}" indirimli! "{product["old_price"]}" yerine "{product["new_price"]}" — sakın kaçırmayın!\n'
                line += f'{product["product_Img"]}\n'
                line += f'{product["product_video"]}\n\n'
                f.write(line)
                print(f"Ürün {idx+1} kaydedildi.")
        messagebox.showinfo("Başarılı", "Veriler başarıyla kaydedildi.")
        print("Veriler başarıyla kaydedildi.")
    else:
        print("Kaydetme işlemi iptal edildi.")

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Steam Otomasyonu")
root.geometry("400x200")

# Butonları oluştur
start_button = tk.Button(root, text="Otomasyonu Başlat", command=start_automation, width=20)
stop_button = tk.Button(root, text="Durdur", command=stop_automation, width=20)
get_data_button = tk.Button(root, text="Verileri Al", command=get_data, width=20)

# Butonları yerleştir
start_button.pack(pady=10)
stop_button.pack(pady=10)
get_data_button.pack(pady=10)

print("Uygulama başlatıldı.")

# Uygulamayı çalıştır
root.mainloop()
