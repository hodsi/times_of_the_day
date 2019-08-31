MORNING_LESSON_TIME = '4:30'
FATHERS_AND_SONS_TIME = '16:15'

HOUR_TO_GO_ACCORDING_TO_SHKIA = 18

DEFAULT_PLACE = 'רמת גן'
DEFAULT_MONTH = None
DEFAULT_YEAR = None

COME_SHABAT_DIFF_FROM_MINHA_ACCORDING_TO_PLAG = 15
COME_SHABAT_DIFF_FROM_MINHA_ACCORDING_TO_SHKIA = -15
MORNING_PRAYER_DIFF_FROM_LESSON = 3 * 60
NOON_LESSON_DIFF_FROM_FATHERS_AND_SONS = 30
SHABAT_MINHA_TIME_BEFORE_SUN_SET = 40

GOOD_DATE_FORMAT_LINE = -1
BAD_DATE_FORMAT_LINE = 2

YESHIVA_TIMES_URL_FORMAT = 'https://www.yeshiva.org.il/calendar/timestable?year={year}&month={month_number}&place={' \
                           'place_number} '
YESHIVA_SHABAT_URL_FORMAT = 'https://www.yeshiva.org.il/calendar/shabatot?year={year}&place={place_number}'
YESHIVA_START_MONTHS_FORMAT = 'https://www.yeshiva.org.il/calendar/moladot?year={year}'

MOLADOT_TIME_TABLE_CLASS_NAME = 'moladotTableTimes'
TIMES_TABLE_CLASS_NAME = 'holydayTableTimes'
SHABAT_TABLE_ID = 'holydayTableTimes'
TABLE_BODY_CSS_SELECTOR = 'tbody'
TABLE_ROW_CSS_SELECTOR = 'tr'
TABLE_CELL_CSS_SELECTOR = 'td'
SCROLLING_DOWN_SCRIPT = 'scroll(0, 300);'
SCROLLING_DOWN_SHABAT_SCRIPT = 'scroll(0, 300);document.body.style.zoom = 0.2;'
FONT_SMALLER_SIZE_CSS_SELECTOR = '[class="font-size small"]'
TIMES_TO_FONT_SIZE_SMALLER = 13
LEAP_YEARS_MODULO = {0, 3, 6, 8, 11, 14, 17}
LEAP_YEAR_MODULO_NUMBER = 19
TIME_FORMAT = '%H:%M'
MINUTES_FORMAT = '%M'

DATE = 'תאריך'
PARASHA = 'פרשת השבוע'
SHABAT_ENTER = 'כניסת השבת והחג'
SHABAT_END = 'יציאת השבת והחג'

DAY_IN_MONTH = 'יום בחודש'
DAY_IN_WEEK = 'יום בשבוע'
WEIRD_DATE = 'תאריך לועזי'
HEBREW_MONTH = 'חודש עברי'
MOLADOT_TIME = 'זמן המולד'
PLAG = 'פלג המנחה'
SUN_SET = 'שקיעה'
FIRST_SHMA = 'סו"ז ק"ש למג"א'
SECOND_SHMA = 'סו"ז ק"ש לגר"א'
STARS_OUT = 'צאת הכוכבים'

FRIDAY = 'שישי'
SHABAT = 'שבת'

FIELD_TO_FILL = 'כלום'
SEP = ','
TIMES_OUTPUT_FOLDER = 'times_output'
TIMES_OUTPUT_FILE_FORMAT = 'זמני שבת {month} {year}.csv'
THOUSANDS_OF_YEARS_OFFSET = 5000

TIMES_FOLDER_FOR_CACHE = 'times_cache'
TIMES_DAY_FILE_FORMAT = 'times_place={place_number}_year={year_number}_month={month_number}.json'
TIMES_DAY_TITLES_FILE = 'times_titles.json'
SHABAT_SPECIAL_TIMES_FILE_FORMAT = 'shabat_times_place={place_number}_year={year_number}.json'
SHABAT_SPECIAL_TIMES_TITLES_FILE = 'shabat_titles.json'
MOLADOT_FILE_FORMAT = 'moladot_year={year_number}.json'
MOLADOT_TITLES_FILE = 'moladot_titles.json'

LEAP_YEAR_MONTH_NUMBERS = {
    'תשרי': 1,
    'חשון': 2,
    'כסלו': 3,
    'טבת': 4,
    'שבט': 5,
    'אדר א': 6,
    'אדר ב': 7,
    'ניסן': 8,
    'אייר': 9,
    'סיון': 10,
    'תמוז': 11,
    'אב': 12,
    'אלול': 13
}

NON_LEAP_YEAR_MONTH_NUMBERS = {
    'תשרי': 1,
    'חשון': 2,
    'כסלו': 3,
    'טבת': 4,
    'שבט': 5,
    'אדר': 6,
    'ניסן': 7,
    'אייר': 8,
    'סיון': 9,
    'תמוז': 10,
    'אב': 11,
    'אלול': 12
}

GIMATRIA_DICT = {
    'א': 1,
    'ב': 2,
    'ג': 3,
    'ד': 4,
    'ה': 5,
    'ו': 6,
    'ז': 7,
    'ח': 8,
    'ט': 9,
    'י': 10,
    'כ': 20,
    'ל': 30,
    'מ': 40,
    'נ': 50,
    'ס': 60,
    'ע': 70,
    'פ': 80,
    'צ': 90,
    'ק': 100,
    'ר': 200,
    'ש': 300,
    'ת': 400
}

REVERSE_GIMATRIAA_DICT = {value: letter for letter, value in GIMATRIA_DICT.items()}

PLACE_DICT = {
    'אופקים': '129',
    'אור יהודה': '218',
    'אור עקיבא': '219',
    'אילת': '130',
    'אלון מורה': '362',
    'אלעד': '131',
    'אפרת': '217',
    'אריאל': '132',
    'אשדוד': '133',
    'אשקלון': '134',
    'באר יעקב': '135',
    'באר שבע': '136',
    'בית אל': '212',
    'בית שאן': '137',
    'בית שמש': '138',
    'ביתר עילית ': '139',
    'בני ברק': '140',
    'בני נצרים': '247',
    'בנימינה': '141',
    'בת ים': '142',
    'גבעת זאב': '338',
    'גבעת שמואל': '234',
    'גבעתיים': '143',
    'דימונה': '144',
    'הוד השרון': '220',
    'הר ברכה': '294',
    'הרצליה': '145',
    'זכרון יעקב ': '146',
    'חברון': '147',
    'חדרה': '148',
    'חולון': '149',
    'חיספין': '150',
    'חיפה': '151',
    'חמאם אל מליח': '244',
    'חפץ חיים': '152',
    'חריש': '248',
    'חרמון': '232',
    'טבריה': '153',
    'טירת הכרמל': '221',
    'טלזסטון': '154',
    'טלמון': '207',
    'יבול': '206',
    'יבנה': '222',
    'יד בנימין': '351',
    'יהוד': '223',
    'יוקנעם': '371',
    'יסוד המעלה': '344',
    'ירוחם': '155',
    'ירושלים': '156',
    'יריחו': '236',
    'יתיר': '365',
    'כינר': '350',
    'כפר חבד': '157',
    'כפר חסידים ': '158',
    'כפר מימון ': '159',
    'כפר סבא': '224',
    'כרמיאל': '160',
    'לביא': '352',
    'לוד': '161',
    'מבשרת ציון': '370',
    'מגדל': '321',
    'מגדל העמק ': '162',
    'מודיעין': '163',
    'מזכרת בתיה': '246',
    'מחולה': '240',
    'מירון': '164',
    'מעגלים': '165',
    'מעלה אדומים ': '166',
    'מעלה אפרים': '373',
    'מעלה לבונה': '312',
    'מעלות': '210',
    'מצדה': '369',
    'מצפה יריחו': '356',
    'מצפה רמון ': '167',
    'נבי מוסא': '208',
    'נהלל': '168',
    'נהריה': '169',
    'ניר עציון ': '170',
    'נס ציונה': '225',
    'נצרת עילית': '226',
    'נריה': '366',
    'נשר': '171',
    'נתיבות': '172',
    'נתניה': '173',
    'סוסיא': '318',
    'סיירים': '216',
    'עטרת': '209',
    'עין בוקק': '174',
    'עין יהב': '237',
    'עכו': '175',
    'עלי': '243',
    'עמנואל': '213',
    'עפולה': '176',
    'עפרה': '241',
    'עציון גבר ': '177',
    'ערד': '178',
    'עתניאל': '242',
    'פדואל': '238',
    'פקיעין': '179',
    'פרדס חנה': '180',
    'פתח תקוה': '181',
    'צאלים': '235',
    'צפת': '182',
    'קדומים': '183',
    'קוממיות': '184',
    'קיבוץ מירב': '367',
    'קידה': '295',
    'קציר': '250',
    'קצרין': '233',
    'קרית אונו': '227',
    'קרית ארבע ': '185',
    'קרית אתא': '228',
    'קרית ביאליק': '229',
    'קרית גת': '186',
    'קרית טבעון ': '187',
    'קרית ים': '188',
    'קרית מוצקין': '230',
    'קרית מלאכי ': '189',
    'קרית נטפים': '245',
    'קרית ספר': '190',
    'קרית שמונה ': '191',
    'קרני שומרון': '211',
    'ראש העין': '192',
    'ראש פינה': '193',
    'ראשון לציון ': '194',
    'רחובות': '195',
    'רכסים': '215',
    'רמלה': '196',
    'רמת גן': '231',
    'רמת השרון ': '197',
    'רמת מגשימים ': '198',
    'רעננה': '199',
    'שבי ציון': '200',
    'שדרות': '214',
    'שהם': '239',
    'שומריה': '349',
    'שילה': '249',
    'שכם': '201',
    'שעלבים': '202',
    'תושיה': '203',
    'תל אביב': '204',
    'תפרח': '205',
}
