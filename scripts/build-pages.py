"""Generate static inner pages with the shared header, footer and homepage styles.

Run from the project root after editing shared chrome or this page content.
Only the named inner HTML files are written. No publishing takes place.
"""
from pathlib import Path
import re
from html import escape as e

ROOT = Path(__file__).resolve().parent.parent
home = (ROOT / 'index.html').read_text(encoding='utf-8')
pages = [('about', 'О компании'), ('careers', 'Вакансии'),
         ('vacancy-sales', 'Менеджер по продажам'), ('buyout', 'Выкуп техники'),
         ('promotions', 'Акции'), ('service', 'Сервис'), ('payment', 'Оплата'),
         ('delivery', 'Доставка'), ('reviews', 'Отзывы'), ('contacts', 'Контакты')]
def block(name):
    return re.search(r'<section class="[^"]*" id="' + name + r'".*?</section>', home, re.S).group()

header = home[home.index('    <div class="header-placeholder">'):home.index('    <main id="main">')]
footer = home[home.index('    <footer'):home.index('</footer>') + 9]
def links(html):
    for anchor in ['catalog', 'top-positions', 'documents', 'personal-data-consent', 'privacy-policy']:
        html = html.replace('href="#' + anchor + '"', 'href="index.html#' + anchor + '"')
    html = html.replace('href="#reviews"', 'href="reviews.html"').replace('href="#contacts"', 'href="contacts.html"')
    return html
header, footer = links(header), links(footer)
footer = re.sub(r'<nav class="site-footer__pages.*?</nav>', '', footer, flags=re.S)
socials = re.search(r'<div class="header-socials" aria-label="Мессенджеры">.*?</div>', home, re.S).group()
contact = '<div class="application__contacts"><div class="application__contact-links"><a class="h3Aa" href="tel:+78006181647">+7 (800) 618-16-47</a><a class="p2" href="mailto:arenda_info@mail.ru">arenda_info@mail.ru</a></div>' + socials + '</div>'
styles = ['header', 'footer', 'hero', 'application', 'equipment-types', 'services', 'reviews', 'videos', 'brands', 'inner-pages']
head = '''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Overpass:ital,wght@0,100..900;1,100..900&amp;family=Nunito+Sans:ital,opsz,wght@0,6..12,200..1000;1,6..12,200..1000&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/base.css?v=4">''' + ''.join(f'<link rel="stylesheet" href="assets/css/blocks/{s}.css?v=11">' for s in styles) + '''<script src="assets/js/header.js?v=2" defer></script><script src="assets/js/application.js?v=3" defer></script><script src="assets/js/inner-pages.js?v=2" defer></script>'''
def button(text, href='#application'):
    return f'<a class="inner-button btn2" href="{href}"><span>{text}</span></a>'
def visual(dark=False):
    return f'<div class="inner-visual{" inner-visual--dark" if dark else ""}" aria-hidden="true"></div>'
def section(title, body, extra=''):
    return f'<section class="section container {extra}"><div class="section__heading"><h2>{title}</h2></div>{body}</section>'
def hero(title, description='', action='', dark=False, split=False, tags=()):
    copy = f'<div class="inner-hero__content"><h1>{title}</h1>' + (f'<p class="p1">{description}</p>' if description else '')
    if tags: copy += '<div class="inner-tags p2">' + ''.join(f'<span>{x}</span>' for x in tags) + '</div>'
    copy += action + '</div>'
    if split: copy = '<div class="inner-split">' + copy + visual() + '</div>'
    return f'<section class="inner-hero{" inner-hero--dark" if dark else ""}"><div class="container">{copy}</div></section>'
def photo_hero(title, description, action, image, alt, tags=()):
    result = hero(title, description, action, split=True, tags=tags)
    return result.replace('class="inner-hero"', 'class="inner-hero inner-hero--photo"').replace(visual(), f'<div class="inner-hero__photo"><img src="{image}" alt="{alt}" fetchpriority="high"></div>')

def information_layout(title, description, sections):
    content = '<div class="vacancy-layout container"><div class="vacancy-layout__intro"><h1>'+title+'</h1><p class="p1">'+description+'</p></div><div class="vacancy-layout__details">'
    for heading, items in sections:
        content += '<section class="vacancy-layout__section"><h2>'+heading+'</h2><ul class="inner-list p1">'+''.join('<li>'+item+'</li>' for item in items)+'</ul></section>'
    return content+'</div></div>'

def cards(items, columns='', icons=()):
    return f'<div class="inner-grid {columns}">' + ''.join('<article class="inner-card">' + (f'<img class="inner-card__icon" src="{icons[i]}" width="64" height="64" alt="" loading="lazy">' if icons else '') + f'<h3>{t}</h3>' + (f'<p class="p1">{d}</p>' if d else '') + '</article>' for i, (t, d) in enumerate(items)) + '</div>'
def steps(items):
    return '<ol class="inner-grid inner-steps" role="list">' + ''.join(f'<li class="inner-card"><span class="inner-step-number" aria-hidden="true">{i:02}</span><p class="p1">{t}</p></li>' for i, t in enumerate(items, 1)) + '</ol>'
def field(name, label, kind='text', required=False):
    auto = {'name':'name', 'phone':'tel', 'email':'email'}.get(name, 'off')
    return f'<label class="application__field"><span class="visually-hidden">{label}</span><input class="application__input p1" name="{name}" type="{kind}" autocomplete="{auto}" placeholder="{label}"' + (' required' if required else '') + '>' + ('<span class="application__required p1" aria-hidden="true">*</span>' if required else '') + '</label>'
def consent(key):
    return f'''<div class="application__consent"><div class="application__checkbox-wrap"><input class="application__checkbox" id="{key}-consent" name="consent" type="checkbox" aria-labelledby="{key}-consent-text" required><svg class="application__check" viewBox="0 0 12 12" aria-hidden="true"><use href="assets/images/check.svg#check"></use></svg></div><p class="p2" id="{key}-consent-text"><label for="{key}-consent">Я даю согласие на </label><a href="index.html#personal-data-consent">обработку персональных данных</a><label for="{key}-consent"> и подтверждаю, что ознакомлен с </label><a href="index.html#privacy-policy">Политикой в отношении обработки персональных данных</a></p></div>'''
def upload(key, label, multiple=False, accept=''):
    if multiple:
        return f'<label class="inner-form__file-label p2"><span class="visually-hidden">{label}, до 5 фотографий</span><input type="file" name="photos" accept="{accept}" multiple data-max-files="5" data-file-list="{key}-files"></label><ul class="inner-form__files p2" id="{key}-files" aria-live="polite"></ul><p class="inner-form__file-status p2" role="status" hidden></p>'
    return f'''<input class="application__file-input visually-hidden" id="{key}-file" type="file" name="file" aria-label="{label}"{(' accept="'+accept+'"') if accept else ''}><div class="application__attachment-row"><button class="application__attach btn3" type="button"><span>{label}</span><svg viewBox="0 0 16 16" aria-hidden="true"><use href="assets/images/attachment.svg#attachment"></use></svg></button><div class="application__file" hidden><button class="application__remove" type="button" aria-label="Удалить файл"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="m5 5 10 10M15 5 5 15" stroke="currentColor" stroke-width="1.5"/></svg></button><span class="application__filename p2"></span></div></div>'''
def form(title, description='', btn='Получить КП', fields=None, attachment=None, message='Комментарий к заявке', key='application', multiple=False, accept=''):
    if fields is None: fields = [('name','Ваше имя','text',True),('phone','Телефон','tel',True),('email','Email','email',False)]
    inputs = ''.join(field(*args) for args in fields)
    if key == 'estimate':
        options = ''.join(f'<option>{v}</option>' for v in ['Погрузчики','Штабелеры','Ричтраки','Электротележки'])
        inputs = f'<label class="application__field"><span class="visually-hidden">Тип техники</span><select class="application__input p1" name="equipment-type" required><option value="">Тип техники</option>{options}</select></label>' + inputs
    body = f'<form class="application__form" aria-labelledby="{key}-title"><div class="application__fields">{inputs}</div>'
    if attachment: body += upload(key, attachment, multiple, accept)
    if message: body += f'<label class="application__message-label"><span class="visually-hidden">{message}</span><textarea class="application__message p1" name="message" placeholder="{message}"></textarea></label>'
    body += consent(key) + f'<button class="application__submit btn2" type="submit"><span>{btn}</span></button><p class="application__status p2" role="status" hidden></p></form>'
    return f'<section class="section application inner-form container" id="{key}" aria-labelledby="{key}-title"><div class="application__card"><div class="application__intro"><div class="application__heading"><h2 id="{key}-title">{title}</h2>' + (f'<p class="p2">{description}</p>' if description else '') + '</div>' + contact + '</div>' + body + '</div></section>'
def category_section(id, title):
    result = block(id)
    old_title = 'Оборудование для любых работ' if id == 'catalog' else 'Услуги для любых работ'
    result = result.replace(old_title, title)
    # Existing homepage assets are reused; no missing new image URLs are emitted.
    return result
contents = {}
contents['about'] = hero('Техника, на которую можно положиться','Помогаем бизнесу решать задачи по перемещению, подъёму и хранению грузов. Подбираем складскую технику под конкретные условия эксплуатации — от разовых работ до постоянного оснащения предприятий.',dark=True)
contents['about'] = contents['about'].replace('inner-hero inner-hero--dark', 'about-hero inner-hero--contained').replace('</div></section>', '</div><img class="about-hero__image" src="assets/images/about-background.webp" width="3156" height="1344" alt="Складская техника в ангаре" fetchpriority="high"></section>')
contents['about'] += '<section class="section container"><div class="inner-split"><div class="inner-copy"><h2>Не просто поставляем технику. Помогаем подобрать рабочее решение.</h2><p class="p1">В каталоге представлены погрузчики, штабелеры, ричтраки, складские тележки и другое оборудование для бизнеса. Помогаем подобрать технику с учётом груза, высоты подъёма, условий эксплуатации и интенсивности работы.</p></div><div class="inner-visuals">'+'<img src="assets/images/about-left.webp" width="1024" height="1024" alt="Погрузчик с палетой на складе" loading="lazy"><img src="assets/images/about-right.webp" width="1024" height="1024" alt="Складская тележка с грузом" loading="lazy">'+'</div></div></section>'
contents['about'] += category_section('catalog','Что мы можем предложить') + category_section('services','Один партнёр — разные задачи')
brand_grid = re.search(r'<div class="brands__grid">.*?</div>\s*<p class="media-showcase__status', home, re.S).group().split('<p class="media-showcase__status')[0]
contents['about'] += section('Работаем с техникой ведущих производителей',brand_grid,'inner-brands') + form('Нужна техника под конкретную задачу?','Расскажите, где и с какими грузами предстоит работать. Поможем подобрать подходящий вариант.','Подобрать технику')
contents['careers'] = hero('Работайте с нами','Ищем людей, которым интересно развиваться вместе с компанией и работать с современной складской техникой.',split=True)
contents['careers'] = contents['careers'].replace(visual(), '<img class="inner-visual inner-visual--photo" src="assets/images/careers-team.png" width="1240" height="680" alt="Команда на территории склада" fetchpriority="high">')
contents['careers'] += section('Работа, в которой есть результат', cards([('Понятные задачи','Вы знаете свою зону ответственности и ожидаемый результат.'),('Работа с техникой','Реальный продукт и понятная сфера бизнеса.'),('Развитие','Возможность получать новый опыт и расти внутри своего направления.'),('Команда','Работаем вместе и помогаем друг другу решать задачи.')], icons=[f'assets/images/careers-benefit-{i}.svg' for i in range(1, 5)]))
jobs = '<div class="inner-grid inner-grid--three inner-jobs">'
for title, link in [('Менеджер по продажам','vacancy-sales.html'),('Сервисный механик','#application'),('Менеджер по работе с клиентами','#application')]:
    jobs += f'<a class="inner-card" href="{link}"><h3>{title}</h3><p class="p2">Москва · Полная занятость</p><span class="inner-card__link">' + ('Подробнее' if '.html' in link else 'Откликнуться') + ' →</span></a>'
contents['careers'] += section('Открытые вакансии',jobs+'</div>') + form('Не нашли подходящей вакансии?','Отправьте резюме. Если появится подходящая позиция, мы сможем с вами связаться.','Отправить резюме',attachment='Прикрепить резюме',message=None)
contents['vacancy-sales'] = '<div class="vacancy-layout container"><div class="vacancy-layout__intro"><h1>Менеджер по продажам складской техники</h1><div class="inner-tags p2"><span>Москва</span><span>Полная занятость</span><span>Опыт: от 1 года</span></div><a class="hero__cta btn1" href="#application"><span>Откликнуться</span></a></div><div class="vacancy-layout__details"><section class="vacancy-layout__section"><h2>О вакансии</h2><p class="p1">Ищем специалиста, который будет работать с входящими обращениями, помогать клиентам выбирать технику и сопровождать сделки.</p></section>'
for title, items in [('Чем предстоит заниматься',['Общаться с клиентами и обрабатывать обращения','Выявлять задачи и потребности клиента','Подбирать подходящую технику','Подготавливать коммерческие предложения','Сопровождать клиента на этапах сделки','Работать с текущей клиентской базой']),('Что ожидаем',['Умение общаться с клиентами','Ответственность и самостоятельность','Желание разбираться в продукте','Опыт продаж будет преимуществом','Уверенная работа с ПК'])]:
    contents['vacancy-sales'] += '<section class="vacancy-layout__section"><h2>'+title+'</h2><ul class="inner-list p1">'+''.join('<li>'+x+'</li>' for x in items)+'</ul></section>'
contents['vacancy-sales'] += '<section class="vacancy-layout__section"><h2>Что предлагаем</h2><ul class="inner-list p1">'+''.join('<li>'+x+'</li>' for x in ['Стабильная работа','Понятная система задач','Обучение продукту','Возможность профессионального роста'])+'</ul></section></div></div>' + form('Хотите работать с нами?','Оставьте контакты и прикрепите резюме.','Откликнуться на вакансию',attachment='Прикрепить резюме',message=None)
contents['buyout'] = photo_hero('Выкупим вашу складскую технику','Предложите погрузчик или другую складскую технику на выкуп. Оценим оборудование и предложим условия сделки.','<a class="hero__cta btn1" href="#application"><span>Оценить технику</span></a>','assets/images/buyout-forklift.webp','Погрузчик с грузом на складе',tags=['Погрузчики','Штабелеры','Ричтраки','Электротележки'])

contents['buyout'] += section('Как проходит выкуп',steps(['Оставляете заявку','Оцениваем технику','Согласовываем условия','Оформляем сделку']))
contents['buyout'] += section('Техника не обязательно должна быть новой','<div class="inner-split"><p class="p1">Рассматриваем оборудование с пробегом и оцениваем его индивидуально с учётом модели, года выпуска, состояния, наработки и комплектации.</p><div class="inner-tags p1">'+''.join('<span>'+x+'</span>' for x in ['Марка','Год','Наработка','Состояние','Комплектация'])+'</div></div>')
faq = [('Как определяется стоимость?','Оцениваем технику индивидуально с учётом модели, года выпуска, состояния, наработки и комплектации.'),('Как быстро можно получить оценку?','Специалист свяжется с вами после рассмотрения заявки. Срок можно уточнить по телефону.'),('Можно ли продать неисправную технику?','Укажите неисправности в комментарии и приложите фотографии, чтобы специалист мог рассмотреть заявку.'),('Какие документы понадобятся?','Перечень документов специалист уточнит при согласовании условий сделки.'),('Выкупаете ли несколько единиц сразу?','Перечислите технику в комментарии. Специалист рассмотрит заявку и предложит условия.')]
contents['buyout'] += section('Вопросы о выкупе','<div class="inner-faq">'+''.join(f'<details'+(' open' if i == 0 else '')+f'><summary>{q}</summary><p class="p1">{a}</p></details>' for i,(q,a) in enumerate(faq))+'</div>') + form('Есть техника на продажу?','Пришлите информацию и фотографии — специалист свяжется с вами после рассмотрения заявки.',btn='Предложить технику',attachment='Добавить фотографии',multiple=True,accept='image/*')
contents['promotions'] = hero('Акции и специальные предложения','Выгодные условия на покупку, аренду и обслуживание складской техники.').replace('class="inner-hero"', 'class="inner-hero inner-hero--compact"')
promo = '<div class="inner-grid inner-grid--two">'
for i,t in enumerate(['Специальные условия на аренду погрузчиков','Выгодные условия на технику с пробегом','Специальное предложение на сервис','Лизинг на специальных условиях']):
    ended = i == 2
    promo += f'<article class="inner-card{" inner-card--ended" if ended else ""}"><span class="inner-promotion__status">' + ('Завершённая акция · пример' if ended else 'Активная акция · пример') + f'</span><h3>{t}</h3><p class="p2">Условия и срок акции уточняются.</p>'+ ('' if ended else button('Подробнее')) + '</article>'
contents['promotions'] += '<section class="section container">'+promo+'</div></section>' + form('Не нашли подходящей акции?','Оставьте заявку — специалист расскажет об актуальных условиях.')
contents['service'] = photo_hero('Сервис складской техники','Диагностика, техническое обслуживание и ремонт погрузчиков и складского оборудования.','<a class="hero__cta btn1" href="#application"><span>Записаться на сервис</span></a>','assets/images/careers-team.png','Специалисты на территории склада')

contents['service'] += section('Услуги',cards([('Диагностика','Поиск неисправностей и оценка технического состояния.'),('Техническое обслуживание','Регламентные работы для стабильной эксплуатации техники.'),('Ремонт','Устранение неисправностей узлов и систем.'),('Запчасти','Подбор необходимых комплектующих.')], icons=[f'assets/images/service-icon-{i}.svg' for i in range(1, 5)]))
contents['service'] += form('Опишите проблему','Поможем определить следующий шаг',btn='Записаться на сервис',fields=[('phone','Телефон','tel',True),('equipment','Техника','text',False)],attachment='Прикрепить фото',message='Описание проблемы',accept='image/*')
contents['payment'] = information_layout('Удобные способы оплаты','Подберём подходящий вариант расчёта в зависимости от техники и условий сделки.', [('Варианты оплаты',['Безналичная оплата','Лизинг','Рассрочка','Оплата по счёту']),('Как проходит оплата',['Выбираете технику','Получаете предложение','Согласовываем условия','Оплачиваете','Получаете технику'])]) + form('Остались вопросы?',btn='Запросить КП')
contents['delivery'] = information_layout('Доставим технику до вашего объекта','Организуем доставку складской техники до согласованного адреса.', [('Доставка техники без лишних сложностей',['Вы выбираете технику','Сообщаете адрес','Рассчитываем доставку','Согласовываем дату','Техника отправляется к вам'])])
contents['delivery'] += form('Рассчитать доставку',btn='Получить расчёт',fields=[('from','Откуда','text',False),('to','Куда','text',True),('equipment','Техника','text',False),('phone','Телефон','tel',True)],message=None)
review_text = re.search(r'<blockquote class="reviews__text p1"[^>]*>(.*?)</blockquote>',home,re.S)
if not review_text: review_text = re.search(r'class="reviews__text p1"[^>]*>(.*?)</',home,re.S)
review_text = review_text.group(1)
rating = '<div class="reviews__rating" aria-label="Оценка: 5 из 5">' + '<svg viewBox="0 0 24 24" aria-hidden="true"><use href="assets/images/star.svg#review-star"></use></svg>'*5 + '</div>'
review_card = '<article class="reviews__card"><div class="reviews__meta"><div class="reviews__author-block"><h3>Вадим</h3><p class="p2">28.09.26</p></div>'+rating+'</div><div class="reviews__line" style="background:var(--color-accent)" aria-hidden="true"></div><blockquote class="reviews__text p1">'+review_text+'</blockquote></article>'
contents['reviews'] = hero('Клиенты о нашей технике').replace('class="inner-hero"', 'class="inner-hero inner-hero--compact"')
review_body = '<div class="inner-review-tabs" role="tablist" aria-label="Тип отзыва">'
for i, (slug,title) in enumerate([('rent','Аренда'),('purchase','Покупка'),('service','Сервис'),('video','Видео')]):
    review_body += f'<button class="inner-review-tab btn3" id="review-tab-{slug}" role="tab" type="button" aria-selected="{str(i==0).lower()}" aria-controls="review-panel-{slug}" tabindex="{0 if i==0 else -1}">{title}</button>'
review_body += '</div>'
for i,slug in enumerate(['rent','purchase','service','video']):
    body = '<div class="inner-grid inner-grid--two">'+review_card*2+'</div>'
    if slug=='video': body='<div class="videos__grid">'+('<div class="videos__item" aria-label="Видеоотзыв, материал пока не добавлен"><div class="videos__play" aria-hidden="true"><svg viewBox="0 0 24 24"><use href="assets/images/play-glyph.svg#play-glyph"></use></svg></div></div>'*2)+'</div>'
    review_body += f'<div class="inner-review-panel" id="review-panel-{slug}" role="tabpanel" aria-labelledby="review-tab-{slug}" tabindex="0"'+ (' hidden' if i else '') + '>'+body+'</div>'
contents['reviews'] += '<section class="section container">'+review_body+'</section>' + form('Уже работали с нами?','Будем рады узнать ваше мнение.','Оставить отзыв',message='Ваш отзыв')
contents['contacts'] = '<section class="contacts-intro container"><div class="inner-split inner-split--map"><div class="inner-copy"><h1>Всегда<br>на связи</h1><p class="h3Aa">Москва, ул. Карла-Маркса, 35</p>'+contact+'</div><iframe class="inner-map" title="Офис на Яндекс Картах" src="https://yandex.ru/map-widget/v1/?text=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C%20%D1%83%D0%BB.%20%D0%9A%D0%B0%D1%80%D0%BB%D0%B0-%D0%9C%D0%B0%D1%80%D0%BA%D1%81%D0%B0%2C%2035&amp;z=12" loading="lazy" referrerpolicy="no-referrer"></iframe></div></section>'

departments = [('Подбор и покупка техники','Нужна техника или консультация по каталогу.'),('Аренда','Нужна техника на определённый срок.'),('Сервис','Необходимо обслуживание или ремонт.'),('Выкуп техники','Хотите предложить свою технику.')]
contents['contacts'] += section('К кому обратиться','<div class="inner-grid">'+''.join(f'<article class="inner-card"><h3>{t}</h3><p class="p1">{d}</p><button class="inner-button inner-button--outline btn2" type="button" aria-haspopup="dialog" aria-controls="contact-dialog" data-contact-topic="{t}"><span>Связаться</span></button></article>' for t,d in departments)+'</div>')
dialog_form = re.search(r'<form class="application__form".*?</form>',form('Связаться',fields=[('name','Ваше имя','text',True),('phone','Телефон','tel',True)],key='contact-dialog'),re.S).group()
dialog_form = dialog_form.replace('<div class="application__fields">','<input type="hidden" name="topic"><div class="application__fields">',1).replace('Получить КП','Отправить сообщение')
contents['contacts'] += '<dialog class="inner-dialog" id="contact-dialog" aria-labelledby="contact-dialog-title"><div class="inner-dialog__head"><h2 id="contact-dialog-title">Связаться</h2><button class="inner-dialog__close" type="button" aria-label="Закрыть окно"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 5 14 14M19 5 5 19" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></button></div>'+dialog_form+'</dialog>'
for slug,title in pages:
    crumbs='<a href="index.html">Главная</a><span aria-hidden="true">/</span>'
    if slug == 'vacancy-sales': crumbs += '<a href="careers.html">Вакансии</a><span aria-hidden="true">/</span>'
    crumbs += f'<span aria-current="page">{title}</span>'
    html = head + f'<title>{title} — Погрузчик</title><meta name="description" content="{e(title)}. Складская техника и услуги компании Погрузчик."></head><body class="inner-page"><a class="skip-link" href="#main">Перейти к содержимому</a>' + header + '<main id="main"><nav class="breadcrumbs container" aria-label="Хлебные крошки">'+crumbs+'</nav>'+contents[slug]+'</main>'+footer+'</body></html>'
    (ROOT/(slug+'.html')).write_text(html.replace('><', '>\n<')+'\n',encoding='utf-8')
    print(slug+'.html')
