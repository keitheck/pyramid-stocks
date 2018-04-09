def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('portfolio', '/portfolio')
    config.add_route('auth', '/auth')
    config.add_route('stock-add', '/stock-add')
    config.add_route('detail', '/detail/{symbol}')
    config.add_route('404', '/404')

