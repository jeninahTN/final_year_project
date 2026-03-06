// Market Pulse - Main Application Logic

// Service Worker Registration for PWA
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/service-worker.js')
            .then(registration => {
                console.log('ServiceWorker registration successful');
            })
            .catch(err => {
                console.log('ServiceWorker registration failed: ', err);
            });
    });
}

// Voice Assistant Logic
function speak(text, lang = 'en-US') {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = lang;
        window.speechSynthesis.speak(utterance);
    } else {
        alert("Sorry, your browser doesn't support text-to-speech.");
    }
}

// --- Internationalization (i18n) ---

const translations = {
    'en': {
        // Nav & Footer
        'nav_home': 'Home',
        'nav_ussd': 'USSD Service',
        'nav_offline': 'Offline App',
        'nav_help': 'Help',
        'nav_login': 'Login',
        'footer_rights': '© 2024 Market Pulse Uganda. All rights reserved.',
        'footer_terms': 'Terms',
        'footer_privacy': 'Privacy',
        'footer_contact': 'Contact',

        // Dashboard (Index)
        'welcome_msg': 'Welcome back, Jeninah!',
        'latest_predictions': 'Here are your latest price predictions',
        'btn_new_prediction': 'Get New Price Prediction',
        'header_monitored_crops': 'My Monitored Crops',
        'header_recent_activity': 'Recent Activity',
        'link_view_all': 'View All History',
        'label_predicted_price': 'Predicted Price',
        'menu_my_crops': 'My Crops',
        'menu_locations': 'My Locations',
        'menu_history': 'Prediction History',
        'menu_settings': 'Settings',

        // Detail Page
        'btn_back': 'Back',
        'last_updated': 'Last updated: Today, 8:00 AM',
        'chart_title': 'Price Trend',
        'why_price_high': 'Why the price is high',
        'why_price_low': 'Why the price is low',
        'future_outlook': 'Future Outlook',
        'change_language': 'Change Language:',

        // Offline Page
        'offline_hero_title': 'Your Market Prices, Even Without Internet.',
        'offline_hero_desc': 'Add Market Pulse to your phone\'s home screen for faster, offline access.',
        'btn_add_home': 'Add to My Home Screen',
        'why_add_title': 'Why Add to Home Screen?',
        'feat_offline_title': 'Offline Access',
        'feat_offline_desc': 'See your last saved price predictions when you have no signal.',
        'feat_fast_title': 'Fast & Light',
        'feat_fast_desc': 'The app opens instantly and uses very little data.',
        'feat_easy_title': 'Easy Access',
        'feat_easy_desc': 'Open Market Pulse with one tap from your home screen.',
        'guide_title': 'Simple 3-Step Guide',
        'step_1_title': '1. Open Menu',
        'step_1_desc': 'Tap the menu button (three dots) in your browser.',
        'step_2_title': '2. Select Add',
        'step_2_desc': 'Find and tap on \'Add to Home Screen\' or \'Install app\'.',
        'step_3_title': '3. Confirm',
        'step_3_desc': 'Follow the prompt and find the app icon on your screen.',

        // Help Page
        'help_title': 'Help & Support',
        'help_subtitle': 'We are here to help. Assistance is available in your local language.',
        'help_get_help': 'Get Help Now',
        'call_desc': 'Call for immediate help',
        'btn_call_now': 'Call Now',
        'sms_desc': 'Send us an SMS',
        'btn_sms_now': 'SMS Now',
        'email_desc': 'Email us your query',
        'btn_email_us': 'Email Us',
        'msg_title': 'Send us a Message',
        'label_name': 'Name',
        'ph_name': 'Enter your full name',
        'label_contact': 'Phone Number or Email',
        'ph_contact': 'Your phone or email',
        'label_message': 'Your Message',
        'ph_message': 'How can we help you today?',
        'btn_send_msg': 'Send Message',
        'faq_title': 'Frequently Asked Questions',
        'faq_1': 'How do I check the price of maize?',
        'faq_2': 'What do the colors in the price trend mean?',
        'faq_3': 'How do I change my market location?',
        'faq_4': 'I forgot my password. What do I do?',

        // USSD Page
        'ussd_hero_title': 'Crop Prices are Now a Call Away',
        'ussd_hero_desc': 'No internet? No smartphone? No problem. Get the latest market prices by dialing a simple code on any phone.',
        'btn_how_it_works': 'See How It Works',
        'ussd_steps_title': 'Get Prices in 3 Easy Steps',
        'ussd_steps_desc': 'Follow these simple steps to get price information right on your phone screen.',
        'ussd_step_1_title': 'Dial The Code',
        'ussd_step_1_desc': 'Open your phone\'s dialer and enter this code: *123#. Then press the call button.',
        'ussd_step_2_title': 'Choose Your Crop & Market',
        'ussd_step_2_desc': 'A menu will appear on your screen. Enter the number for your crop (e.g., 1 for Maize), then enter the number for your market (e.g., 2 for Kampala).',
        'ussd_step_3_title': 'Get Price Advice',
        'ussd_step_3_desc': 'You will instantly see the price advice on your screen in your chosen language.',
        'ussd_benefits_title': 'Benefits for Every Farmer',
        'ben_internet_title': 'Works Without Internet',
        'ben_internet_desc': 'Get important market information even if you don\'t have internet data or a smartphone.',
        'ben_instant_title': 'Get Instant Replies',
        'ben_instant_desc': 'Receive price information in seconds, so you can decide quickly when to sell.',
        'ben_profit_title': 'Make More Profit',
        'ben_profit_desc': 'Knowing the right price helps you sell at the best time to earn more from your harvest.',

        // Login Page
        'login_subtitle': 'Price insights for your farm.',
        'tab_signin': 'Sign In',
        'tab_signup': 'Create Account',
        'label_login_id': 'Your Name or Phone Number',
        'ph_login_id': 'e.g. John Doe or 07...',
        'label_password': 'Password',
        'ph_password': 'Enter your password',
        'link_forgot': 'Forgot Password?',
        'btn_signin': 'Sign In',
        'btn_google': 'Sign in with Google'
    },
    'lg': {
        // Nav & Footer
        'nav_home': 'Awaka',
        'nav_ussd': 'Empeereza ya USSD',
        'nav_offline': 'App y\'okumsimu',
        'nav_help': 'Obuyambi',
        'nav_login': 'Yingira',
        'footer_rights': '© 2024 Market Pulse Uganda. Eddembe lyonna lirikuumibwa.',
        'footer_terms': 'Ebyokugoberera',
        'footer_privacy': 'Eby\'ekyama',
        'footer_contact': 'Tuukirira',

        // Dashboard (Index)
        'welcome_msg': 'Kulikaayo, Jeninah!',
        'latest_predictions': 'Wano waliwo ebeeyi y\'ebirime empya',
        'btn_new_prediction': 'Funa Ebeeyi Empya',
        'header_monitored_crops': 'Ebirime Byange',
        'header_recent_activity': 'Ebibaddewo',
        'link_view_all': 'Laba Byonna',
        'label_predicted_price': 'Ebeeyi Esuubirwa',
        'menu_my_crops': 'Ebirime Byange',
        'menu_locations': 'Ebifo Byange',
        'menu_history': 'Ebyayita',
        'menu_settings': 'Tegeka',

        // Detail Page
        'btn_back': 'Ddayo',
        'last_updated': 'Kisembyeyo: Leero, 2:00 Ez\'okumakya',
        'chart_title': 'Enkyukakyuka y\'ebeeyi',
        'why_price_high': 'Lwaki ebeeyi eri waggulu',
        'why_price_low': 'Lwaki ebeeyi eri wansi',
        'future_outlook': 'Ebisuubirwa mu maaso',
        'change_language': 'Kyusa Olulimi:',

        // Offline Page
        'offline_hero_title': 'Ebeeyi y\'akatale, ne bweuba toli ku yintaneti.',
        'offline_hero_desc': 'Teeka Market Pulse ku simu yo osobole okugikozesa amangu, ne bweuba toli ku yintaneti.',
        'btn_add_home': 'Teeka ku Home Screen',
        'why_add_title': 'Lwaki Oteeka ku Home Screen?',
        'feat_offline_title': 'Kozesa nga toli ku yintaneti',
        'feat_offline_desc': 'Laba ebeeyi esembyeyo okuterekebwa ne bweuba tolina network.',
        'feat_fast_title': 'Eyanguye & Nnyangu',
        'feat_fast_desc': 'App egguka mangu era ekozesa data mutono nnyo.',
        'feat_easy_title': 'Nyangu Okukozesa',
        'feat_easy_desc': 'Ggulawo Market Pulse n\'ekinyiga kimu okuva ku home screen yo.',
        'guide_title': 'Emitendera 3 Emirambulukufu',
        'step_1_title': '1. Ggulawo Menu',
        'step_1_desc': 'Nyiga ku menu (obutonnyeze busatu) ku browser yo.',
        'step_2_title': '2. Londa Add',
        'step_2_desc': 'Noonya era onyige ku \'Add to Home Screen\' oba \'Install app\'.',
        'step_3_title': '3. Kakasa',
        'step_3_desc': 'Goberera ebiragiro era onoonye akabonero ka app ku screen yo.',

        // Help Page
        'help_title': 'Obuyambi & Okuyambibwa',
        'help_subtitle': 'Tuli wano okukuyamba. Obuyambi buliwo mu lulimi lwo.',
        'help_get_help': 'Funa Obuyambi Kati',
        'call_desc': 'Kuba essimu okufuna obuyambi amangu',
        'btn_call_now': 'Kuba Kati',
        'sms_desc': 'Tuweereze SMS',
        'btn_sms_now': 'SMS Kati',
        'email_desc': 'Tuweereze email',
        'btn_email_us': 'Tuweereze Email',
        'msg_title': 'Tuweereze Obubaka',
        'label_name': 'Erinnya',
        'ph_name': 'Yingiza erinnya lyo lyonna',
        'label_contact': 'Namba y\'essimu oba Email',
        'ph_contact': 'Essimu yo oba email',
        'label_message': 'Obubaka Bwo',
        'ph_message': 'Tuyinza tutya okukuyamba leero?',
        'btn_send_msg': 'Weereza Obubaka',
        'faq_title': 'Ebibuuzibwa Baterako',
        'faq_1': 'Nkebera ntya ebeeyi ya kasooli?',
        'faq_2': 'Langiki zitegeeza ki ku nkyukakyuka y\'ebeeyi?',
        'faq_3': 'Nkyusa ntya ekifo kyange eky\'akatale?',
        'faq_4': 'Nneerabidde password yange. Nkole ki?',

        // USSD Page
        'ussd_hero_title': 'Ebeeyi y\'Ebirime Kati Eri ku Ssimu',
        'ussd_hero_desc': 'Tolina yintaneti? Tolina smartphone? Tewali buzibu. Funa ebeeyi y\'akatale esembyeyo ng\'okuba koodi ennyangu ku ssimu yonna.',
        'btn_how_it_works': 'Laba Bwekikola',
        'ussd_steps_title': 'Funa Ebeeyi mu Mitendera 3',
        'ussd_steps_desc': 'Goberera emitendera gino emirambulukufu okufuna amawulire g\'ebeeyi butereevu ku screen y\'essimu yo.',
        'ussd_step_1_title': 'Kuba Koodi',
        'ussd_step_1_desc': 'Ggulawo essimu yo oyingize koodi eno: *123#. Oluvannyuma onyige okukuba.',
        'ussd_step_2_title': 'Londa Ekirime Kyo & Akatale',
        'ussd_step_2_desc': 'Menu ejja kulabika ku screen yo. Yingiza ennamba y\'ekirime kyo (okugeza, 1 ya Kasooli), oluvannyuma oyingize ennamba y\'akatale ko (okugeza, 2 ya Kampala).',
        'ussd_step_3_title': 'Funa Amagezi ku Beeyi',
        'ussd_step_3_desc': 'Ojja kulaba amagezi ku beeyi amangu ddala ku screen yo mu lulimi lw\'olonze.',
        'ussd_benefits_title': 'Emigaso eri Buli Mulimi',
        'ben_internet_title': 'Kikola nga Tewali Yintaneti',
        'ben_internet_desc': 'Funa amawulire g\'akatale amakulu ne bweuba tolina data ya yintaneti oba smartphone.',
        'ben_instant_title': 'Funa Ebiwandiiko Amangu',
        'ben_instant_desc': 'Funa amawulire g\'ebeeyi mu bukyufu, osobole okusalawo amangu ddi lw\'olina okutunda.',
        'ben_profit_title': 'Kola Amagoba Mangi',
        'ben_profit_desc': 'Okumanya ebeeyi entuufu kikuyamba okutunda mu kiseera ekituufu okufuna ensimbi ennyingi mu makungula go.',

        // Login Page
        'login_subtitle': 'Amagezi ku beeyi g\'ennimiro yo.',
        'tab_signin': 'Yingira',
        'tab_signup': 'Kola Account',
        'label_login_id': 'Erinnya Lyo oba Namba y\'Essimu',
        'ph_login_id': 'okugeza John Doe oba 07...',
        'label_password': 'Password',
        'ph_password': 'Yingiza password yo',
        'link_forgot': 'Weerabidde Password?',
        'btn_signin': 'Yingira',
        'btn_google': 'Yingira ne Google'
    }
};

function updateLanguage(lang) {
    if (!translations[lang]) return;

    // Save preference
    localStorage.setItem('preferred_language', lang);

    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang][key]) {
            // Handle input placeholders specifically
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = translations[lang][key];
            } else {
                element.innerText = translations[lang][key];
            }
        }
    });

    // Update dropdown value if it exists
    const selector = document.getElementById('language-selector');
    if (selector) {
        selector.value = lang;
    }
}

// Initialize Language
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('preferred_language') || 'en';

    // Set initial value for selector
    const selector = document.getElementById('language-selector');
    if (selector) {
        selector.value = savedLang;
        selector.addEventListener('change', (e) => {
            updateLanguage(e.target.value);
        });
    }

    // Apply translation
    updateLanguage(savedLang);
});
