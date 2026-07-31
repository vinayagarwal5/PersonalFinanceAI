from services.merchant_normalizer import normalize_merchant

samples = [

    "IND*AMAZON.IN",

    "AMAZON MUMBAI",

    "GROFERS INDIA PRIVATE LIMITED",

    "Paid to Blinkit",

    "LAATA PHARMACY"

]

for merchant in samples:

    print(merchant, "->", normalize_merchant(merchant))