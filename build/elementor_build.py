"""Generate Elementor JSON for the Niementyvi header, footer and Home page.

Every visible piece is a native Elementor / UAE widget so it stays editable
in the Elementor editor. Output: build/out/{header,footer,home}.json
"""
import itertools
import json
import os
import random

random.seed(20261002)
SITE = 'https://niementyvi.fi-e.seravo.com'
UP = SITE + '/wp-content/uploads/2026/10/'

INK = '#222222'
ACCENT = '#E8892B'
BROWN = '#5B2A1A'
HONEY = '#6B4A1E'
SCRIPT = 'Dancing Script'
SANS = 'Rubik'

_ids = set()


def eid():
    while True:
        i = '%07x' % random.getrandbits(28)
        if i not in _ids:
            _ids.add(i)
            return i


def px(size, unit='px'):
    return {'unit': unit, 'size': size, 'sizes': []}


def box(top=0, right=0, bottom=0, left=0, unit='px'):
    vals = [str(top), str(right), str(bottom), str(left)]
    return {'unit': unit, 'top': vals[0], 'right': vals[1], 'bottom': vals[2], 'left': vals[3],
            'isLinked': len(set(vals)) == 1}


def gap(size):
    return {'unit': 'px', 'size': size, 'column': str(size), 'row': str(size), 'isLinked': True}


def link(url):
    return {'url': url, 'is_external': '', 'nofollow': '', 'custom_attributes': ''}


def typo(prefix, family=None, size=None, weight=None, lh=None, lh_unit='em',
         transform=None, ls=None, size_tablet=None, size_mobile=None):
    t = {prefix + '_typography': 'custom'}
    if family:
        t[prefix + '_font_family'] = family
    if size is not None:
        t[prefix + '_font_size'] = px(size)
    if size_tablet is not None:
        t[prefix + '_font_size_tablet'] = px(size_tablet)
    if size_mobile is not None:
        t[prefix + '_font_size_mobile'] = px(size_mobile)
    if weight:
        t[prefix + '_font_weight'] = str(weight)
    if lh is not None:
        t[prefix + '_line_height'] = px(lh, lh_unit)
    if transform:
        t[prefix + '_text_transform'] = transform
    if ls is not None:
        t[prefix + '_letter_spacing'] = px(ls)
    return t


def img(media_id, filename, alt=''):
    return {'url': UP + filename, 'id': media_id, 'size': '', 'alt': alt, 'source': 'library'}


# ---------- element factories ----------

def con(children, **s):
    settings = {'content_width': 'full', 'flex_direction': 'column'}
    settings.update(s)
    return {'id': eid(), 'elType': 'container', 'isInner': False,
            'settings': settings, 'elements': children}


def inner(children, **s):
    el = con(children, **s)
    el['isInner'] = True
    return el


def widget(kind, **s):
    return {'id': eid(), 'elType': 'widget', 'widgetType': kind,
            'settings': s, 'elements': []}


def heading(text, tag='h2', family=SCRIPT, size=30, weight=700, color=INK,
            align='center', lh=1.2, url=None, size_tablet=None, size_mobile=None, **extra):
    s = {'title': text, 'header_size': tag, 'align': align, 'title_color': color}
    s.update(typo('typography', family, size, weight, lh,
                  size_tablet=size_tablet, size_mobile=size_mobile))
    if url:
        s['link'] = link(url)
    s.update(extra)
    return widget('heading', **s)


def text(html, size=14, lh=1.8, color='#333333', align='center', **extra):
    s = {'editor': html, 'align': align, 'text_color': color}
    s.update(typo('typography', SANS, size, 400, lh))
    s.update(extra)
    return widget('text-editor', **s)


def button(label, url, pad=(13, 36, 13, 36), size=11, ls=0.9, align='center', **extra):
    s = {
        'text': label,
        'link': link(url),
        'align': align,
        'button_text_color': '#FFFFFF',
        'background_background': 'classic',
        'background_color': INK,
        'hover_color': '#FFFFFF',
        'button_background_hover_background': 'classic',
        'button_background_hover_color': ACCENT,
        'border_radius': box(0, 0, 0, 0),
        'text_padding': box(*pad),
    }
    s.update(typo('typography', SANS, size, 700, 1, 'em', 'uppercase', ls))
    s.update(extra)
    return widget('button', **s)


def image(media_id, filename, alt, size='large', **extra):
    s = {'image': img(media_id, filename, alt), 'image_size': size,
         'width': px(100, '%'), 'align': 'center', 'link_to': 'none'}
    s.update(extra)
    return widget('image', **s)


def icon_list(items, **extra):
    s = {'icon_list': [dict({'_id': eid(), 'selected_icon': {'value': '', 'library': ''}}, **i) for i in items]}
    s.update(extra)
    return widget('icon-list', **s)


# ---------- HEADER ----------

def build_header():
    topbar = icon_list(
        [{'text': t} for t in [
            'Honey straight from the farm',
            'We deliver ourselves or by post',
            'Also at Jaanan Kirppis & K-Market Nuotta, Polvijärvi',
            'Call 050 363 3693',
        ]],
        view='inline',
        icon_align='center',
        divider='yes', divider_style='solid', divider_weight=px(1),
        divider_height=px(60, '%'), divider_color='#E3A9A9',
        space_between=px(28),
        text_color='#C0392B',
        _css_classes='nt-marquee nt-topbar',
        **typo('icon_typography', SANS, 12, 500, 1.4),
    )

    service = icon_list(
        [{'text': 'Customer Service 050 363 3693', 'link': link('tel:0503633693')}],
        view='traditional', text_color=INK, text_color_hover=ACCENT, icon_align_mobile='left',
        icon_typography_font_size_mobile=px(10), icon_typography_line_height_mobile=px(1.3, 'em'),
        **typo('icon_typography', SANS, 12, 400, 1.4),
    )

    logo = heading('Niementyven tila', tag='div', size=32, size_tablet=28, size_mobile=19,
                   color=BROWN, lh=1, url=SITE + '/', _css_classes='nt-logo')

    def icon(value, library, url, label):
        return widget('icon', selected_icon={'value': value, 'library': library},
                      link=link(url), primary_color=INK, hover_primary_color=ACCENT,
                      size=px(18), size_mobile=px(16), _title=label)

    mobile_menu = widget(
        'navigation-menu',
        _title='Mobile menu', hide_desktop='hidden-desktop', hide_tablet='hidden-tablet',
        menu='main-menu', layout='horizontal', navmenu_align='right', pointer='none',
        dropdown='mobile', resp_align='right', full_width_dropdown='yes',
        _element_width='initial', _element_custom_width=px(24),
        toggle_color=INK, toggle_hover_color=ACCENT, toggle_size=px(20), toggle_border_width=px(0),
        color_menu_item=INK, color_menu_item_hover=ACCENT, color_menu_item_active=ACCENT,
        color_dropdown_item=INK, color_dropdown_item_hover=ACCENT, color_dropdown_item_active=ACCENT,
        background_color_dropdown_item='#FFFFFF', background_color_dropdown_item_hover='#FFFFFF',
        background_color_dropdown_item_active='#FFFFFF',
        **typo('dropdown_typography', SANS, 12, 700, None, 'em', 'uppercase', 0.66),
        **typo('menu_typography', SANS, 11, 700, None, 'em', 'uppercase'),
    )

    right = inner(
        [icon('fas fa-phone-alt', 'fa-solid', 'tel:0503633693', 'Call'),
         icon('fas fa-envelope', 'fa-solid', 'mailto:niementyvi@gmail.com', 'Email'),
         mobile_menu],
        flex_direction='row', flex_justify_content='flex-end', flex_align_items='center',
        flex_gap=gap(16), flex_gap_mobile=gap(10), width=px(32, '%'),
        width_mobile={'unit': 'custom', 'size': 'max-content', 'sizes': []},
        flex_justify_content_mobile='flex-end', flex_wrap_mobile='nowrap',
        flex_align_items_mobile='center', padding=box(0, 0, 0, 0),
    )

    top_row = con(
        [inner([service], width=px(32, '%'),
               width_mobile={'unit': 'custom', 'size': 'calc(100% - 222px)', 'sizes': []},
               flex_align_items_mobile='flex-start', padding=box(0, 0, 0, 0)),
         inner([logo], width=px(30, '%'),
               width_mobile={'unit': 'custom', 'size': 'max-content', 'sizes': []},
               padding=box(0, 0, 0, 0)),
         right],
        content_width='boxed', boxed_width=px(1240),
        flex_direction='row', flex_direction_mobile='row', flex_align_items_mobile='center',
        flex_align_items='center', flex_gap=gap(20), flex_gap_mobile=gap(8), flex_wrap='nowrap',
        padding=box(16, 40, 0, 40), padding_mobile=box(12, 16, 12, 16),
    )

    nav = widget(
        'navigation-menu',
        menu='main-menu', layout='horizontal', navmenu_align='center',
        pointer='none', dropdown='mobile', resp_align='center', full_width_dropdown='yes',
        padding_horizontal_menu_item=px(15), padding_vertical_menu_item=px(4),
        color_menu_item=INK, color_menu_item_hover=ACCENT, color_menu_item_active=ACCENT,
        bg_color_menu_item='rgba(0,0,0,0)', bg_color_menu_item_hover='rgba(0,0,0,0)',
        bg_color_menu_item_active='rgba(0,0,0,0)',
        color_dropdown_item=INK, color_dropdown_item_hover=ACCENT, toggle_color=INK,
        **typo('menu_typography', SANS, 11, 700, 1.2, 'em', 'uppercase', 0.66),
    )
    nav_row = con([nav], padding=box(14, 24, 10, 24), hide_mobile='hidden-mobile')

    header = con(
        [con([topbar], padding=box(7, 0, 7, 0), background_background='classic',
             background_color='#FCE9EC', overflow='hidden'),
         top_row,
         nav_row],
        html_tag='header', background_background='classic', background_color='#FFFFFF',
        border_border='solid', border_width=box(0, 0, 1, 0), border_color='#EEEEEE',
        padding=box(0, 0, 0, 0), flex_gap=gap(0),
    )
    return [header]


# ---------- FOOTER ----------

def build_footer():
    def col_title(t):
        return heading(t, tag='div', family=SANS, size=12, weight=700, color='#FFFFFF',
                       align='left', lh=1.4,
                       **dict(typo('typography', SANS, 12, 700, 1.4, 'em', 'uppercase', 0.72),
                              _margin=box(0, 0, 6, 0)))

    white_list = dict(view='traditional', text_color='#FFFFFF', text_color_hover=ACCENT,
                      space_between=px(10), **typo('icon_typography', SANS, 12, 400, 1.5))

    pages_menu = widget(
        'navigation-menu',
        menu='main-menu', layout='vertical', navmenu_align='left', pointer='none',
        dropdown='none', padding_horizontal_menu_item=px(0), padding_vertical_menu_item=px(5),
        color_menu_item='#FFFFFF', color_menu_item_hover=ACCENT, color_menu_item_active='#FFFFFF',
        bg_color_menu_item='rgba(0,0,0,0)', bg_color_menu_item_hover='rgba(0,0,0,0)',
        bg_color_menu_item_active='rgba(0,0,0,0)',
        **typo('menu_typography', SANS, 12, 400, 1.5),
    )

    def column(children):
        return inner(children, width=px(22, '%'), width_tablet=px(45, '%'), width_mobile=px(100, '%'),
                     _flex_size='grow', flex_gap=gap(10), padding=box(0, 0, 0, 0))

    columns = inner(
        [column([col_title('Pages'), pages_menu]),
         column([col_title('Where to buy'),
                 icon_list([{'text': t} for t in
                            ['At the farm', 'Delivery or post', 'Jaanan Kirppis', 'K-Market Nuotta']],
                           **white_list)]),
         column([col_title('Policies'),
                 icon_list([{'text': 'Privacy policy', 'link': link(SITE + '/privacy-policy/')},
                            {'text': 'Cookies', 'link': link('#')}], **white_list)]),
         column([col_title('Contact'),
                 text('<p>Sari Nevalainen<br>Mikonniementie 8<br>83700 Polvijärvi</p>',
                      size=12, lh=1.5, color='#FFFFFF', align='left'),
                 icon_list([{'text': '050 363 3693', 'link': link('tel:0503633693')},
                            {'text': 'niementyvi@gmail.com', 'link': link('mailto:niementyvi@gmail.com')}],
                           **white_list)])],
        flex_direction='row', flex_wrap='wrap', flex_gap=gap(32), padding=box(0, 0, 0, 0),
        flex_wrap_tablet='wrap',
    )

    copyright_w = widget(
        'copyright',
        shortcode='© [hfe_current_year] Niementyven tila | All Rights Reserved.',
        align='left', title_color='#CCCCCC',
        **typo('caption_typography', SANS, 11, 400, 1.5),
    )

    footer = con(
        [columns, copyright_w],
        html_tag='footer', _element_id='contact',
        content_width='boxed', boxed_width=px(1000),
        flex_gap=gap(64), padding=box(56, 32, 28, 32), padding_mobile=box(48, 16, 24, 16),
        background_background='classic', background_color=INK,
    )
    return [footer]


# ---------- HOME ----------

def build_home():
    # 1. Hero
    circles = [
        (8, 'hero-honey-comb-bowl.jpg', 'Honey and honeycomb in a wooden bowl', dict(h='end', x=-6, v='start', y=-14, w=44)),
        (9, 'hero-honeycomb.jpg', 'Honeycomb', dict(h='start', x=34, v='start', y=36, w=32)),
        (10, 'hero-honey-white-bowl.jpg', 'Honey in a white bowl', dict(h='end', x=4, v='start', y=44, w=30)),
        (11, 'hero-honey-jar.jpg', 'Honey jar', dict(h='start', x=34, v='start', y=6, w=15)),
        (12, 'hero-honey-dipper.jpg', 'Honey dipper on a plate', dict(h='start', x=52, v='end', y=-16, w=24)),
    ]
    circle_widgets = []
    for n, (mid, fn, alt, p) in enumerate(circles, 1):
        s = {
            '_css_classes': 'nt-circle nt-circle--%d' % n,
            '_position': 'absolute',
            '_element_width': 'initial',
            '_element_custom_width': px(p['w'], '%'),
            '_offset_orientation_h': p['h'],
            '_offset_orientation_v': p['v'],
            'image_border_border': 'solid',
            'image_border_width': box(6, 6, 6, 6),
            'image_border_color': '#F4EBDD',
            'image_border_radius': box(50, 50, 50, 50, '%'),
            'image_box_shadow_box_shadow_type': 'yes',
            'image_box_shadow_box_shadow': {'horizontal': 0, 'vertical': 18, 'blur': 30, 'spread': 0,
                                            'color': 'rgba(20,60,50,0.28)'},
            'object-fit': 'cover',
            # Circle height tracks its width: circles sit in a 60%-wide layer of a full-width hero.
            'height': {'unit': 'custom', 'size': '%.1fvw' % (p['w'] * 0.6), 'sizes': []},
            'height_mobile': {'unit': 'custom', 'size': '%.1fvw' % p['w'], 'sizes': []},
        }
        s['_offset_x' if p['h'] == 'start' else '_offset_x_end'] = px(p['x'], '%')
        s['_offset_y' if p['v'] == 'start' else '_offset_y_end'] = px(p['y'], '%')
        circle_widgets.append(image(mid, fn, alt, size='large', **s))

    hero_circles = inner(
        circle_widgets,
        css_classes='nt-hero-circles', position='absolute',
        _offset_orientation_h='end', _offset_x_end=px(0, '%'),
        _offset_orientation_v='start', _offset_y=px(0, '%'),
        width=px(60, '%'), width_mobile=px(100, '%'), min_height=px(100, '%'),
        padding=box(0, 0, 0, 0), z_index=1,
    )

    hero_text = inner(
        [heading('Honey, naturally<br>good!', tag='h1', size=50, weight=600, align='left',
                 **typo('typography', SCRIPT, 50, 600, 1.2, size_tablet=42, size_mobile=36)),
         text('<p>Finnish honey from the pure nature and fields of North Karelia.</p>',
              size=14, lh=1.7, color='#2F3D38', align='left'),
         button('Order now', '#honey', pad=(11, 34, 11, 34), size=11, ls=0.66, align='left',
                border_border='solid', border_width=box(1.5, 1.5, 1.5, 1.5), border_color=INK,
                button_hover_border_color=ACCENT, _css_classes='nt-btn-inset')],
        css_classes='nt-hero-text', width=px(320), width_tablet=px(320), width_mobile=px(100, '%'),
        flex_gap=gap(18), flex_align_items='flex-start', padding=box(0, 0, 0, 0), z_index=4,
    )

    hero = con(
        [hero_circles, hero_text],
        css_classes='nt-hero nt-bees-hero',
        flex_direction='row', flex_align_items='center',
        min_height=px(600), min_height_tablet=px(520), min_height_mobile=px(460),
        padding=box(60, 32, 60, 260), padding_tablet=box(60, 32, 60, 48), padding_mobile=box(48, 16, 48, 16),
        background_background='gradient', background_color='#DCEDE4', background_color_stop=px(0, '%'),
        background_color_b='#9ED8C7', background_color_b_stop=px(100, '%'),
        background_gradient_type='linear', background_gradient_angle=px(95, 'deg'),
        overflow='hidden',
    )

    # 2. Feature strip (each item: icon image + heading)
    feats = [
        (21, 'icon-finnish-honey.png', 'Honeycomb icon', '100% Finnish honey'),
        (22, 'icon-karelian-nature.png', 'Leaf icon', 'From pure North Karelian nature'),
        (23, 'icon-clover-fields.png', 'Clover icon', 'Clover & honey-flower fields'),
        (24, 'icon-naturally-good.png', 'Heart in hand icon', 'Naturally good'),
    ]
    feat_items = [
        inner([image(mid, fn, alt, size='full', width=px(52), _element_width='initial',
                     _element_custom_width=px(52)),
               heading(label, tag='div', family=SANS, size=17, weight=500, color=HONEY,
                       align='left', lh=1.3, _element_width='auto')],
              flex_direction='row', flex_align_items='center', flex_gap=gap(20),
              flex_wrap='nowrap', padding=box(0, 0, 0, 0), _flex_size='none',
              width={'unit': 'custom', 'size': 'max-content', 'sizes': []})
        for mid, fn, alt, label in feats
    ]
    feature_strip = con(
        [inner(feat_items, css_classes='nt-marquee nt-feats', flex_direction='row',
               flex_wrap='nowrap', flex_gap=gap(88), flex_justify_content='center',
               flex_align_items='center', padding=box(0, 0, 0, 0), overflow='hidden')],
        padding=box(26, 0, 26, 0), background_background='classic', background_color='#E6DAC2',
        overflow='hidden',
    )

    # 3. Welcome + Our Honey
    products = [
        (14, 'product-honey-450g.jpg', 'Honey 450 g jar', 'Honey (450 g)',
         'Soft and easy to spoon. Pohjois-Karjalan Hunaja.', '7,00 €'),
        (15, 'product-box-of-10-jars.jpg', 'Box of 10 honey jars', 'Box of 10 jars',
         'Ten 450 g jars, cheaper per jar than buying singly.', 'Ask for price'),
        (16, 'product-honeycomb.jpg', 'Honeycomb', 'Honeycomb',
         'Placeholder product. Replace or remove once the range is confirmed.', '— €'),
        (17, 'product-gift-jar.jpg', 'Gift jar of honey', 'Gift jar',
         'Placeholder product. Replace or remove once the range is confirmed.', '— €'),
    ]
    product_cards = [
        inner([image(mid, fn, alt, size='large', _css_classes='nt-ratio-product', _element_width='inherit', height=px(266),
                     height_tablet=px(410), height_mobile=px(410), **{'object-fit': 'cover'}),
               heading(name, tag='h3', family=SANS, size=13, weight=500, lh=1.4, _margin=box(6, 0, 0, 0)),
               text('<p>%s</p>' % desc, size=12, lh=1.6, color='#5A5A5A', _padding=box(0, 6, 0, 6)),
               heading(price, tag='div', family=SANS, size=12, weight=600, lh=1.4)],
              flex_gap=gap(10), flex_align_items='center', padding=box(0, 0, 0, 0))
        for mid, fn, alt, name, desc, price in products
    ]
    honey = con(
        [inner([heading('Welcome to Niementyvi farm!', size=34, size_mobile=30),
                text('<p>We produce the best of nature\'s strength, honey, from the pure nature and fields '
                     'of North Karelia. Naturally good!</p>')],
               flex_gap=gap(10), flex_align_items='center', width=px(620), width_mobile=px(100, '%'),
               padding=box(0, 0, 0, 0), margin=box(0, 0, 24, 0)),
         heading('Our Honey', size=30),
         inner(product_cards, container_type='grid',
               grid_columns_grid={'unit': 'fr', 'size': 4, 'sizes': []},
               grid_columns_grid_tablet={'unit': 'fr', 'size': 2, 'sizes': []},
               grid_columns_grid_mobile={'unit': 'fr', 'size': 1, 'sizes': []},
               grid_rows_grid={'unit': 'fr', 'size': 1, 'sizes': []},
               grid_gaps={'unit': 'px', 'column': '16', 'row': '16', 'isLinked': True},
               grid_auto_flow='row', padding=box(0, 0, 0, 0)),
         button('Order now', 'tel:0503633693', _margin=box(20, 0, 0, 0))],
        _element_id='honey', content_width='boxed', boxed_width=px(1000),
        flex_align_items='center', flex_gap=gap(30),
        padding=box(56, 32, 96, 32), padding_mobile=box(48, 16, 72, 16),
    )

    # 4. Story
    story = con(
        [inner(
            [inner([image(13, 'story-honey-jars.webp', 'Honey jars outdoors', size='full',
                          _css_classes='nt-story-image', height=px(480), height_tablet=px(400),
                          height_mobile=px(360), **{'object-fit': 'contain'})],
                   width=px(50, '%'), width_mobile=px(100, '%'), padding=box(0, 0, 0, 0)),
             inner([heading('Made by our bees', size=46, size_tablet=40, size_mobile=34),
                    widget('divider', style='solid', weight=px(1.5), color=INK, width=px(44),
                           align='center', gap=px(2)),
                    text('<p>On our farm we grow clover meadow, honey flower and biodiversity plants, plus a '
                         'small kitchen garden and potatoes. Our bees gather nectar from these fields and the '
                         'wild plants of the Finnish summer.</p>')],
                   width=px(420), width_mobile=px(100, '%'), flex_gap=gap(16),
                   flex_align_items='center', flex_justify_content='center', padding=box(0, 0, 0, 0))],
            content_width='boxed', boxed_width=px(1200),
            flex_direction='row', flex_direction_mobile='column', flex_justify_content='space-around',
            flex_align_items='center', flex_gap=gap(40),
            padding=box(150, 32, 120, 32), padding_mobile=box(80, 16, 72, 16), z_index=2)],
        css_classes='nt-story nt-bees-story', padding=box(0, 0, 0, 0), overflow='hidden',
    )

    # 5. Explore
    explore_items = [
        (18, 'explore-honey.jpg', 'Honey', 'Honey', 'Finnish honey for sale.', '#honey'),
        (19, 'explore-beekeeping.jpg', 'Beekeeping', "Beekeeper's Diary",
         "Read more about the apiary's year.", '#diary'),
        (20, 'explore-contact.jpg', 'Contact', 'Contact', 'What, where?', '#contact'),
    ]
    explore_cards = [
        inner([image(mid, fn, alt, size='large', _css_classes='nt-ratio-square', _element_width='inherit', height=px(301),
                     height_tablet=px(230), height_mobile=px(340), **{'object-fit': 'cover'}),
               heading(title, tag='h3', size=30, _margin=box(6, 0, 0, 0)),
               text('<p>%s</p>' % desc, size=13, lh=1.7),
               button('Learn more', url, _margin=box(6, 0, 0, 0))],
              flex_gap=gap(14), flex_align_items='center', padding=box(0, 0, 0, 0))
        for mid, fn, alt, title, desc, url in explore_items
    ]
    explore = con(
        [heading('Explore', size=30),
         inner(explore_cards, container_type='grid',
               grid_columns_grid={'unit': 'fr', 'size': 3, 'sizes': []},
               grid_columns_grid_tablet={'unit': 'fr', 'size': 3, 'sizes': []},
               grid_columns_grid_mobile={'unit': 'fr', 'size': 1, 'sizes': []},
               grid_rows_grid={'unit': 'fr', 'size': 1, 'sizes': []},
               grid_gaps={'unit': 'px', 'column': '16', 'row': '32', 'isLinked': False},
               grid_auto_flow='row', padding=box(0, 0, 0, 0))],
        _element_id='diary', content_width='boxed', boxed_width=px(1000),
        flex_align_items='center', flex_gap=gap(30),
        padding=box(0, 32, 110, 32), padding_mobile=box(0, 16, 72, 16),
    )

    return [hero, feature_strip, honey, story, explore]


def clean(el):
    el['settings'] = {k: v for k, v in el['settings'].items() if v is not None}
    for c in el['elements']:
        clean(c)
    return el


def walk(els):
    for e in els:
        yield e
        yield from walk(e['elements'])


if __name__ == '__main__':
    out = os.path.join(os.path.dirname(__file__), 'out')
    os.makedirs(out, exist_ok=True)
    keys = {}
    for name, fn in [('header', build_header), ('footer', build_footer), ('home', build_home)]:
        tree = [clean(e) for e in fn()]
        with open(os.path.join(out, name + '.json'), 'w') as f:
            json.dump(tree, f, ensure_ascii=False)
        for e in walk(tree):
            k = e.get('widgetType', e['elType'])
            keys.setdefault(k, {}).update(e['settings'])
        print(name, len(list(walk(tree))), 'elements')
    with open(os.path.join(out, 'keys.json'), 'w') as f:
        json.dump(keys, f, ensure_ascii=False)
