/* KAIF Arabic: loaded only when the visitor chooses Arabic.
   It translates the page text in place, including text the shop adds later
   (products, cart, checkout, quiz). English stays in index.html untouched. */
(function () {
  "use strict";

  var NORM = function (s) {
    return String(s).replace(/[‘’]/g, "'").replace(/\s+/g, " ").trim();
  };

  /* ---------- exact phrases ---------- */
  var RAW = {
    /* navigation and header */
    "Shop": "المتجر", "Guides": "الأدلة", "About": "من نحن", "Contact": "تواصل معنا",
    "Coffee": "القهوة", "All coffee": "كل القهوة", "All": "الكل",
    "Brewing tools": "أدوات التحضير", "Barista tools": "أدوات الباريستا",
    "Open cart": "افتح السلة", "Open menu": "افتح القائمة", "Close": "إغلاق",
    "KAIF home": "الصفحة الرئيسية", "Chat with KAIF on WhatsApp": "تحدث مع KAIF على واتساب",
    "Shopping cart and checkout": "السلة وإتمام الطلب", "Why order from KAIF": "لماذا تطلب من KAIF",
    "Map of coffee origins": "خريطة أصول القهوة", "Filter coffee": "قهوة فلتر",

    /* hero and trust strip */
    "KAIF · Specialty coffee · Egypt": "KAIF · قهوة مختصة · مصر",
    "Specialty coffee, roasted in small batches": "قهوة مختصة، محمّصة على دفعات صغيرة",
    "Beans from around the world, roasted in Egypt and delivered to your door.": "حبوب من أنحاء العالم، محمّصة في مصر وتصلك حتى باب بيتك.",
    "Shop Now": "تسوّق الآن", "Find your coffee": "اعثر على قهوتك",
    "Roasted in small batches": "تحميص على دفعات صغيرة",
    "Roasted in Egypt, a little at a time.": "نحمّص في مصر، كمية صغيرة كل مرة.",
    "Delivery across Egypt": "توصيل لجميع أنحاء مصر",
    "Confirmed by phone or WhatsApp": "نؤكد الطلب بالهاتف أو واتساب",
    "Cash on delivery or InstaPay": "الدفع عند الاستلام أو إنستاباي",
    "Origin, roast and tasting notes on every bag": "بلد المنشأ ودرجة التحميص ونكهات القهوة على كل كيس",
    "Packed with the details": "كل التفاصيل على الكيس",
    "250g bags with origin, roast and tasting notes on the label.": "أكياس 250 جم وعليها بلد المنشأ ودرجة التحميص والنكهات.",
    "Small batches": "دفعات صغيرة", "Roasted in Egypt": "محمّصة في مصر",
    "Clear labels": "ملصقات واضحة", "Pay your way": "ادفع بالطريقة التي تناسبك",
    "Delivered to your door": "توصيل حتى الباب",
    "Across Egypt, confirmed by phone or WhatsApp.": "في جميع أنحاء مصر، ونؤكد معك بالهاتف أو واتساب.",
    "Every order confirmed by phone or WhatsApp": "كل طلب نؤكده معك بالهاتف أو واتساب",
    "Cash on delivery": "الدفع عند الاستلام", "InstaPay": "إنستاباي",

    /* shop section */
    "Our Specialty Coffee": "قهوتنا المختصة",
    "Bags are 250g, or 20g in Tal2eema. Add it to your cart, and we'll confirm your order.": "الأكياس 250 جم، أو 20 جم في Tal2eema. أضف ما تريد إلى السلة وسنؤكد طلبك.",
    "Sort coffee": "ترتيب القهوة", "Best Selling": "الأكثر مبيعًا", "Featured": "مميزة",
    "Price: low to high": "السعر: من الأقل إلى الأعلى", "Price: high to low": "السعر: من الأعلى إلى الأقل",
    "Name A–Z": "الاسم من الألف إلى الياء",
    "Loading coffee…": "جارٍ تحميل القهوة…", "Add to cart": "أضف إلى السلة",
    "Added to cart": "تمت الإضافة إلى السلة", "Added ✓": "تمت الإضافة ✓", "Added to your cart": "تمت الإضافة إلى سلتك",
    "View details": "عرض التفاصيل", "Coming soon": "قريبًا", "Not available": "غير متاح", "Not available yet": "غير متاح بعد",
    "More coming soon in this category.": "المزيد قريبًا في هذا القسم.",
    "Tal2eema bags are 20 g each. If you order only Tal2eema, the minimum is 4 bags. Add any other coffee and there is no minimum.": "أكياس Tal2eema وزن الكيس 20 جم. إذا طلبت Tal2eema فقط فالحد الأدنى 4 أكياس. وإذا أضفت أي قهوة أخرى فلا يوجد حد أدنى.",
    "Ordering only Tal2eema? The minimum is 4 bags. Add any other coffee and there is no minimum.": "تطلب Tal2eema فقط؟ الحد الأدنى 4 أكياس. أضف أي قهوة أخرى وسيختفي الحد الأدنى.",
    "Add more bags to your cart: orders with only Tal2eema need at least 4 bags.": "أضف أكياسًا أخرى إلى السلة: الطلبات التي فيها Tal2eema فقط تحتاج 4 أكياس على الأقل.",
    "Quantity": "الكمية", "Increase": "زيادة", "Decrease": "تقليل", "More": "المزيد", "Fewer": "أقل",
    "More bags": "أكياس أكثر", "Fewer bags": "أكياس أقل", "Previous photo": "الصورة السابقة", "Next photo": "الصورة التالية",
    "At a glance": "نظرة سريعة",

    /* categories (from the shop database) */
    "Single Origin": "أحادية المصدر", "Blends": "توليفات", "Flavoured": "بنكهات", "Decaf": "منزوعة الكافيين",
    "Turkish Coffee": "قهوة تركي", "Turkish": "تركي", "Tal2eema": "Tal2eema", "Tools": "الأدوات",
    "Single origin": "أحادية المصدر", "Blend": "توليفة", "Specialty blend": "توليفة مختصة",
    "Flavoured filter coffee": "قهوة فلتر بنكهة", "99.9% decaffeinated": "منزوعة الكافيين بنسبة 99.9%",
    "Plain": "سادة", "Spiced": "محوّج", "Plain · Light roast": "سادة · تحميص فاتح",

    /* product spec labels and values */
    "Origin": "بلد المنشأ", "Roast": "التحميص", "Process": "المعالجة", "Variety": "الصنف", "Altitude": "الارتفاع",
    "Body": "القوام", "Acidity": "الحموضة", "Sweetness": "الحلاوة", "Aftertaste": "الطعم المتبقي",
    "Format": "الشكل", "Type": "النوع", "Brew": "التحضير", "Whole beans": "حبوب كاملة",
    "Washed": "مغسولة", "Natural": "طبيعية", "Light": "فاتح", "Medium": "متوسط", "Dark": "غامق",
    "Medium dark": "متوسط إلى غامق", "Light roast": "تحميص فاتح", "Medium roast": "تحميص متوسط",
    "Dark roast": "تحميص غامق", "Medium dark roast": "تحميص متوسط إلى غامق", "Darker roast": "تحميص أغمق",
    "Decaffeinated": "منزوعة الكافيين",
    "Cinnamon": "قرفة", "Red Fruit": "فواكه حمراء", "Almond": "لوز", "Orange Blossom": "زهر البرتقال", "Fig": "تين",
    "Caramel": "كراميل", "Chocolate": "شوكولاتة", "Lemon Citrus": "ليمون وحمضيات", "Berry": "توت",
    "Strawberry": "فراولة", "Lime": "ليمون أخضر", "Floral": "زهري", "Apricot": "مشمش", "Honey": "عسل",
    "Blueberry": "توت أزرق", "Peach": "خوخ", "Mango": "مانجو", "Dark Chocolate": "شوكولاتة داكنة",
    "Roasted Nuts": "مكسرات محمّصة", "Nuts": "مكسرات", "Brown Sugar": "سكر بني", "Vanilla": "فانيليا", "Hazelnut": "بندق",
    "Berries, citrus, floral": "توت وحمضيات وأزهار", "Chocolate, nuts, caramel": "شوكولاتة ومكسرات وكراميل",
    "Caramel, hazelnut, vanilla": "كراميل وبندق وفانيليا",
    "Chocolate, lemon citrus, berry": "شوكولاتة وليمون وتوت",
    "Cinnamon, red fruit, almond": "قرفة وفواكه حمراء ولوز",
    "Orange blossom, fig, caramel": "زهر البرتقال وتين وكراميل",
    "Strawberry, lime, caramel": "فراولة وليمون أخضر وكراميل",

    "Rwanda Ruhango": "رواندا روهانجو", "Rwanda, Ruhango": "رواندا، روهانجو", "Rwanda": "رواندا", "Ruhango": "روهانجو",
    "Cherry · Molasses · Mandarin": "كرز · دبس · يوسفي", "Cherry": "كرز", "Molasses": "دبس", "Mandarin": "يوسفي",
    "Chocolatey and bold": "شوكولاتة وقوة", "No caffeine": "بدون كافيين", "Turkish grind": "طحن تركي", "NA": "—",
    "Turkish Coffee, Plain, Light Roast": "قهوة تركي سادة، تحميص فاتح",

    /* origin names */
    "Ethiopia": "إثيوبيا", "Colombia": "كولومبيا", "Brazil": "البرازيل",
    "Oromia (Guji)": "أوروميا (جوجي)", "Oromia, Guji": "أوروميا، جوجي", "Guji": "جوجي", "Oromia": "أوروميا",
    "Kaffa": "كافا", "Kaffa, Ethiopia": "كافا، إثيوبيا", "Huila": "ويلا", "Huila, Colombia": "ويلا، كولومبيا",
    "Paraná": "بارانا", "Jacarezinho, Paraná": "جاكاريزينيو، بارانا", "Castillo, Huila": "كاستيو، ويلا",
    "Brazil, Paraná": "البرازيل، بارانا", "Colombia, Huila": "كولومبيا، ويلا", "Ethiopia, Guji": "إثيوبيا، جوجي",
    "Ethiopia, Kaffa": "إثيوبيا، كافا", "Ethiopia, Oromia (Guji)": "إثيوبيا، أوروميا (جوجي)",
    "Castillo": "كاستيو", "Jacarezinho": "جاكاريزينيو", "Dijammah": "دجاما",

    /* product names */
    "Ethiopia Guji": "إثيوبيا جوجي", "Ethiopia Dijammah": "إثيوبيا دجاما", "Colombia Huila": "كولومبيا ويلا",
    "Brazil Paraná": "البرازيل بارانا", "Aura Blend": "أورا بلند", "Dolce Blend": "دولتشي بلند",
    "Ember Blend": "إمبر بلند", "Caramel": "كراميل", "Decaf Coffee": "قهوة منزوعة الكافيين",
    "Turkish Coffee, Plain, Light Roast": "قهوة تركي سادة، تحميص فاتح",
    "Turkish Coffee, Plain, Medium Roast": "قهوة تركي سادة، تحميص وسط",
    "Turkish Coffee, Spiced, Light Roast": "قهوة تركي محوّجة، تحميص فاتح",
    "Turkish Coffee, Spiced, Medium Roast": "قهوة تركي محوّجة، تحميص وسط",
    "AeroPress Original": "إيروبريس أوريجينال", "AeroPress": "إيروبريس",
    "Anti-Static Coffee Bean Spray Bottle": "زجاجة رش لحبوب القهوة ضد الكهرباء الساكنة",
    "BaristaSpace Stainless Steel Pitcher With Splash 600ml": "إبريق حليب ستانلس ستيل BaristaSpace بتصميم رذاذ، سعة 600 مل",
    "Hario V60 Ceramic Dripper 02, White": "قمع هاريو V60 سيراميك مقاس 02، أبيض",
    "Hario V60 Paper Filters, White, Size 02 (100 sheets)": "فلاتر ورقية هاريو V60 مقاس 02، أبيض (100 ورقة)",
    "Rhino Shot Glass 2oz Lined": "كوب شوت Rhino سعة 2 أونصة بخطوط قياس",
    "Timemore Scale, Black": "ميزان تايم مور، أسود", "Timemore Scale, White": "ميزان تايم مور، أبيض",
    "Timemore Scale, Black/White": "ميزان تايم مور، أسود/أبيض",
    "Barista Space": "Barista Space", "Hario": "هاريو", "Rhino": "Rhino", "Timemore": "تايم مور",
    "Specialty blend · Medium roast · Pure Arabica (100%)": "توليفة مختصة · تحميص متوسط · عربيكا 100%",
    "Specialty blend · Medium roast · 80% Arabica, 20% Robusta": "توليفة مختصة · تحميص متوسط · 80% عربيكا و20% روبوستا",
    "Specialty blend · Dark roast · Built on 70% Arabica and 30% Robusta": "توليفة مختصة · تحميص غامق · 70% عربيكا و30% روبوستا",
    "Flavoured filter coffee · 80% Arabica, 20% Robusta": "قهوة فلتر بنكهة · 80% عربيكا و20% روبوستا",
    "Spiced · Light roast": "محوّجة · تحميص فاتح", "Spiced · Medium roast": "محوّجة · تحميص متوسط",
    "Plain · Medium roast": "سادة · تحميص متوسط",

    /* product descriptions */
    "A natural-process single origin from Jacarezinho in Paraná, Brazil, grown at 800 to 1,000 metres. Full-bodied, with cinnamon, red fruit and almond. Medium dark roast, brewed as filter.": "قهوة أحادية المصدر بمعالجة طبيعية من جاكاريزينيو في بارانا بالبرازيل، تُزرع على ارتفاع 800 إلى 1000 متر. قوامها ممتلئ، وفيها نكهات القرفة والفواكه الحمراء واللوز. تحميص متوسط إلى غامق، وتناسب القهوة المفلترة.",
    "A flavoured filter coffee with caramel. A blend of 80% Arabica and 20% Robusta, roasted medium dark and sold as whole beans.": "قهوة فلتر بنكهة الكراميل. توليفة من 80% عربيكا و20% روبوستا، محمّصة تحميصًا متوسطًا إلى غامق وتُباع حبوبًا كاملة.",
    "A flavoured filter coffee with caramel. A blend of 80% Arabica and 20% Robusta, roasted medium dark and sold as whole beans in a 20 g Tal2eema bag.": "قهوة فلتر بنكهة الكراميل. توليفة من 80% عربيكا و20% روبوستا، محمّصة تحميصًا متوسطًا إلى غامق وتُباع حبوبًا كاملة في كيس Tal2eema وزن 20 جم.",
    "A washed Castillo from Huila, Colombia, grown at 1,500 to 2,000 metres. Soft and sweet, with orange blossom, fig and caramel. A balanced cup that works for espresso and filter.": "قهوة كاستيو مغسولة من ويلا في كولومبيا، تُزرع على ارتفاع 1500 إلى 2000 متر. ناعمة وحلوة، وفيها زهر البرتقال والتين والكراميل. فنجان متوازن يناسب الإسبريسو والفلتر.",
    "99.9% decaffeinated specialty Arabica, with notes of nuts, brown sugar and dark chocolate. Sold as whole beans and brewed as espresso or filter.": "عربيكا مختصة منزوعة الكافيين بنسبة 99.9%، بنكهات المكسرات والسكر البني والشوكولاتة الداكنة. تُباع حبوبًا كاملة وتناسب الإسبريسو والفلتر.",
    "A natural-process coffee from Dijammah in Kaffa, Ethiopia, grown at 1,800 to 2,200 metres. Bright and fruity, with chocolate, lemon citrus and berry. Brewed as filter.": "قهوة بمعالجة طبيعية من دجاما في كافا بإثيوبيا، تُزرع على ارتفاع 1800 إلى 2200 متر. منعشة وفواكهية، وفيها الشوكولاتة والليمون والتوت. تناسب القهوة المفلترة.",
    "A washed coffee from Guji in Oromia, Ethiopia, grown at 1,900 to 2,300 metres. Lively acidity and real sweetness, with strawberry, lime and caramel. Medium roast, for espresso and filter.": "قهوة مغسولة من جوجي في أوروميا بإثيوبيا، تُزرع على ارتفاع 1900 إلى 2300 متر. حموضة حيوية وحلاوة حقيقية، وفيها الفراولة والليمون الأخضر والكراميل. تحميص متوسط، للإسبريسو والفلتر.",
    "A flavoured filter coffee with hazelnut. A blend of 80% Arabica and 20% Robusta, roasted medium dark and sold as whole beans.": "قهوة فلتر بنكهة البندق. توليفة من 80% عربيكا و20% روبوستا، محمّصة تحميصًا متوسطًا إلى غامق وتُباع حبوبًا كاملة.",
    "A flavoured filter coffee with hazelnut. A blend of 80% Arabica and 20% Robusta, roasted medium dark and sold as whole beans in a 20 g Tal2eema bag.": "قهوة فلتر بنكهة البندق. توليفة من 80% عربيكا و20% روبوستا، محمّصة تحميصًا متوسطًا إلى غامق وتُباع حبوبًا كاملة في كيس Tal2eema وزن 20 جم.",
    "A flavoured filter coffee with vanilla. A blend of 80% Arabica and 20% Robusta, roasted medium dark and sold as whole beans.": "قهوة فلتر بنكهة الفانيليا. توليفة من 80% عربيكا و20% روبوستا، محمّصة تحميصًا متوسطًا إلى غامق وتُباع حبوبًا كاملة.",
    "A flavoured filter coffee with vanilla. A blend of 80% Arabica and 20% Robusta, roasted medium dark and sold as whole beans in a 20 g Tal2eema bag.": "قهوة فلتر بنكهة الفانيليا. توليفة من 80% عربيكا و20% روبوستا، محمّصة تحميصًا متوسطًا إلى غامق وتُباع حبوبًا كاملة في كيس Tal2eema وزن 20 جم.",
    "Finely ground Turkish coffee with a light roast. Clean, bright flavour with no added ingredients. Brew in a cezve and serve unfiltered. 250 g.": "قهوة تركي مطحونة ناعمًا بتحميص فاتح. نكهة نقية ومنعشة بدون أي إضافات. تُحضَّر في الكنكة وتُقدَّم بدون تصفية. 250 جم.",
    "Finely ground Turkish coffee with a light roast. Clean, bright flavour with no added ingredients. Brew in a cezve and serve unfiltered. 20 g.": "قهوة تركي مطحونة ناعمًا بتحميص فاتح. نكهة نقية ومنعشة بدون أي إضافات. تُحضَّر في الكنكة وتُقدَّم بدون تصفية. 20 جم.",
    "Finely ground Turkish coffee with a medium roast. Fuller, rounder flavour with no added ingredients. Brew in a cezve and serve unfiltered. 250 g.": "قهوة تركي مطحونة ناعمًا بتحميص متوسط. نكهة أغنى وأكثر استدارة بدون أي إضافات. تُحضَّر في الكنكة وتُقدَّم بدون تصفية. 250 جم.",
    "Finely ground Turkish coffee with a medium roast. Fuller, rounder flavour with no added ingredients. Brew in a cezve and serve unfiltered. 20 g.": "قهوة تركي مطحونة ناعمًا بتحميص متوسط. نكهة أغنى وأكثر استدارة بدون أي إضافات. تُحضَّر في الكنكة وتُقدَّم بدون تصفية. 20 جم.",
    "Finely ground Turkish coffee with a light roast and added spices. Bright base with a warm, aromatic finish. Brew in a cezve and serve unfiltered. 250 g.": "قهوة تركي مطحونة ناعمًا بتحميص فاتح مع التحويجة. أساس منعش ونهاية دافئة عطرية. تُحضَّر في الكنكة وتُقدَّم بدون تصفية. 250 جم.",
    "Finely ground Turkish coffee with a light roast and added spices. Bright base with a warm, aromatic finish. Brew in a cezve and serve unfiltered. 20 g.": "قهوة تركي مطحونة ناعمًا بتحميص فاتح مع التحويجة. أساس منعش ونهاية دافئة عطرية. تُحضَّر في الكنكة وتُقدَّم بدون تصفية. 20 جم.",
    "Finely ground Turkish coffee with a medium roast and added spices. Fuller base with a warm, aromatic finish. Brew in a cezve and serve unfiltered. 250 g.": "قهوة تركي مطحونة ناعمًا بتحميص متوسط مع التحويجة. أساس أغنى ونهاية دافئة عطرية. تُحضَّر في الكنكة وتُقدَّم بدون تصفية. 250 جم.",
    "Finely ground Turkish coffee with a medium roast and added spices. Fuller base with a warm, aromatic finish. Brew in a cezve and serve unfiltered. 20 g.": "قهوة تركي مطحونة ناعمًا بتحميص متوسط مع التحويجة. أساس أغنى ونهاية دافئة عطرية. تُحضَّر في الكنكة وتُقدَّم بدون تصفية. 20 جم.",
    "A quick, easy brewer that blends a few methods in one. You get a rich, clean cup in about two minutes, and you can change the recipe to suit your taste.": "أداة تحضير سريعة وسهلة تجمع عدة طرق في واحدة. تحصل على فنجان غني ونظيف في دقيقتين تقريبًا، ويمكنك تعديل الوصفة على ذوقك.",
    "A small spray bottle for misting beans or grounds before grinding. One or two sprays cut down on static, so grounds don't clump or cling to the grinder. Its compact aluminium and glass body fits easily on any counter.": "زجاجة رش صغيرة لرذاذ الحبوب أو البن قبل الطحن. رشة أو رشتان تقللان الكهرباء الساكنة فلا يتكتل البن ولا يلتصق بالمطحنة. جسمها المدمج من الألومنيوم والزجاج يناسب أي رف.",
    "A stainless steel pitcher for steaming and frothing milk for cappuccinos and lattes. Its moulded spout gives you precise control over the flow, which helps when you're pouring latte art. The 600 ml size holds enough milk for one or two drinks.": "إبريق ستانلس ستيل لتسخين الحليب ورغوته للكابتشينو واللاتيه. فوهته المصبوبة تعطيك تحكمًا دقيقًا في التدفق، وهذا يساعد في رسم اللاتيه آرت. سعة 600 مل تكفي حليبًا لمشروب أو اثنين.",
    "A cone-shaped pour-over dripper that many baristas use. Its single large hole and spiral ribs keep the water flowing evenly, and changing how fast you pour lets you make a lighter or a stronger cup.": "قمع تحضير مخروطي الشكل يستخدمه كثير من الباريستا. ثقبه الكبير الواحد وأضلاعه الحلزونية يحافظان على تدفق الماء بالتساوي، وبتغيير سرعة الصب تحصل على فنجان أخف أو أقوى.",
    "Paper filters cut for the V60 size 02 dripper, for one to four cups. They're biodegradable and chemical-free, and they let the coffee's flavour come through clearly. Rinse them with hot water before brewing to remove any papery taste.": "فلاتر ورقية مقصوصة لقمع V60 مقاس 02، من فنجان إلى أربعة. قابلة للتحلل وخالية من المواد الكيميائية، وتترك نكهة القهوة واضحة. اشطفها بالماء الساخن قبل التحضير لإزالة طعم الورق.",
    "A small heat-resistant glass that holds about 60 ml, enough for a single espresso shot. Its measurement lines every half ounce help you check your shots and measure liquids or dry ingredients in the kitchen.": "كوب زجاجي صغير مقاوم للحرارة يسع نحو 60 مل، يكفي شوت إسبريسو واحدًا. خطوط القياس كل نصف أونصة تساعدك على متابعة الشوت وقياس السوائل أو المكونات الجافة في المطبخ.",
    "A compact digital scale for weighing beans and water. It reads from 0.1 g up to 2 kg, has a built-in timer and a flow-rate readout, and charges by USB so you can keep brewing the same cup every time.": "ميزان رقمي صغير لوزن الحبوب والماء. يقرأ من 0.1 جم حتى 2 كجم، وفيه مؤقت مدمج وعرض لمعدل التدفق، ويُشحن بـ USB لتحضّر نفس الفنجان في كل مرة.",

    /* about */
    "About KAIF": "عن KAIF", "Roasted in Egypt, a little at a time": "محمّصة في مصر، قليلًا في كل مرة",
    "KAIF roasts specialty beans from Ethiopia, Colombia and Brazil in small batches in Egypt. Every bag is labelled with its origin, roast and tasting notes, then delivered across Egypt.": "تحمّص KAIF حبوبًا مختصة من إثيوبيا وكولومبيا والبرازيل على دفعات صغيرة في مصر. على كل كيس بلد المنشأ ودرجة التحميص ونكهات القهوة، ثم نوصله إلى جميع أنحاء مصر.",
    "We take coffee seriously. The cat takes it personally.": "نحن نأخذ القهوة بجدية. أما القط فيأخذها على محمل شخصي.",
    "The cat inspects each one. He is rarely impressed, which is how we know it's good.": "القط يفحص كل كيس. نادرًا ما يعجبه شيء، ولهذا نعرف أن القهوة جيدة.",
    "Specialty coffee beans, roasted in small batches for the Egyptian market.": "حبوب قهوة مختصة، محمّصة على دفعات صغيرة للسوق المصري.",
    "Brewed for coffee nerds": "مصنوعة لعشّاق القهوة",
    "From farm to your cup": "من المزرعة إلى فنجانك", "Follow the cat. He knows the way.": "اتبع القط. هو يعرف الطريق.",
    "Where our coffee comes from": "من أين تأتي قهوتنا", "Beans from Ethiopia, Colombia and Brazil.": "حبوب من إثيوبيا وكولومبيا والبرازيل.",
    "Tap a pin on the map to see its notes.": "اضغط على علامة في الخريطة لترى ملاحظاتها.",
    "Tap a pin to see the origin. Locations are approximate, at region level.": "اضغط على علامة لترى بلد المنشأ. المواقع تقريبية على مستوى المنطقة.",
    "Grown at origin": "تُزرع في بلد المنشأ", "Small-batch roasting": "تحميص على دفعات صغيرة",
    "© OpenStreetMap contributors": "© مساهمو OpenStreetMap",

    /* quiz */
    "Not sure where to start?": "لست متأكدًا من أين تبدأ؟",
    "Find your coffee in 3 taps": "اعثر على قهوتك بثلاث ضغطات",
    "Tell the cat how you brew and what you like.": "أخبر القط كيف تحضّر قهوتك وماذا تحب.",
    "Three taps and the cat picks a bag for you": "ثلاث ضغطات ويختار لك القط كيسًا",
    "Find your match →": "اعثر على ما يناسبك ←", "Start": "ابدأ",
    "How do you brew at home?": "كيف تحضّر قهوتك في البيت؟",
    "Espresso machine": "ماكينة إسبريسو", "Or a moka pot": "أو موكا بوت",
    "Filter or V60": "فلتر أو V60", "Pour-over, drip, French press": "تقطير أو فلتر أو فرنش برس",
    "Turkish, in a kanaka": "تركي، في الكنكة", "Not sure yet": "لست متأكدًا بعد", "Show me something easy": "اقترح عليّ شيئًا سهلًا",
    "Plain or spiced?": "سادة أم محوّجة؟", "Which roast?": "أي تحميص تفضّل؟",
    "What taste do you enjoy?": "أي طعم تحب؟",
    "Fruity and bright": "فواكهي ومنعش", "Chocolatey and nutty": "شوكولاتة ومكسرات", "Sweet and flavoured": "حلو وبنكهة",
    "How strong do you like it?": "ما درجة القوة التي تحبها؟",
    "Light and smooth": "خفيفة وناعمة", "Balanced": "متوازنة", "Bold and dark": "قوية وغامقة",
    "No caffeine, please": "بدون كافيين من فضلك",
    "What size would you like?": "أي حجم تريد؟", "A full bag": "كيس كامل", "A small bag to try": "كيس صغير للتجربة",
    "20 g, easy to carry or travel with": "20 جم، سهل الحمل والسفر",
    "250 g": "250 جم", "20 g": "20 جم",
    "← Back": "→ رجوع", "Back": "رجوع", "Start again": "ابدأ من جديد",
    "This one is for you.": "هذا الكيس لك.",
    "Not ready for a full bag?": "لست جاهزًا لكيس كامل؟",
    "The shop is still loading. Try again in a moment.": "المتجر ما زال يُحمَّل. حاول مرة أخرى بعد لحظة.",
    "Order the same again": "اطلب نفس الطلب مرة أخرى", "order the same again": "اطلب نفس الطلب مرة أخرى",
    "Order again": "اطلب مرة أخرى",

    /* cat lines */
    "Nice pick.": "اختيار جميل.", "Excellent choice.": "اختيار ممتاز.", "Good taste.": "ذوقك رائع.",
    "In the cart it goes.": "إلى السلة.", "Stocking up, I see.": "تخزّن القهوة، فهمت.",
    "Three bags. Now we're talking.": "ثلاثة أكياس. الآن نتفاهم.", "The usual. Coming right up.": "المعتاد. حاضر.",
    "Added. I approve.": "تمت الإضافة. أوافق.", "First one in. Good start.": "أول كيس. بداية موفقة.",
    "Coffee at this hour? Respect.": "قهوة في هذه الساعة؟ تحية لك.",
    "I was drinking that.": "كنت أشرب هذا!", "That was my last cup.": "كان هذا آخر فنجان لي.",
    "You owe me a coffee.": "أنت مدين لي بفنجان قهوة.",
    "Welcome back. Same again?": "أهلًا بعودتك. نفس الطلب؟",
    "Your cart is empty. The cat is napping until you pick a bag.": "سلتك فارغة. القط نائم حتى تختار كيسًا.",
    "Your cart": "سلتك", "Cart": "السلة", "View cart": "عرض السلة", "Continue shopping": "تابع التسوق",
    "Browse coffee": "تصفّح القهوة", "Remove": "إزالة",

    /* checkout */
    "Review order": "راجع الطلب", "Cart": "السلة", "Review your order": "راجع طلبك", "Review": "المراجعة", "Delivery": "التوصيل",
    "Delivery details": "بيانات التوصيل", "Continue to delivery": "المتابعة إلى التوصيل",
    "Subtotal": "المجموع الفرعي", "Total": "الإجمالي", "Total:": "الإجمالي:", "Your coffee": "قهوتك",
    "Where should we deliver?": "أين نوصّل؟", "Who is this for?": "لمن هذا الطلب؟", "Deliver to": "التوصيل إلى",
    "Full name": "الاسم بالكامل", "Mobile number": "رقم الموبايل", "Email (optional)": "البريد الإلكتروني (اختياري)",
    "Governorate": "المحافظة", "Area": "المنطقة", "Street and number": "الشارع ورقم المبنى",
    "Building": "المبنى", "Floor": "الدور", "Apartment": "الشقة", "Near": "بالقرب من",
    "Nearby landmark (optional)": "علامة مميزة قريبة (اختياري)",
    "Notes for the courier (optional)": "ملاحظات للمندوب (اختياري)",
    "Next to a mosque, mall, metro station...": "بجوار مسجد أو مول أو محطة مترو...",
    "Your city, town or neighbourhood": "مدينتك أو بلدتك أو حيّك",
    "Choose your area": "اختر منطقتك", "Choose a governorate first": "اختر المحافظة أولًا", "Choose governorate": "اختر المحافظة",
    "Choose": "اختر", "Pay with": "طريقة الدفع", "Card": "بطاقة",
    "We call or WhatsApp this number to confirm your order.": "سنتصل بهذا الرقم أو نراسلك على واتساب لتأكيد طلبك.",
    "We'll call or WhatsApp you on": "سنتصل بك أو نراسلك على واتساب على الرقم",
    "to confirm your delivery.": "لتأكيد التوصيل.",
    "Place order": "تأكيد الطلب", "Placing your order...": "جارٍ إرسال طلبك...",
    "Order placed": "تم إرسال الطلب", "Your order has been received.": "تم استلام طلبك.",
    "Message us on WhatsApp": "راسلنا على واتساب", "Try again": "حاول مرة أخرى",
    "The coffee didn't load": "تعذّر تحميل القهوة", "Please check your connection and try again.": "تحقق من اتصالك بالإنترنت وحاول مرة أخرى.",
    "We'll send you our InstaPay details to confirm your order.": "سنرسل لك بيانات إنستاباي لتأكيد طلبك.",
    "Please enter your full name.": "من فضلك اكتب اسمك بالكامل.",
    "Please enter a valid mobile number.": "من فضلك اكتب رقم موبايل صحيحًا.",
    "Please choose a governorate.": "من فضلك اختر المحافظة.", "Please choose your area.": "من فضلك اختر المنطقة.",
    "Please enter your street and number.": "من فضلك اكتب الشارع ورقم المبنى.",
    "That email doesn't look right. Fix it or leave it empty.": "البريد الإلكتروني غير صحيح. صحّحه أو اتركه فارغًا.",
    "We couldn't place your order. Please try again.": "تعذّر إرسال طلبك. حاول مرة أخرى.",
    "Dismiss": "إغلاق", "01x xxxx xxxx": "01x xxxx xxxx",

    /* FAQ */
    "FAQ": "الأسئلة الشائعة", "Coffee questions, answered by the nerds who roast them.": "أسئلة عن القهوة، يجيب عنها من يحمّصونها.",
    "Delivery & payment": "التوصيل والدفع",
    "How do I order?": "كيف أطلب؟",
    "Add your bags to the cart and place the order. We confirm every order by phone or WhatsApp before we ship.": "أضف الأكياس إلى السلة وأرسل الطلب. نؤكد كل طلب بالهاتف أو واتساب قبل الشحن.",
    "Where do you deliver?": "إلى أين توصّلون؟",
    "We deliver across Egypt. We confirm the delivery fee and timing with you by phone or WhatsApp before we ship.": "نوصّل إلى جميع أنحاء مصر. نؤكد معك رسوم التوصيل وموعده بالهاتف أو واتساب قبل الشحن.",
    "Should I buy whole beans or ground coffee?": "هل أشتري حبوبًا كاملة أم قهوة مطحونة؟",
    "Whole beans, always. Coffee loses its flavour fast once it's ground, so grind it just before you brew. Every bag in our shop is whole beans.": "حبوبًا كاملة دائمًا. تفقد القهوة نكهتها بسرعة بعد الطحن، لذلك اطحنها قبل التحضير مباشرة. كل الأكياس في متجرنا حبوب كاملة.",
    "What grind do I need?": "ما درجة الطحن المناسبة؟",
    "Espresso: fine. Pour-over or filter: medium. French press: coarse. Too fine for your brewer tastes bitter, and too coarse tastes sour and weak.": "الإسبريسو: ناعم. التقطير أو الفلتر: متوسط. الفرنش برس: خشن. إذا كان الطحن أنعم من اللازم يصبح الطعم مرًّا، وإذا كان أخشن يصبح حامضًا وضعيفًا.",
    "What's the difference between single origin, blends and flavoured?": "ما الفرق بين الأحادية المصدر والتوليفات والمنكّهة؟",
    "Single origin tastes like one farm or region, so you get its character straight. Blends mix beans to balance the flavour. Flavoured bags have added flavour on top of Arabica and Robusta beans.": "القهوة أحادية المصدر تعبّر عن مزرعة أو منطقة واحدة، فتحصل على طابعها كما هو. التوليفات تمزج الحبوب لتوازن النكهة. الأكياس المنكّهة فيها نكهة مضافة فوق حبوب العربيكا والروبوستا.",
    "How should I store my beans?": "كيف أحفظ الحبوب؟",
    "Keep them in the sealed bag or an airtight jar, somewhere cool and dark. Skip the fridge, since it adds moisture. If you won't finish them within a month, freeze them in small portions.": "احفظها في الكيس المغلق أو في برطمان محكم، في مكان بارد ومظلم. تجنّب الثلاجة لأنها تضيف رطوبة. وإذا لن تنهيها خلال شهر فجمّدها في أجزاء صغيرة.",
    "Is my coffee fresh?": "هل قهوتي طازجة؟",
    "We roast in small batches, so every bag is made close to when it reaches you. Want to know the roast date of your bag? Message us on WhatsApp and we'll tell you.": "نحمّص على دفعات صغيرة، فكل كيس يُجهَّز قريبًا من موعد وصوله إليك. تريد معرفة تاريخ تحميص كيسك؟ راسلنا على واتساب وسنخبرك.",
    "Is the decaf really decaf?": "هل القهوة منزوعة الكافيين خالية فعلًا؟",
    "Our decaf is 99.9% decaffeinated, so you can enjoy a cup late at night without the buzz.": "قهوتنا منزوعة الكافيين بنسبة 99.9%، فيمكنك الاستمتاع بفنجان في آخر الليل دون أن يطير النوم.",
    "How many cups does a 250g bag make?": "كم فنجانًا يصنع كيس 250 جم؟",
    "Roughly 15 to 18 filter cups, or about 13 espresso shots, depending on how strong you like it.": "نحو 15 إلى 18 فنجان فلتر، أو حوالي 13 شوت إسبريسو، حسب درجة القوة التي تحبها.",
    "How many cups does a 20g Tal2eema bag make?": "كم فنجانًا يصنع كيس Tal2eema وزن 20 جم؟",
    "One cup of filter coffee, or one espresso. For Turkish coffee, about 2 to 3 cups, since a cup needs roughly 7g of coffee.": "فنجان فلتر واحد، أو إسبريسو واحد. وفي القهوة التركي نحو 2 إلى 3 فناجين، لأن الفنجان يحتاج حوالي 7 جم من القهوة.",
    "I can't decide which bag to pick.": "لا أستطيع أن أقرر أي كيس أختار.",
    "Ask us which bag to pick": "اسألنا أي كيس تختار",
    "Tell us what you enjoy, whether fruity, chocolatey or nutty, and we'll point you to the right bag. Message us on WhatsApp anytime.": "أخبرنا بما تحب، فواكه أو شوكولاتة أو مكسرات، وسنرشدك إلى الكيس المناسب. راسلنا على واتساب في أي وقت.",

    /* footer */
    "Help & contact": "المساعدة والتواصل", "Brewing guides": "أدلة التحضير", "WhatsApp": "واتساب", "WhatsApp support": "دعم واتساب",
    "Instagram": "إنستجرام",
    "© 2026 KAIF – Specialty Coffee. All rights reserved.": "© 2026 KAIF – قهوة مختصة. جميع الحقوق محفوظة.",

    /* governorates */
    "Cairo": "القاهرة", "Giza": "الجيزة", "Alexandria": "الإسكندرية", "Beheira": "البحيرة", "Dakahlia": "الدقهلية",
    "Damietta": "دمياط", "Gharbia": "الغربية", "Kafr El-Sheikh": "كفر الشيخ", "Menoufia": "المنوفية",
    "Qalyubia": "القليوبية", "Sharqia": "الشرقية", "Ismailia": "الإسماعيلية", "Port Said": "بورسعيد", "Suez": "السويس",
    "Red Sea": "البحر الأحمر", "South Sinai": "جنوب سيناء", "Matrouh": "مطروح", "North Sinai": "شمال سيناء",
    "Fayoum": "الفيوم", "Beni Suef": "بني سويف", "Minya": "المنيا", "Assiut": "أسيوط", "Sohag": "سوهاج",
    "Qena": "قنا", "Luxor": "الأقصر", "Aswan": "أسوان", "New Valley": "الوادي الجديد"
  };

  var D = {};
  Object.keys(RAW).forEach(function (k) { D[NORM(k)] = RAW[k]; });

  /* ---------- helpers ---------- */
  var AR_RE = /[؀-ۿ]/;
  function num(s) { return s; }

  function translate(text) {
    var n = NORM(text);
    if (!n || AR_RE.test(n) && !/ · /.test(n)) return null;
    if (Object.prototype.hasOwnProperty.call(D, n)) return D[n];

    /* "English · Arabic" (area names in the delivery list): keep the Arabic part */
    var m = n.match(/^.+? · ([؀-ۿ][^·]*)$/);
    if (m) return m[1].trim();

    m = n.match(/^Thank you, ?(.*?)!$/);
    if (m) return m[1] ? "شكرًا يا " + m[1] + "!" : "شكرًا لك!";
    m = n.match(/^\(coffee EGP ([\d,.]+) \+ delivery EGP ([\d,.]+)\)$/);
    if (m) return "(القهوة " + m[1] + " ج.م + التوصيل " + m[2] + " ج.م)";
    m = n.match(/^Pay to InstaPay:$/);
    if (m) return "حوّل إلى إنستاباي:";
    if (n === "Put your order number in the reference.") return "اكتب رقم طلبك في خانة المرجع.";
    m = n.match(/^(\d)\. (.+)$/);
    if (m) { var st = translate(m[2]); if (st) return m[1] + ". " + st; }
    m = n.match(/^View details for (.+)$/);
    if (m) { var vd = translate(m[1]); return "عرض تفاصيل " + (vd || m[1]); }
    m = n.match(/^Turkish Coffee, (Plain|Spiced), (Light|Medium) Roast$/);
    if (m) return "قهوة تركي " + (m[1] === "Plain" ? "سادة" : "محوّجة") + "، تحميص " + (m[2] === "Light" ? "فاتح" : "متوسط");

    /* prices: "EGP 2,300" */
    m = n.match(/^EGP ([\d,.]+)$/);
    if (m) return m[1] + " ج.م";
    m = n.match(/^\+ ?EGP ([\d,.]+)$/);
    if (m) return "+ " + m[1] + " ج.م";

    /* weights: "250g" or "20 g" */
    m = n.match(/^(\d+) ?g$/);
    if (m) return m[1] + " جم";

    /* product name with a size in brackets: "Caramel (20 g)" */
    m = n.match(/^(.+?) \((\d+) ?g\)$/);
    if (m) {
      var base = translate(m[1]);
      if (base) return base + " (" + m[2] + " جم)";
    }

    /* altitude: "1800–2200 m" */
    m = n.match(/^(\d[\d,]*)\s?[–-]\s?(\d[\d,]*) m$/);
    if (m) return m[1] + "–" + m[2] + " م";

    /* lists joined by " · " or ", " (tasting notes, subtitles, map notes) */
    var parts, joiner;
    if (n.indexOf(" · ") > -1) { parts = n.split(" · "); joiner = " · "; }
    else if (n.indexOf(", ") > -1 && !/^Turkish Coffee,/.test(n)) { parts = n.split(", "); joiner = "، "; }
    if (parts) {
      var any = false;
      var out = parts.map(function (p) {
        var t = translate(p);
        if (t) { any = true; return t; }
        return p;
      });
      if (any) return out.join(joiner);
    }

    /* cart size lines like "Ethiopia Guji · 250g" are handled by the list rule above */
    /* "3 items" and similar */
    m = n.match(/^(\d+) items?$/);
    if (m) return m[1] + (m[1] === "1" ? " منتج" : " منتجات");
    return null;
  }

  function keepSpace(orig, tr) {
    var lead = (orig.match(/^\s*/) || [""])[0];
    var trail = (orig.match(/\s*$/) || [""])[0];
    return lead + tr + trail;
  }

  var SKIP = { SCRIPT: 1, STYLE: 1, TEXTAREA: 1, SVG: 1, svg: 1, NOSCRIPT: 1 };
  var ATTRS = ["aria-label", "placeholder", "title", "alt"];
  var busy = false;

  function doText(node) {
    var v = node.nodeValue;
    if (!v || !/[A-Za-z]/.test(v)) return;
    var t = translate(v);
    if (t && t !== NORM(v)) node.nodeValue = keepSpace(v, t);
  }

  function doEl(el) {
    if (el.nodeType !== 1 || SKIP[el.tagName]) return;
    ATTRS.forEach(function (a) {
      var v = el.getAttribute && el.getAttribute(a);
      if (v && /[A-Za-z]/.test(v)) {
        var t = translate(v);
        if (t) el.setAttribute(a, t);
      }
    });
  }

  function walk(root) {
    if (!root) return;
    if (root.nodeType === 3) { doText(root); return; }
    if (root.nodeType !== 1 || SKIP[root.tagName]) return;
    doEl(root);
    var w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (n.nodeType === 1 && SKIP[n.tagName]) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var n;
    while ((n = w.nextNode())) {
      if (n.nodeType === 3) doText(n); else doEl(n);
    }
  }

  function start() {
    document.title = "KAIF | قهوة مختصة محمّصة على دفعات صغيرة في مصر";
    var md = document.querySelector('meta[name="description"]');
    if (md) md.setAttribute("content", "قهوة مختصة محمّصة على دفعات صغيرة في مصر. حبوب أحادية المصدر وتوليفات وقهوة تركي وأكياس 20 جم للتجربة. توصيل لجميع أنحاء مصر.");
    busy = true; walk(document.body); busy = false;
    var pending = [], timer = null;
    new MutationObserver(function (muts) {
      if (busy) return;
      muts.forEach(function (m) {
        if (m.type === "childList") m.addedNodes.forEach(function (n) { pending.push(n); });
        else if (m.type === "characterData") pending.push(m.target);
      });
      if (timer) return;
      timer = setTimeout(function () {
        timer = null; busy = true;
        pending.splice(0).forEach(walk);
        busy = false;
      }, 0);
    }).observe(document.body, { childList: true, subtree: true, characterData: true });
  }

  /* the "cat says" bubble and a few strings are set with textContent, which the observer sees too */
  window.KAIF_AR = { translate: translate, walk: walk };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
