# cTrader Store widget

Статичный виджет-витрина cBot'ов из cTrader Store. Без бэкенда, без сборки, без зависимостей — три файла.

```
index.html       страница виджета (тянет products.json; внутри есть inline-копия как фолбэк)
products.json    ← единственное место, где редактируются продукты
standalone.html  всё в одном файле (для превью / если хостинг не отдаёт .json)
build.py         обновляет inline-копию и standalone.html из products.json (опционально)
embed-example.html  пример страницы клиента с iframe и авто-высотой
```

## Как обновить продукты

Открыть `products.json`, добавить/убрать объект в `products`. Поля:

| поле | что это |
|---|---|
| `id`, `name`, `type` | ID продукта в Store, название, `cBot` / `Indicator` / `Plugin` |
| `seller`, `url`, `image` | продавец, ссылка на страницу продукта, ссылка на логотип (cdn.ctrader.com) |
| `price`, `promoPrice` | цена и акционная цена (`null`, если акции нет; `0` = Free) |
| `rating`, `reviews` | рейтинг (`null`, если нет) и число отзывов |
| `market` | группа для фильтра-чипов: `Gold`, `Indices`, `Forex`, `Crypto`, `Multi-asset` — любые свои |
| `tags` | до 4 показываются на карточке, все участвуют в поиске |
| `summary` | 1–2 предложения |
| `stats` | `profitFactor`, `maxDrawdown` — опционально |
| `featured` | `true` — карточка подсвечивается и идёт первой |

`meta.title / subtitle / updated` — заголовок, подзаголовок и дата «актуально на».

На хостинге `index.html` читает `products.json` при каждой загрузке — деплой = залить обновлённый json. `build.py` нужен только чтобы пересобрать `standalone.html`.

## Хостинг

Любой статический: GitHub Pages, Cloudflare Pages, Netlify, Vercel или папка на своём nginx. Залить папку целиком, никакой настройки. Единственное требование — HTTPS (иначе iframe на https-сайте клиента не откроется).

## Встраивание у клиента

```html
<iframe src="https://widget.example.com/?theme=light"
        style="width:100%;border:0;min-height:600px" loading="lazy"
        title="Recommended cBots"></iframe>
```

Авто-высота (виджет шлёт свою высоту через `postMessage`) — добавить на страницу клиента:

```html
<script>
window.addEventListener('message', function (e) {
  if (e.data && e.data.type === 'ctrader-widget:height') {
    document.querySelectorAll('iframe[src*="widget.example.com"]').forEach(function (f) {
      f.style.height = e.data.height + 'px';
    });
  }
});
</script>
```

## Параметры URL

| параметр | значения | по умолчанию |
|---|---|---|
| `theme` | `light`, `dark`, `auto` | `auto` — по системной теме посетителя |
| `transparent` | `1` — без фона, виджет сливается с сайтом клиента | выкл |
| `layout` | `grid`, `list` | `grid` |
| `market` | стартовый фильтр, напр. `Gold` | `All` |
| `sort` | `featured`, `rating`, `price-asc`, `price-desc`, `name` | `featured` |
| `limit` | число карточек, напр. `6` | все |
| `header` | `0` — скрыть заголовок | показан |
| `controls` | `0` — скрыть поиск, сортировку и чипы | показаны |

Пример компактного блока для сайдбара: `/?layout=list&limit=5&controls=0&transparent=1`

## Откуда цены

Цены, рейтинги и логотипы сняты со страниц ctrader.com 09.09.2026. Store показывает их из своего JSON-LD/SSR, так что при желании обновление можно автоматизировать (скрипт раз в день → products.json), но в этой версии всё руками.
