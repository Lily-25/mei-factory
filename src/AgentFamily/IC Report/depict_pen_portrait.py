"""
Draw a company's pen portrait covering its history, its location, its main areas of production or services,
and its main types of clients. For example:
“Mark Donaldson and Wendy Tang established Doh-Si-Doh in 2014. The company makes musical
instruments designed for students learning wind band music in a school or club setting. The company employs 34 staff.
Doh-Si-Doh designs its products in Hong Kong and manufactures them in Tianjin. To keep costs down, they use an
external materials testing company, which can do tests on strength, resistance to wear, and provide certifications that are
required by a number of countries.”
"""

class PenPortrait():

    def __init__(self, companyName, website = "", limited_words = 100):
        self.companyName = companyName
        self.website = website
        self.limited_words = limited_words
        self.prompt = f"""
you're an expert of intellectual capital management, 
and now you should write a brief pen portrait for {self.companyName} in {self.limited_words} words. 
while depicting the pen portrait, you should cover such items:its history, its location, its main areas of production or services,
and its main types of clients. 

For example:
“Mark Donaldson and Wendy Tang established Doh-Si-Doh in 2014. The company makes musical
instruments designed for students learning wind band music in a school or club setting. The company employs 34 staff.
Doh-Si-Doh designs its products in Hong Kong and manufactures them in Tianjin. To keep costs down, they use an
external materials testing company, which can do tests on strength, resistance to wear, and provide certifications that are
required by a number of countries.”

please make sure that all information you used has official data to support it through checking each part with reference.

Please start.
"""

    def getCompanyName(self):
        return self.companyName

    def getWebsite(self):
        return self.website

    def getPrompt(self):
        return self.prompt


if __name__ == '__main__':
    company = PenPortrait("Insight Lifetech")
    print(company.getPrompt())

