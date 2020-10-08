# load library
import requests
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR
import fitz
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# download file from url
def pdfDownload(url, headers, file_nm, param=None, retries=3):
    resp = None

    try:
        resp = requests.get(url, params=param, headers=headers)
        resp.raise_for_status()

        pdf_layer = "/Users/jongwon/python/economy/macro_economy/data" + "/" +  file_nm+ ".pdf"

        with open(pdf_layer, 'wb') as f:
            f.write(resp.content)
        #print("complete writing pdf!")

    except requests.exceptions.HTTPError as e:
        if 500 <= resp.status_code < 600 and retries > 0:
            print('Retries : {0}'.format(retries))
            return getDownload(url, param, retries - 1)
        else:
            return resp.status_code
    return resp

def importImgFromPDF(file, save_path, start_page = 1, end_page = 1):

    doc = fitz.open(file)

    # get img page by
    for i in range( start_page-1, end_page ):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:  # this is GRAY or RGB
                pix.writePNG(save_path + "p%s-%s.png" % (i, xref))
            else:  # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG(save_path + "p%s-%s.png" % (i, xref))
                pix1 = None
            pix = None

    #print("img from PDF has been saved!")

def importImgFromURL(url, file_nm):

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img_save_path = "/Users/jongwon/python/economy/macro_economy/data" + '/' + file_nm + '.png'
    img.save(img_save_path)
    #print("img from URL has been saved!")

# download file from url
def fredREQ(url, headers, param=None, retries=3):
    resp = None

    try:
        resp = requests.get(url, params=param, headers=headers)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if 500 <= resp.status_code < 600 and retries > 0:
            print('Retries : {0}'.format(retries))
            return fredREQ(url, param, retries - 1)
        else:
            return resp.status_code
    return resp


# main definition
if __name__ == "__main__":

    # 1. get PMI image
    url = "https://tradingeconomics.com/united-states/business-confidence"
    headers = {'Referer': url,
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

    req = fredREQ(url, headers)
    req_txt = req.text
    soup = BeautifulSoup(req_txt, 'html.parser')

    imgs = soup.find_all('img')
    img_url = imgs[0]['src']

    today = datetime.now()
    #today_str = today.strftime("%m%d%y")

    pmi_nm = "PMI_image" #+ today_str
    importImgFromURL(img_url, pmi_nm)

    # 2. S&P500 image    
    last_friday = datetime.now() + relativedelta(weekday=FR(-1))
    last_friday_str = last_friday.strftime("%m%d%y")

    pdf_url = "https://www.factset.com/hubfs/Resources%20Section/Research%20Desk/Earnings%20Insight/EarningsInsight_" + last_friday_str + "A.pdf"
    headers = {'Referer': pdf_url,
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    save_name = "12fwd_" + last_friday_str
    
    pdfDownload(pdf_url, headers, save_name)

    if not os.path.isfile(save_name):
        last_friday = datetime.now() + relativedelta(weekday=FR(-2))
        last_friday_str = last_friday.strftime("%m%d%y")

        pdf_url = "https://www.factset.com/hubfs/Resources%20Section/Research%20Desk/Earnings%20Insight/EarningsInsight_" + last_friday_str + "A.pdf"
        headers = {'Referer': pdf_url,
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        save_name = "12fwd_" + last_friday_str
    
        pdfDownload(pdf_url, headers, save_name)

    save_path = "/Users/jongwon/python/economy/macro_economy/data/"
    pdf_which = save_path + save_name + ".pdf"

    importImgFromPDF(pdf_which, save_path, 1, 1)

    rm_file = "/Users/jongwon/python/economy/macro_economy/data" + "/p0-12.png"
    os.remove(pdf_which)
    os.remove(rm_file)
    #print("delete un-necessary file")