from flask import *
import pandas as pd
import requests
import bs4

app = Flask(__name__)
website = "https://www.sgdtips.com/grabfood-promo-codes"
res = requests.get(website)
soup = bs4.BeautifulSoup(res.text, "lxml")


def promo_code_scraper(soup):
    """
    The web scraper code is very specific for each individual website, so likely it won't work if you change the
    website link to another one, or the website changes its format subsequently.
    :param soup: the output from beautifulsoup module
    :return: the voucher_df in pandas df format.
    """
    voucher_desc_lst = []
    voucher_code_lst = []
    voucher_detail_lst = []
    for item in soup.select(".item.procoupon_item--voucher"):
        for voucher in item.select(".sgdtpro_voucher-content"):
            for voucher_desc in voucher.select('.sgdt-brief-promo.promo-code-h3'):
                voucher_desc_lst.append(voucher_desc.text)
            if not voucher.select('.sgdt_code-value'):
                voucher_code_lst.append('NA')
            else:
                for code in voucher.select('.sgdt_code-value'):
                    # Here the get method helps to obtain the value filed in the hidden tag (.text is not working..)
                    voucher_code_lst.append(code.get('value'))
        for details in item.select(".sgdtpro_content-detail"):
            if not details.text.replace('\n', ''):
                voucher_detail_lst.append('NA')
            else:
                voucher_detail_lst.append(details.text.replace('\n', ''))

    voucher_df = pd.DataFrame(list(zip(voucher_desc_lst, voucher_code_lst, voucher_detail_lst)),
                              columns=['Description', 'Code', 'Details'])
    return voucher_df

voucher_tbl = promo_code_scraper(soup)

@app.route('/')
def show_tables():
    return render_template('basic_table.html', data = voucher_tbl.to_dict(orient='records'), title = 'Grab Voucher Code')


if __name__ == '__main__':
    app.run(debug=True)