from holehe.core import *
from holehe.localuseragent import *

def fetlife(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en,en-US;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    s = requests.session()
    req = s.get("https://fetlife.com/signup_step_profile", headers=headers)
    soup = BeautifulSoup(req.content, features="lxml")

    inp_method = soup.find("input", attrs={"type": "hidden", "name": "_method"})
    inp_authenticity_token = soup.find(
        "input",
        attrs={"type": "hidden", "name": "authenticity_token"}
    )

    if inp_method is None or inp_authenticity_token is None:
        raise NotImplementedError(
            "Fetlife register page changed, this module need to be updated."
        )

    data = {
        "_method": inp_method.get("value"),
        "authenticity_token": inp_authenticity_token.get("value"),
        "user[nickname]": "",
        "user[email]": email,
        "user[password]": "",
    }

    post = s.post(
        "https://fetlife.com/signup_step_profile",
        headers=headers,
        data=data
    )
    resp_soup = BeautifulSoup(post.content, features="lxml")

    EMAIL_MSG_ERROR = (
        "We're having problems processing the above email address. "
        "We recommend you verify the spelling or try a different one."
    )

    email_error_tag = resp_soup.findAll(text=EMAIL_MSG_ERROR)

    email_is_present = len(email_error_tag) > 0

    return({
        "rateLimit": False,
        "exists": email_is_present,
        "emailrecovery": None,
        "phoneNumber": None,
        "others": None
    })
