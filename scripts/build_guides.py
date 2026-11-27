#!/usr/bin/env python3
"""Generate the coffee guides at /guides/ and /guides/<slug>/.

Run after editing GUIDES below:

    python3 scripts/build_guides.py

Each guide is a static page with its own title and description, a short answer,
and links to the bags it relates to. Sitemap entries are added to sitemap.xml.
"""
import html
import pathlib
import re
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://kaifcoffee.net"
TODAY = date.today().isoformat()

GUIDES = [
    {
        "slug": "aeropress",
        "ar_title": "إزاي تعمل قهوة إيروبريس؟",
        "en_title": "How to brew AeroPress coffee",
        "answer": "Use 15 grams of medium-fine coffee and about 200 ml of water just off the boil. Put a rinsed paper filter in the cap, add the coffee, pour the water and stir gently. Fit the plunger and wait about one minute. Press down slowly over 30 seconds and stop when you hear a hiss. The result is a clean, strong cup that you can drink as it is or dilute with hot water. If it tastes bitter, grind a little coarser or press more gently.",
        "links": [("ethiopia-guji", "Ethiopia Guji"), ("colombia-huila", "Colombia Huila"), ("brazil-parana", "Brazil Paraná")],
    },
    {
        "slug": "coffee-to-water-ratio",
        "ar_title": "نسبة القهوة للمية: كام جرام لكل كوباية؟",
        "en_title": "Coffee to water ratio: how much coffee per cup",
        "answer": "For filter coffee, use about 1 gram of coffee for every 15 to 17 grams of water. For one 250 ml cup that is roughly 15 to 16 grams of coffee. For espresso, a common starting point is 18 grams of coffee for a 36 gram drink, which is a 1 to 2 ratio. For Turkish coffee, use about 7 grams for a small cup. Weigh your coffee with a scale instead of using spoons, because spoons vary a lot. If the cup is too weak, add more coffee. If it is too strong, add more water.",
        "links": [("ethiopia-guji", "Ethiopia Guji"), ("ember-blend", "Ember Blend"), ("turkish-coffee-plain-light", "Turkish Plain Light")],
    },
    {
        "slug": "sour-or-bitter-coffee",
        "ar_title": "قهوتي حامضة أو مرة: أعمل إيه؟",
        "en_title": "Why your coffee tastes sour or bitter, and how to fix it",
        "answer": "Sour coffee is usually under-extracted: the water did not pull enough out of the grounds. Grind finer, use hotter water, or brew a little longer. Bitter coffee is usually over-extracted: too much was pulled out. Grind coarser, use slightly cooler water, or shorten the brew. Change only one thing at a time so you know what worked. Also check that your beans are fresh, because stale coffee tastes flat and harsh whatever you do.",
        "links": [("ethiopia-guji", "Ethiopia Guji"), ("colombia-huila", "Colombia Huila"), ("aura-blend", "Aura Blend")],
    },
    {
        "slug": "espresso-at-home",
        "ar_title": "إزاي تظبط الإسبريسو في البيت؟",
        "en_title": "How to dial in espresso at home",
        "answer": "Start with 18 grams of finely ground coffee and aim for about 36 grams of espresso in 25 to 30 seconds. Level and tamp the coffee evenly before you lock in the portafilter. If the shot runs faster than that and tastes sour or thin, grind finer. If it runs slower and tastes bitter or burnt, grind coarser. Change only the grind between shots, and taste each one. A fresh blend made for espresso is the easiest place to begin.",
        "links": [("ember-blend", "Ember Blend"), ("aura-blend", "Aura Blend"), ("dolce-blend", "Dolce Blend")],
    },
    {
        "slug": "coffee-roast-levels",
        "ar_title": "درجات تحميص البن: فاتح ومتوسط وغامق",
        "en_title": "Coffee roast levels: light, medium and dark",
        "answer": "Light roasts keep more of the origin: they taste brighter and fruitier, with more acidity. Medium roasts are balanced, with sweetness and notes like chocolate and caramel. Dark roasts taste bolder and smokier, with less acidity and a heavier body. None is better than the others. Light and medium roasts suit filter brewing. Medium and darker roasts are popular for espresso and milk drinks. Pick the roast by the flavour you enjoy.",
        "links": [("ethiopia-guji", "Ethiopia Guji"), ("colombia-huila", "Colombia Huila"), ("ember-blend", "Ember Blend")],
    },
    {
        "slug": "decaf-coffee",
        "ar_title": "القهوة منزوعة الكافيين: كل اللي محتاج تعرفه",
        "en_title": "What is decaf coffee, and does it taste different?",
        "answer": "Decaf coffee is made from regular coffee beans that have had most of their caffeine removed before roasting. It is not caffeine-free, but the amount left is small. Good decaf can taste close to regular coffee, and it brews the same way. Decaf is a good choice for the evening or for people who want to cut down on caffeine. Check the bag for how the caffeine was removed and when it was roasted.",
        "links": [("decaf-coffee", "KAIF Decaf")],
    },
    {
        "slug": "coffee-for-milk-drinks",
        "ar_title": "أنهي بن أحسن للقهوة بالحليب؟",
        "en_title": "Which coffee is best for milk drinks?",
        "answer": "Milk softens acidity and covers delicate flavours, so choose coffee with enough body and sweetness to stay noticeable. A medium to medium-dark espresso blend with chocolate and caramel notes works well in lattes, cappuccinos and flat whites. Flavoured coffees such as caramel, vanilla and hazelnut are also popular with milk. Make the coffee a little stronger than you would drink it black, and use fresh milk.",
        "links": [("ember-blend", "Ember Blend"), ("dolce-blend", "Dolce Blend"), ("caramel", "Caramel"), ("vanilla", "Vanilla"), ("hazelnut", "Hazelnut")],
    },
    {
        "slug": "moka-pot",
        "ar_title": "إزاي تعمل قهوة بالموكا بوت؟",
        "en_title": "How to brew coffee in a moka pot",
        "answer": "Fill the bottom chamber with hot water up to just below the valve. Fill the basket with medium-fine coffee, a little coarser than espresso, level it without pressing, and screw the top on tight. Heat on low to medium. When the coffee starts to flow, wait until it turns pale and begins to sputter, then take the pot off the heat and run the base under cold water to stop the brew. Stir, and pour. If the cup tastes bitter or burnt, use lower heat or a slightly coarser grind.",
        "links": [("ember-blend", "Ember Blend"), ("aura-blend", "Aura Blend"), ("dolce-blend", "Dolce Blend")],
    },
    {
        "slug": "cold-brew",
        "ar_title": "إزاي تعمل كولد برو في البيت؟",
        "en_title": "How to make cold brew at home",
        "answer": "Mix 100 grams of coarsely ground coffee with 1 litre of cold water in a jar. Stir so all the grounds are wet, cover, and leave in the fridge for 12 to 16 hours. Strain through a paper filter or fine cloth. This makes a strong concentrate, so serve it over ice and dilute with water or milk to taste. Keep it in the fridge and drink it within about five days.",
        "links": [("brazil-parana", "Brazil Paraná"), ("colombia-huila", "Colombia Huila"), ("ember-blend", "Ember Blend")],
    },
    {
        "slug": "v60-pour-over",
        "ar_title": "إزاي تعمل قهوة V60 في البيت؟",
        "en_title": "How to brew V60 pour-over at home",
        "answer": "Use 15 grams of coffee and 250 ml of water as a starting point. Grind medium-fine, a little finer than table salt, and use water just off the boil. Rinse the paper filter, add the coffee, and pour 50 ml to wet the grounds. Wait 30 seconds, then pour the rest in slow circles. Aim to finish in about two and a half to three minutes. If it drips through too fast and tastes sour, grind finer. If it drips slowly and tastes bitter, grind coarser.",
        "links": [("ethiopia-guji", "Ethiopia Guji"), ("ethiopia-dijammah", "Ethiopia Dijammah"), ("colombia-huila", "Colombia Huila")],
    },
    {
        "slug": "turkish-coffee-at-home",
        "ar_title": "إزاي تعمل قهوة تركي في البيت؟",
        "en_title": "How to make Turkish coffee at home",
        "answer": "Use about 7 grams of finely ground Turkish coffee and 70 ml of cold water for each small cup. Put both in a cezve, add sugar now if you want it, and stir once. Heat on low and do not stir again. When the foam rises to the rim, take the cezve off the heat before it boils over. Pour slowly so the foam lands in the cup, and let it rest for a minute so the grounds settle. Sip, and leave the grounds at the bottom. A 20 g bag makes about 2 to 3 cups, so it is an easy way to try.",
        "links": [("turkish-coffee-plain-light", "Turkish Plain Light"), ("turkish-coffee-plain-medium", "Turkish Plain Medium"), ("turkish-coffee-spiced-light", "Turkish Spiced Light"), ("turkish-coffee-spiced-medium", "Turkish Spiced Medium"), ("turkish-coffee-plain-light-20g", "Try a 20 g bag")],
    },
    {
        "slug": "filter-coffee-at-home",
        "ar_title": "كيف أعمل قهوة فلتر في البيت؟",
        "en_title": "How to brew filter coffee at home",
        "answer": "Use 300 ml of water for 20 grams of coffee as a starting point. Grind to a medium size, and use water just off the boil. Pour in slow circles, and finish the brew in about three to four minutes. Adjust the grind if the cup tastes sour or bitter.",
        "links": [("ethiopia-guji", "Ethiopia Guji"), ("ethiopia-dijammah", "Ethiopia Dijammah"), ("brazil-parana", "Brazil Paraná")],
    },
    {
        "slug": "french-press",
        "ar_title": "إزاي تعمل قهوة الفرنش برس في البيت؟",
        "en_title": "How to brew French press at home",
        "answer": "Use 300 ml of water for 20 grams of coffee as a starting point. Grind coarse, like sea salt, and use water just off the boil. Pour the water over the grounds, stir gently, and put the lid on with the plunger up. Wait four minutes, then press down slowly and pour out the whole cup at once so the coffee stops brewing. If the cup tastes bitter, use a slightly coarser grind or a shorter wait. If it tastes sour, wait a little longer or grind a little finer.",
        "links": [("ethiopia-guji", "Ethiopia Guji"), ("colombia-huila", "Colombia Huila"), ("brazil-parana", "Brazil Paraná")],
    },
    {
        "slug": "grind-size",
        "ar_title": "درجة الطحن المناسبة لكل طريقة تحضير",
        "en_title": "How to choose your grind size",
        "answer": "Espresso needs a fine grind, like sand. Filter needs a medium grind, like table salt. French press needs a coarse grind, like sea salt. If your coffee tastes sour, grind finer. If it tastes bitter or harsh, grind coarser.",
        "links": [],
    },
    {
        "slug": "espresso-or-filter",
        "ar_title": "الإسبريسو ولا الفلتر؟ الفرق بينهم",
        "en_title": "Espresso or filter: which is right for you?",
        "answer": "Espresso is a small, strong shot made under pressure, so the body feels heavy and the flavour is concentrated. Filter is a larger, lighter cup that shows more of the coffee's fruit and floral notes. Choose espresso if you drink milk drinks or want a strong shot. Choose filter if you want to taste the origin.",
        "links": [("ember-blend", "Ember Blend"), ("aura-blend", "Aura Blend"), ("dolce-blend", "Dolce Blend"), ("ethiopia-guji", "Ethiopia Guji")],
    },
    {
        "slug": "store-coffee-beans",
        "ar_title": "إزاي تحافظ على البن بعد ما تفتحه",
        "en_title": "How to store coffee beans after opening",
        "answer": "Keep beans in their airtight bag, or move them to an airtight jar. Store them in a cool, dark place away from heat and sunlight. Do not keep them in the fridge, because moisture gets in every time you open it. Use the beans within a few weeks of opening for the best flavour.",
        "links": [],
    },
]


def esc(s):
    return html.escape(str(s), quote=True)


AR_ANSWERS = {
    "aeropress": "استخدم 15 جرامًا من القهوة المطحونة طحنًا متوسطًا إلى ناعم، ونحو 200 مل من الماء بعد الغليان بقليل. ضع فلترًا ورقيًا مشطوفًا في الغطاء، وأضف القهوة، واسكب الماء وقلّب بلطف. ركّب المكبس وانتظر دقيقة تقريبًا. اضغط ببطء على مدى 30 ثانية، وتوقف عندما تسمع صوت فحيح. النتيجة فنجان نظيف وقوي، تشربه كما هو أو تخففه بماء ساخن. إذا كان طعمه مرًّا فاطحن أخشن قليلًا أو اضغط بلطف أكثر.",
    "coffee-to-water-ratio": "للقهوة المفلترة استخدم نحو جرام واحد من القهوة لكل 15 إلى 17 جرامًا من الماء. وللفنجان الواحد سعة 250 مل يعني هذا حوالي 15 إلى 16 جرامًا من القهوة. وفي الإسبريسو نقطة البداية الشائعة 18 جرامًا من القهوة لمشروب وزنه 36 جرامًا، أي نسبة 1 إلى 2. وللقهوة التركي استخدم حوالي 7 جرامات للفنجان الصغير. زن القهوة بميزان بدل الملاعق، لأن حجم الملعقة يختلف كثيرًا. إذا كان الفنجان ضعيفًا فزد القهوة، وإذا كان قويًا فزد الماء.",
    "sour-or-bitter-coffee": "القهوة الحامضة غالبًا لم يُستخلص منها ما يكفي: الماء لم يسحب من البن كفايته. اطحن أنعم، أو استخدم ماءً أسخن، أو أطل وقت التحضير قليلًا. أما القهوة المرّة فغالبًا استُخلص منها أكثر من اللازم. اطحن أخشن، أو استخدم ماءً أبرد قليلًا، أو قصّر وقت التحضير. غيّر شيئًا واحدًا فقط في كل مرة لتعرف ما الذي نفع. وتأكد أيضًا أن الحبوب طازجة، فالقهوة القديمة طعمها باهت وقاسٍ مهما فعلت.",
    "espresso-at-home": "ابدأ بـ 18 جرامًا من القهوة المطحونة ناعمًا، واستهدف نحو 36 جرامًا من الإسبريسو خلال 25 إلى 30 ثانية. سوِّ القهوة وكبسها بالتساوي قبل تثبيت حامل الفلتر. إذا نزل الشوت أسرع من ذلك وكان طعمه حامضًا أو خفيفًا فاطحن أنعم. وإذا نزل أبطأ وكان طعمه مرًّا أو محروقًا فاطحن أخشن. غيّر درجة الطحن فقط بين الشوتات، وتذوّق كل واحد. وأسهل بداية توليفة طازجة مخصصة للإسبريسو.",
    "coffee-roast-levels": "التحميص الفاتح يحتفظ بمزيد من طابع بلد المنشأ: طعمه أكثر إشراقًا وفواكهية، وحموضته أعلى. التحميص المتوسط متوازن، فيه حلاوة ونكهات مثل الشوكولاتة والكراميل. التحميص الغامق أقوى وأدخن، وحموضته أقل وقوامه أثقل. لا توجد درجة أفضل من غيرها. التحميص الفاتح والمتوسط يناسبان القهوة المفلترة، والمتوسط والأغمق شائعان في الإسبريسو ومشروبات الحليب. اختر التحميص حسب النكهة التي تحبها.",
    "decaf-coffee": "القهوة منزوعة الكافيين تُصنع من حبوب قهوة عادية أُزيل معظم كافيينها قبل التحميص. ليست خالية من الكافيين تمامًا، لكن الكمية المتبقية قليلة. والديكاف الجيد يقترب طعمه من القهوة العادية، ويُحضَّر بنفس الطريقة. وهو اختيار جيد للمساء أو لمن يريد تقليل الكافيين. اقرأ على الكيس طريقة إزالة الكافيين وتاريخ التحميص.",
    "coffee-for-milk-drinks": "الحليب يخفف الحموضة ويغطي النكهات الدقيقة، لذلك اختر قهوة بقوام ممتلئ وحلاوة تظل ظاهرة. توليفة إسبريسو متوسطة إلى متوسطة الغامقة بنكهات الشوكولاتة والكراميل تناسب اللاتيه والكابتشينو والفلات وايت. والقهوة المنكّهة مثل الكراميل والفانيليا والبندق شائعة مع الحليب أيضًا. اجعل القهوة أقوى قليلًا مما تشربها سادة، واستخدم حليبًا طازجًا.",
    "moka-pot": "املأ الحوض السفلي بماء ساخن حتى أسفل الصمام بقليل. املأ السلة بقهوة مطحونة طحنًا متوسطًا إلى ناعم، أخشن قليلًا من الإسبريسو، وسوِّها دون كبس، وأغلق الجزء العلوي بإحكام. سخّن على نار هادئة إلى متوسطة. عندما تبدأ القهوة بالنزول، انتظر حتى يصير لونها باهتًا وتبدأ بالطرطشة، ثم ارفع الإبريق عن النار وضع قاعدته تحت ماء بارد لإيقاف التحضير. قلّب وصبّ. إذا كان الطعم مرًّا أو محروقًا فخفف النار أو اطحن أخشن قليلًا.",
    "cold-brew": "اخلط 100 جرام من القهوة المطحونة خشنًا مع لتر من الماء البارد في برطمان. قلّب ليتبلل كل البن، وغطِّه واتركه في الثلاجة من 12 إلى 16 ساعة. صفِّه عبر فلتر ورقي أو قماش ناعم. هذا يعطي مركّزًا قويًا، فقدّمه على الثلج وخففه بالماء أو الحليب حسب ذوقك. احفظه في الثلاجة واشربه خلال خمسة أيام تقريبًا.",
    "v60-pour-over": "ابدأ بـ 15 جرامًا من القهوة و250 مل من الماء. اطحن طحنًا متوسطًا إلى ناعم، أنعم قليلًا من ملح الطعام، واستخدم ماءً بعد الغليان بقليل. اشطف الفلتر الورقي، وأضف القهوة، واسكب 50 مل لترطيب البن. انتظر 30 ثانية ثم اسكب الباقي في دوائر بطيئة. استهدف الانتهاء في حوالي دقيقتين ونصف إلى ثلاث دقائق. إذا نزل الماء بسرعة كبيرة وكان الطعم حامضًا فاطحن أنعم. وإذا نزل ببطء وكان الطعم مرًّا فاطحن أخشن.",
    "turkish-coffee-at-home": "استخدم نحو 7 جرامات من القهوة التركي المطحونة ناعمًا و70 مل من الماء البارد لكل فنجان صغير. ضعهما في الكنكة، وأضف السكر الآن إن أردت، وقلّب مرة واحدة. سخّن على نار هادئة ولا تقلّب مرة أخرى. عندما تصل الرغوة إلى حافة الكنكة، ارفعها عن النار قبل أن تفور وتفيض. صبّ ببطء لتسقط الرغوة في الفنجان، واتركه دقيقة ليترسب البن. ارتشف واترك الرواسب في القاع. كيس 20 جم يكفي لنحو 2 إلى 3 فناجين، فهو طريقة سهلة للتجربة.",
    "filter-coffee-at-home": "ابدأ بـ 300 مل من الماء لكل 20 جرامًا من القهوة. اطحن طحنًا متوسطًا، واستخدم ماءً بعد الغليان بقليل. اسكب في دوائر بطيئة، وأنهِ التحضير في حوالي ثلاث إلى أربع دقائق. عدّل الطحن إذا كان الفنجان حامضًا أو مرًّا.",
    "french-press": "ابدأ بـ 300 مل من الماء لكل 20 جرامًا من القهوة. اطحن خشنًا، مثل ملح البحر، واستخدم ماءً بعد الغليان بقليل. اسكب الماء على البن، وقلّب بلطف، وضع الغطاء والمكبس مرفوع. انتظر أربع دقائق، ثم اضغط ببطء واسكب الفنجان كله دفعة واحدة حتى يتوقف التحضير. إذا كان الطعم مرًّا فاطحن أخشن قليلًا أو قلّل وقت الانتظار. وإذا كان حامضًا فانتظر أطول قليلًا أو اطحن أنعم قليلًا.",
    "grind-size": "الإسبريسو يحتاج طحنًا ناعمًا، مثل الرمل. والفلتر يحتاج طحنًا متوسطًا، مثل ملح الطعام. والفرنش برس يحتاج طحنًا خشنًا، مثل ملح البحر. إذا كان طعم قهوتك حامضًا فاطحن أنعم. وإذا كان مرًّا أو قاسيًا فاطحن أخشن.",
    "espresso-or-filter": "الإسبريسو شوت صغير وقوي يُحضَّر تحت الضغط، لذلك قوامه ثقيل ونكهته مركّزة. أما الفلتر فهو فنجان أكبر وأخف يُظهر نكهات الفواكه والأزهار في القهوة أكثر. اختر الإسبريسو إذا كنت تشرب مشروبات الحليب أو تريد شوتًا قويًا. واختر الفلتر إذا أردت أن تتذوق بلد المنشأ.",
    "store-coffee-beans": "احفظ الحبوب في كيسها المحكم، أو انقلها إلى برطمان محكم الإغلاق. خزّنها في مكان بارد ومظلم بعيدًا عن الحرارة وضوء الشمس. لا تضعها في الثلاجة، لأن الرطوبة تدخل كلما فتحتها. استخدم الحبوب خلال أسابيع قليلة من فتح الكيس للحصول على أفضل نكهة.",
}

AR_LABELS = {
    "ethiopia-guji": "إثيوبيا جوجي", "ethiopia-dijammah": "إثيوبيا دجاما", "colombia-huila": "كولومبيا ويلا",
    "brazil-parana": "البرازيل بارانا", "aura-blend": "أورا بلند", "dolce-blend": "دولتشي بلند",
    "ember-blend": "إمبر بلند", "caramel": "كراميل", "vanilla": "فانيليا", "hazelnut": "بندق",
    "decaf-coffee": "قهوة منزوعة الكافيين",
    "turkish-coffee-plain-light": "تركي سادة فاتح", "turkish-coffee-plain-medium": "تركي سادة وسط",
    "turkish-coffee-spiced-light": "تركي محوّج فاتح", "turkish-coffee-spiced-medium": "تركي محوّج وسط",
    "turkish-coffee-plain-light-20g": "تركي سادة فاتح (20 جم)",
}

FOOTER = """<footer id="contact">
  <div class="container">
    <div class="foot-grid">
      <div>
        <h4>KAIF</h4>
        <p>Specialty coffee beans, roasted in small batches for the Egyptian market.</p>
      </div>
      <div>
        <h4>Shop</h4>
        <ul><li><a href="/#shop">All coffee</a></li></ul>
      </div>
      <div>
        <h4>Delivery &amp; payment</h4>
        <ul class="foot-list">
          <li>Delivery across Egypt</li>
          <li>Cash on delivery</li>
          <li>InstaPay</li>
          <li>Every order confirmed by phone or WhatsApp</li>
        </ul>
      </div>
      <div>
        <h4>Help &amp; contact</h4>
        <ul>
          <li><a href="/#about">About KAIF</a></li>
          <li><a href="/#faq">FAQ</a></li>
          <li><a href="/guides/">Brewing guides</a></li>
          <li><a href="https://wa.me/201043083831" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="https://www.instagram.com/kaif.coffee_eg" target="_blank" rel="noopener">Instagram</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">&copy; 2026 KAIF &ndash; Specialty Coffee. All rights reserved.</div>
  </div>
</footer>"""

LANG_HEAD = """<script>
(function(){var l="en";try{var q=location.search.match(/[?&]lang=(ar|en)/);if(q){l=q[1];localStorage.setItem("kaif-lang",l);}else{l=localStorage.getItem("kaif-lang")||"en";}}catch(e){}
window.KAIF_LANG=l;
if(l==="ar"){document.documentElement.lang="ar";document.documentElement.dir="rtl";document.write('<script src="/ar.js?v=2"><\\/script>');}})();
</script>"""

LANG_JS = """<script>
(function(){
  var btn=document.getElementById("langBtn"),txt=document.getElementById("langBtnText");
  if(!btn)return;
  var ar=window.KAIF_LANG==="ar";
  txt.textContent=ar?"EN":"عربي";
  btn.setAttribute("aria-label",ar?"Switch to English":"التبديل إلى العربية");
  btn.addEventListener("click",function(){
    try{localStorage.setItem("kaif-lang",ar?"en":"ar");}catch(e){}
    location.reload();
  });
})();
</script>"""


def shared_styles():
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    return re.search(r"<style>(.*?)</style>", index, re.S).group(1)


def page(title, description, canonical, body, styles, ar_title=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="KAIF">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
{LANG_HEAD}
<style>{styles}
.ar-only{{display:none}}
html[lang="ar"] .ar-only{{display:revert}}
html[lang="ar"] .en-only{{display:none}}
html[dir="rtl"] .guide .shop-links a{{margin:6px 0 0 8px}}
.guide{{max-width:760px;margin:0 auto;padding:48px 20px}}
.guide h1{{font-size:34px;margin:0 0 6px}}
.guide .en{{color:#5d6a6e;font-size:18px;margin:0 0 24px}}
.guide .answer{{font-size:18px;line-height:1.7;color:#2b3538}}
.guide .shop-links{{margin-top:28px}}
.guide .shop-links a{{display:inline-block;margin:6px 8px 0 0;padding:8px 14px;border:1px solid #cfc7b6;border-radius:999px;color:#1f2a2e;text-decoration:none}}
</style>
</head>
<body data-ar-title="{esc(ar_title)}">
<header>
  <div class="container nav">
    <a href="/" class="brand" aria-label="KAIF home"><span class="cat " aria-hidden="true"><img src="/cat-hero.png" alt="" width="44" height="44"><i class="lid lid-l"></i><i class="lid lid-r"></i><i class="steam"></i><i class="steam s2"></i></span><span>KAIF</span></a>
    <ul class="nav-links" id="navLinks"><li><a href="/#shop">Shop</a></li><li><a href="/guides/">Guides</a></li><li><a href="/#about">About</a></li><li><a href="/#contact">Contact</a></li></ul>
    <div class="nav-actions">
      <button class="lang-btn" id="langBtn" type="button" aria-label="Language"><span id="langBtnText">عربي</span></button>
      <a class="cart-btn" href="/#shop" aria-label="Open cart"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.4 12.2a2 2 0 0 0 2 1.6h8.2a2 2 0 0 0 2-1.5L21 8H6"/></svg></a>
      <button class="menu-toggle" id="menuToggle" type="button" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<script>document.getElementById("menuToggle").addEventListener("click",function(){{var n=document.getElementById("navLinks");n.classList.toggle("open");this.setAttribute("aria-expanded",n.classList.contains("open"));}});</script>
<main>
{body}
</main>
{FOOTER}
{LANG_JS}
</body>
</html>
"""


def guide_body(g):
    ar = AR_ANSWERS.get(g["slug"])
    if g["links"]:
        links = '<div class="shop-links">' + "".join(
            f'<a href="/{esc(slug)}"><span class="en-only">{esc(label)}</span><span class="ar-only">{esc(AR_LABELS.get(slug, label))}</span></a>'
            for slug, label in g["links"]
        ) + "</div>"
    else:
        links = '<div class="shop-links"><a href="/#shop"><span class="en-only">Shop KAIF coffee</span><span class="ar-only">تسوّق قهوة KAIF</span></a></div>'
    ar_p = f'\n  <p class="answer ar-only">{esc(ar)}</p>' if ar else ""
    en_cls = "answer en-only" if ar else "answer"
    return f"""<article class="guide">
  <h1 lang="ar" dir="rtl">{esc(g["ar_title"])}</h1>
  <p class="en en-only">{esc(g["en_title"])}</p>
  <p class="{en_cls}">{esc(g["answer"])}</p>{ar_p}
  {links}
</article>"""


def build():
    styles = shared_styles()
    guides_dir = ROOT / "guides"
    guides_dir.mkdir(exist_ok=True)
    listing = "".join(
        f'<li><a href="/guides/{esc(g["slug"])}"><span class="en-only">{esc(g["en_title"])}</span><span class="ar-only">{esc(g["ar_title"])}</span></a></li>' for g in GUIDES
    )
    index_body = f"""<style>body{{background:linear-gradient(rgba(251,250,247,.6),rgba(251,250,247,.6)),url('/hero_bg.jpg') center/cover fixed no-repeat;min-height:100vh}}.guides-index{{background:rgba(251,250,247,.9);border-radius:0;padding:72px 8vw;margin:0;max-width:none;width:100%;min-height:calc(100vh - 72px);box-sizing:border-box;display:flex;flex-direction:column;justify-content:center;box-shadow:none}}.guides-index h1{{font-size:44px;margin-bottom:14px}}.guides-index .answer{{font-size:18px;margin-bottom:28px}}.guides-index ul{{list-style:none;padding:0}}.guides-index li{{padding:16px 0;border-bottom:1px solid rgba(31,42,46,.12);font-size:18px}}.guides-index li:last-child{{border-bottom:0}}.guides-index a{{text-decoration:none;color:var(--ink);font-weight:600}}.guides-index a:hover{{color:var(--teal-dark);text-decoration:underline}}</style>
<article class="guide guides-index">
  <h1><span class="en-only">Coffee guides</span><span class="ar-only">أدلة القهوة</span></h1>
  <p class="answer"><span class="en-only">Short, practical answers about brewing, grinding and buying specialty coffee.</span><span class="ar-only">إجابات قصيرة وعملية عن تحضير القهوة وطحنها وشرائها.</span></p>
  <ul class="answer">{listing}</ul>
</article>"""
    (guides_dir / "index.html").write_text(
        page("Coffee guides | KAIF", "Short guides on brewing, grinding and storing specialty coffee, from KAIF in Egypt.",
             f"{SITE}/guides/", index_body, styles, "أدلة القهوة"),
        encoding="utf-8",
    )
    urls = [f"{SITE}/guides/"]
    for g in GUIDES:
        out = guides_dir / g["slug"]
        out.mkdir(exist_ok=True)
        desc = g["answer"][:157].rsplit(" ", 1)[0] + "..." if len(g["answer"]) > 160 else g["answer"]
        (out / "index.html").write_text(
            page(f'{g["en_title"]} | KAIF', desc, f'{SITE}/guides/{g["slug"]}', guide_body(g), styles, g["ar_title"]),
            encoding="utf-8",
        )
        urls.append(f'{SITE}/guides/{g["slug"]}')
    # add guide URLs to the sitemap (drop any earlier guide entries first)
    sm = ROOT / "sitemap.xml"
    text = sm.read_text(encoding="utf-8")
    text = re.sub(r"\s*<url>\s*<loc>https://kaifcoffee\.net/guides[^<]*</loc>.*?</url>", "", text, flags=re.S)
    entries = "".join(
        f"\n  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>"
        for u in urls
    )
    text = text.replace("</urlset>", entries + "\n</urlset>")
    sm.write_text(text, encoding="utf-8")
    print(f"built {len(GUIDES)} guides + index")


if __name__ == "__main__":
    build()
