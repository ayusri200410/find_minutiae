🛠️ Langkah-Langkah Wajib untuk Laptop Baru
Anda akan memerlukan Python 3.7 dan file requirements.txt yang Anda buat. Jika Anda belum membuat file tersebut, gunakan perintah ini di lingkungan lama Anda: pip freeze > requirements.txt.

**PERSIAPAN: Buat Folder baru bernama "models" pada project root, dan di dalam folder tersebut di isi dengan Model:**
  - ClassifyNet_6_classes.h5: https://drive.google.com/file/d/1roV9m5fBUdhuLBFTAWKiz6aHcu_1ulhz/view?usp=sharing
  - CoarseNet.h5: https://drive.google.com/file/d/136657mmIpoEP8omWEptlq5oZdQjvxJYb/view?usp=drive_link
  - CoreNet.weights: https://drive.google.com/file/d/1bxlkJXIunbCNVPFQpqQBSgqE-nnURb3v/view?usp=drive_link
  - FineNet.h5: https://drive.google.com/file/d/1RDxPikWtwDiP02GiOxbnmrqJEInRwWd1/view?usp=drive_link

**Langkah 1: Instal Python 3.7**
  - Instal versi Python yang sama persis yang terbukti bekerja (Python 3.7) untuk memastikan kompatibilitas SciPy 1.2.1.
  - Instal Python 3.7.9 (64-bit): Unduh dan instal versi ini dari situs web Python (pilih Windows x86-64 executable installer). Pastikan instalasi diatur ke jalur yang mudah diingat (misalnya, C:\Python37).

**Langkah 2: Buat Virtual Environment Baru**
  - Buat virtual environment menggunakan instalasi Python 3.7 yang baru.
  - Buka Terminal/CMD di folder aplikasi Anda.
  - Buat Venv: Ganti C:\Path\To\Python37\python.exe dengan jalur instalasi Python 3.7 Anda.
    -> "C:\Path\To\Python37\python.exe" -m venv venv_fingerflow_37_new
  - Aktifkan Venv:
    ->  venv_fingerflow_37_new\Scripts\activate

**Langkah 3: Instalasi Dependency Krusial (Memperbaiki Konflik Lama)**
  - Kita akan menginstal paket secara terpisah untuk memastikan kita mengunci versi yang benar-benar krusial sebelum yang lain.
  - Instal TensorFlow dan Protobuf: Ini memperbaiki konflik Protobuf yang kita temui.
    -> pip install tensorflow==2.5.0 protobuf==3.20.3
  - Instal SciPy dan NumPy: Ini memperbaiki error multichannel dan typeDict.
    -> pip install scipy==1.2.1 numpy==1.19.5
    
**Langkah 4: Instal Sisa Dependencies**
  - Daripada menggunakan requirements.txt sepenuhnya, kita akan menginstal sisa library yang kita temukan hilang satu per satu, dengan menambahkan flag --no-deps pada fingerflow untuk menjaga SciPy 1.2.1 tetap    aman.
  - Instal Fingerflow dan Sisanya dengan Perlindungan:
    -> pip install fingerflow --no-deps
    -> pip install scikit-image pandas pytz keras-applications customtkinter opencv-python matplotlib
    
**Langkah 5: Uji Coba**
- Jalankan aplikasi Anda:
  -> python main.py
- Dengan mengikuti langkah-langkah ini, Anda menduplikasi lingkungan kerja yang proven dan menghindari semua jebakan dependency yang sudah kita selesaikan bersama. Selamat!
