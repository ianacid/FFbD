from FFbD import FFbd

if __name__ == "__main__":
    app = FFbd()
    app.run()
    app.factory_html()

    for plugin in app.plugins:
        plugin.run(app)

    app.factory_webpage()

    exit(0)
