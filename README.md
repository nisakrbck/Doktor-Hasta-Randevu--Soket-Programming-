# 🩺 Doktor-Hasta Randevu Sistemi (TCP & UDP Soket Programlama)  

Bu proje, Python kullanılarak geliştirilen bir **doktor-hasta randevu simülasyon sistemidir**. Sistem, TCP ve UDP istemcilerinin aynı sunucuya bağlanabildiği çok istemcili bir yapıya sahiptir.  
Doktorlar TCP üzerinden, hastalar UDP üzerinden bağlanarak randevu sürecine katılır.  
Sistem, threading, socket programlama, zaman aşımı gibi kavramları pratiğe dökmek için geliştirilmiştir.


## 🎯 Amaç

- TCP ve UDP protokollerinin farklarını uygulamalı göstermek  
- Threading ile aynı anda birden fazla istemciyi yönetebilmek  
- Timeout ve eşzamanlı mesajlaşma mantığını kavratmak  
- Soket programlamayı gerçek bir senaryo ile uygulamak  


## 🧠 Sistem Mimarisi

- ### Sunucu (Server)
- Aynı anda TCP ve UDP bağlantıları kabul eder  
- Doktorları ve hastaları sırayla karşılar  
- Randevu eşleştirmesini ve sonuç bildirimini yönetir  

### Doktor (TCP Client)
- TCP üzerinden bağlanır  
- "Hasta Kabul" komutu ile sıradaki hastayı çağırır  
- Hasta randevuyu kabul ederse kaydedilir
  
### Hasta (UDP Client)
- UDP ile bağlanır  
- Randevu çağrısı gelirse 10 saniye içinde kabul/red yanıtı verir  
- Randevu sonucu ekranda gösterilir  

📌 Notlar
Bu proje, "Bilgisayar Ağları" dersi kapsamında geliştirilmiştir.
Socket programlama, protokol farkları ve bağlantı yönetimi konularını öğretmeye yöneliktir.

---

# 🩺 Doctor-Patient Appointment System (TCP & UDP Socket Programming)

This project is a **doctor-patient appointment simulation system** developed in Python.  
It supports a multi-client structure where both TCP and UDP clients can connect to the same server.  
Doctors connect via TCP, patients via UDP, and the server handles the appointment management process.  
The system is designed to practice concepts like threading, socket programming, and timeout handling.


## 🎯 Purpose

- Demonstrate the differences between TCP and UDP through a practical simulation  
- Handle multiple clients simultaneously using threads  
- Understand timeout management and real-time interaction  
- Practice socket programming with a realistic scenario  


## 🧠  System Architecture

### Server
- Accepts both TCP and UDP connections concurrently  
- Identifies and separates doctor and patient clients  
- Handles appointment matching and notification  

### Doctor (TCP Client)
- Connects via TCP  
- Uses "Hasta Kabul" (Call Patient) command to request the next patient  
- If the patient accepts, it is recorded as an appointment  

### Patient (UDP Client)
- Connects via UDP  
- If called by a doctor, responds within 10 seconds (Yes/No)  
- The result of the appointment is shown on screen



📌 Notes

This project was developed as part of a Computer Networks course.
It is aimed at teaching socket programming, protocol differences, and connection handling.
