"""English and Arabic translations for the 1,284 Iranian medical centers,
31 provinces, 60 ownership categories, 418 cities, and 155 featured logo cards ([t288u]).
"""
import json
import re
from pathlib import Path

ROOT = Path('/workspace/abadis-med-website-redesign')

PROV_EN = {
    'آذربایجان شرقی': 'East Azerbaijan',
    'آذربایجان غربی': 'West Azerbaijan',
    'اردبیل': 'Ardabil',
    'اصفهان': 'Isfahan',
    'البرز': 'Alborz',
    'ایلام': 'Ilam',
    'بوشهر': 'Bushehr',
    'تهران': 'Tehran',
    'چهارمحال و بختیاری': 'Chaharmahal & Bakhtiari',
    'خراسان جنوبی': 'South Khorasan',
    'خراسان رضوی': 'Razavi Khorasan',
    'خراسان شمالی': 'North Khorasan',
    'خوزستان': 'Khuzestan',
    'زنجان': 'Zanjan',
    'سمنان': 'Semnan',
    'سیستان و بلوچستان': 'Sistan & Baluchestan',
    'فارس': 'Fars',
    'قزوین': 'Qazvin',
    'قم': 'Qom',
    'کردستان': 'Kurdistan',
    'کرمان': 'Kerman',
    'کرمانشاه': 'Kermanshah',
    'کهگیلویه و بویراحمد': 'Kohgiluyeh & Boyer-Ahmad',
    'گلستان': 'Golestan',
    'گیلان': 'Gilan',
    'لرستان': 'Lorestan',
    'مازندران': 'Mazandaran',
    'مرکزی': 'Markazi',
    'هرمزگان': 'Hormozgan',
    'همدان': 'Hamadan',
    'یزد': 'Yazd',
}

PROV_AR = {
    'آذربایجان شرقی': 'أذربيجان الشرقية',
    'آذربایجان غربی': 'أذربيجان الغربية',
    'اردبیل': 'أردبيل',
    'اصفهان': 'أصفهان',
    'البرز': 'ألبرز',
    'ایلام': 'إيلام',
    'بوشهر': 'بوشهر',
    'تهران': 'طهران',
    'چهارمحال و بختیاری': 'جهارمحال وبختياري',
    'خراسان جنوبی': 'خراسان الجنوبية',
    'خراسان رضوی': 'خراسان الرضوية',
    'خراسان شمالی': 'خراسان الشمالية',
    'خوزستان': 'خوزستان',
    'زنجان': 'زنجان',
    'سمنان': 'سمنان',
    'سیستان و بلوچستان': 'سيستان وبلوشستان',
    'فارس': 'فارس',
    'قزوین': 'قزوين',
    'قم': 'قم',
    'کردستان': 'كردستان',
    'کرمان': 'كرمان',
    'کرمانشاه': 'كرمانشاه',
    'کهگیلویه و بویراحمد': 'كهكيلويه وبوير أحمد',
    'گلستان': 'غلستان',
    'گیلان': 'جيلان',
    'لرستان': 'لرستان',
    'مازندران': 'مازندران',
    'مرکزی': 'مركزي',
    'هرمزگان': 'هرمزغان',
    'همدان': 'همدان',
    'یزد': 'يزد',
}

OWN_EN_SINGLE = {
    'ارتش': 'Army Medical Command',
    'بنیاد شهید': 'Martyrs Foundation',
    'تامین اجتماعی': 'Social Security Org.',
    'خصوصی': 'Private Sector',
    'خیریه': 'Charity Foundation',
    'دانشگاه آزاد': 'Islamic Azad University',
    'دانشگاه شاهد': 'Shahed University',
    'دانشگاهی؛ نیازمند بررسی': 'University Affiliated',
    'دولتی': 'Public / Government',
    'سپاه': 'IRGC Medical Command',
    'شرکت نفت': 'National Iranian Oil Co. (NIOC)',
    'عمومی؛ نوع نهاد نیازمند بررسی': 'Public Institution',
    'فراجا': 'Police Command (FARAJA)',
    'قوه قضائیه': 'Judiciary Organization',
    'ناجا': 'Law Enforcement (NAJA)',
    'نامشخص': '',
}

OWN_AR_SINGLE = {
    'ارتش': 'الخدمات الطبية للجيش',
    'بنیاد شهید': 'مؤسسة الشهيد',
    'تامین اجتماعی': 'منظمة التأمين الاجتماعي',
    'خصوصی': 'قطاع خاص',
    'خیریه': 'مؤسسة خيرية',
    'دانشگاه آزاد': 'الجامعة الإسلامية الحرة',
    'دانشگاه شاهد': 'جامعة شاهد',
    'دانشگاهی؛ نیازمند بررسی': 'جامعي',
    'دولتی': 'حكومي',
    'سپاه': 'الخدمات الطبية للحرس',
    'شرکت نفت': 'شركة النفط الوطنية',
    'عمومی؛ نوع نهاد نیازمند بررسی': 'مؤسسة عامة',
    'فراجا': 'قيادة الشرطة',
    'قوه قضائیه': 'السلطة القضائية',
    'ناجا': 'قوى الأمن الداخلي',
    'نامشخص': '',
}

CITY_DICT = {
    'تهران': 'Tehran', 'مشهد': 'Mashhad', 'اصفهان': 'Isfahan', 'شیراز': 'Shiraz',
    'تبریز': 'Tabriz', 'کرج': 'Karaj', 'اهواز': 'Ahvaz', 'قم': 'Qom',
    'کرمانشاه': 'Kermanshah', 'ارومیه': 'Urmia', 'رشت': 'Rasht', 'زاهدان': 'Zahedan',
    'همدان': 'Hamadan', 'کرمان': 'Kerman', 'یزد': 'Yazd', 'اردبیل': 'Ardabil',
    'بندرعباس': 'Bandar Abbas', 'اراک': 'Arak', 'اسلامشهر': 'Eslamshahr', 'زنجان': 'Zanjan',
    'سنندج': 'Sanandaj', 'قزوین': 'Qazvin', 'خرم‌آباد': 'Khorramabad', 'خرم آباد': 'Khorramabad',
    'گرگان': 'Gorgan', 'ساری': 'Sari', 'بجنورد': 'Bojnurd', 'بوشهر': 'Bushehr',
    'بیرجند': 'Birjand', 'ایلام': 'Ilam', 'شهرکرد': 'Shahrekord', 'یاسوج': 'Yasuj',
    'سمنان': 'Semnan', 'آبادان': 'Abadan', 'خرمشهر': 'Khorramshahr', 'دزفول': 'Dezful',
    'کاشان': 'Kashan', 'بابل': 'Babol', 'آمل': 'Amol', 'قائم‌شهر': 'Qaemshahr', 'قائمشهر': 'Qaemshahr',
    'نیشابور': 'Neyshabur', 'سبزوار': 'Sabzevar', 'تربت حیدریه': 'Torbat-e Heydarieh',
    'قوچان': 'Quchan', 'گناباد': 'Gonabad', 'کاشمر': 'Kashmar', 'مراغه': 'Maragheh',
    'مرند': 'Marand', 'میانه': 'Mianeh', 'اهر': 'Ahar', 'بناب': 'Bonab', 'سراب': 'Sarab',
    'خوی': 'Khoy', 'مهاباد': 'Mahabad', 'میاندوآب': 'Miandoab', 'بوکان': 'Bukan',
    'سلماس': 'Salmas', 'پیرانشهر': 'Piranshahr', 'نقده': 'Naqadeh', 'ماکو': 'Maku',
    'پارس‌آباد': 'Parsabad', 'مشگین‌شهر': 'Meshginshahr', 'خلخال': 'Khalkhal',
    'نجف‌آباد': 'Najafabad', 'خمینی‌شهر': 'Khomeynishahr', 'شاهین‌شهر': 'Shahinshahr',
    'شهرضا': 'Shahreza', 'فلاورجان': 'Falavarjan', 'لنجان': 'Lenjan', 'گلپایگان': 'Golpayegan',
    'فریدن': 'Fereydan', 'نائین': 'Nain', 'اردستان': 'Ardestan', 'سمیرم': 'Semirom',
    'کازرون': 'Kazerun', 'جهرم': 'Jahrom', 'مرودشت': 'Marvdasht', 'فسا': 'Fasa',
    'داراب': 'Darab', 'لار': 'Lar', 'لارستان': 'Larestan', 'آباده': 'Abadeh',
    'فیروزآباد': 'Firuzabad', 'نی‌ریز': 'Neyriz', 'اقلید': 'Eqlid', 'استهبان': 'Estahban',
    'برازجان': 'Borazjan', 'گناوه': 'Ganaveh', 'کنگان': 'Kangan', 'عسلویه': 'Asaluyeh',
    'ورامین': 'Varamin', 'شهریار': 'Shahriar', 'پاکدشت': 'Pakdasht', 'ری': 'Ray', 'شهرری': 'Shahr-e Ray',
    'قدس': 'Qods', 'ملارد': 'Malard', 'رباط‌کریم': 'Robat Karim', 'دماوند': 'Damavand',
    'فیروزکوه': 'Firuzkuh', 'شمیرانات': 'Shemiranat', 'لواسان': 'Lavasan',
    'بروجرد': 'Borujerd', 'دورود': 'Dorud', 'الیگودرز': 'Aligudarz', 'کوهدشت': 'Kuhdasht',
    'چالوس': 'Chalus', 'نوشهر': 'Nowshahr', 'تنکابن': 'Tonekabon', 'رامسر': 'Ramsar',
    'بهشهر': 'Behshahr', 'نکا': 'Neka', 'بابلسر': 'Babolsar', 'محمودآباد': 'Mahmudabad',
    'لاهیجان': 'Lahijan', 'بندر انزلی': 'Bandar Anzali', 'انزلی': 'Bandar Anzali',
    'لنگرود': 'Langarud', 'رودسر': 'Rudsar', 'تالش': 'Talesh', 'آستارا': 'Astara',
    'صومعه‌سرا': 'Sowmeeh Sara', 'فومن': 'Fuman', 'آستانه اشرفیه': 'Astaneh-ye Ashrafiyeh',
    'رفسنجان': 'Rafsanjan', 'سیرجان': 'Sirjan', 'جیرفت': 'Jiroft', 'بم': 'Bam', 'زرند': 'Zarand',
    'زابل': 'Zabol', 'چابهار': 'Chabahar', 'ایرانشهر': 'Iranshahr', 'خاش': 'Khash', 'سراوان': 'Saravan',
    'شاهرود': 'Shahrud', 'دامغان': 'Damghan', 'گرمسار': 'Garmsar',
    'ملایر': 'Malayer', 'نهاوند': 'Nahavand', 'تویسرکان': 'Tuyserkan', 'اسدآباد': 'Asadabad',
    'ساوه': 'Saveh', 'خمین': 'Khomeyn', 'محلات': 'Mahallat', 'دلیجان': 'Delijan',
    'گنبد کاووس': 'Gonbad-e Kavus', 'گنبدکاووس': 'Gonbad-e Kavus', 'بندر ترکمن': 'Bandar Torkaman',
    'علی‌آباد': 'Aliabad', 'آق‌قلا': 'Aqqala', 'مینودشت': 'Minudasht', 'کردکوی': 'Kordkuy',
    'بهبهان': 'Behbahan', 'ماهشهر': 'Mahshahr', 'بندر ماهشهر': 'Bandar Mahshahr',
    'ایذه': 'Izeh', 'شوشتر': 'Shushtar', 'شوش': 'Shush', 'اندیمشک': 'Andimeshk',
    'مسجدسلیمان': 'Masjed Soleyman', 'رامهرمز': 'Ramhormoz', 'امیدیه': 'Omidiyeh',
    'شادگان': 'Shadegan', 'سوسنگرد': 'Susangerd', 'آغاجاری': 'Aghajari',
    'سقز': 'Saqqez', 'مریوان': 'Marivan', 'بانه': 'Baneh', 'قروه': 'Qorveh', 'بیجار': 'Bijar', 'کامیاران': 'Kamyaran',
    'اسلام‌آباد غرب': 'Eslamabad-e Gharb', 'جوانرود': 'Javanrud', 'کنگاور': 'Kangavar', 'سرپل ذهاب': 'Sarpol-e Zahab', 'سنقر': 'Sonqor',
    'ابهر': 'Abhar', 'خرمدره': 'Khorramdarreh', 'خدابنده': 'Khodabandeh',
    'تاکستان': 'Takestan', 'الوند': 'Alvand', 'آبیک': 'Abyek', 'بوئین‌زهرا': 'Buin Zahra',
    'اردکان': 'Ardakan', 'میبد': 'Meybod', 'بافق': 'Bafq', 'مهریز': 'Mehriz', 'ابرکوه': 'Abarkuh', 'طبس': 'Tabas',
    'میناب': 'Minab', 'بندر لنگه': 'Bandar Lengeh', 'قشم': 'Qeshm', 'کیش': 'Kish', 'جاسک': 'Jask', 'ابوموسی': 'Abu Musa',
    'بروجن': 'Borujen', 'لردگان': 'Lordegan', 'فارسان': 'Farsan',
    'گچساران': 'Gachsaran', 'دوگنبدان': 'Dogonbadan', 'دهدشت': 'Dehdasht',
    'دهلران': 'Dehloran', 'ایوان': 'Eyvan', 'آبدانان': 'Abdanan', 'مهران': 'Mehran',
    'قائن': 'Qaen', 'فردوس': 'Ferdows', 'نهبندان': 'Nehbandan',
    'شیروان': 'Shirvan', 'اسفراین': 'Esfarayen',
}

# Exact hand-verified translations for all 155 featured medical centers
FEATURED_155_EN = {
    'بیمارستان باهنر کرمان': 'Bahonar Hospital, Kerman',
    'دی کلینیک ولنجک': 'Velenjak Day Clinic',
    'مرکز جراحی میرداماد': 'Mirdamad Surgery Center',
    'بیمارستان مهرگان قزوین': 'Mehregan Hospital, Qazvin',
    'بیمارستان الزهرا اصفهان': 'Al-Zahra Hospital, Isfahan',
    'بیمارستان مادر مشهد': 'Madar Hospital, Mashhad',
    'بیمارستان میلاد ارومیه': 'Milad Hospital, Urmia',
    'مرکز جراحی پارسیان کاشان': 'Parsian Surgery Center, Kashan',
    'بیمارستان سوم شعبان': 'Sevvom-e Shaban Hospital',
    'بیمارستان خیریه صدیقه الزهرا': 'Sediqeh Al-Zahra Charity Hospital',
    'بیمارستان نیکان سپید': 'Nikan Sepid Hospital',
    'کلینیک زخم التیام': 'Eltiam Wound Care Clinic',
    'بیمارستان چشم پزشکی بینا': 'Bina Eye Hospital',
    'پژوهشگاه رویان': 'Royan Research Institute',
    'مرکز ناباروری مام': 'MOM Fertility & Infertility Center',
    'بیمارستان فیض اصفهان': 'Feiz Hospital, Isfahan',
    'بیمارستان حضرت فاطمه کرمان': 'Hazrat Fatemeh Hospital, Kerman',
    'بیمارستان جم': 'Jam Hospital',
    'بیمارستان بهارلو': 'Baharloo Hospital',
    'بیمارستان فرشچیان همدان': 'Farshchian Heart Hospital, Hamadan',
    'کلینیک مرکزی شهر': 'Shahr Central Clinic',
    'درمانگاه شبانه روزی درنیان': 'Dornian 24-Hour Medical Clinic',
    'مرکز جراحی دکتر خیرخواه': 'Dr. Kheirkhah Subspecialty Surgery Center',
    'بیمارستان یاس': 'Yas Hospital',
    'بیمارستان سورنا': 'Sorena Hospital',
    'بیمارستان شهید شوریده': 'Shahid Shoorideh Hospital',
    'بیمارستان مهرآیین لواسان': 'Mehraeen Hospital, Lavasan',
    'بیمارستان محب مهر': 'Moheb Mehr Hospital',
    'بیمارستان مرکز طبی کودکان': "Children's Medical Center Hospital",
    'بیمارستان نجمیه': 'Najmieh Hospital',
    'بیمارستان توس': 'Toos Hospital',
    'بیمارستان کودکان بهرامی': "Bahrami Children's Hospital",
    'بیمارستان بقیه الله اعظم': 'Baqiyatallah Al-Azam Hospital',
    'بیمارستان چشم پزشکی دکتر جوادی': 'Dr. Javadi Eye Hospital',
    'بیمارستان پیامبران تهران': 'Payambaran Hospital, Tehran',
    'مرکز جراحی فاطمه زهرا (س) شهرری': 'Fatemeh Zahra Surgery Center, Ray',
    'بیمارستان بیستون کرمانشاه': 'Bistoon Hospital, Kermanshah',
    'موسسه خیریه محک': 'MAHAK Pediatric Cancer Charity Institute',
    'مرکز جراحی محدود نیاوران': 'Niavaran Day Surgery Center',
    'مرکز درمانی و جراحی درمان بهار': 'Darman Bahar Medical & Surgery Center',
    'بیمارستان شهید دکتر رهنمون': 'Shahid Dr. Rahnemoon Hospital',
    'بیمارستان ولیعصر تبریز': 'Valiasr Hospital, Tabriz',
    'بیمارستان میلاد اصفهان': 'Milad Hospital, Isfahan',
    'مرکز پزشکی آموزشی و درمانی مهدیه': 'Mahdieh Educational & Medical Center',
    'بیمارستان دکتر مسیح دانشوری': 'Dr. Masih Daneshvari Hospital',
    'بیمارستان مادران': 'Madaran Hospital',
    'بیمارستان کودکان مفید': "Mofid Children's Hospital",
    'بیمارستان فوق تخصصی غرضی اصفهان': 'Gharazi Subspecialty Hospital, Isfahan',
    'مرکز درمانی شهید چمران اصفهان': 'Shahid Chamran Medical Center, Isfahan',
    'بیمارستان بازرگانان': 'Bazarganan Hospital',
    'بیمارستان ایرانشهر': 'Iranshahr Hospital',
    'بیمارستان امید ارومیه': 'Omid Charity Hospital, Urmia',
    'مرکز آموزش درمانی افضلی پور کرمان': 'Afzalipour Educational & Medical Center, Kerman',
    'بیمارستان آسیا': 'Asia Hospital',
    'بیمارستان آراد': 'Arad Hospital',
    'بیمارستان آپادانا': 'Apadana Hospital',
    'بیمارستان سعدی': 'Saadi Hospital',
    'بیمارستان میلاد': 'Milad Hospital',
    'بیمارستان موقوفه گودرز': 'Goodarz Endowment Hospital, Yazd',
    'بیمارستان مادر و کودک غدیر': 'Ghadir Mother & Child Hospital',
    'بیمارستان عارفیان': 'Arefian Hospital',
    'بیمارستان شهید محلاتی تبریز': 'Shahid Mahallati Hospital, Tabriz',
    'بیمارستان شهریار': 'Shahriar Hospital',
    'بیمارستان سیدالشهدا یزد': 'Seyed Al-Shohada Hospital, Yazd',
    'مرکز آموزشی درمانی حضرت زینب': 'Hazrat Zeinab Educational & Medical Center',
    'بیمارستان دکتر مجیبیان یزد': 'Dr. Mojibian Hospital, Yazd',
    'بیمارستان شهید چمران شیراز': 'Shahid Chamran Hospital, Shiraz',
    'بیمارستان بهبود': 'Behboud Hospital',
    'بیمارستان بعثت': 'Besat Hospital',
    'بیمارستان دکتر امامی': 'Dr. Emami Hospital',
    'مجتمع درمانی آزادی': 'Azadi Medical Complex',
    'مرکزپزشکی پانزده خرداد': '15 Khordad Medical Center',
    'بیمارستان آتیه': 'Atieh Hospital',
    'بیمارستان تهران': 'Tehran Hospital',
    'بیمارستان شمال': 'Shomal Hospital',
    'بیمارستان پاسارگاد': 'Pasargad Hospital',
    'بیمارستان شفا ساری': 'Shafa Hospital, Sari',
    'بیمارستان نیکان غرب': 'Nikan West Hospital',
    'بیمارستان آریا': 'Arya Hospital',
    'بیمارستان فوق تخصصی مهر اهواز': 'Mehr Subspecialty Hospital, Ahvaz',
    'ایرانیان': 'Iranian Hospital',
    'بیمارستان سید الشهدا': 'Seyed Al-Shohada Hospital',
    'بیمارستان امام خمینی کنگان': 'Imam Khomeini Hospital, Kangan',
    'بیمارستان سوانح و سوختگی گناوه': 'Ganaveh Trauma & Burn Hospital',
    'بیمارستان امام حسین': 'Imam Hossein Hospital',
    'مرکز پزشکی سهند': 'Sahand Medical Center',
    'بیمارستان سلامت فردا': 'Salamat Farda Hospital',
    'بیمارستان بانک ملی': 'Bank Melli Hospital',
    'بیمارستان مهرگان': 'Mehregan Hospital',
    'بیمارستان شهید هاشمی نژاد': 'Shahid Hasheminejad Hospital',
    'بیمارستان نور شهریار': 'Noor Hospital, Shahriar',
    'بیمارستان غیاثی': 'Ghiassi Hospital',
    'پبیمارستان شهید صدوقی یزد': 'Shahid Sadoughi Hospital, Yazd',
    'بیمارستان شهید صدوقی یزد': 'Shahid Sadoughi Hospital, Yazd',
    'بیمارستان دکتر میر': 'Dr. Mir Hospital',
    'مرکز آموزش درمانی نمازی': 'Namazi Educational & Medical Center',
    'کلینیک رازی': 'Razi Clinic',
    'درمانگاه پوست و مو پری سیما': 'Parisima Skin & Hair Clinic',
    'بیمارستان امید': 'Omid Hospital',
    'بیمارستان شهید صدوقی اصفهان': 'Shahid Sadoughi Hospital, Isfahan',
    'کلینیک شیان': 'Shian Clinic',
    'مرکز پزشکی حج و زیارت': 'Hajj & Pilgrimage Medical Center',
    'بیمارستان اقبال': 'Eghbal Hospital',
    'مرکز آموزشی درمانی امام خمینی': 'Imam Khomeini Educational & Medical Center',
    'بیمارستان شهید صادق گنجی براز جان': 'Shahid Sadegh Ganji Hospital, Borazjan',
    'بیمارستان تخصصی پارسا': 'Parsa Specialty Hospital',
    'بیمارستان پاستورنو': 'Pasteur No Hospital',
    'بیمارستان تهران پارس': 'Tehranpars Hospital',
    'بیمارستان فوق تخصصی لاله': 'Laleh Subspecialty Hospital',
    'بیمارستان فوق تخصصی صارم': 'Sarem Subspecialty Hospital',
    'مرکز جراحی محدود شقایق': 'Shaghayegh Day Surgery Center',
    'بیمارستان علوی': 'Alavi Hospital',
    'بیمارستان شهید مطهری': 'Shahid Motahari Hospital',
    'بیمارستان فوق تخصصی شفا': 'Shafa Subspecialty Hospital',
    'بیمارستان تریتا': 'Treata Hospital',
    'بیمارستان تخصصی و فوق تخصصی دنا': 'Dena Specialty & Subspecialty Hospital',
    'بیمارستان بین المللی میلاد فردا': 'Milad Farda International Hospital',
    'بیمارستان مدنی کرج': 'Madani Hospital, Karaj',
    'بیمارستان فوق تخصصی مدائن': 'Madaen Subspecialty Hospital',
    'بیمارستان قلب الزهرا': 'Al-Zahra Heart Hospital',
    'بیمارستان شهید دکتر فقیهی': 'Shahid Dr. Faghihi Hospital',
    'بیمارستان فوق تخصصی آبان': 'Aban Subspecialty Hospital',
    'بیمارستان ابن سینا': 'Ibn Sina (Avicenna) Hospital',
    'بیمارستان البرز': 'Alborz Hospital',
    'بیمارستان الغدیر': 'Al-Ghadir Hospital',
    'کلینیک جراحی آلفا': 'Alpha Surgery Clinic',
    'بیمارستان بهمن': 'Bahman Hospital',
    'بیمارستان پارسیان': 'Parsian Hospital',
    'مرکز پزشکی شهدا تجریش': 'Shohada-ye Tajrish Medical Center',
    'بیمارستان فوق تخصصی تخت جمشید': 'Takht-e Jamshid Subspecialty Hospital',
    'بیمارستان امیرالمومنین': 'Amir Al-Momenin Hospital',
    'بیمارستان دادگستری': 'Dadgostari (Judiciary) Hospital',
    'بیمارستان دی': 'Day General Hospital',
    'بیمارستان قلب و عروق شهید رجایی': 'Shahid Rajaei Cardiovascular Hospital',
    'بیمارستان شهید رجایی کرج': 'Shahid Rajaei Hospital, Karaj',
    'عرفان سلامت': 'Erfan Salamat Medical Center',
    'بیمارستان فوق تخصصی خاتم الانبیا': 'Khatam Al-Anbia Subspecialty Hospital',
    'بیمارستان کمالی کرج': 'Kamali Hospital, Karaj',
    'بیمارستان کیان': 'Kian Hospital',
    'هتل بیمارستان گاندی': 'Gandhi Hotel-Hospital',
    'بیمارستان شهرام': 'Shahram Hospital',
    'بیمارستان تخصصی شهید دکتر لواسانی': 'Shahid Dr. Lavasani Specialty Hospital',
    'بیمارستان عرفان نیایش': 'Erfan Niayesh Hospital',
    'بیمارستان عرفان': 'Erfan Hospital',
    'بیمارستان فرمانیه': 'Farmanieh Hospital',
    'بیمارستان مهراد': 'Mehrad Hospital',
    'بیمارستان تخصصی مهر': 'Mehr Specialty Hospital',
    'بیمارستان مفرح': 'Mofarah Hospital',
    'کسرا': 'Kasra Hospital',
    'بیمارستان امام خمینی': 'Imam Khomeini Hospital',
    'بیمارستان نیکان': 'Nikan Hospital',
    'بیمارستان تندیس': 'Tandis Hospital',
    'بیمارستان فوق تخصصی نور افشار': 'Noor Afshar Subspecialty Hospital',
    'بیمارستان شهید مصطفی خمینی': 'Shahid Mostafa Khomeini Hospital',
    'بیمارستان محب کوثر': 'Moheb Kowsar Hospital',
    'بیمارستان جماران': 'Jamaran Hospital',
}

WORD_MAP_EN = [
    ('بیمارستان تخصصی و فوق تخصصی', 'Specialty & Subspecialty Hospital'),
    ('بیمارستان فوق تخصصی', 'Subspecialty Hospital'),
    ('بیمارستان تخصصی', 'Specialty Hospital'),
    ('بیمارستان آموزشی درمانی', 'Educational & Medical Hospital'),
    ('مرکز آموزشی درمانی', 'Educational & Medical Center'),
    ('مرکز آموزش درمانی', 'Educational & Medical Center'),
    ('مرکز پزشکی آموزشی و درمانی', 'Educational & Medical Center'),
    ('بیمارستان کودکان', "Children's Hospital"),
    ('بیمارستان چشم پزشکی', 'Eye Hospital'),
    ('بیمارستان قلب و عروق', 'Cardiovascular Hospital'),
    ('بیمارستان قلب', 'Heart Hospital'),
    ('بیمارستان سوانح و سوختگی', 'Trauma & Burn Hospital'),
    ('بیمارستان زنان و زایمان', 'Maternity & Women Hospital'),
    ('بیمارستان مادر و کودک', 'Mother & Child Hospital'),
    ('بیمارستان روانپزشکی', 'Psychiatric Hospital'),
    ('بیمارستان خیریه', 'Charity Hospital'),
    ('هتل بیمارستان', 'Hotel-Hospital'),
    ('بیمارستان بین المللی', 'International Hospital'),
    ('بیمارستان بین‌المللی', 'International Hospital'),
    ('مرکز جراحی محدود', 'Day Surgery Center'),
    ('مرکز جراحی', 'Surgery Center'),
    ('مجتمع درمانی', 'Medical Complex'),
    ('مرکز درمانی', 'Medical Center'),
    ('مرکز پزشکی', 'Medical Center'),
    ('کلینیک تخصصی', 'Specialty Clinic'),
    ('دی کلینیک', 'Day Clinic'),
    ('کلینیک', 'Clinic'),
    ('درمانگاه شبانه روزی', '24-Hour Clinic'),
    ('درمانگاه', 'Medical Clinic'),
    ('پژوهشگاه', 'Research Institute'),
    ('بیمارستان', 'Hospital'),
    ('پبیمارستان', 'Hospital'),
    ('حضرت ابوالفضل', 'Hazrat Abolfazl'),
    ('حضرت ولیعصر', 'Hazrat Valiasr'),
    ('حضرت فاطمه', 'Hazrat Fatemeh'),
    ('حضرت زینب', 'Hazrat Zeinab'),
    ('حضرت معصومه', 'Hazrat Masoumeh'),
    ('حضرت رسول اکرم', 'Hazrat Rasoul Akram'),
    ('حضرت رسول', 'Hazrat Rasoul'),
    ('حضرت علی اصغر', 'Hazrat Ali Asghar'),
    ('حضرت قمر بنی هاشم', 'Hazrat Qamar Bani Hashem'),
    ('حضرت مریم', 'Hazrat Maryam'),
    ('امام خمینی', 'Imam Khomeini'),
    ('امام رضا', 'Imam Reza'),
    ('امام حسین', 'Imam Hossein'),
    ('امام علی', 'Imam Ali'),
    ('امام حسن مجتبی', 'Imam Hassan Mojtaba'),
    ('امام حسن', 'Imam Hassan'),
    ('امام سجاد', 'Imam Sajjad'),
    ('امام جعفر صادق', 'Imam Jafar Sadegh'),
    ('امام صادق', 'Imam Sadegh'),
    ('امام موسی کاظم', 'Imam Mousa Kazem'),
    ('امام محمد باقر', 'Imam Mohammad Bagher'),
    ('امام هادی', 'Imam Hadi'),
    ('امام جواد', 'Imam Javad'),
    ('امام زمان', 'Imam Zaman'),
    ('امام مهدی', 'Imam Mahdi'),
    ('صاحب الزمان', 'Saheb Al-Zaman'),
    ('بقیه الله اعظم', 'Baqiyatallah Al-Azam'),
    ('بقیة الله', 'Baqiyatallah'),
    ('بقیه الله', 'Baqiyatallah'),
    ('خاتم الانبیاء', 'Khatam Al-Anbia'),
    ('خاتم الانبیا', 'Khatam Al-Anbia'),
    ('سیدالشهدا', 'Seyed Al-Shohada'),
    ('سید الشهدا', 'Seyed Al-Shohada'),
    ('سیدالشهداء', 'Seyed Al-Shohada'),
    ('ولیعصر', 'Valiasr'),
    ('ولی عصر', 'Valiasr'),
    ('الزهرا', 'Al-Zahra'),
    ('الزهراء', 'Al-Zahra'),
    ('الغدیر', 'Al-Ghadir'),
    ('امیرالمومنین', 'Amir Al-Momenin'),
    ('امیرالمؤمنین', 'Amir Al-Momenin'),
    ('ثامن الائمه', 'Samen Al-Aemeh'),
    ('ثامن الحجج', 'Samen Al-Hojaj'),
    ('باب الحوائج', 'Bab Al-Havaej'),
    ('تامین اجتماعی', 'Social Security'),
    ('تأمین اجتماعی', 'Social Security'),
    ('شفا', 'Shafa'),
    ('شهید دکتر', 'Shahid Dr.'),
    ('شهید', 'Shahid'),
    ('شهدای', 'Shohada-ye'),
    ('شهدا', 'Shohada'),
    ('دکتر', 'Dr.'),
    ('آیت الله', 'Ayatollah'),
    ('آیت‌الله', 'Ayatollah'),
    ('پروفسور', 'Prof.'),
    ('باهنر', 'Bahonar'),
    ('چمران', 'Chamran'),
    ('رجایی', 'Rajaei'),
    ('بهشتی', 'Beheshti'),
    ('مطهری', 'Motahari'),
    ('صدوقی', 'Sadoughi'),
    ('مدنی', 'Madani'),
    ('رهنمون', 'Rahnemoon'),
    ('فقیهی', 'Faghihi'),
    ('لواسانی', 'Lavasani'),
    ('هاشمی نژاد', 'Hasheminejad'),
    ('هاشمی‌نژاد', 'Hasheminejad'),
    ('طالقانی', 'Taleghani'),
    ('شریعتی', 'Shariati'),
    ('اشرفی اصفهانی', 'Ashrafi Esfahani'),
    ('منتظری', 'Montazeri'),
    ('دستغیب', 'Dastgheib'),
    ('کلانتری', 'Kalantari'),
    ('بهبهانی', 'Behbahani'),
    ('سلیمانی', 'Soleimani'),
    ('قاسم سلیمانی', 'Qasem Soleimani'),
    ('همت', 'Hemmat'),
    ('باکری', 'Bakeri'),
    ('بروجردی', 'Borujerdi'),
    ('خرازی', 'Kharrazi'),
    ('کاظمی', 'Kazemi'),
    ('صیاد شیرازی', 'Sayyad Shirazi'),
    ('ستاری', 'Sattari'),
    ('بابایی', 'Babaei'),
    ('چمران', 'Chamran'),
    ('تندگویان', 'Tondgooyan'),
    ('فیاض بخش', 'Fayyazbakhsh'),
    ('فیاض‌بخش', 'Fayyazbakhsh'),
    ('لبافی نژاد', 'Labbafinejad'),
    ('لبافی‌نژاد', 'Labbafinejad'),
    ('میلاد', 'Milad'),
    ('سینا', 'Sina'),
    ('ابن سینا', 'Ibn Sina'),
    ('بوعلی سینا', 'Bouali Sina'),
    ('بوعلی', 'Bouali'),
    ('رازی', 'Razi'),
    ('فارابی', 'Farabi'),
    ('لقمان حکیم', 'Loghman Hakim'),
    ('لقمان', 'Loghman'),
    ('مسیح دانشوری', 'Masih Daneshvari'),
    ('فیروزگر', 'Firouzgar'),
    ('رسول اکرم', 'Rasoul Akram'),
    ('طوس', 'Toos'),
    ('توس', 'Toos'),
    ('نیکان', 'Nikan'),
    ('عرفان', 'Erfan'),
    ('پارسیان', 'Parsian'),
    ('پارس', 'Pars'),
    ('آتیه', 'Atieh'),
    ('بهمن', 'Bahman'),
    ('لاله', 'Laleh'),
    ('صارم', 'Sarem'),
    ('تریتا', 'Treata'),
    ('کسری', 'Kasra'),
    ('کسرا', 'Kasra'),
    ('مهراد', 'Mehrad'),
    ('مهرگان', 'Mehregan'),
    ('مهر', 'Mehr'),
    ('امید', 'Omid'),
    ('نور', 'Noor'),
    ('کوثر', 'Kowsar'),
    ('محب', 'Moheb'),
    ('یاس', 'Yas'),
    ('بهارلو', 'Baharloo'),
    ('جم', 'Jam'),
    ('آراد', 'Arad'),
    ('آسیا', 'Asia'),
    ('آپادانا', 'Apadana'),
    ('پاستور', 'Pasteur'),
    ('سعدی', 'Saadi'),
    ('حافظ', 'Hafez'),
    ('نمازی', 'Namazi'),
    ('خلیلی', 'Khalili'),
    ('پاسارگاد', 'Pasargad'),
    ('تخت جمشید', 'Takht-e Jamshid'),
    ('کورش', 'Kourosh'),
    ('کوروش', 'Kourosh'),
    ('آریا', 'Arya'),
    ('ایرانمهر', 'Iranmehr'),
    ('تهرانپارس', 'Tehranpars'),
    ('تهران پارس', 'Tehranpars'),
    ('فرمانیه', 'Farmanieh'),
    ('نیاوران', 'Niavaran'),
    ('ولنجک', 'Velenjak'),
    ('میرداماد', 'Mirdamad'),
    ('تجریش', 'Tajrish'),
    ('قائم', 'Qaem'),
    ('رضوی', 'Razavi'),
    ('مادر', 'Madar'),
    ('کودکان', 'Children'),
    ('زنان', 'Women'),
    ('قلب', 'Heart'),
    ('چشم', 'Eye'),
    ('سوانح', 'Trauma'),
    ('سوختگی', 'Burn'),
    ('روانپزشکی', 'Psychiatric'),
    ('ارتش', 'Army'),
    ('ناجا', 'NAJA'),
    ('سپاه', 'IRGC'),
    ('نفت', 'Oil'),
    ('بانک ملی', 'Bank Melli'),
    ('دادگستری', 'Judiciary'),
    ('فرهنگیان', 'Farhangian'),
    ('مرکزی', 'Central'),
    ('بزرگ', 'Grand'),
    ('جدید', 'New'),
    ('قدیم', 'Old'),
    ('شماره یک', 'No. 1'),
    ('شماره دو', 'No. 2'),
    ('شماره ۱', 'No. 1'),
    ('شماره ۲', 'No. 2'),
    ('شماره 1', 'No. 1'),
    ('شماره 2', 'No. 2'),
    ('پانزده خرداد', '15 Khordad'),
    ('۱۵ خرداد', '15 Khordad'),
    ('15 خرداد', '15 Khordad'),
    ('هفده شهریور', '17 Shahrivar'),
    ('۱۷ شهریور', '17 Shahrivar'),
    ('17 شهریور', '17 Shahrivar'),
    ('بیست و دو بهمن', '22 Bahman'),
    ('۲۲ بهمن', '22 Bahman'),
    ('22 بهمن', '22 Bahman'),
    ('سوم شعبان', '3 Shaban'),
    ('سوم خرداد', '3 Khordad'),
    ('نه دی', '9 Dey'),
    ('۹ دی', '9 Dey'),
    ('هفت تیر', '7 Tir'),
    ('۷ تیر', '7 Tir'),
    ('بعثت', 'Besat'),
    ('غدیر', 'Ghadir'),
    ('فجر', 'Fajr'),
    ('قدس', 'Qods'),
    ('آزادی', 'Azadi'),
    ('انقلاب', 'Enghelab'),
    ('جمهوری', 'Jomhouri'),
    ('وحدت', 'Vahdat'),
    ('سلامت', 'Salamat'),
    ('درمان', 'Darman'),
    ('شفا', 'Shafa'),
    ('بهبود', 'Behboud'),
    ('حکیم', 'Hakim'),
    ('لقمان', 'Loghman'),
    ('زکریا', 'Zakaria'),
    ('رازی', 'Razi'),
]

# Persian-to-English phonetic transliteration for any remaining proper nouns
CHAR_TRANSLIT = {
    'آ': 'A', 'ا': 'a', 'أ': 'a', 'إ': 'e', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's',
    'ج': 'j', 'چ': 'ch', 'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'z', 'ر': 'r', 'ز': 'z',
    'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'z', 'ط': 't', 'ظ': 'z',
    'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'gh', 'ک': 'k', 'ك': 'k', 'گ': 'g',
    'ل': 'l', 'م': 'm', 'ن': 'n', 'و': 'o', 'ه': 'h', 'ة': 'h', 'ی': 'i', 'ي': 'i',
    'ئ': 'y', 'ء': '', '‌': ' ',
    '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
    '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
    '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9',
    'ى': 'i', 'ٔ': '', '،': ', ', '؛': '; ', '؟': '?',
}


def translit_word(w):
    w = w.strip()
    if not w:
        return ''
    if w in CITY_DICT:
        return CITY_DICT[w]
    out = []
    for i, ch in enumerate(w):
        if i == 0 and ch == 'ا':
            out.append('A')
        elif i == 0 and ch == 'ع':
            out.append('A')
        elif i == 0 and ch == 'و':
            out.append('V')
        elif i == 0 and ch == 'ی':
            out.append('Y')
        else:
            out.append(CHAR_TRANSLIT.get(ch, ch))
    res = ''.join(out)
    res = re.sub(r'\s+', ' ', res).strip()
    return res.title()


def translate_city(city_fa, lang='en'):
    c = (city_fa or '').strip()
    if not c:
        return ''
    if lang == 'ar':
        return c.replace('ک', 'ك').replace('ی', 'ي').replace('گ', 'غ').replace('چ', 'تش').replace('پ', 'ب')
    if c in CITY_DICT:
        return CITY_DICT[c]
    if c in PROV_EN:
        return PROV_EN[c]
    return translit_word(c)


def translate_ownership(own_fa, lang='en'):
    o = (own_fa or '').strip()
    if not o or o == 'نامشخص':
        return ''
    parts = [p.strip() for p in re.split(r'[;·]', o) if p.strip()]
    out = []
    for p in parts:
        if lang == 'en':
            if p in OWN_EN_SINGLE:
                if OWN_EN_SINGLE[p]:
                    out.append(OWN_EN_SINGLE[p])
                continue
            m = re.match(r'^(?:دانشگاه\s+)?علوم پزشکی\s+(.+)$', p)
            if m:
                place = translate_city(m.group(1), 'en')
                out.append(f'{place} Univ. of Medical Sciences')
                continue
            out.append(translit_word(p))
        else:
            if p in OWN_AR_SINGLE:
                if OWN_AR_SINGLE[p]:
                    out.append(OWN_AR_SINGLE[p])
                continue
            m = re.match(r'^(?:دانشگاه\s+)?علوم پزشکی\s+(.+)$', p)
            if m:
                place = translate_city(m.group(1), 'ar')
                out.append(f'جامعة العلوم الطبية في {place}')
                continue
            out.append(p.replace('ک', 'ك').replace('ی', 'ي'))
    return ' · '.join(out)


def translate_hospital(name_fa, lang='en'):
    s = (name_fa or '').strip()
    if not s:
        return ''
    if lang == 'ar':
        ar = s
        ar_swaps = [
            ('بیمارستان تخصصی و فوق تخصصی', 'مستشفى تخصصي وفوق تخصصي'),
            ('بیمارستان فوق تخصصی', 'مستشفى فوق تخصصي'),
            ('بیمارستان تخصصی', 'مستشفى تخصصي'),
            ('مرکز آموزشی درمانی', 'المركز التعليمي والعلاجي'),
            ('مرکز آموزش درمانی', 'المركز التعليمي والعلاجي'),
            ('مرکز پزشکی آموزشی و درمانی', 'المركز الطبي التعليمي والعلاجي'),
            ('بیمارستان کودکان', 'مستشفى الأطفال'),
            ('بیمارستان چشم پزشکی', 'مستشفى طب العيون'),
            ('بیمارستان قلب و عروق', 'مستشفى القلب والأوعية الدموية'),
            ('بیمارستان سوانح و سوختگی', 'مستشفى الحوادث والحروق'),
            ('بیمارستان خیریه', 'مستشفى خيري'),
            ('هتل بیمارستان', 'فندق ومستشفى'),
            ('مرکز جراحی محدود', 'مركز الجراحة المحدودة'),
            ('مرکز جراحی', 'مركز الجراحة'),
            ('مجتمع درمانی', 'المجمع العلاجي'),
            ('مرکز درمانی', 'المركز العلاجي'),
            ('مرکز پزشکی', 'المركز الطبي'),
            ('دی کلینیک', 'عيادة نهارية'),
            ('کلینیک', 'عيادة'),
            ('درمانگاه شبانه روزی', 'مستوصف على مدار الساعة'),
            ('درمانگاه', 'مستوصف'),
            ('پژوهشگاه', 'معهد أبحاث'),
            ('پبیمارستان', 'مستشفى'),
            ('بیمارستان', 'مستشفى'),
        ]
        for k, v in ar_swaps:
            ar = ar.replace(k, v)
        return ar.replace('ک', 'ك').replace('ی', 'ي')

    if s in FEATURED_155_EN:
        return FEATURED_155_EN[s]

    work = s.replace('\u200c', ' ').replace('ي', 'ی').replace('ى', 'ی').replace('ك', 'ک').replace('ٔ', '').replace('،', ' ')
    for a_d, f_d in zip('٠١٢٣٤٥٦٧٨٩', '0123456789'): work = work.replace(a_d, f_d)
    work = re.sub(r'\((?:س|ع|ره|ص| عج)\)', '', work)

    # Detect facility prefix so we can place "Hospital" / "Medical Center" naturally at the end
    suffix = ''
    prefixes = [
        ('بیمارستان تخصصی و فوق تخصصی', 'Specialty & Subspecialty Hospital'),
        ('بیمارستان فوق تخصصی', 'Subspecialty Hospital'),
        ('بیمارستان تخصصی', 'Specialty Hospital'),
        ('بیمارستان آموزشی درمانی', 'Educational & Medical Hospital'),
        ('مرکز آموزشی درمانی', 'Educational & Medical Center'),
        ('مرکز آموزش درمانی', 'Educational & Medical Center'),
        ('مرکز پزشکی آموزشی و درمانی', 'Educational & Medical Center'),
        ('بیمارستان کودکان', "Children's Hospital"),
        ('بیمارستان چشم پزشکی', 'Eye Hospital'),
        ('بیمارستان قلب و عروق', 'Cardiovascular Hospital'),
        ('بیمارستان سوانح و سوختگی', 'Trauma & Burn Hospital'),
        ('بیمارستان زنان و زایمان', 'Maternity Hospital'),
        ('بیمارستان مادر و کودک', 'Mother & Child Hospital'),
        ('بیمارستان روانپزشکی', 'Psychiatric Hospital'),
        ('بیمارستان خیریه', 'Charity Hospital'),
        ('هتل بیمارستان', 'Hotel-Hospital'),
        ('بیمارستان بین المللی', 'International Hospital'),
        ('مرکز جراحی محدود', 'Day Surgery Center'),
        ('مرکز جراحی', 'Surgery Center'),
        ('مجتمع درمانی', 'Medical Complex'),
        ('مرکز درمانی', 'Medical Center'),
        ('مرکز پزشکی', 'Medical Center'),
        ('دی کلینیک', 'Day Clinic'),
        ('کلینیک', 'Clinic'),
        ('درمانگاه شبانه روزی', '24-Hour Clinic'),
        ('درمانگاه', 'Clinic'),
        ('پژوهشگاه', 'Research Institute'),
        ('پبیمارستان', 'Hospital'),
        ('بیمارستان', 'Hospital'),
    ]
    for fa_pre, en_suf in prefixes:
        if work.startswith(fa_pre + ' '):
            work = work[len(fa_pre):].strip()
            suffix = en_suf
            break
        elif work == fa_pre:
            return en_suf

    for fa_w, en_w in WORD_MAP_EN:
        work = re.sub(r'(?<![\w])' + re.escape(fa_w) + r'(?![\w])', ' ' + en_w + ' ', work)
    for fa_c, en_c in sorted(CITY_DICT.items(), key=lambda x: -len(x[0])):
        work = re.sub(r'(?<![\w])' + re.escape(fa_c) + r'(?![\w])', ' ' + en_c + ' ', work)

    # Transliterate any remaining Persian tokens
    tokens = work.split()
    out_tokens = []
    for tok in tokens:
        if re.search(r'[\u0600-\u06FF]', tok):
            out_tokens.append(translit_word(tok))
        else:
            out_tokens.append(tok)
    core = ' '.join(t for t in out_tokens if t).strip()
    if suffix and suffix.lower() not in core.lower():
        res = f'{core} {suffix}'.strip()
    else:
        res = core or suffix or 'Medical Center'
    res = re.sub(r'\s+', ' ', res).strip()
    return res


def enrich_json():
    path = ROOT / 'site/assets/data/iran-hospitals-centers.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    centers = data.get('centers', [])
    for c in centers:
        p_fa = c.get('province') or ''
        c_fa = c.get('city_fa') or c.get('city') or ''
        n_fa = c.get('name') or ''
        o_fa = c.get('ownership') or ''
        c['name_en'] = translate_hospital(n_fa, 'en')
        c['province_en'] = PROV_EN.get(p_fa, translit_word(p_fa))
        c['city_en'] = translate_city(c_fa, 'en')
        c['ownership_en'] = translate_ownership(o_fa, 'en')
        c['name_ar'] = translate_hospital(n_fa, 'ar')
        c['province_ar'] = PROV_AR.get(p_fa, p_fa)
        c['city_ar'] = translate_city(c_fa, 'ar')
        c['ownership_ar'] = translate_ownership(o_fa, 'ar')
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    # Verify zero Persian chars in English fields
    persian_left = sum(
        1 for c in centers
        for k in ('name_en', 'province_en', 'city_en', 'ownership_en')
        if re.search(r'[\u0600-\u06FF]', c.get(k, ''))
    )
    print(f'Enriched {len(centers)} centers in iran-hospitals-centers.json (Persian chars left in EN fields: {persian_left})')


if __name__ == '__main__':
    enrich_json()
