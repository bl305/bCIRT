from selenium import webdriver
import argparse
import os

class screenshot_url():
    def __init__(self):
        pass

    def screenshot_chrome(self, aurl, afile):
        DRIVER = '/usr/bin/chromedriver'
        BROWSER = '/usr/bin/chromium-browser'
        # driver = webdriver.Chrome(DRIVER)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = BROWSER
        driver = webdriver.Chrome(executable_path=DRIVER, chrome_options=chrome_options)
        driver.get(aurl)
        screenshot = driver.save_screenshot(afile)
        driver.quit()

    def fix_url(self, purl):
        resp = None
        print(purl)
        if purl.startswith('/'):
            resp = 'file://' + purl
        elif not purl.startswith('http://') and not purl.startswith('https://') and not purl.startswith('hsts://') \
                and not purl.startswith('file://'):
            resp = 'http://' + purl
        else:
            resp = purl
        print(resp)
        return resp

def build_parser():
    parser = argparse.ArgumentParser(description='Take Website Screenshot.', usage='screenshot_url [options]')
    parser.add_argument("URL", help="URL to screenshot")
    parser.add_argument('-o', '--outfile', action='store', type=str, help='Save output file full path', dest="save-outfile-to")
    args = vars(parser.parse_args())
    return args

if __name__ == "__main__":
    args = build_parser()
    # print(args)

    if args['save-outfile-to'] and args['URL'] and args['save-outfile-to']:
        # napath = os.path.dirname(args['save-outfile-to'])
        # nafile = os.path.basename(args['save-outfile-to'])
        purl = screenshot_url().fix_url(args['URL'])
        pfile = args['save-outfile-to']
        # purl = "http://www.google.com"
        res = screenshot_url().screenshot_chrome(aurl=purl, afile=pfile)



