import webview


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    webview.create_window('Financial Calculator', 'web/index.html')
    webview.start(gui='edgehtml', debug=True)
