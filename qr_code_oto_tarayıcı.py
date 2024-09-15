import cv2
from pyzbar.pyzbar import decode
import pyperclip
import numpy as np
import webbrowser

def scan_qr_code():
    # Kamera erişimi (0, varsayılan kamerayı açar)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Kamera açılamadı. Lütfen kameranın bağlı olduğundan emin olun.")
        return
    
    opened_urls = set()  # Açılmış URL'leri takip etmek için bir küme
    
    while True:
        # Kameradan bir kare oku
        ret, frame = cap.read()

        # Eğer kare alınamadıysa, döngüye devam et
        if not ret:
            print("Kare okunamadı, kamerayı kontrol edin.")
            continue
        
        # QR kodlarını tara
        qr_codes = decode(frame)
        
        for qr_code in qr_codes:
            # QR kodun içindeki veriyi oku
            qr_data = qr_code.data.decode('utf-8')
            print(f'Taranan QR kodu: {qr_data}')
            
            # Veriyi panoya kopyala
            pyperclip.copy(qr_data)
            print("Veri panoya kopyalandı!")
            
            # Eğer taranan veri bir URL ise, tarayıcıda aç
            if qr_data.startswith("http://") or qr_data.startswith("https://"):
                if qr_data not in opened_urls:
                    webbrowser.open(qr_data)
                    opened_urls.add(qr_data)  # URL'yi küme ekle
                    print("Taranan link tarayıcıda açılıyor.")
            
            # QR kodun çevresine bir dikdörtgen çiz
            points = qr_code.polygon
            if len(points) == 4:
                pts = [(point.x, point.y) for point in points]
                pts = np.array(pts, dtype=np.int32)
                cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
        
        # Kameradan gelen görüntüyü göster
        cv2.imshow('QR Kod Tarayıcı', frame)
        
        # 'q' tuşuna basarak çıkış yapın
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Kamerayı ve pencereyi kapat
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_qr_code()
