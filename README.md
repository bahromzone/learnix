# 🎓 Learnix — O'quv Markazi CRM Tizimi

Learnix — o'quv markazlari uchun mo'ljallangan zamonaviy CRM tizimi. O'quvchilar, o'qituvchilar, guruhlar va to'lovlarni boshqarishni soddalashtiradi.

---

## 🚀 Asosiy imkoniyatlar

- 👨‍🎓 **O'quvchilar boshqaruvi** — ro'yxatga olish, ma'lumotlarni tahrirlash, holat kuzatuvi
- 👨‍🏫 **O'qituvchilar boshqaruvi** — profil, dars jadvali, ish haqi hisobi
- 📚 **Guruhlar boshqaruvi** — guruh yaratish, o'quvchi biriktirish, jadval tuzish
- 💰 **To'lovlar tizimi** — oylik to'lovlarni kuzatish, qarzdorlar ro'yxati
- 📊 **Hisobotlar** — davomat, moliyaviy statistika, o'sish grafiklari
- 🔔 **Bildirishnomalar** — to'lov eslatmalari, dars o'zgarishlari
- 🔐 **Autentifikatsiya** — JWT asosida xavfsiz kirish tizimi

---

## 🛠️ Texnologiyalar

| Qatlam | Texnologiya |
|--------|-------------|
| Backend | Python, Flask |
| Ma'lumotlar bazasi | MySQL |
| Autentifikatsiya | JWT, bcrypt |
| Real-time | Flask-SocketIO |
| API | RESTful API |

---

## 📦 O'rnatish

### Talablar
- Python 3.11+
- MySQL 8.0+
- Git

### Qadamlar

```bash
# 1. Reponi klonlash
git clone https://github.com/bahromzone/learnix.git
cd learnix

# 2. Virtual muhit yaratish
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac

# 3. Paketlarni o'rnatish
pip install -r requirements.txt

# 4. .env faylini sozlash
cp .env.example .env
# .env faylini o'zingizga mos tahrirlang

# 5. Ma'lumotlar bazasini sozlash
flask db upgrade

# 6. Serverni ishga tushirish
flask run
```

---

## ⚙️ Muhit sozlamalari (.env)

```env
SECRET_KEY=your_secret_key
DATABASE_URL=mysql+aiomysql://user:password@localhost/learnix
JWT_SECRET_KEY=your_jwt_secret
```

---

## 📁 Loyiha tuzilmasi

```
learnix/
├── app/
│   ├── models/        # Ma'lumotlar bazasi modellari
│   ├── routes/        # API endpointlar
│   ├── services/      # Biznes logika
│   └── utils/         # Yordamchi funksiyalar
├── migrations/        # DB migratsiyalari
├── tests/             # Testlar
├── .env.example       # Muhit o'zgaruvchilari namunasi
├── requirements.txt   # Python paketlari
└── README.md
```

---

## 📡 API Endpointlar

| Method | Endpoint | Tavsif |
|--------|----------|--------|
| POST | `/auth/login` | Tizimga kirish |
| GET | `/students` | O'quvchilar ro'yxati |
| POST | `/students` | Yangi o'quvchi qo'shish |
| GET | `/groups` | Guruhlar ro'yxati |
| POST | `/payments` | To'lov qabul qilish |
| GET | `/reports/finance` | Moliyaviy hisobot |

---

## 🤝 Hissa qo'shish

1. Reponi fork qiling
2. Yangi branch yarating (`git checkout -b feature/yangi-imkoniyat`)
3. O'zgarishlarni commit qiling (`git commit -m "Yangi imkoniyat qo'shildi"`)
4. Branch ga push qiling (`git push origin feature/yangi-imkoniyat`)
5. Pull Request oching

---

## 📄 Litsenziya

Bu loyiha [MIT](LICENSE) litsenziyasi ostida tarqatiladi.

---

## 📞 Aloqa

- GitHub: [@bahromzone](https://github.com/bahromzone)

---

<p align="center">Learnix — O'qishni boshqarish, kelajakni qurish 🚀</p>
